"""Validate, document and package the 16-session apps edition.

Run only after manuscript reorganization, PDF generation and full rendering.
This script does not edit the manuscript, example programs, source metadata,
assets, renderer or PDF.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import zipfile

from pypdf import PdfReader
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coala-book-md/vibe-coding-16"
PDF = ROOT / "output/pdf/vibe-coding-16-source7.pdf"
ARCHIVE = BOOK / "previous-reports/20261011-before-second-compaction"
REVISION_ARCHIVE = BOOK / "previous-reports/20261011-before-source7-reference"
BASELINE = ARCHIVE / "vibe-coding-16-graph-first.json"
QA_INPUT = ROOT / "tmp/pdfs/source7-edition-review/automated-qa.json"
DATE = "2026-10-11"
HALLUCINATION_EXAMPLES = [
    {
        "topic": "제1차 십자군의 연도",
        "question": "제1차 십자군은 1492년에 시작했나요?",
        "learning_only_wrong_answer": "네, 1492년에 시작했습니다.",
        "verified_fact": "제1차 십자군은 1096~1099년에 진행되었습니다.",
        "source_title": "OpenStax · 13.4 The Crusading Movement",
        "source_url": "https://openstax.org/books/world-history-volume-1/pages/13-4-the-crusading-movement",
        "source_support": "Figure 13.19의 First Crusade, 1096-1099 표기와 1099년 예루살렘 도착 설명",
    },
    {
        "topic": "소설 연금술사의 작가·출간 연도",
        "question": "산티아고가 나오는 소설 『연금술사』는 셰익스피어의 작품인가요?",
        "learning_only_wrong_answer": "네, 셰익스피어가 쓴 작품입니다.",
        "verified_fact": "파울로 코엘료의 소설로, 1988년에 처음 출간되었습니다.",
        "source_title": "Paulo Coelho and Christina Oiticica Foundation · The Alchemist",
        "source_url": "https://fondationpaulocoelho.com/books/paulo-coelho-the-alchemist/",
        "source_support": "작가 Paulo Coelho, 주인공 Santiago, First publication year: 1988 확인",
    },
]
SOURCE_PAGES = {
    1: "5-8", 2: "9-15", 3: "16-18", 4: "19-27", 5: "27-32",
    6: "33-36", 7: "37-40", 8: "41-53", 9: "54-66", 10: "67-87",
    11: "88-94", 12: "128-145", 13: "95-105", 14: "106-110 · 118-127",
    15: "146-151", 16: "93-94",
}
ACTIVITIES = {
    1: "AI 질문과 답의 검증", 2: "질문 비교·앱 입력 데이터 설계",
    3: "아이디어를 입력·처리·출력으로 나누기",
    4: "가족 나이 합·학생 세 명의 총점",
    5: "운동 시간 누적·카페인 입력 반복", 6: "수면 시간 분류",
    7: "학생 점수 판정·영화 관람 조건",
    8: "버튼 색·메시지 창·Field 복사와 삭제",
    9: "누적곱·계산기·Text 추가·구구단",
    10: "Dropdown·Checkbox·RadioButton·진행 막대·이미지",
    11: "성적표의 행 추가·셀 값 변경",
    12: "Matplotlib 선·마커·설명·막대·산점도",
    13: "직접 입력한 값의 선 그래프·산점도·막대그래프",
    14: "학생 자료·학교별 학생 수·저장과 불러오기",
    15: "Series·요일별 DataFrame·학생 정보·행과 열 이름",
    16: "프로젝트 아이디어·UI 설계·실행 확인",
}
REPORTS = [
    "README.md", "notes.md", "canva-production-status.md", "validation-summary.md",
    "pdf-final-review.md", "handover.md", "final-draft.md", "curriculum.md",
    "teacher-guide.md", "print-activities.md", "source-audit.md",
    "practice-source-review.md", "asset-audit.md", "asset-review.html",
    "page-compaction-review.md", "apps-edition-review.md", "flowchart-canva.md",
    "flow-source-review.md",
    "hallucination-source-review.md", "hallucination-source-review.json",
    "hallucination-page-comparison.json",
    "graph-first-edition-review.md", "graph-first-edition-comparison.json",
    "page-merge-review.md", "page-merge-comparison.json",
    "calculator-widget-correction.json",
    "source-reference-review.md",
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(name: str, value: str):
    (BOOK / name).write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(value: bytes):
    return hashlib.sha256(value).hexdigest()


def json_digest(value):
    return digest(json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8"))


def signature(item):
    return (item["src"], tuple(item["pixels"]), item["printWidthPt"], item["effectiveDpi"])


def is_robot_asset(path: str):
    return "cocobot" in path.lower() or "robot" in path.lower()


def page_numbers(values):
    return ", ".join(str(v) for v in sorted(set(values))) or "제외"


metadata = read_json(PDF.with_suffix(".json"))
baseline = read_json(BASELINE)
qa = read_json(QA_INPUT)
assets = read_json(BOOK / "asset-manifest.json")
flows = read_json(BOOK / "flow-source-map.json")
source_reference = read_json(BOOK / "source-reference-review.json")
code_specs = read_json(BOOK / "code-specs.json")
codes = read_json(BOOK / "code-results.json")
previous_code_specs = read_json(ARCHIVE / "code-specs.json")
previous_codes = read_json(ARCHIVE / "code-results.json")
validations = read_json(BOOK / "validation-full.json")
practice_source = read_json(BOOK / "practice-source-map.json")
catalog = practice_source["practices"]
spec = read_json(ROOT / "tmp/pdfs/book-spec.json")
restructure = read_json(BOOK / "page-merge-plan.json")
current_pages = metadata["pages"]
previous_pages = baseline["pages"]
saved_pages = previous_pages - current_pages
canva_pages = validations[0]["layout"]["canvaPages"]

assert previous_pages == 139
assert metadata["pages"] == qa["pages"] == qa["renderedPages"]
assert current_pages > 0
assert len(validations) == 17 and validations[0]["pages"] == 167
assert all(value["ok"] and not value["issues"] for value in validations)
assert len(spec["pages"]) == 167
assert len(catalog) == metadata["pageTypes"]["practice-opening"] == 40
assert len(assets["items"]) == 34
assert len(metadata["images"]) == qa["images"] == 35
assert qa["flowcharts"] == 4
assert len(code_specs) == codes["executed_blocks"] == codes["passed"] == 12
assert qa["manuscriptCodeBlocks"] == qa["printedCodeBlocks"] == 12
assert all(not is_robot_asset(item["src"]) for item in assets["items"])
assert all(not is_robot_asset(item["src"]) for item in metadata["images"])
assert digest((BOOK / "book.md").read_bytes()) == metadata["manuscriptSha256"]
assert digest(PDF.read_bytes()) == metadata["pdfSha256"]
for key in ("outOfPageGlyphs", "missingSourceIds", "contentsErrors",
            "codeContentDifferences", "replacementGlyphPages",
            "institutionLogoTextPages", "editorialReferencePages", "boxOverflows"):
    assert not qa[key], (key, qa[key])

# Reuse all retained figures at their established physical size.
old_images = [item for item in baseline["images"]
              if item.get("format") not in ("native-vector-pdf", "generated-vector-pdf")]
assert len(old_images) == 30
retained_images = [item for item in metadata["images"]
                   if item.get("format") not in ("native-vector-pdf", "generated-vector-pdf")]
native_images = [item for item in metadata["images"] if item.get("format") == "native-vector-pdf"]
generated_images = [item for item in metadata["images"] if item.get("format") == "generated-vector-pdf"]
assert len(retained_images) == 30 and len(native_images) == 4 and len(generated_images) == 1
assert sorted(map(signature, retained_images)) == sorted(map(signature, old_images))
for item in assets["items"]:
    path = BOOK / item["src"]
    assert path.is_file(), path
    expected = item.get("sha256")
    if expected:
        assert digest(path.read_bytes()) == expected, path

# The printed diagrams reuse the source's native vectors. PNG dimensions/DPI
# describe the separate Canva previews, not the vector content printed in PDF.
diagrams = flows["diagrams"]
assert len(diagrams) == 4
assert sorted(item["source_pdf_page"] for item in diagrams) == [23, 31, 36, 39]
assert flows["source_sha256"] == assets["source_sha256"]
source_pdf = ROOT / flows["source_pdf"]
source_pdf_checked = source_pdf.is_file()
if source_pdf_checked:
    assert digest(source_pdf.read_bytes()) == flows["source_sha256"]
diagram_ids = {item["page_id"] for item in diagrams}
assert {item["sourceId"] for item in native_images} == diagram_ids
assert len([item for item in assets["items"] if item.get("vector_src")]) == 5
vector_checks = []
for diagram in diagrams:
    vector = BOOK / diagram["vector_src"]
    preview = BOOK / diagram["src"]
    assert digest(vector.read_bytes()) == diagram["vector_sha256"]
    assert digest(preview.read_bytes()) == diagram["sha256"]
    with Image.open(preview) as image:
        assert image.size == (diagram["width"], diagram["height"])
    vector_reader = PdfReader(str(vector))
    assert len(vector_reader.pages) == 1
    page = vector_reader.pages[0]
    bbox = diagram["crop_bbox_top_left_pt"]
    assert abs(float(page.cropbox.width) - (bbox[2] - bbox[0])) < .01
    assert abs(float(page.cropbox.height) - (bbox[3] - bbox[1])) < .01
    raster_objects = [value for value in page.get("/Resources", {}).get("/XObject", {}).values()
                      if value.get_object().get("/Subtype") == "/Image"]
    assert not raster_objects
    fences = re.findall(r"```flowchart\s*\n(.*?)^```\s*$",
                        (BOOK / f"ch{diagram['chapter']:02d}.md").read_text(encoding="utf-8"), re.M | re.S)
    assert len(fences) == 1 and digest(fences[0].encode("utf-8")) == diagram["flowchart_sha256"]
    placed = next(item for item in native_images if item["sourceId"] == diagram["page_id"])
    assert placed["vectorAsset"] == diagram["vector_src"]
    assert placed["vectorSha256"] == diagram["vector_sha256"]
    vector_checks.append({"sourceId": diagram["page_id"], "sourcePdfPage": diagram["source_pdf_page"],
                          "vectorAsset": diagram["vector_src"], "vectorSha256": diagram["vector_sha256"],
                          "previewAsset": diagram["src"], "previewSha256": diagram["sha256"],
                          "cropBoxPt": bbox, "vectorPages": 1, "rasterXObjects": 0,
                          "diagramPathsAndColorsPreserved": True,
                          "background": diagram["background"]})

assert flows["declaration_shape"] == "six-sided preparation symbol preserved from source"
trace = []
time1, total = 1, 0
while time1 <= 10:
    total += time1
    trace.append({"time1": time1, "total": total})
    time1 += 1
assert len(trace) == flows["loop_trace"]["iterations"] == 10
assert {"time1": time1, "total": total} == flows["loop_trace"]["exit"] == {"time1": 11, "total": 55}
assert flows["loop_trace"]["start"] == {"time1": 1, "total": 0}
assert flows["loop_trace"]["condition"] == "time1 <= 10"
assert flows["loop_trace"]["updates"] == ["total = total + time1", "time1 += 1"]
movie_boundaries = [{"age": age, "canWatch": age >= 15} for age in [14, 15, 16, 13]]
assert [item["canWatch"] for item in movie_boundaries] == [False, True, True, False]

# Check the current source against executed programs by ID, then compare the
# whole set of hashes to the previous edition independently of chapter numbers.
executed_hashes = {item["page_id"]: item["code_sha256"] for item in codes["records"]}
current_hashes = {}
for page in spec["pages"]:
    for section in page.get("sections", []):
        for code in re.findall(r"```python\s*\n(.*?)\n```", section.get("content", ""), re.S):
            assert page["id"] not in current_hashes
            current_hashes[page["id"]] = digest(code.encode("utf-8"))
assert len(current_hashes) == 12 and current_hashes == executed_hashes
assert sorted(current_hashes.values()) == sorted(item["code_sha256"] for item in previous_codes["records"])
def code_output_signature(item):
    return digest(item["code"].encode("utf-8")), digest((item.get("output") or "").encode("utf-8"))
assert sorted(map(code_output_signature, code_specs)) == sorted(map(code_output_signature, previous_code_specs))
for item in code_specs:
    path = BOOK / "examples/source-based" / (item["page_id"] + ".py")
    assert path.is_file(), path
    assert path.read_text(encoding="utf-8").rstrip() == item["code"].rstrip(), path

openings = {page["chapterNumber"]: page for page in spec["pages"] if page["type"] == "chapter-opening"}
assert sorted(openings) == list(range(1, 17))
chapter_titles = {number: page["chapterTitle"] for number, page in openings.items()}
practice_counts = Counter(item["chapter"] for item in catalog)
assert practice_counts[12] == 8 and practice_counts[13] == 3
assert practice_counts[14] == 3 and practice_counts[15] == 3
assert practice_counts[16] == 1

reader = PdfReader(str(PDF))
assert len(reader.pages) == current_pages
assert len(reader.outline) == 16
contents_links = sum(len(page.get("/Annots", [])) for page in reader.pages[:3])
assert contents_links == 16
fonts = {}
standard_fonts = set()
robot_mentions = []
editorial_mentions = []
for number, page in enumerate(reader.pages, 1):
    text = page.extract_text() or ""
    if re.search(r"코코봇|로봇|cocobot|robot", text, re.I):
        robot_mentions.append(number)
    if re.search(r"원본|\bPDF\b", text, re.I):
        editorial_mentions.append(number)
    for reference in page["/Resources"].get("/Font", {}).values():
        font = reference.get_object()
        candidates = [font] + [v.get_object() for v in font.get("/DescendantFonts", [])]
        for candidate in candidates:
            descriptor = candidate.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                fonts[str(candidate.get("/BaseFont"))] = any(
                    key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
            elif candidate.get("/Subtype") == "/Type1":
                standard_fonts.add(str(candidate.get("/BaseFont")))
assert not robot_mentions, robot_mentions
assert not editorial_mentions, editorial_mentions
assert fonts and all(fonts.values())

# Read the explicit manuscript ID mapping written by the reorganization step.
id_map = next((restructure[key] for key in ("old_to_new", "id_mapping", "idMap", "id_map", "mapping")
               if key in restructure), None)
if isinstance(id_map, list):
    id_map = {item.get("old_id", item.get("oldId")): item.get("new_id", item.get("newId"))
              for item in id_map}
assert isinstance(id_map, dict), list(restructure)
removed_ids = set(restructure.get("removed_pages", restructure.get("removed_ids", restructure.get("removedIds", []))))
new_ids = set(restructure.get("added_pages", restructure.get("new_ids", restructure.get("newIds", []))))
assert not removed_ids
assert not new_ids
new_pages_by_id = defaultdict(list)
for number, page in enumerate(metadata["layout"], 1):
    for source_id in set([page["id"]] + page.get("includedSources", [])):
        new_pages_by_id[source_id].append(number)
source_ids = {page["id"] for page in spec["pages"]}
assert source_ids <= set(new_pages_by_id)
assert new_pages_by_id["ch01-ethics"] == [7]
assert new_pages_by_id["ch05-exercise-flow"] == [29]
for item in vector_checks:
    item["physicalPages"] = new_pages_by_id[item["sourceId"]]
assert all(len(item["physicalPages"]) == 1 for item in vector_checks)
loop_physical_page = new_pages_by_id["ch05-exercise-flow"][0]
movie_physical_page = new_pages_by_id["ch07-movie-flow"][0]
hallucination_text = re.sub(r"\s+", "", reader.pages[6].extract_text() or "")
for required in ("학습용가상오답", "직접확인하기", "책임있는사용", "질문의전제", "연도", "작가"):
    assert required in hallucination_text, required
for example in HALLUCINATION_EXAMPLES:
    for field in ("question", "learning_only_wrong_answer", "verified_fact"):
        assert re.sub(r"\s+", "", example[field]) in hallucination_text, (example["topic"], field)
for obsolete in ("컴퓨터실", "체육관", "금요일오전10시", "금요일오후3시"):
    assert obsolete not in hallucination_text, obsolete
assert "http://" not in hallucination_text and "https://" not in hallucination_text
ethics_layout = metadata["layout"][6]
old_ethics = next(page for page in baseline["layout"] if page["id"] == "ch01-ethics")
assert ethics_layout["y"] < 786
hallucination_check = {"page": 7, "sourceId": "ch01-ethics", "labeledHypothetical": True,
                       "constructedLearningWrongAnswers": True, "actualAiOutputClaimed": False,
                       "verifiedExampleCount": len(HALLUCINATION_EXAMPLES),
                       "questionPremiseYearAndAuthorVerificationPresent": True,
                       "verifiedFacts": HALLUCINATION_EXAMPLES,
                       "responsibleUsePresent": True, "previousBodyBottomPt": old_ethics["y"],
                       "currentBodyBottomPt": ethics_layout["y"],
                       "bodyBottomExtendedPt": ethics_layout["y"] - old_ethics["y"]}
mapping = []
for number, page in enumerate(baseline["layout"], 1):
    old_ids = set([page["id"]] + page.get("includedSources", []))
    current_ids = {id_map.get(source_id, source_id) for source_id in old_ids
                   if source_id not in removed_ids and id_map.get(source_id, source_id)}
    assert all(source_id in new_pages_by_id for source_id in current_ids), current_ids
    destinations = sorted({n for source_id in current_ids for n in new_pages_by_id[source_id]})
    mapping.append({"previousPage": number, "previousSourceIds": sorted(old_ids),
                    "currentSourceIds": sorted(current_ids), "currentPages": destinations,
                    "excluded": not destinations, "previousTitle": page["title"]})
assert len(mapping) == previous_pages

# The calculator uses fld3 for its result. txt1 remains valid in the separate
# Text and multiplication-table exercises, so check only these two sections.
calculator_corrections = [
    {"sourceId": "ch09-calculator-request", "physicalPage": 57,
     "sentence": "결과 표시 위젯 fld3에서 계산한 값을 확인합니다."},
    {"sourceId": "ch09-calculator-code", "physicalPage": 58,
     "sentence": "두 숫자와 선택한 사칙연산을 처리하고 결과를 fld3에 표시합니다."},
]
for item in calculator_corrections:
    assert new_pages_by_id[item["sourceId"]] == [item["physicalPage"]]
    page_text = re.sub(r"\s+", "", reader.pages[item["physicalPage"] - 1].extract_text() or "")
    assert re.sub(r"\s+", "", item["sentence"]) in page_text
    assert "결과표시위젯txt1" not in page_text and "결과를txt1에표시" not in page_text
calculator_correction_check = {"date": DATE, "resultWidget": "fld3",
                              "correctedPages": [57, 58], "correctedSentences": calculator_corrections,
                              "pdfSha256": metadata["pdfSha256"], "manuscriptSha256": metadata["manuscriptSha256"],
                              "otherTxt1ExercisesRetained": True}
correction_baseline_pdf = BOOK / "previous-reports/20261011-before-fld3-correction/vibe-coding-16-merged.pdf"
if correction_baseline_pdf.is_file():
    previous_corrected_reader = PdfReader(str(correction_baseline_pdf))
    assert len(previous_corrected_reader.pages) == current_pages
    changed_text_pages = [number for number, (old, current) in enumerate(
        zip(previous_corrected_reader.pages, reader.pages), 1)
        if (old.extract_text() or "") != (current.extract_text() or "")]
    assert changed_text_pages == [57, 58], changed_text_pages
    calculator_correction_check.update({"directPreviousPdfCompared": True,
                                       "previousPdf": correction_baseline_pdf.relative_to(ROOT).as_posix(),
                                       "previousPdfSha256": digest(correction_baseline_pdf.read_bytes()),
                                       "onlyPages57And58TextChanged": True,
                                       "unchangedTextPages": current_pages - 2})
else:
    calculator_correction_check["directPreviousPdfCompared"] = False

# The first chapter adds one original teaching diagram, not a new exercise.
summary_asset = next(item for item in assets["items"] if item["src"] == "assets/ch01/ai-human-summary.png")
summary_map = read_json(BOOK / "intro-summary-map.json")
for key in ("src", "vector_src", "sha256", "vector_sha256", "width", "height"):
    assert summary_asset[key] == summary_map[key], key
assert summary_map["body_font_pt"] == 14 and summary_map["heading_font_pt"] == 15
summary_placement = generated_images[0]
assert summary_placement["sourceId"] == "ch01-opening"
assert summary_asset["vector_src"] == "assets/ch01/ai-human-summary.pdf"
assert summary_placement["vectorAsset"] == summary_asset["vector_src"]
assert summary_placement["vectorSha256"] == summary_asset["vector_sha256"]
assert new_pages_by_id["ch01-opening"] == [5]
summary_pdf = PdfReader(str(BOOK / summary_asset["vector_src"]))
assert len(summary_pdf.pages) == 1
assert abs(float(summary_pdf.pages[0].mediabox.width) - summary_map["print_width_pt"]) < .01
assert abs(float(summary_pdf.pages[0].mediabox.height) - summary_map["print_height_pt"]) < .01
assert abs(summary_placement["printWidthPt"] - summary_map["print_width_pt"]) < .01
assert digest((BOOK / summary_asset["vector_src"]).read_bytes()) == summary_asset["vector_sha256"]
with Image.open(BOOK / summary_asset["src"]) as image:
    assert image.size == (summary_asset["width"], summary_asset["height"])
summary_rasters = [value for value in summary_pdf.pages[0].get("/Resources", {}).get("/XObject", {}).values()
                   if value.get_object().get("/Subtype") == "/Image"]
assert not summary_rasters
summary_text = re.sub(r"\s+", "", summary_pdf.pages[0].extract_text() or "")
assert "AI" in summary_text and "사람" in summary_text
assert not any("subway-top5-result.png" in item["src"] for item in assets["items"])
assert not any("subway-top5-result.png" in item["src"] for item in metadata["images"])
api_reference_pages = [number for number, page in enumerate(reader.pages, 1)
                       if re.search(r"\bAPI\b|지하철역|공공데이터|인증키", page.extract_text() or "", re.I)]
assert not api_reference_pages, api_reference_pages
assert Counter(item["chapter"] for item in code_specs) == {12: 7, 15: 5}
assert ethics_layout == old_ethics
assert id_map == {source_id: source_id for source_id in source_ids}
assert sorted(map(signature, metadata["images"])) == sorted(map(signature, baseline["images"]))
assert sorted(map(signature, native_images)) == sorted(map(signature,
    [item for item in baseline["images"] if item.get("format") == "native-vector-pdf"]))
summary_check = {"physicalPage": 5, "sourceId": "ch01-opening",
                 "previewAsset": summary_asset["src"], "previewSha256": summary_asset["sha256"],
                 "vectorAsset": summary_asset["vector_src"], "vectorSha256": summary_asset["vector_sha256"],
                 "pixels": [summary_asset["width"], summary_asset["height"]],
                 "vectorPages": 1, "rasterXObjects": 0,
                 "bodyFontPt": summary_map["body_font_pt"], "headingFontPt": summary_map["heading_font_pt"],
                 "printWidthPt": summary_map["print_width_pt"], "printHeightPt": summary_map["print_height_pt"],
                 "chapterOpeningBodyBottomPt": metadata["layout"][4]["y"],
                 "printFormat": "generated-vector-pdf", "roles": ["AI 제안", "사람 확인·수정"],
                 "newExerciseAdded": False, "unchangedFromPreviousEdition": True}
merge_comparison = {"date": DATE, "previousPdfPages": previous_pages, "currentPdfPages": current_pages,
                    "savedPages": saved_pages, "baselineMetadata": BASELINE.relative_to(ROOT).as_posix(),
                    "baselinePdfSha256": baseline["pdfSha256"], "currentPdfSha256": metadata["pdfSha256"],
                    "previousManuscriptContainers": 167, "currentManuscriptContainers": 167,
                    "previousPracticeCards": 40, "currentPracticeCards": 40,
                    "chapterOrder": {"12": "Matplotlib", "13": "입력 Chart", "14": "학생 자료·저장",
                                     "15": "Pandas", "16": "프로젝트"},
                    "identitySourceIdMapping": True, "removedSourceIds": [], "addedSourceIds": [],
                    "all35ImagePlacementsUnchanged": True, "all34PngAssetsAnd5VectorAssetsRetained": True,
                    "retainedImagePixelsAndPrintWidthsUnchanged": True,
                    "nativeFlowchartsUnchanged": True, "executedCodeAndOutputHashesUnchanged": True,
                    "hallucinationPage7LayoutUnchanged": True, "summaryPage5Unchanged": True,
                    "chapterStartPages": metadata["chapterPages"],
                    "previousPhysicalPagesMapping": mapping}
assert saved_pages == 5
assert metadata["layout"][4] == baseline["layout"][4]
previous_pdf = ARCHIVE / "vibe-coding-16-graph-first.pdf"
if previous_pdf.is_file():
    old_reader = PdfReader(str(previous_pdf))
    assert digest(previous_pdf.read_bytes()) == baseline["pdfSha256"]
    assert (old_reader.pages[6].extract_text() or "") == (reader.pages[6].extract_text() or "")
    assert (old_reader.pages[4].extract_text() or "") == (reader.pages[4].extract_text() or "")
    merge_comparison["pages5And7PdfTextDirectlyCompared"] = True
else:
    merge_comparison["pages5And7PdfTextDirectlyCompared"] = False

# Validate the selected pairs by their source IDs, not a fixed new page number.
selected_pair_checks = []
assert len(restructure["selected_pairs"]) == 5
assert current_pages == restructure["expected_pdf_pages"]
assert previous_pages == restructure["previous_pdf_pages"]
for pair in restructure["selected_pairs"]:
    old_pair_ids = {source_id for number in pair["previous_pages"]
                    for source_id in [baseline["layout"][number - 1]["id"]] +
                    baseline["layout"][number - 1].get("includedSources", [])}
    assert set(pair["source_ids"]) <= old_pair_ids
    targets = {number for source_id in pair["source_ids"] for number in new_pages_by_id[source_id]}
    assert len(targets) == 1, pair
    target = targets.pop()
    page = metadata["layout"][target - 1]
    max_bottom = max((float(block["y"]) + float(block.get("height", 0))
                      for block in page["blocks"] if isinstance(block.get("y"), (int, float))), default=0)
    assert page["y"] <= 786 and max_bottom <= 786
    selected_pair_checks.append({"previousPages": pair["previous_pages"], "sourceIds": pair["source_ids"],
                                 "currentPage": target, "bodyBottomPt": page["y"],
                                 "maximumBlockBottomPt": max_bottom, "edit": pair["edit"]})
deferred_pair_checks = []
for pair in restructure["deferred_pairs"]:
    destinations = sorted({number for old_number in pair["previous_pages"]
                           for number in mapping[old_number - 1]["currentPages"]})
    assert len(destinations) == 2
    deferred_pair_checks.append({"previousPages": pair["previous_pages"], "currentPages": destinations,
                                 "reason": pair["reason"], "keptSeparate": True})
assert metadata["images"] == baseline["images"]
assert catalog == read_json(ARCHIVE / "practice-source-map.json")["practices"]
current_checkbox_count = len(re.findall(r"^\s*[-*]\s+\[[ xX]\]", (BOOK / "book.md").read_text(encoding="utf-8"), re.M))
previous_book = ARCHIVE / "book.md"
if previous_book.is_file():
    previous_checkbox_count = len(re.findall(r"^\s*[-*]\s+\[[ xX]\]", previous_book.read_text(encoding="utf-8"), re.M))
    assert previous_checkbox_count == current_checkbox_count
    checkbox_counts_directly_compared = True
else:
    # The portable bundle omits the previous manuscript, so distinguish preserved
    # evidence from a new direct comparison of that old file.
    record = read_json(BOOK / "page-merge-comparison.json")
    previous_checkbox_count = record["previousCheckboxItems"]
    assert previous_checkbox_count == current_checkbox_count
    checkbox_counts_directly_compared = False
merge_comparison.update({"selectedPairs": selected_pair_checks, "deferredPairs": deferred_pair_checks,
                         "all40PracticeMetadataUnchanged": True,
                         "previousCheckboxItems": previous_checkbox_count,
                         "currentCheckboxItems": current_checkbox_count,
                         "checkboxCountsDirectlyCompared": checkbox_counts_directly_compared,
                         "checkboxItemsUnchanged": True,
                         "fontsAndBodyLeadingPreserved": True,
                         "movieFlowCurrentPage": movie_physical_page})

previous_reference_metadata = read_json(REVISION_ARCHIVE / "vibe-coding-16-fld3.json")
assert metadata["manuscriptSha256"] == previous_reference_metadata["manuscriptSha256"]
assert metadata["layout"] == previous_reference_metadata["layout"]
assert metadata["images"] == previous_reference_metadata["images"]
assert metadata["chapterPages"] == previous_reference_metadata["chapterPages"]
assert metadata["pages"] == previous_reference_metadata["pages"] == 134
assert assets["source_sha256"] == "a4aa668621a7c59c36c9666fa1019182d5ed999c9fb8620f2ddcf509840b2729"
assert source_reference["source_sha256"] == assets["source_sha256"] == flows["source_sha256"] == practice_source["source_pdf_sha256"]
assert source_reference["workspace_source_pdf"] == flows["source_pdf"]
assert (BOOK / assets["source_pdf"]).resolve() == source_pdf.resolve()
assert (BOOK / practice_source["source_pdf"]).resolve() == source_pdf.resolve()
assert metadata["sourcePdfSha256"] == source_reference["source_sha256"]
assert source_reference["source_pages"] == 158
assert source_reference["normalized_page_text_comparison"] == {
    "pages_compared": 158, "identical_pages": 158, "different_pages": []}
assert source_reference["page_sizes_identical"]
assert source_reference["native_ui_images_comparison"]["images_compared"] == 21
assert source_reference["native_ui_images_comparison"]["all_pixels_and_dimensions_identical"]
assert all(item["native_image_identical"] for item in source_reference["native_ui_images_comparison"]["items"])
assert source_reference["native_flowcharts_comparison"]["diagrams_compared"] == 4
assert source_reference["native_flowcharts_comparison"]["all_identical"]
assert all(item["coordinates_shapes_strokes_fills_identical"]
           for item in source_reference["native_flowcharts_comparison"]["items"])
assert not source_reference["student_edition"]["required_source_based_content_changes"]
assert source_reference["student_edition"]["manuscript_unchanged"]
assert source_reference["student_edition"]["sessions"] == 16
assert source_reference["student_edition"]["practices"] == 40
assert source_reference["student_edition"]["pdf_pages"] == 134
source_reference_check = {"sourcePdf": flows["source_pdf"], "sourceSha256": assets["source_sha256"],
                          "sourcePdfHashDirectlyVerified": source_pdf_checked,
                          "evidenceFile": "source-reference-review.json", "evidence": source_reference,
                          "previousStudentPdfMetadata": (REVISION_ARCHIVE / "vibe-coding-16-fld3.json").relative_to(ROOT).as_posix(),
                          "studentManuscriptUnchanged": True, "studentLayoutUnchanged": True,
                          "all35ImagePlacementsUnchanged": True, "chapterStartPagesUnchanged": True,
                          "studentBodyRevisionRequired": False}
previous_render_dir = ROOT / "tmp/pdfs/fld3-review"
current_render_dir = QA_INPUT.parent
if (previous_render_dir / "text.txt").is_file():
    assert (previous_render_dir / "text.txt").read_bytes() == (current_render_dir / "text.txt").read_bytes()
    old_pngs = sorted(previous_render_dir.glob("page-*.png"))
    current_pngs = sorted(current_render_dir.glob("page-*.png"))
    assert len(old_pngs) == len(current_pngs) == 134
    assert all(old.name == new.name and old.read_bytes() == new.read_bytes()
               for old, new in zip(old_pngs, current_pngs))
    source_reference_check.update({"finalPdfTextDirectlyCompared": True,
                                   "finalRenderedPagesByteCompared": 134,
                                   "allFinalPageTextsAndRenderedPngBytesIdentical": True})
else:
    source_reference_check.update({"finalPdfTextDirectlyCompared": False,
                                   "finalRenderedPagesByteCompared": 0})

# Reports are separate from the student textbook. Preserve the prior edition.
REVISION_ARCHIVE.mkdir(parents=True, exist_ok=True)
for name in REPORTS:
    path = BOOK / name
    if path.exists() and not (REVISION_ARCHIVE / name).exists():
        shutil.copy2(path, REVISION_ARCHIVE / name)
for relative in ("examples/README.md", "examples/source-based/README.md"):
    path = BOOK / relative
    backup = REVISION_ARCHIVE / relative
    if path.exists() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
bundle = ROOT / "coala-book-md/vibe-coding-16-source-revised.zip"
if bundle.exists() and not (REVISION_ARCHIVE / bundle.name).exists():
    shutil.copy2(bundle, REVISION_ARCHIVE / bundle.name)

qa.update({"date": DATE, "edition": "merged-16-sessions", "manuscriptContainers": 167,
           "previousPdfPages": previous_pages, "savedPages": saved_pages, "practiceCards": 40,
           "uniqueAssets": 34, "retainedRasterAssets": 29, "retainedRasterPlacements": 30,
           "nativeVectorAssets": 4, "generatedVectorAssets": 1, "totalVectorAssets": 5,
           "canvaFlowchartPreviewAssets": 4, "nativeFlowchartSourceChecks": vector_checks,
           "sourcePdfHashVerified": source_pdf_checked, "generatedSummaryVerification": summary_check,
           "apiReferencePages": api_reference_pages, "apiPracticeExcluded": True,
           "bookmarks": 16, "contentsLinks": contents_links, "fonts": fonts,
           "standardPdfFonts": sorted(standard_fonts), "robotReferencePages": robot_mentions,
           "editorialReferencePages": editorial_mentions,
           "executedCodeHashesUnchanged": True, "codeHashes": current_hashes,
           "executedCodeBlocks": 12, "executedCodePassed": 12, "codeOutputsUnchanged": True,
           "retainedImagePixelsAndPrintWidthUnchanged": True,
           "declarationSymbol": "six-sided preparation symbol",
           "loopVerification": {"physicalPage": loop_physical_page, "trace": trace, "iterations": 10,
                                "exit": {"time1": time1, "total": total},
                                "updateOrder": flows["loop_trace"]["updates"]},
           "movieBoundaryVerification": movie_boundaries,
           "hallucinationPageVerification": hallucination_check,
           "pageMergeEditionComparison": merge_comparison,
           "calculatorResultWidgetCorrection": calculator_correction_check,
           "referenceSourceUpdateVerification": source_reference_check,
           "pdfSha256": metadata["pdfSha256"], "manuscriptSha256": metadata["manuscriptSha256"],
           "typography": {"bodyPt": 14, "bodyLeadingPt": 28, "sectionHeadingPt": 15, "chapterTitlePt": 25},
           "removedManuscriptIds": sorted(removed_ids), "newManuscriptIds": sorted(new_ids),
           "previousPhysicalPagesMapping": mapping})
qa_path = PDF.with_name(PDF.stem + "-qa.json")
write_json(qa_path, qa)
write_json(BOOK / "page-merge-comparison.json", merge_comparison)
write_json(BOOK / "calculator-widget-correction.json", calculator_correction_check)
write_json(BOOK / "graph-first-edition-comparison.json", {
    "date": DATE, "status": "historical-comparison-archived",
    "description": "그래프 선행·API 제외 과정 개편 비교는 이전 판의 기록으로 보존",
    "archivedRecord": "previous-reports/20261011-before-second-compaction/graph-first-edition-comparison.json",
    "currentComparison": "page-merge-comparison.json"})
write_json(BOOK / "hallucination-page-comparison.json", {
    "date": DATE, "status": "historical-comparison-archived",
    "description": "직전 환각 예시 교체에서 7쪽만 바뀐 기록은 이전 판의 검증이며 현재 과정 개편의 변경 범위가 아님",
    "archivedRecord": "previous-reports/20261011-before-second-compaction/hallucination-page-comparison.json",
    "currentComparison": "page-merge-comparison.json"})
write_json(BOOK / "hallucination-source-review.json", {
    "date": DATE, "physicalPage": 7, "sourceId": "ch01-ethics", "actualAiOutput": False,
    "notice": "다음 답변은 환각을 살펴보기 위해 만든 학습용 가상 오답입니다.",
    "examples": HALLUCINATION_EXAMPLES, "sourcesReviewedDate": DATE,
    "verificationTask": "질문의 전제·연도·작가를 근거 자료와 비교하고 맞음·틀림·확인하지 못함으로 구분",
    "pdfSha256": metadata["pdfSha256"], "manuscriptSha256": metadata["manuscriptSha256"],
    "layoutVerification": hallucination_check})

write("source-reference-review.md", f"""# 새 기준 PDF 대조·적용 검토 · {DATE}

현재 학생용 완성본은 output/pdf/{PDF.name}, A4 {current_pages}쪽입니다. 이 기록은 제작 관리용이며 학생용 본문에 원본 대조·출처 쪽수·긴 파일 경로를 넣지 않습니다.

- 새 기준 파일: {source_reference['workspace_source_pdf']}
- 새 기준 SHA-256: {source_reference['source_sha256']}
- 기준 PDF: {source_reference['source_pages']}쪽.
- 이전 기준 파일: {source_reference['previous_source_pdf']}
- 이전 기준 SHA-256: {source_reference['previous_source_sha256']}

## 대조 결과

공백을 정규화한 158쪽 본문이 모두 동일하고 페이지 크기도 같습니다. 현재 사용하는 UI 이미지 21개의 디코딩 픽셀·크기, 순서도 4개의 좌표·도형·선·채움 경로도 같습니다. 따라서 새 원본을 기준으로 삼기 위해 학생용 내용을 다시 작성할 부분은 없었습니다.

반해상도 렌더링 비교에서는 {source_reference['preview_comparison']['nonzero_difference_pages']}쪽에 미세한 차이가 있었으나 RGB 채널 최대 차이는 {source_reference['preview_comparison']['maximum_rgb_channel_difference']}이고 최대 다른 픽셀 비율은 {source_reference['preview_comparison']['maximum_different_pixel_percentage']}%입니다. 이는 본문·배치·그림 변경으로 판정하지 않았습니다. PDF 파일의 바이트까지 동일하다는 뜻은 아닙니다.

## 현재 교재 적용

asset-manifest.json·flow-source-map.json·practice-source-map.json의 기준 파일·SHA-256을 새 값으로 일치시켰습니다. 기존 추출 자산은 새 기준 원본의 이미지 픽셀·벡터 경로와 동일함을 확인해 그대로 사용했습니다. 자산을 새로 추출하거나 학생용 본문을 수정하지 않았습니다.

직전 fld3 정정판과 학생용 원고 SHA-256·전체 layout·이미지 35개 배치·차시 시작 쪽이 같습니다. 16차시·40개 실습·134쪽, 계산기 결과 위젯 fld3, API·코코봇 제외 구성을 유지했습니다. 139→134쪽 통합 기록의 비교 기준도 유지합니다.

세부 증거는 [검증 JSON](source-reference-review.json)과 output/pdf/{PDF.stem}-qa.json에 보관합니다. 새 원본이 로컬에 있으면 파일 해시를 직접 검증하고, 원본이 없는 다른 컴퓨터에서는 보존 검증 기록과 포함 자산 해시 확인을 구분합니다. 일반 PDF 재생성에는 새 원본 PDF가 필요하지 않습니다.
""")

chapter_table = ["| 차시 | 주제 | 실습 카드 |", "|---|---|---|"]
curriculum_table = ["| 차시 | 주제 | 핵심 활동 | 실습 | 관리용 출처 쪽 |", "|---|---|---|---|---|"]
teacher_table = ["| 차시 | 운영할 활동 |", "|---|---|"]
for number in range(1, 17):
    chapter_table.append(f"| {number} | {chapter_titles[number]} | {practice_counts[number]} |")
    curriculum_table.append(f"| {number} | {chapter_titles[number]} | {ACTIVITIES[number]} | {practice_counts[number]} | {SOURCE_PAGES[number]} |")
    teacher_table.append(f"| {number} | {ACTIVITIES[number]} |")
chapter_table_text = "\n".join(chapter_table)
current_structure = "12차시 Matplotlib → 13차시 입력 Chart → 14차시 학생 자료·저장 → 15차시 Pandas → 16차시 자율 프로젝트"
asset_counts = "PNG 34개·벡터 PDF 5개·전체 배치 35곳"
content_counts = "16차시·167개 원고 컨테이너·40개 실습 카드·12개 실행 코드·4개 순서도"
archive_notice = "직전 139쪽 그래프 선행판과 관리 기록은 previous-reports/20261011-before-second-compaction에 보관했습니다. 이전 통합·과정 개편 기록도 previous-reports에 남아 있습니다."
student_policy = "학생용 본문에는 원본 대조·출처 쪽수·제작 과정·PDF 안내 문구를 넣지 않습니다. 출처와 검증 기록은 별도 관리 문서에 보관합니다."
revision_summary = f"직전 {previous_pages}쪽에서 내용이 이어지는 5쌍을 통합해 {current_pages}쪽으로 줄였습니다. 38·39쪽의 7차시 도입·개념을 한 장에 놓고 Chart 도입·완료 확인, 저장 화면, DataFrame 이름 변경의 반복 안내를 간결하게 정리했습니다. 모든 실습 조건·확인 항목·코드·결과·이미지 크기를 유지했습니다."
widget_correction_summary = "계산기 2의 57·58쪽 결과 위젯 설명 두 문장을 fld3로 바로잡았습니다. 별도의 Text·구구단 실습에서 사용하는 txt1은 유지합니다."
reference_summary = f"기준 파일을 {source_reference['workspace_source_pdf']}로 갱신했습니다. 새 원본의 공백 정규화 본문·현재 UI 이미지 21개·네이티브 순서도 경로를 기존 기준과 대조한 결과 학습 내용 변경이 없었습니다. 따라서 학생용 원고·실습·코드·이미지·지면을 fld3 정정판과 동일하게 유지하고 관리용 기준 파일 정보만 바꿨습니다."
preservation_summary = "실행 코드 12개와 출력의 해시를 유지했습니다. 남은 기존 래스터 이미지 29개·배치 30곳의 픽셀·출력 폭·비율과 원본 순서도 4개를 보존했습니다. 7쪽 역사·문학 가상 오답 설명은 그대로 유지합니다."
quality_summary = f"{current_pages}쪽 전체 렌더링에서 글자·상자 넘침·원고 ID 누락·목차 오류·대체 문자·코드 내용 차이 0입니다. 학생용 본문의 기관 로고·원본 대조·PDF 안내·코코봇·API 과정 언급 0을 확인했습니다. 목차 링크·차시 책갈피 각 16개와 주요 글꼴 포함을 확인했습니다."
fence = chr(96) * 3

write("README.md", f"""# AI와 함께하는 바이브 코딩 · 그래프 선행 16차시 완성본

{DATE} 현재 구성: **{current_structure}**. 1~11차시는 기본 개념과 앱 위젯 실습, 12~15차시는 그래프·자료 활용, 16차시는 프로젝트입니다.

- [현재 학생용 PDF](../../output/pdf/{PDF.name}): A4 {current_pages}쪽.
- [전체 원고](book.md): ch01.md~ch16.md를 합친 167개 컨테이너.
- [16차시 구성](curriculum.md), [교사용 안내](teacher-guide.md), [수정·재생성 지침](notes.md).
- [페이지 통합 검토](page-merge-review.md), [이전→현재 지면 대응](page-compaction-review.md).
- [PDF 검토](pdf-final-review.md), [검증 요약](validation-summary.md).
- [이미지 미리보기](asset-review.html): {asset_counts}.
- [Python 예제](examples/source-based/README.md): 12차시 Matplotlib 7개·15차시 Pandas 5개.
- [7쪽 사실 확인 근거](hallucination-source-review.md), [순서도 검증](flow-source-review.md).
- [새 기준 파일 검증](source-reference-review.md), [검증 근거 JSON](source-reference-review.json).

{chapter_table_text}

{revision_summary} {preservation_summary}

{reference_summary}

{content_counts}. {student_policy}

다른 컴퓨터에서는 상위 폴더 vibe-coding-16-source-revised.zip의 START-HERE.txt를 확인합니다. PDF는 바로 열 수 있습니다. {archive_notice}
""")

write("curriculum.md", f"""# 그래프 선행 16차시 구성 · {DATE}

{current_structure}

Matplotlib에서 그래프의 기본 표현을 먼저 확인하고 입력 Chart와 자료·저장으로 연결합니다. Matplotlib 예제는 리스트·NumPy를 사용하므로 Pandas 선행 학습이 필요하지 않습니다. 공공데이터 API 실습은 현재 과정에서 제외했습니다.

{chr(10).join(curriculum_table)}

총 16차시·40개 실습 카드입니다. 출처 쪽수는 제작 관리용이며 학생용 본문에는 표시하지 않습니다. 14차시에는 기준 교재 106~110쪽과 118~127쪽의 학생 자료·학교별 학생 수·저장 활동을 사용합니다. 제외 범위는 111~117쪽입니다. 수업 시간에 맞춰 핵심·선택 활동을 운영합니다.
""")

write("teacher-guide.md", f"""# 교사용 운영 안내 · 그래프 선행 16차시 · {DATE}

{current_structure}

1~7차시는 AI 질문·문제 분해·순서도·반복과 조건, 8~11차시는 알고플로/Flet 디자이너의 위젯을 다룹니다. 12차시는 Python·Matplotlib·NumPy로 그래프를 표현하고, 13차시는 직접 입력 Chart, 14차시는 학생 자료·학교별 학생 수·저장과 불러오기, 15차시는 Pandas, 16차시는 프로젝트입니다.

학생 100명 자료와 저장 환경을 수업 전에 준비합니다. GUI 메뉴·저장 동작은 수업 도구에서 확인합니다. 한글 축 제목을 사용하는 Matplotlib 예제는 한글 글꼴을 설정합니다. API 주소·인증키는 이번 과정의 준비 항목이 아닙니다.

{chr(10).join(teacher_table)}

12차시의 여덟 그래프 활동은 코드 7개를 사용하고, 제목·설명 활동은 앞 그래프를 함께 활용합니다. 13차시는 입력값·축·누적 여부를 확인합니다. 14차시는 자료의 열과 저장 전후 값을 확인합니다. 15차시의 세 실습은 코드 5개를 사용합니다.

5쪽 그림은 AI가 제안하고 사람이 목적·근거·실행 결과를 확인한 뒤 수정하는 관계를 설명합니다. 새 실습 과제를 추가한 것은 아닙니다. 7쪽 두 답변은 설명을 위해 만든 학습용 가상 오답이며 실제 AI 출력 기록이 아닙니다. 제1차 십자군의 기간 1096~1099년, 『연금술사』의 작가 파울로 코엘료·첫 출간 1988년을 근거와 비교합니다.

{loop_physical_page}쪽은 total에 time1을 먼저 더하고 time1을 1 증가시킵니다. 누적값은 1, 3, 6, 10, 15, 21, 28, 36, 45, 55이며 time1=11에서 종료합니다. 선언 기호는 6각형입니다. {movie_physical_page}쪽 영화 조건은 15세 미만 관람 불가이고 14·15·16·13세의 결과는 불가·가능·가능·불가입니다. N명 점수 판정·80점 조건은 별도로 유지합니다.

examples/source-based의 12개 코드는 원고와 같습니다. 코드·출력은 이전 실행 검증본과 동일합니다. GUI·저장을 새로 실행하지 못했으면 그 상태를 기록합니다. 출처·제작·검증 메모는 이 관리 문서에서 다룹니다.
""")

write("notes.md", f"""# 다음 수정·재생성 관리 지침 · {DATE}

## 현재 구성

{current_structure}

{content_counts}. {asset_counts}. 공공데이터 API 과정·인증키 입력·지하철 API 과제를 다시 넣지 않습니다. 14차시는 학생 자료·학교별 학생 수·저장과 불러오기 3개 실습입니다. 기존 과제·입력값·위젯·코드·결과를 우선하고 새 앱·임의 숫자 과제를 추가하지 않습니다.

## 학생용 내용과 지면

{reference_summary} 기준 파일 SHA-256은 {assets['source_sha256']}입니다. 검증은 source-reference-review.md/json에서 관리합니다. 이 안내는 학생용 본문에 넣지 않습니다.

{widget_correction_summary} 상세 검증은 calculator-widget-correction.json에 있습니다.

{student_policy} 캡션은 보이는 내용·입력·동작·결과를 설명합니다. AI 답변의 근거 확인은 학습 내용으로 유지합니다. 7쪽은 역사·문학 질문의 학습용 가상 오답이며 실제 AI 출력으로 소개하지 않습니다. 사실 확인 출처는 hallucination-source-review.md/json에 보관합니다.

5쪽 요약 그림은 assets/ch01/ai-human-summary.pdf를 인쇄 벡터로 사용하고 같은 이름의 PNG를 Canva용으로 준비했습니다. 원본 순서도 4개는 assets/source-flowcharts의 벡터 PDF와 PNG를 사용합니다. 본문 14pt·행간 28pt·소제목 15pt·차시 제목 25pt를 유지합니다. 흰 배경·선명한 글자·둥근 실습 상자를 사용하고 기관 로고·대형 빈 기록칸을 추가하지 않습니다. 짧은 연속 내용은 읽는 순서대로 함께 배치합니다.

## 일상 수정·재생성

각 chXX.md를 수정한 후 전체 원고 조합→파서→조판→전체 렌더링→보고 순서로 진행합니다. 저장소 루트에서 Node 앱 파서·Python 패키지·필요 글꼴을 준비합니다.

{fence}powershell
python scripts/finalize_student_manuscript.py
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/{PDF.name}
python scripts/review_textbook_pdf.py --pdf output/pdf/{PDF.name} --dest tmp/pdfs/source7-edition-review
python scripts/report_apps_edition.py
{fence}

이전 과정 재편 스크립트나 prepare_source_flowcharts.py는 일상 편집 때 실행하지 않습니다. 후속 수정을 덮어쓸 수 있습니다. prepare_source_flowcharts.py는 원본 순서도 재추출 때만 사용하며 원본 PDF·PyMuPDF가 필요하고 ch04/ch07의 문구도 적용합니다. 현재 포함된 벡터 자산으로 PDF를 만드는 데는 원본 PDF·PyMuPDF가 필요하지 않으며 pypdf를 사용합니다.

원본 순서도를 다시 추출해야 할 때 기준 파일은 flow-source-map.json의 source_pdf를 사용합니다. 여러 PDF 중 폴더의 첫 파일을 임의로 고르지 않습니다. 이번 기준 갱신에서는 검증된 기존 자산을 유지하고 재추출하지 않았습니다.

flow-source-map.json의 flowchart_sha256와 해당 원고 블록을 일치시킵니다. 논리를 바꾸면 그림·문구·맵을 함께 검토합니다. 보고는 전체 렌더링 검토 이후 실행합니다. 직전 비교 기준은 previous-reports/20261011-before-second-compaction입니다. 묶음에는 이전 metadata·코드 검증 JSON과 수정 근거 문서만 포함합니다. 이전 PDF·이미지·원고는 포함하지 않습니다.

원본 파일이 있으면 해시를 직접 확인하고 없으면 보존 출처 기록과 포함 자산의 해시를 검증합니다. 본문 글꼴은 Wanted Sans·Windows Consolas이며 순서도는 원본 벡터 글자·도형을 보존합니다. Canva 안내는 flowchart-canva.md를 참고합니다.
""")

write("canva-production-status.md", f"""# 제작 상태 · 그래프 선행 16차시 · {DATE}

[현재 학생용 완성본](../../output/pdf/{PDF.name})은 A4 {current_pages}쪽의 독립 PDF입니다. {content_counts}. {asset_counts}.

{current_structure}. {revision_summary} {preservation_summary}

독립 PDF와 Canva용 자산을 완성했습니다. Canva 디자인 자체를 이번 과정으로 다시 생성한 것은 아닙니다. Canva 이미지 입력에는 현재 자산 폴더를 지정합니다. 인쇄 순서도·요약 그림은 벡터 PDF를 사용합니다. {archive_notice}
""")

write("validation-summary.md", f"""# 검증 결과 · 그래프 선행 16차시 · {DATE}

현재 학생용 PDF A4 {current_pages}쪽입니다. book.md와 ch01.md~ch16.md의 17개 파일이 파서·레이아웃 검사에 통과했습니다. 167개 원고 컨테이너, Canva 앱 추정 {canva_pages}장입니다.

- 실습 40개: 12차시 8개·13차시 3개·14차시 3개·15차시 3개·16차시 1개.
- 코드 12개·출력 유지. 코드 SHA-256·출력 해시 동일, 출력 코드 내용 차이 0.
- 기존 래스터 29개·배치 30곳과 전체 35개 이미지 배치의 픽셀·출력 폭·비율 유지.
- 원본 순서도 벡터 4개·5쪽 자체 제작 요약 벡터 1개 유지.
- PNG 34개·벡터 PDF 5개·지면 배치 35곳. 자산 해시·픽셀·벡터 1쪽·내부 래스터 객체 0 확인.
- 5쪽의 AI 제안·사람 확인 요약, 7쪽 가상 오답·직접 확인·책임 있는 사용 한 장 배치.
- {loop_physical_page}쪽 누적 10회·종료 time1=11·total=55, 15세 영화 관람 경계 유지.

{quality_summary}

직전 {previous_pages}쪽 판의 각 원고 ID와 물리 지면 대응, 실제 통합 5쌍은 page-merge-comparison.json에 기록했습니다. 167개 ID·40개 실습·완료 확인 항목·코드·이미지를 보존했습니다. GUI·저장을 새로 실행했다고 주장하지 않습니다. 상세는 validation-full.json, code-results.json 및 output/pdf/{qa_path.name}입니다.
""")

write("pdf-final-review.md", f"""# 독립 PDF 검토 · 그래프 선행 16차시 · {DATE}

[현재 완성본](../../output/pdf/{PDF.name})은 A4 {current_pages}쪽이며 직전 환각 수정판은 {previous_pages}쪽입니다.

## 내용과 구성

{current_structure}. {revision_summary}

{widget_correction_summary} 지면 통합·과정 구성·글꼴·이미지 크기는 유지했습니다.

{reference_summary} 이번에는 필수 본문 수정이 없었으며 직전 학생판과 원고 SHA-256·전체 layout·이미지 배치·차시 시작 쪽이 일치합니다.

{content_counts}. {preservation_summary} {student_policy}

## 조판과 검증

본문 14pt·행간 28pt·소제목 15pt·차시 제목 25pt를 유지하고 주요 글꼴을 포함했습니다. 요약 그림 1개와 순서도 4개는 네이티브 벡터를 인쇄에 사용합니다. PNG 34개는 캡처·실행 결과 및 Canva용 미리보기입니다. 벡터의 DPI를 래스터 해상도로 해석하지 않습니다.

{quality_summary}

실제로 통합한 5개 지면과 전체 {current_pages}쪽을 검토했습니다. 현재 167개 ID의 identity 매핑을 사용하며 추가·제거한 ID는 없습니다. 원본 순서도·5쪽 요약·7쪽 가상 오답은 유지했습니다. 65·66쪽은 읽기 밀도를 검토한 뒤 각각 유지했습니다. 현재 비교는 page-merge-comparison.json입니다.

원본 캡처의 작은 글자를 복원했다거나 GUI·저장을 새로 실행했다고 주장하지 않습니다. {archive_notice}
""")

handover = f"""# 그래프 선행 16차시 완성본 인계 · {DATE}

- 학생용 PDF: output/pdf/{PDF.name}, A4 {current_pages}쪽.
- 원고: book.md와 ch01.md~ch16.md, 167개 컨테이너·16차시.
- 구성: {current_structure}.
- 실습: 40개. 코드: examples/source-based Python 12개, 12차시 7개·15차시 5개.
- 자산: {asset_counts}. 자체 제작 요약 그림 1개·원본 순서도 4개.
- 제외: 공공데이터 API 실습·관련 컨테이너 3개·결과 이미지 1개.
- QA: output/pdf/{qa_path.name}; 페이지 통합 비교: page-merge-comparison.json.
- 전달: 상위 폴더 vibe-coding-16-source-revised.zip.

{student_policy} {archive_notice}

다른 컴퓨터에서는 PDF를 바로 열 수 있습니다. 저장소에서 수정하려면 ZIP의 vibe-coding-16 폴더를 coala-book-md/vibe-coding-16에 복사하고 output·scripts도 복사합니다. START-HERE.txt·notes.md를 확인합니다.
"""
write("handover.md", handover)
write("final-draft.md", handover.replace("# 그래프 선행 16차시 완성본 인계", "# 현재 전달본 · 그래프 선행 16차시"))

write("print-activities.md", f"""# 실습 결과·기록 안내 · {DATE}

현재 40개 실습 카드와 차시별 완료 확인을 사용합니다. 입력값·연산·표·그래프·수정 전후 실행 결과를 기록합니다. 임의 숫자·새 앱 과제를 추가하지 않습니다.

12차시는 Matplotlib 코드와 그래프, 13차시는 직접 입력값과 Chart, 14차시는 학생 자료·학교별 학생 수·저장 전후 값, 15차시는 Pandas 표·행·열, 16차시는 프로젝트 아이디어·UI·실행 결과를 확인합니다. API 과제는 제외했습니다.

5쪽은 두 역할의 요약이며 별도 실습이 아닙니다. 7쪽 가상 오답은 실제 AI 실행 결과로 제출하지 않고 질문의 전제·연도·작가를 근거와 비교합니다. {loop_physical_page}쪽은 누적 후 증가하는 순서와 10이 포함되는지 확인합니다. 출처·제작 메모와 대형 빈 기록칸을 학생용 본문에 추가하지 않습니다.
""")

previous_audit = (ARCHIVE / "source-audit.md").read_text(encoding="utf-8")
corrections = previous_audit.split("## 포함한 내용의 수정 근거", 1)[1].split("## 코드와 이미지 검증", 1)[0]
write("source-audit.md", f"""# 제작 관리용 출처·수정 기록 · {DATE}

기준 PDF: {assets['source_pdf']}
SHA-256: {assets['source_sha256']}. 원본 파일은 수정하지 않았습니다.

{reference_summary} 상세 근거는 source-reference-review.md/json에 있습니다. 기준 갱신은 학생용 본문 수정과 구분합니다.

## 현재 범위

{current_structure}. 12차시는 128~145쪽, 13차시는 95~105쪽, 14차시는 106~110·118~127쪽, 15차시는 146~151쪽, 16차시는 93~94쪽을 사용합니다. 공공데이터 API 111~117쪽과 코코봇 내용은 현재 과정에서 제외했습니다.

{revision_summary} 5쪽 요약 그림은 현재 교육 내용을 설명하기 위해 자체 제작한 벡터이며 원본에서 추출했다고 소개하지 않습니다. {student_policy}

## 포함한 내용의 수정 근거
{corrections}

## 코드와 이미지 검증

{preservation_summary} 남은 원본 캡처 21개·실행 그래프 7개·실행 표 1개에 원본 순서도 PNG 4개·자체 제작 요약 PNG 1개를 더해 PNG 34개입니다. 인쇄에는 순서도 벡터 PDF 4개와 요약 벡터 PDF 1개를 사용합니다.

순서도 자산은 crop 밖 글자와 전체 페이지 회색 배경만 정리하고 도형·연결·글꼴·경로·색을 보존했습니다. 원본 파일을 새로 직접 검증했는지는 QA의 sourcePdfHashVerified에 기록합니다. 원본이 없는 환경에서는 보존 기록과 포함 자산 해시 확인을 구분합니다.

7쪽 가상 오답은 실제 AI 출력이 아니며 확인한 사실과 출처는 hallucination-source-review.md/json에 있습니다. 작은 UI 캡처를 고해상도로 복원했다거나 GUI를 새로 실행했다고 주장하지 않습니다.
""")

practice_rows = ["| 차시 | 현재 실습 | 관리용 출처 쪽 | 기준 예시 |", "|---|---|---|---|"]
for item in catalog:
    practice_rows.append(f"| {item['chapter']} | {item['practice_id']} {item['title']} | {item['source_pdf_pages']} | {item['source_label']} |")
write("practice-source-review.md", f"""# 제작 관리용 실습 대응 기록 · {DATE}

현재 16차시·40개 실습 카드입니다. {current_structure}

Matplotlib 8개 활동을 12차시, 입력 Chart 3개를 13차시, 학생 자료·학교별 학생 수·저장 3개를 14차시에 두었습니다. API 실습 1개와 컨테이너 3개·결과 이미지 1개를 제외했습니다. 기존 과제·데이터·위젯·결과를 유지했고 코드 12개와 출력의 해시도 같습니다.

5쪽 그림은 기존 개념의 요약이며 실습을 추가하지 않았습니다. 7쪽 역사·문학 가상 오답은 학습용임을 표시합니다. 원본 순서도 4개와 {loop_physical_page}쪽 반복 결과 55·15세 관람 경계를 유지합니다. 원본이 값을 정하지 않은 과제는 학생이 직접 입력합니다.

메시지 창·학생 100명·학교별 학생 수·Matplotlib 여덟 그래프 활동·mon~sun DataFrame을 사용합니다. 계산기는 두 숫자와 사칙연산 기호를 사용합니다. 수업 전에는 학생 자료·GUI 저장 환경을 준비하며 API 주소·인증키를 요구하지 않습니다.

{chr(10).join(practice_rows)}

이 기록은 관리용이며 학생용 본문에는 표시하지 않습니다. 이전 대응표는 previous-reports/20261011-before-second-compaction에 보관했습니다.
""")

flow_rows = ["| 현재 쪽 | 순서도 | 관리용 출처 쪽 | 벡터 PDF | Canva용 PNG |", "|---|---|---|---|---|"]
for item in diagrams:
    flow_rows.append(f"| {page_numbers(new_pages_by_id[item['page_id']])} | {item['alt']} | {item['source_pdf_page']} | {item['vector_src']} | {item['src']} |")
write("flow-source-review.md", f"""# 순서도 재사용·검증 · {DATE}

순서도 4개는 기준 교재의 네이티브 벡터를 사용합니다. Canva용 300dpi PNG는 별도 미리보기이며 인쇄 PDF의 그림은 래스터가 아닙니다.

{chr(10).join(flow_rows)}

각 자산은 1쪽·래스터 이미지 객체 0이며 PNG·벡터·cropbox·원고 논리 해시를 확인했습니다. 도형·글꼴·연결·경로·색은 보존했고 crop 밖의 글자와 전체 페이지 회색 배경만 정리했습니다. 원본 PDF 자체는 수정하지 않았습니다. 원본 파일의 직접 해시 확인 여부는 QA에 기록합니다.

선언은 6각형입니다. {loop_physical_page}쪽 반복은 time1=1·total=0에서 시작해 total에 time1을 더하고 time1을 1 증가시킵니다. 10회 후 time1=11·total=55로 종료합니다. {movie_physical_page}쪽 영화 조건은 15세 미만 관람 불가입니다. N명·80점 점수 판정 활동은 별도로 유지합니다.

5쪽의 자체 제작 요약 벡터 1개를 그대로 유지했습니다. 7쪽 가상 오답 내용은 직전 판과 같습니다. 전체 {current_pages}쪽 조판 검토를 마쳤으며 이 보고서는 원고·그림·코드를 변경하지 않습니다.
""")

write("flowchart-canva.md", f"""# Canva 순서도·요약 그림 안내 · {DATE}

현재 순서도 4개와 요약 그림 1개를 준비했습니다. 독립 인쇄 PDF에는 네이티브 벡터 PDF 5개를 사용합니다. Canva에는 같은 이름의 PNG를 입력합니다.

{chr(10).join(flow_rows)}

5쪽 요약 그림은 assets/ch01/ai-human-summary.png를 사용합니다. 순서도는 assets/source-flowcharts 폴더의 PNG 4개를 사용합니다. 비율을 유지하고 글자·화살표·분기가 잘리지 않게 배치합니다. PNG 내부 노드가 각각 편집 가능한 Canva 도형이 되는 것은 아닙니다.

원본 순서도의 선언은 6각형이고 글꼴·노드·연결을 보존합니다. 벡터에는 DPI를 적용하지 않습니다. PNG의 effectiveDpi는 대체 미리보기 파일 정보입니다. 상세 출처·해시는 flow-source-map.json·asset-manifest.json·현재 QA에 있습니다.

prepare_source_flowcharts.py는 원본 재추출 때만 사용하며 원본 PDF·PyMuPDF가 필요하고 일부 원고 문구도 적용합니다. 일상 원고 편집·현재 자산 PDF 재생성에서는 실행하지 않습니다.
""")

write("hallucination-source-review.md", f"""# 7쪽 환각 예시 사실 검증 · {DATE}

두 답변은 환각을 살펴보기 위해 만든 **학습용 가상 오답**이며 실제 AI 실행에서 수집한 응답이 아닙니다. 직전 판의 내용을 유지했습니다.

- 역사 질문: {HALLUCINATION_EXAMPLES[0]['question']}
- 가상 오답: {HALLUCINATION_EXAMPLES[0]['learning_only_wrong_answer']}
- 사실: {HALLUCINATION_EXAMPLES[0]['verified_fact']} [OpenStax · The Crusading Movement]({HALLUCINATION_EXAMPLES[0]['source_url']})

해당 절의 Figure 13.19 기간 표시와 1099년 예루살렘 도착 설명을 확인했습니다.

- 문학 질문: {HALLUCINATION_EXAMPLES[1]['question']}
- 가상 오답: {HALLUCINATION_EXAMPLES[1]['learning_only_wrong_answer']}
- 사실: {HALLUCINATION_EXAMPLES[1]['verified_fact']} [작가재단 · The Alchemist]({HALLUCINATION_EXAMPLES[1]['source_url']})

작가·주인공 산티아고·첫 출간 연도를 확인했습니다. 질문의 전제·연도·작가를 근거와 비교하고 맞음·틀림·확인하지 못함으로 구분합니다. 긴 웹 URL·제작 메모는 학생용 본문에 넣지 않습니다.

7쪽 본문 끝 좌표는 {ethics_layout['y']:g}pt이며 가상 오답·사실 확인·책임 있는 사용을 한 장에 배치했습니다. 현재 PDF 해시는 hallucination-source-review.json·현재 QA에 있습니다. 이번 변경 범위는 page-merge-comparison.json으로 확인합니다.
""")

asset_rows = ["| 파일 | 구분 | 픽셀 | 사용 원고 ID |", "|---|---|---|---|"]
asset_cards = []
for item in assets["items"]:
    if item["src"] == summary_asset["src"]:
        label = "자체 제작 AI·사람 역할 요약 · 인쇄 벡터와 Canva용 PNG"
    elif item.get("vector_src"):
        label = f"기준 PDF {item['source_pdf_page']}쪽 순서도 · 인쇄 벡터와 Canva용 PNG"
    elif item["kind"] == "user-supplied-pdf-embedded-image":
        label = f"기준 PDF {item['pdf_page']}쪽 캡처"
    else:
        label = "검증한 코드 실행 결과"
    used = item["used_in"] if isinstance(item["used_in"], list) else [item["used_in"]]
    asset_rows.append(f"| {item['src']} | {label} | {item['width']}×{item['height']} | {', '.join(used)} |")
    asset_cards.append(f'<article><h2>{html.escape(Path(item["src"]).name)}</h2><p>{html.escape(label)}</p><img src="{html.escape(item["src"])}" alt="{html.escape(label)}"><p>{item["width"]} × {item["height"]}</p></article>')
write("asset-audit.md", f"""# 제작 관리용 자산 검증 · {DATE}

{asset_counts}. 기존 원본 캡처 21개·실행 그래프 7개·실행 표 1개, 원본 순서도 PNG 4개, 자체 제작 요약 PNG 1개입니다. 인쇄에는 순서도 벡터 4개·요약 벡터 1개를 사용합니다.

기존 래스터 29개·배치 30곳의 픽셀·출력 폭·비율과 순서도 4개를 유지했습니다. 현재 34개 PNG·5개 벡터 자산 전체를 직전 판과 동일하게 유지했습니다. 벡터에는 DPI를 적용하지 않으며 effectiveDpi는 별도 PNG 대체 파일에 대한 정보입니다. 요약 그림은 자체 제작 자산임을 구분합니다.

{chr(10).join(asset_rows)}
""")
write("asset-review.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><title>현재 교재 PNG 34개</title><style>body{font-family:Malgun Gothic,sans-serif;margin:32px;background:white}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}article{border:1px solid #ccc;padding:16px}img{max-width:100%;height:auto}h2{font-size:18px}</style><h1>그래프 선행 16차시 PNG 34개</h1><p>' + DATE + ' · 인쇄용 벡터 PDF 5개·배치 35곳. 관리용 미리보기입니다.</p><main>' + ''.join(asset_cards) + '</main></html>')

merge_rows = ["| 직전 쪽 | 현재 쪽 | 이어진 내용 | 조정 |", "|---|---|---|---|"]
for item in selected_pair_checks:
    merge_rows.append(f"| {'·'.join(map(str, item['previousPages']))} | {item['currentPage']} | {', '.join(item['sourceIds'])} | {item['edit']} |")
merge_table = "\n".join(merge_rows)
edition_review = f"""# 페이지 통합 검토 · {DATE}

현재 [완성 PDF](../../output/pdf/{PDF.name})는 A4 {current_pages}쪽입니다. 직전 그래프 선행판 {previous_pages}쪽에서 5쌍을 합쳐 {saved_pages}쪽을 줄였습니다.

{merge_table}

{widget_correction_summary} 이 두 문장 정정은 통합된 지면·자산·코드에 영향을 주지 않습니다.

38·39쪽의 7차시 도입과 반복·조건 개념을 한 장에 놓았습니다. 13차시의 도입과 그래프 구분, 막대그래프 결과와 완료 확인도 각각 한 장으로 합쳤습니다. 저장 화면은 반복 안내·일반 소제목을 간결하게 정리해 같은 이미지가 두 쪽으로 나뉘던 배치를 해소했습니다. DataFrame 행·열 이름 변경은 한 문장으로 요약했습니다.

167개 원고 ID와 40개 실습을 모두 유지했습니다. 체크 항목·코드 12개·출력 5개·이미지 35개 배치와 자산 34 PNG·5 벡터를 보존했습니다. 글꼴 크기·본문 행간과 이미지의 출력 폭·비율을 줄이지 않았습니다. 65·66쪽은 한 장으로 합치면 읽기 여유가 부족해 각각 유지했습니다.

{current_structure}. API 제외 구성·5쪽 요약·7쪽 역사/문학 가상 오답·순서도 4개를 유지합니다. 현재 순서도 쪽수는 {', '.join(str(item['physicalPages'][0]) for item in vector_checks)}입니다. 목차와 차시 시작 쪽은 현재 metadata와 일치합니다.

{quality_summary}

이번 비교는 page-merge-plan.json의 167개 ID identity 매핑과 page-merge-comparison.json을 사용합니다. 이전 graph-first-restructure.json의 과정 재편 매핑을 다시 적용하지 않습니다. 이전의 179→149쪽 및 과정 개편 기록은 보관 폴더에 유지합니다. {archive_notice}
"""
write("page-merge-review.md", edition_review)
write("apps-edition-review.md", edition_review.replace("# 페이지 통합 검토", "# 현재 앱 개발 교재 지면 검토"))
write("graph-first-edition-review.md", f"""# 그래프 선행 과정 개편 기록 안내 · {DATE}

현재 학생용 PDF는 output/pdf/{PDF.name}, {current_pages}쪽입니다. 그래프 선행·API 제외 과정은 유지했고 이번에는 지면 5쌍을 통합했습니다. 현재 검토는 [페이지 통합 검토](page-merge-review.md)와 page-merge-comparison.json을 확인합니다.

이전 142→139쪽 과정 개편 기록은 previous-reports/20261011-before-second-compaction/graph-first-edition-review.md와 graph-first-edition-comparison.json에 보관했습니다. 현재 identity 매핑에 이 이전 과정 매핑을 다시 적용하지 않습니다.
""")

mapping_rows = ["| 직전 쪽 | 현재 쪽 | 원고 ID | 상태 |", "|---|---|---|---|"]
for item in mapping:
    mapping_rows.append(f"| {item['previousPage']} | {page_numbers(item['currentPages'])} | {', '.join(item['previousSourceIds'])} | 현재 지면 대응 |")
write("page-compaction-review.md", f"""# 현재 페이지 통합·전체 지면 대응 · {DATE}

현재 PDF output/pdf/{PDF.name}는 {current_pages}쪽이며 직전 그래프 선행판은 {previous_pages}쪽입니다. 내용이 이어지는 5쌍을 합쳤습니다. ID 추가·제거 없이 167개 identity 매핑을 사용했습니다.

{merge_table}

각 물리 페이지의 원고 ID로 현재 지면을 찾았습니다. 이전 여러 페이지가 같은 원고 ID에 속하면 동일한 현재 지면으로 연결됩니다. 65·66쪽은 읽기 여유를 위해 별도로 유지했습니다.

{chr(10).join(mapping_rows)}

페이지 계획은 page-merge-plan.json, 보존 검증과 실제 대응은 page-merge-comparison.json입니다. 이전 과정 매핑과 더 오래된 페이지 통합 기록은 previous-reports에 보관했습니다.
""")

example_rows = ["| 차시 | 파일 | 동작 |", "|---|---|---|"]
code_titles = {page["id"]: page.get("title", page["id"]) for page in spec["pages"]}
for item in code_specs:
    example_rows.append(f"| {item['chapter']} | {item['page_id']}.py | {code_titles[item['page_id']]} |")
write("examples/source-based/README.md", f"""# 현재 교재의 Python 실행 예제 · {DATE}

12차시 Matplotlib 7개·15차시 Pandas 5개입니다. 데이터·코드·출력은 이전 실행 검증본과 동일하며 현재 차시 번호·파일 이름으로 맞췄습니다.

Python 3.10 이상에서 requirements.txt의 패키지를 설치하고 각 .py 파일을 실행합니다. 한글 축 제목은 한글 글꼴 설정이 필요합니다.

{chr(10).join(example_rows)}

실습 대응과 실행 기록은 ../../practice-source-review.md·../../code-results.json에 있습니다. 임의 콘솔 대체 활동·새 앱 과제를 추가하지 않습니다.
""")
write("examples/README.md", """# 실습 예제

현재 12차시 Matplotlib·15차시 Pandas 실행 예제 12개는 [source-based](source-based/README.md)에 있습니다. 실행 검증은 [code-results.json](../code-results.json)에서 확인합니다. index.html과 이전 assets/chXX 화면은 과거 별도 앱 초안입니다.
""")

# Package the current PDF, active assets and reporting dependencies only.
members = set()
for pattern in ("*.md", "*.json"):
    members.update(BOOK.glob(pattern))
members.add(BOOK / "asset-review.html")
members.update(BOOK / item["src"] for item in assets["items"])
members.update(BOOK / item["vector_src"] for item in assets["items"] if item.get("vector_src"))
members.update((BOOK / "examples/source-based").glob("*"))
members.add(BOOK / "examples/README.md")
members.update(ARCHIVE / name for name in
               ("vibe-coding-16-graph-first.json", "code-specs.json", "code-results.json", "source-audit.md", "practice-source-map.json"))
with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(members):
        if path.is_file():
            archive.write(path, "vibe-coding-16/" + path.relative_to(BOOK).as_posix())
    for path in (PDF, PDF.with_suffix(".json"), qa_path):
        archive.write(path, "output/pdf/" + path.name)
    for name in ("build_textbook_pdf.py", "finalize_student_manuscript.py", "finalize_textbook_pdf.py",
                 "review_textbook_pdf.py", "report_apps_edition.py", "prepare_source_flowcharts.py",
                 "prepare_intro_summary.py", "restructure_graph_first.py"):
        archive.write(ROOT / "scripts" / name, "scripts/" + name)
    archive.writestr("START-HERE.txt", f"""{DATE} 그래프 선행 16차시 학생용 완성본

완성 PDF: output/pdf/{PDF.name} (A4 {current_pages}쪽)
원고: vibe-coding-16/book.md 및 ch01.md~ch16.md (167개 컨테이너·40실습)
구성: {current_structure}
코드: vibe-coding-16/examples/source-based (Python 12개)
자산: vibe-coding-16/assets (PNG 34개·벡터 PDF 5개·배치 35곳)
통합: 5쌍의 페이지 / 유지: 5쪽 요약 그림·7쪽 가상 오답
제외: 공공데이터 API 과정
검증: output/pdf/{qa_path.name}
안내: vibe-coding-16/curriculum.md 및 notes.md

PDF는 바로 열 수 있습니다. 저장소에서 수정하려면 vibe-coding-16 폴더를
coala-book-md/vibe-coding-16에 복사하고 output·scripts도 복사합니다.
일상 재생성은 원고 조합→파서→조판→전체 렌더→보고 순서입니다.
원본 PDF·PyMuPDF는 일반 재생성에 필요하지 않습니다.
prepare_source_flowcharts.py는 원본 재추출 때만 사용합니다.

출처·검증 기록은 관리용입니다. 비교에 필요한 이전 metadata·코드 JSON과
수정 근거 문서만 포함하며 이전 완성 PDF·이미지·원고는 포함하지 않습니다.
""")

with zipfile.ZipFile(bundle) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert [name for name in names if name.startswith("output/pdf/") and name.endswith(".pdf")] == ["output/pdf/" + PDF.name]
    assert not any(is_robot_asset(name) for name in names)
    assert not any("subway-top5-result.png" in name for name in names)
    assert sum(name.startswith("vibe-coding-16/assets/") and name.endswith(".png") for name in names) == 34
    assert sum(name.startswith("vibe-coding-16/assets/") and name.endswith(".pdf") for name in names) == 5
    assert "scripts/prepare_intro_summary.py" in names
    assert "scripts/restructure_graph_first.py" in names
    for item in assets["items"]:
        assert digest(archive.read("vibe-coding-16/" + item["src"])) == item["sha256"]
        if item.get("vector_src"):
            assert digest(archive.read("vibe-coding-16/" + item["vector_src"])) == item["vector_sha256"]
    assert sum(name.startswith("vibe-coding-16/examples/source-based/") and name.endswith(".py") for name in names) == 12
    assert sum(name.startswith("vibe-coding-16/ch") and name.endswith(".md") for name in names) == 16
    packaged_hash = digest(archive.read("output/pdf/" + PDF.name))
    assert packaged_hash == metadata["pdfSha256"] == qa["pdfSha256"]
    assert json.loads(archive.read("output/pdf/" + PDF.stem + ".json"))["pdfSha256"] == packaged_hash
    assert json.loads(archive.read("output/pdf/" + qa_path.name))["pdfSha256"] == packaged_hash
    assert digest(archive.read("vibe-coding-16/book.md")) == metadata["manuscriptSha256"]

print(json.dumps({"pages": current_pages, "previous_pages": previous_pages,
                  "manuscript_containers": 167, "practice_cards": 40,
                  "code_blocks": 12, "png_assets": 34, "vector_assets": 5, "images": 35, "flowcharts": 4,
                  "bookmarks": 16, "contents_links": contents_links,
                  "pdf_sha256": packaged_hash, "code_hashes_unchanged": True,
                  "image_sizes_unchanged": True, "bundle_bytes": bundle.stat().st_size},
                 ensure_ascii=False))
