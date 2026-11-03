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
PDF = ROOT / "output/pdf/vibe-coding-16-hallucination.pdf"
ARCHIVE = BOOK / "previous-reports/20261011-before-no-robot"
REVISION_ARCHIVE = BOOK / "previous-reports/20261011-before-history-hallucination"
BASELINE = ARCHIVE / "vibe-coding-16-student.json"
QA_INPUT = ROOT / "tmp/pdfs/apps-review/automated-qa.json"
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
    11: "88-94", 12: "95-105", 13: "106-127", 14: "128-145",
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
    12: "직접 입력한 값의 선 그래프·산점도·막대그래프",
    13: "학생 자료·학교별 학생 수·API·저장과 불러오기",
    14: "Matplotlib 선·마커·설명·막대·산점도",
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
code_specs = read_json(BOOK / "code-specs.json")
codes = read_json(BOOK / "code-results.json")
previous_code_specs = read_json(ARCHIVE / "code-specs.json")
previous_codes = read_json(ARCHIVE / "code-results.json")
validations = read_json(BOOK / "validation-full.json")
catalog = read_json(BOOK / "practice-source-map.json")["practices"]
spec = read_json(ROOT / "tmp/pdfs/book-spec.json")
restructure = read_json(BOOK / "page-restructure.json")
current_pages = metadata["pages"]
previous_pages = baseline["pages"]
saved_pages = previous_pages - current_pages
canva_pages = validations[0]["layout"]["canvaPages"]

assert previous_pages == 149
assert metadata["pages"] == qa["pages"] == qa["renderedPages"]
assert current_pages > 0
assert len(validations) == 17 and validations[0]["pages"] == 170
assert all(value["ok"] and not value["issues"] for value in validations)
assert len(spec["pages"]) == 170
assert len(catalog) == metadata["pageTypes"]["practice-opening"] == 41
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
old_images = [item for item in baseline["images"] if not is_robot_asset(item["src"])]
assert len(old_images) == 31
retained_images = [item for item in metadata["images"] if item.get("format") != "native-vector-pdf"]
native_images = [item for item in metadata["images"] if item.get("format") == "native-vector-pdf"]
assert len(retained_images) == 31 and len(native_images) == 4
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
assert len([item for item in assets["items"] if item.get("vector_src")]) == 4
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
assert practice_counts[12] == 3 and practice_counts[13] == 4
assert practice_counts[14] == 8 and practice_counts[15] == 3
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

# Compare to the previous completed edition when it is present. On another
# computer, verify current text against the preserved comparison evidence.
previous_completed_pdf = ROOT / "output/pdf/vibe-coding-16-revised.pdf"
previous_completed_backup = REVISION_ARCHIVE / previous_completed_pdf.name
comparison_record_path = BOOK / "hallucination-page-comparison.json"
current_page_text_hashes = [digest((page.extract_text() or "").encode("utf-8")) for page in reader.pages]
direct_previous_pdf_compared = previous_completed_pdf.is_file()
if direct_previous_pdf_compared:
    previous_completed_reader = PdfReader(str(previous_completed_pdf))
    assert len(previous_completed_reader.pages) == current_pages
    previous_page_text_hashes = [digest((page.extract_text() or "").encode("utf-8"))
                                for page in previous_completed_reader.pages]
    changed_text_pages = [number for number, pair in enumerate(
        zip(previous_page_text_hashes, current_page_text_hashes), 1) if pair[0] != pair[1]]
    assert changed_text_pages == [7], changed_text_pages
    previous_completed_metadata = read_json(previous_completed_pdf.with_suffix(".json"))
    assert metadata["images"] == previous_completed_metadata["images"]
    assert metadata["chapterPages"] == previous_completed_metadata["chapterPages"]
    changed_layout_pages = [number for number, pair in enumerate(
        zip(previous_completed_metadata["layout"], metadata["layout"]), 1) if pair[0] != pair[1]]
    assert changed_layout_pages == [7], changed_layout_pages
    completed_pdf_comparison = {
        "date": DATE, "previousPdf": previous_completed_pdf.relative_to(ROOT).as_posix(),
        "previousPdfBackup": previous_completed_backup.relative_to(ROOT).as_posix(),
        "previousPdfSha256": digest(previous_completed_pdf.read_bytes()),
        "currentPdf": PDF.relative_to(ROOT).as_posix(), "currentPdfSha256": metadata["pdfSha256"],
        "pages": current_pages, "changedTextPages": changed_text_pages,
        "onlyPage7TextChanged": True, "unchangedTextPages": current_pages - 1,
        "changedLayoutPages": changed_layout_pages, "onlyPage7LayoutChanged": True,
        "all35ImagePlacementsUnchanged": True, "chapterStartPagesUnchanged": True,
        "currentImagesSha256": json_digest(metadata["images"]),
        "currentChapterPagesSha256": json_digest(metadata["chapterPages"]),
        "previousPageTextSha256": previous_page_text_hashes,
        "currentPageTextSha256": current_page_text_hashes,
        "method": "pypdf extract_text SHA-256 comparison for every physical page",
    }
else:
    completed_pdf_comparison = read_json(comparison_record_path)
    assert completed_pdf_comparison["currentPdfSha256"] == metadata["pdfSha256"]
    assert completed_pdf_comparison["currentPageTextSha256"] == current_page_text_hashes
    assert completed_pdf_comparison["changedTextPages"] == [7]
    assert completed_pdf_comparison["currentImagesSha256"] == json_digest(metadata["images"])
    assert completed_pdf_comparison["currentChapterPagesSha256"] == json_digest(metadata["chapterPages"])

# Read the explicit manuscript ID mapping written by the reorganization step.
id_map = next((restructure[key] for key in ("old_to_new", "id_mapping", "idMap", "id_map", "mapping")
               if key in restructure), None)
if isinstance(id_map, list):
    id_map = {item.get("old_id", item.get("oldId")): item.get("new_id", item.get("newId"))
              for item in id_map}
assert isinstance(id_map, dict), list(restructure)
removed_ids = set(restructure.get("removed_pages", restructure.get("removed_ids", restructure.get("removedIds", []))))
new_ids = set(restructure.get("added_pages", restructure.get("new_ids", restructure.get("newIds", []))))
assert len(removed_ids) == 11 and len(new_ids) == 2
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
assert [item["physicalPages"] for item in vector_checks] == [[23], [29], [36], [42]]
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
assert ethics_layout["y"] > old_ethics["y"] and ethics_layout["y"] < 786
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

# Reports are separate from the student textbook. Preserve the prior edition.
REVISION_ARCHIVE.mkdir(parents=True, exist_ok=True)
if direct_previous_pdf_compared and not previous_completed_backup.exists():
    shutil.copy2(previous_completed_pdf, previous_completed_backup)
    shutil.copy2(previous_completed_pdf.with_suffix(".json"), previous_completed_backup.with_suffix(".json"))
if previous_completed_backup.exists():
    assert digest(previous_completed_backup.read_bytes()) == completed_pdf_comparison["previousPdfSha256"]
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

qa.update({"date": DATE, "edition": "apps-16-sessions", "manuscriptContainers": 170,
           "previousPdfPages": previous_pages, "savedPages": saved_pages,
           "practiceCards": 41, "uniqueAssets": 34, "sourceImages": 26,
           "retainedRasterAssets": 30, "retainedRasterPlacements": 31,
           "nativeVectorAssets": 4, "canvaFlowchartPreviewAssets": 4,
           "nativeFlowchartSourceChecks": vector_checks,
           "sourcePdfHashVerified": source_pdf_checked,
           "declarationSymbol": "six-sided preparation symbol",
           "loopVerification": {"physicalPage": 29, "trace": trace, "iterations": 10,
                                "exit": {"time1": time1, "total": total},
                                "updateOrder": flows["loop_trace"]["updates"]},
           "movieBoundaryVerification": movie_boundaries,
           "hallucinationPageVerification": hallucination_check,
           "onlyPage7TextChanged": True,
           "directPreviousCompletedPdfCompared": direct_previous_pdf_compared,
           "previousCompletedPdfComparison": completed_pdf_comparison,
           "bookmarks": 16, "contentsLinks": contents_links, "fonts": fonts,
           "standardPdfFonts": sorted(standard_fonts), "robotReferencePages": robot_mentions,
           "editorialReferencePages": editorial_mentions,
           "executedCodeHashesUnchanged": True, "codeHashes": current_hashes,
           "executedCodeBlocks": 12, "executedCodePassed": 12,
           "codeOutputsUnchanged": True, "nonRobotImagePixelsAndPrintWidthUnchanged": True,
           "pdfSha256": metadata["pdfSha256"], "manuscriptSha256": metadata["manuscriptSha256"],
           "typography": {"bodyPt": 14, "bodyLeadingPt": 28, "sectionHeadingPt": 15, "chapterTitlePt": 25},
           "removedManuscriptIds": sorted(removed_ids), "newManuscriptIds": sorted(new_ids),
           "previousPhysicalPagesMapping": mapping})
qa_path = PDF.with_name(PDF.stem + "-qa.json")
write_json(qa_path, qa)
write_json(comparison_record_path, completed_pdf_comparison)
hallucination_evidence = {
    "date": DATE, "physicalPage": 7, "sourceId": "ch01-ethics",
    "purpose": "질문의 틀린 전제를 받아들이는 환각을 알아보는 학습용 가상 오답",
    "notice": "다음 답변은 환각을 살펴보기 위해 만든 학습용 가상 오답입니다.",
    "actualAiOutput": False, "examples": HALLUCINATION_EXAMPLES,
    "verificationTask": "질문의 전제·연도·작가를 근거 자료와 비교하고 맞음·틀림·확인하지 못함으로 구분",
    "sourcesReviewedDate": DATE,
    "webVerification": "OpenStax 해당 절과 작가재단 도서 페이지의 사실을 확인",
    "pdfSha256": metadata["pdfSha256"], "manuscriptSha256": metadata["manuscriptSha256"],
    "layoutVerification": hallucination_check,
}
write_json(BOOK / "hallucination-source-review.json", hallucination_evidence)
write("hallucination-source-review.md", f"""# 7쪽 환각 예시의 사실 검증 · {DATE}

이 문서는 제작·교사용 근거 기록입니다. 학생용 본문에는 긴 웹 URL이나 제작 메모를 넣지 않습니다. 현재 학생용 PDF는 output/pdf/{PDF.name}, A4 {current_pages}쪽입니다.

## 예시의 성격

안내 문구는 “다음 답변은 환각을 살펴보기 위해 만든 학습용 가상 오답입니다.”입니다. 아래 오답은 설명을 위해 작성한 것이며 실제 AI를 실행해 수집한 답변이 아닙니다. 틀린 질문의 전제를 답이 그대로 받아들이는 문제를 알아보도록 구성했습니다.

## 역사 질문

- 질문: {HALLUCINATION_EXAMPLES[0]['question']}
- 학습용 가상 오답: {HALLUCINATION_EXAMPLES[0]['learning_only_wrong_answer']}
- 확인한 사실: {HALLUCINATION_EXAMPLES[0]['verified_fact']} [OpenStax · The Crusading Movement]({HALLUCINATION_EXAMPLES[0]['source_url']})

근거는 해당 절의 Figure 13.19에 표시된 제1차 십자군의 기간과 본문의 1099년 예루살렘 도착 설명입니다. 질문의 1492년이라는 전제를 확인 없이 받아들이지 않도록 합니다.

## 문학 질문

- 질문: {HALLUCINATION_EXAMPLES[1]['question']}
- 학습용 가상 오답: {HALLUCINATION_EXAMPLES[1]['learning_only_wrong_answer']}
- 확인한 사실: {HALLUCINATION_EXAMPLES[1]['verified_fact']} [Paulo Coelho and Christina Oiticica Foundation · The Alchemist]({HALLUCINATION_EXAMPLES[1]['source_url']})

작가재단의 도서 설명에서 주인공 산티아고와 작가 파울로 코엘료를 확인하고 첫 출간 연도를 대조했습니다. 동명의 다른 작품과 혼동하지 않도록 질문에 산티아고를 명시했습니다.

## 학습·지면 확인

질문의 전제·연도·작가를 근거 자료와 비교하고 맞음·틀림·확인하지 못함으로 구분합니다. 가상 오답·정확한 사실·직접 확인·책임 있는 사용을 7쪽 한 장에 배치했습니다. 원고의 두 질문·가상 오답·사실과 PDF 출력이 일치합니다. 본문 끝 좌표는 {ethics_layout['y']:g}pt이며 글자·상자 넘침은 0입니다. 상세 출처 기록과 SHA-256은 hallucination-source-review.json 및 output/pdf/{qa_path.name}에 보관합니다.
""")

chapter_table = ["| 차시 | 주제 | 실습 카드 |", "|---|---|---|"]
curriculum_table = ["| 차시 | 주제 | 핵심 활동 | 실습 카드 | 제작 관리용 출처 쪽 |",
                    "|---|---|---|---|---|"]
teacher_table = ["| 차시 | 운영할 활동 |", "|---|---|"]
for number in range(1, 17):
    chapter_table.append(f"| {number} | {chapter_titles[number]} | {practice_counts[number]} |")
    curriculum_table.append(f"| {number} | {chapter_titles[number]} | {ACTIVITIES[number]} | {practice_counts[number]} | {SOURCE_PAGES[number]} |")
    teacher_table.append(f"| {number} | {ACTIVITIES[number]} |")
chapter_table_text = "\n".join(chapter_table)

write("README.md", f"""# AI와 함께하는 바이브 코딩 · 앱 개발 16차시 학생용 완성본

{DATE}에 코코봇 차시를 제외하고 앱·데이터 실습 중심으로 16차시를 재구성했습니다. 12차시는 직접 입력한 값의 Chart, 13차시는 자료·API·저장, 14차시는 Matplotlib, 15차시는 Pandas, 16차시는 자율 프로젝트입니다.

- [현재 학생용 PDF](../../output/pdf/{PDF.name}): A4 {current_pages}쪽.
- [전체 원고](book.md): 170개 페이지 컨테이너. ch01.md-ch16.md와 같은 내용입니다.
- [16차시 구성](curriculum.md), [교사용 안내](teacher-guide.md), [제작 지침](notes.md).
- [개편 내역](apps-edition-review.md), [이전→현재 쪽수 대응](page-compaction-review.md).
- [검증 결과](validation-summary.md), [PDF 검토](pdf-final-review.md).
- [이미지 미리보기](asset-review.html): PNG 34개·배치 35곳. 인쇄 순서도는 벡터 PDF 4개를 사용합니다.
- [순서도 재사용·검증](flow-source-review.md), [Canva 이미지 사용 안내](flowchart-canva.md).
- [실행 예제](examples/source-based/README.md): 14차시 Matplotlib 7개·15차시 Pandas 5개.
- 제작 관리용 [실습 대조 기록](practice-source-review.md), [실습 출처 목록](practice-source-map.json).

{chapter_table_text}

실습 카드 41개·코드 12개·순서도 4개를 포함합니다. 학생용 본문에는 원본 대조·출처 쪽수·제작 과정·PDF 안내 문구를 넣지 않습니다. 출처와 검증 기록은 별도 관리 문서에 보관합니다.

7쪽에는 제1차 십자군의 연도와 소설 『연금술사』의 작가를 틀리게 답하는 학습용 가상 오답·사실 확인 방법을 넣었습니다. 실제 AI가 출력한 답변 사례가 아닙니다. 확인 근거는 [환각 예시 사실 검증](hallucination-source-review.md)에 보관합니다. 순서도는 기준 교재에서 가져온 도형·글꼴·연결을 사용하며 선언은 6각형입니다. 29쪽 반복은 1부터 10까지 누적한 뒤 55를 출력합니다.

다른 컴퓨터로 옮길 때는 상위 폴더의 vibe-coding-16-source-revised.zip과 묶음의 START-HERE.txt를 사용합니다. PDF는 바로 열 수 있습니다. [설치 안내](../../OTHER-PC-SETUP.md)도 참고하세요. 이전 학생판과 코코봇 자료는 previous-reports/20261011-before-no-robot에 보관했습니다.
""")

write("curriculum.md", f"""# 앱·데이터 실습 중심 16차시 구성 · {DATE}

1-11차시의 구성은 유지했습니다. Chart 차시를 직접 입력 실습과 자료 활용으로 나누고 Matplotlib·Pandas를 각각 14·15차시에 배치했습니다. 16차시는 자율 프로젝트입니다. 코코봇 장비 실습은 현재 과정에서 제외했습니다.

{chr(10).join(curriculum_table)}

총 16차시·41개 실습 카드입니다. 차시별 쪽수는 제작 관리용 출처이며 학생용 본문에 표시하지 않습니다. 실습의 입력값·조건과 출처 대응은 practice-source-map.json에서 확인합니다. 수업 시간은 정해져 있지 않으므로 차시별 핵심·선택 활동을 수업 환경에 맞춰 운영합니다.
""")

write("teacher-guide.md", f"""# 교사용 운영 안내 · 앱 개발 16차시 · {DATE}

1-7차시는 AI 질문·문제 분해·순서도·반복과 조건을 다룹니다. 8-13차시는 알고플로/Flet 디자이너를 사용해 위젯·Chart·자료 활용과 저장을 실습합니다. 14-15차시는 Python의 Matplotlib·NumPy·Pandas를 사용하며, 16차시는 앞선 기능으로 자율 프로젝트를 완성합니다.

코코봇 장비 차시는 제외했습니다. 학생 100명 자료, 수업용 API 주소와 인증 정보, 저장 설정은 수업 전에 준비합니다. GUI 메뉴와 저장 동작은 사용하는 수업 도구에서 확인합니다. 한글 축 제목이 있는 Matplotlib 예제는 한글 글꼴을 설정합니다.

{chr(10).join(teacher_table)}

여러 실습이 있는 차시는 핵심과 선택 활동으로 나눠 운영합니다. 12차시에서는 입력값과 차트의 축·누적 여부를 확인하고, 13차시에서는 불러온 자료의 열·API 데이터 구조·저장 전후 값을 확인합니다. 14차시의 여덟 그래프 활동은 코드 7개를 사용합니다. 제목·설명 활동은 앞 그래프를 함께 사용합니다. 15차시의 세 실습은 코드 5개를 사용합니다.

examples/source-based의 12개 코드는 현재 원고와 같습니다. 데이터와 코드·출력은 이전 실행 검증본에서 유지했고 차시 번호와 파일 이름을 바꿨습니다. GUI·API를 실행하지 못했으면 그 상태를 기록합니다. 각 실습의 입력·결과·완료 기준으로 직접 확인하며 새 앱 예시나 임의 숫자 과제를 추가하지 않습니다.

7쪽의 두 답변은 환각을 살펴보기 위해 만든 학습용 가상 오답이며 실제 AI 출력 기록이 아닙니다. 제1차 십자군이 1492년에 시작했다는 답을 1096~1099년 진행 사실과 비교합니다. 산티아고가 나오는 소설 『연금술사』를 셰익스피어의 작품이라고 한 답은 작가 파울로 코엘료·첫 출간 1988년 사실과 비교합니다. 질문의 전제·연도·작가를 근거 자료로 확인하고 맞음·틀림·확인하지 못함을 구분합니다. 검증 출처는 hallucination-source-review.md/json에 기록합니다.

29쪽 반복은 total에 time1을 먼저 더한 뒤 time1을 1 증가시킵니다. 실행 추적은 1→1, 2→3, 3→6, 4→10, 5→15, 6→21, 7→28, 8→36, 9→45, 10→55입니다. time1이 11이 되면 조건이 거짓이고 55를 출력합니다. 선언·초기 준비 기호는 6각형입니다. 42쪽 영화 조건은 15세 미만이 관람 불가이며, 14·15·16·13세의 판정은 불가·가능·가능·불가입니다. N명 점수 판정의 80점 조건 활동은 별도로 유지합니다.

이 문서는 교사용 관리 안내입니다. 출처·제작·검증 메모는 학생용 본문 밖에서 관리합니다.
""")

write("notes.md", f"""# 다음 제작·수정에 사용할 관리 지침 · {DATE}

## 현재 16차시 구조

1-11차시는 유지합니다. 12차시에는 직접 입력한 값의 선 그래프·키와 몸무게 산점도·막대그래프를, 13차시에는 학생 자료·학교별 학생 수·공공데이터 API·저장과 불러오기를 둡니다. 14차시는 Matplotlib, 15차시는 Pandas, 16차시는 자율 프로젝트입니다. 코코봇 장비 실습은 추가하지 않습니다.

실습 카드 41개, 원고 컨테이너 170개, 실행 코드 12개, 순서도 4개를 유지합니다. 기존 이미지 30개·배치 31곳에 순서도 PNG 4개를 더해 PNG 34개·배치 35곳이며 인쇄에는 벡터 PDF 4개를 포함합니다. 원본 과제·데이터·위젯·결과를 우선하고 임의 숫자 예시·새 앱 과제를 추가하지 않습니다. 원본이 입력값을 정하지 않은 활동은 학생이 직접 입력하도록 둡니다. 사용자가 요청한 7쪽 환각 예시는 제1차 십자군·『연금술사』 질문의 전제를 그대로 받아들이는 학습용 가상 오답으로 유지합니다. 실제 AI 출력으로 소개하지 않으며 사실 확인 근거는 hallucination-source-review.md/json에서 관리합니다.

## 학생용 문구와 조판

학생용 본문에는 기준 교재의 대조·출처 쪽수·과거 실습 번호·제작 과정·PDF 안내를 넣지 않습니다. 이미지 캡션은 보이는 입력과 동작·결과를 설명합니다. 오류 정정 고지는 정확한 개념 설명으로 바꿉니다. 출처와 수정 근거는 practice-source-review.md, practice-source-map.json, source-audit.md에서 관리합니다. AI 답변의 근거 확인처럼 학습에 필요한 자료 비교 활동은 유지합니다.

본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt와 현재 이미지 픽셀·출력 폭·비율을 유지합니다. 흰 배경·선명한 글자와 도형·둥근 실습 상자를 사용하고 삼육보건대 로고를 넣지 않습니다. 연속된 짧은 설명·표·완료 확인을 읽는 순서대로 함께 배치합니다. 차시 시작 아래에 충분한 공간이 있으면 다음 개념을 함께 놓습니다. 대형 빈 기록칸과 반복 안내를 자동으로 추가하지 않습니다.

## 생성과 검증

현재 학생용 PDF는 output/pdf/{PDF.name}, A4 {current_pages}쪽입니다. 원고·metadata의 차시 번호와 예제 파일 이름을 함께 유지합니다. Node 앱 파서·Python 패키지·필요 글꼴을 준비한 뒤 저장소 루트에서 실행합니다.

```powershell
python scripts/finalize_student_manuscript.py
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/{PDF.name}
python scripts/review_textbook_pdf.py --pdf output/pdf/{PDF.name} --dest tmp/pdfs/apps-review
python scripts/report_apps_edition.py
```

각 chXX.md를 수정한 후 위 순서대로 전체 원고 조합→파서→조판→전체 렌더링→보고를 진행합니다. 이전 과정 개편 스크립트와 prepare_source_flowcharts.py는 일상 본문 편집 때 실행하지 않습니다. 후속 편집을 덮어쓸 수 있습니다. prepare_source_flowcharts.py는 원본 순서도를 재추출할 때만 실행하며 원본 PDF와 PyMuPDF가 필요합니다. 이 스크립트는 자산뿐 아니라 ch04/ch07의 순서도 문구도 적용합니다.

flow-source-map.json의 flowchart_sha256는 원고의 해당 flowchart 블록과 일치해야 합니다. 순서도 논리 블록을 바꿀 때는 그림·문구·맵의 일치를 함께 확인합니다. 현재는 기준 그림과 문구를 유지합니다. 일반 PDF 재생성은 묶음에 있는 4개 벡터 PDF를 사용하므로 원본 PDF나 PyMuPDF가 필요하지 않습니다. 벡터 합성에는 pypdf를 사용합니다.

보고 스크립트는 조판과 전체 렌더링 검증 이후에 실행합니다. 이전 학생판과의 비교 기준은 previous-reports/20261011-before-no-robot입니다. 묶음에는 재검증에 필요한 이전 metadata·코드 검증 JSON과 수정 근거 문서만 보관하며 이전 PDF·이미지·원고는 넣지 않습니다. 원본 PDF가 로컬에 있으면 원본 파일의 해시를 다시 확인하고, 없으면 보존된 출처 기록과 묶음의 4개 벡터 PDF·PNG 해시를 검증합니다.

현재 본문 글꼴은 Wanted Sans·Windows Consolas이며 순서도는 원본의 벡터 글자·도형을 그대로 포함합니다. Canva 제작은 flowchart-canva.md를 참고하고 현재 독립 PDF의 쪽수와 Canva 자동 생성 쪽수를 구분합니다.
""")

write("canva-production-status.md", f"""# 제작 상태 · 앱 개발 16차시 · {DATE}

[현재 학생용 완성본](../../output/pdf/{PDF.name})은 A4 {current_pages}쪽의 독립 PDF입니다. 이전 학생판 {previous_pages}쪽에서 과정 개편과 지면 통합을 반영했습니다. 16차시·41실습·12코드·35곳 이미지 배치·4순서도를 포함합니다.

12차시는 직접 입력 Chart, 13차시는 자료·API·저장, 14차시는 Matplotlib, 15차시는 Pandas, 16차시는 자율 프로젝트입니다. 코코봇 장비 실습과 이미지 3개는 제외했습니다. 학생용 본문의 출처·제작 메모는 관리 문서로 분리했습니다.

7쪽의 환각 예시·직접 확인 활동을 추가했고 선언 기호는 6각형으로 확인했습니다. 29쪽 반복 결과는 55입니다. 순서도 4개는 원본의 벡터 PDF를 인쇄에 사용하며 Canva용 300dpi PNG를 함께 준비했습니다. 실제 도형 제작이 남았다는 과거 안내는 현재 완성본에 해당하지 않습니다.

사용자가 승인한 독립 PDF 제작 방식입니다. Canva 디자인 자체를 이 개편본으로 다시 생성한 것은 아닙니다. Canva 제작 절차는 notes.md와 flowchart-canva.md를 참고합니다. 이전 학생판과 제외한 자료는 previous-reports/20261011-before-no-robot에 보관했습니다.
""")

write("validation-summary.md", f"""# 검증 결과 · 앱 개발 16차시 · {DATE}

현재 학생용 PDF는 A4 {current_pages}쪽입니다. book.md와 ch01.md-ch16.md 총 17개 파일이 파서·레이아웃 검사에 통과했습니다. 원고 컨테이너 170개, Canva 앱 추정 {canva_pages}장입니다.

- 16차시·41개 실습 카드·4개 벡터 순서도 유지.
- 12차시 3실습, 13차시 4실습, 14차시 8실습, 15차시 3실습, 16차시 1실습.
- 코드 12개와 출력 유지. 이전 실행본의 코드 SHA-256과 일치, 출력 코드 내용 차이 0.
- 기존 래스터 이미지 파일 30개·배치 31곳의 픽셀·출력 폭·비율 유지.
- 순서도 벡터 PDF 4개·Canva용 PNG 4개 추가. PNG 34개·전체 배치 35곳.
- 기준 파일과 순서도 자산 해시·cropbox·원고 논리 해시 확인. 벡터 자산 내부 래스터 이미지 0.
- 7쪽 역사·문학 질문의 학습용 가상 오답 2개·정확한 사실·직접 확인·책임 있는 사용 한 장 배치. 본문 끝은 이전 {old_ethics['y']:g}pt에서 {ethics_layout['y']:g}pt로 변경.
- 직전 revised 완성본과 전체 쪽을 비교해 텍스트·layout 변경은 7쪽만 확인. 나머지 {current_pages - 1}쪽·이미지 35개 배치·차시 시작 쪽 동일.
- 23·29·36·42쪽 원본 순서도 사용·선언 6각형 시각 확인. 29쪽 10회 누적·종료 time1=11·total=55 확인.
- {current_pages}쪽 전체 렌더링. 글자·상자 넘침, 원고 ID 누락, 목차 오류, 대체 문자 0.
- 학생용 본문의 코코봇·기준 교재 대조·PDF 안내 문구 노출 0.
- 목차 링크 16개·차시 책갈피 16개·주요 글꼴 포함 확인.

검사 상세는 validation-full.json, code-results.json과 output/pdf/{qa_path.name}에 있습니다. 코드·GUI·외부 API를 새로 실행한 변경은 없습니다. 실행 코드의 동일성과 현재 PDF 출력·지면·내용 보존을 검증했습니다.
""")

write("pdf-final-review.md", f"""# 독립 PDF 검토 · 앱 개발 16차시 학생용 완성본 · {DATE}

[현재 완성 PDF](../../output/pdf/{PDF.name})는 A4 {current_pages}쪽입니다. 이전 학생판은 {previous_pages}쪽이며, 지면 대응은 page-compaction-review.md에 기록했습니다.

## 과정과 내용

코코봇 차시를 제외하고 12차시의 Chart 활동을 직접 입력과 자료 활용으로 나눴습니다. Matplotlib는 14차시, Pandas는 15차시로 이동했고 16차시는 자율 프로젝트입니다. 170개 원고 컨테이너·41개 실습 카드·12개 코드·4개 순서도를 포함합니다.

기존 이미지 파일 30개·배치 31곳의 픽셀·출력 폭·비율과 실행 코드·출력을 유지했습니다. 순서도 4개는 기준 교재의 벡터 PDF를 사용하고 별도의 Canva용 PNG 4개를 준비했습니다. 전체 PNG 34개·배치 35곳입니다. 학생용 본문에는 원본 대조·출처 쪽수·오류 수정 고지·제작 과정·PDF 안내를 넣지 않습니다.

7쪽에 역사·문학 질문의 학습용 가상 오답 2개와 정확한 사실·확인 방법을 넣었습니다. 실제 AI 출력 기록이 아님을 표시했으며 질문의 전제·연도·작가를 근거와 비교합니다. 23·29·36·42쪽의 순서도 도형·글자·연결과 선언 6각형을 시각 검토했습니다. 29쪽 반복은 10회 누적한 뒤 total=55, time1=11로 종료합니다. 42쪽 영화 관람의 15세 경계와 N명 점수 판정 활동도 확인했습니다.

## 조판과 검증

본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt를 유지했습니다. 본문 Wanted Sans·Consolas와 순서도에 사용된 주요 글꼴을 PDF에 포함했습니다. 흰 배경·벡터 글자와 도형·둥근 실습 상자를 사용하고, 연속된 짧은 개념·표·완료 확인을 함께 배치합니다. 순서도는 재그린 도형이나 래스터 이미지가 아닌 원본에서 추출한 네이티브 벡터입니다.

{current_pages}쪽을 모두 렌더링했습니다. 자동 검사에서 글자·상자 넘침·원고 ID 누락·목차 오류·대체 문자·코드 내용 차이는 0입니다. 코코봇·기준 교재 대조·PDF 메타 언급은 학생용 본문에서 0입니다. 목차 링크·책갈피 각각 16개와 주요 글꼴 포함을 확인했습니다.

직전 revised 완성본과 모든 쪽의 추출 텍스트·layout을 비교했으며 변경은 7쪽만입니다. 나머지 {current_pages - 1}쪽의 텍스트·지면, 이미지 35개 배치, 차시 시작 쪽은 동일합니다. 이전 PDF의 로컬 보관 위치는 previous-reports/20261011-before-history-hallucination/vibe-coding-16-revised.pdf입니다. 이전 PDF는 전달 ZIP에 포함하지 않으며 비교 근거 JSON은 hallucination-page-comparison.json에 보관합니다.

## 제작 범위

사용자가 승인한 독립 PDF 배치입니다. 원본 캡처의 낮은 해상도를 복원했다거나 GUI·외부 API를 새로 실행했다고 주장하지 않습니다. 출처와 이전 대조 기록은 관리 문서에 보관하며, 이전 학생판과 제외한 차시는 previous-reports/20261011-before-no-robot에 있습니다.
""")

handover = f"""# 앱 개발 16차시 학생용 완성본 인계 · {DATE}

- 학생용 PDF: output/pdf/{PDF.name}, A4 {current_pages}쪽.
- 원고: book.md 및 ch01.md-ch16.md, 컨테이너 170개·16차시.
- 실습: 41개 카드. 12차시 직접 입력 Chart, 13차시 자료·API·저장.
- 14차시 Matplotlib·15차시 Pandas·16차시 자율 프로젝트.
- 실행 코드: examples/source-based의 Python 12개. 데이터·코드·출력 유지.
- 이미지: 기존 래스터 파일 30개·배치 31곳과 순서도 PNG 4개. 전체 PNG 34개·배치 35곳.
- 순서도: assets/source-flowcharts의 원본 벡터 PDF 4개와 Canva용 PNG 4개.
- 추가 내용: 7쪽 가상 환각 예시·확인 활동. 선언 6각형·29쪽 반복 결과 55 검증.
- 메타데이터·QA: output/pdf/{PDF.stem}.json 및 {qa_path.name}.
- 구성·검토: curriculum.md, apps-edition-review.md, pdf-final-review.md.
- 전달 ZIP: 상위 폴더 vibe-coding-16-source-revised.zip.

코코봇 장비 실습은 제외했습니다. 학생용 본문에는 출처·제작 메모가 없고 관련 기록은 별도 관리 문서로 보존합니다. 이전 학생판과 제외한 자료는 previous-reports/20261011-before-no-robot에 있습니다.

다른 컴퓨터에서 PDF는 바로 열 수 있습니다. 저장소에서 수정할 경우 ZIP의 vibe-coding-16 폴더를 coala-book-md/vibe-coding-16에 복사하고 START-HERE.txt와 notes.md를 확인합니다.
"""
write("handover.md", handover)
write("final-draft.md", handover.replace("# 앱 개발 16차시 학생용 완성본 인계", "# 현재 전달본 · 앱 개발 16차시"))

write("print-activities.md", f"""# 실습 결과·기록 안내 · {DATE}

현재 원고의 41개 실습 카드와 차시별 완료 확인을 사용합니다. 입력값·선택한 연산·표와 그래프의 결과·수정 전후 실행 화면을 기록합니다. 임의 숫자·새 앱·가상 오류를 별도 추가 과제로 제시하지 않습니다.

7쪽의 두 답변은 학습을 위해 만든 가상 오답입니다. 제1차 십자군의 연도와 『연금술사』의 작가를 답변의 주장·질문의 전제·근거 자료로 나누어 확인합니다. 연도·작가가 맞음·틀림·확인하지 못함 중 어디에 해당하는지 기록합니다. 실제 AI 실행 결과로 제출하지 않습니다. 29쪽 반복에서는 누적 후 증가하는 순서와 10이 포함되는지 확인합니다.

12차시는 직접 입력값과 차트를, 13차시는 불러온 자료·API·저장 전후 값을, 14-15차시는 코드와 실행 결과를 확인합니다. 16차시는 자신의 프로젝트 아이디어·UI·실행 가능한 결과를 남깁니다.

출처와 제작 기록은 practice-source-map.json 및 practice-source-review.md에서 관리합니다. 학생용 본문에 관리 메모나 별도의 대형 빈 기록칸을 추가하지 않습니다.
""")

# Preserve correction evidence, but describe only the current included course.
previous_audit = (ARCHIVE / "source-audit.md").read_text(encoding="utf-8")
corrections = previous_audit.split("## 원본에서 바로잡은 부분", 1)[1].split("## 코드 확인 근거", 1)[0]
corrections = "\n".join(line for line in corrections.splitlines() if not line.startswith("| 152-157 |"))
write("source-audit.md", f"""# 제작 관리용 출처·수정 기록 · {DATE}

기준 PDF: {assets['source_pdf']}

실제 158쪽, SHA-256: {assets['source_sha256']}. 이 기록은 학생용 본문 밖에서 관리합니다. 원본 파일은 수정하지 않았습니다.

## 현재 내용의 범위

1-11차시는 기존 앱 개발 과정입니다. 12차시는 95-105쪽의 직접 입력 Chart, 13차시는 106-127쪽의 학생 자료·API·저장, 14차시는 128-145쪽의 Matplotlib, 15차시는 146-151쪽의 Pandas, 16차시는 93-94쪽 자율 프로젝트입니다. 152-157쪽 코코봇 내용은 현재 교재에서 제외했습니다.

현재 본문의 출처 쪽수·과거 실습 번호·제작 과정·원본 오류 고지는 제거했고 정확한 개념과 실습 동작 설명으로 정리했습니다. 출처 대응은 practice-source-map.json 및 practice-source-review.md에 있습니다. 사용자 요청으로 7쪽에 제1차 십자군의 연도·『연금술사』의 작가를 틀리게 답하는 학습용 가상 오답 2개와 정확한 사실을 넣었습니다. 실제 AI 출력 사례가 아님을 명시했습니다. 사실은 OpenStax와 작가재단 자료로 확인했으며 URL·확인 내용은 hallucination-source-review.md/json에 보관합니다. 그 밖의 임의 고정 입력값·새 앱 예시는 추가하지 않습니다.

## 포함한 내용의 수정 근거
{corrections}

## 코드와 이미지 검증

Matplotlib 7개·Pandas 5개 코드는 이전 실제 실행본과 SHA-256이 같습니다. 출력 데이터도 유지했고 차시 번호와 파일 이름만 새 구조에 맞췄습니다. 실행 환경과 결과는 code-results.json에 보존했습니다. 이번 과정 개편에서 GUI·외부 API를 새로 실행했다고 주장하지 않습니다.

기존 이미지 30개는 원본 캡처 22개·실행 그래프 7개·실행 표 1개입니다. 이전 학생판의 비코코봇 이미지와 픽셀·출력 폭·비율이 일치합니다. 여기에 원본 23·31·36·39쪽 순서도 4개를 가져와 현재 23·29·36·42쪽에 사용했습니다. 네이티브 벡터 PDF 4개는 인쇄용, 300dpi PNG 4개는 Canva용입니다. 기존 31개 래스터 배치에 순서도 4개를 더해 전체 배치는 35곳이며 PNG 파일은 34개입니다.

순서도 외부 글자만 제거하고 전체 페이지의 회색 배경 색상을 흰색으로 바꿨습니다. 순서도 노드·연결·글꼴·벡터 경로와 색은 보존했습니다. 원본 PDF 파일은 수정하지 않았습니다. 각 자산과 논리 블록의 해시는 flow-source-map.json 및 현재 QA에 기록했습니다. 벡터에는 DPI를 적용하지 않으며 metadata의 순서도 effectiveDpi는 별도 PNG 대체 자산에 대한 정보입니다.

원본 파일이 로컬에 있으면 SHA-256을 직접 재확인합니다. 없는 환경에서는 원본을 새로 검증했다고 주장하지 않고 보존된 출처 기록과 포함 자산의 SHA-256을 확인합니다. 작은 UI 캡처의 선명도를 복원했다고 주장하지 않습니다. PDF의 종이 배경·기관 로고·그림자를 전체 이미지로 붙이지 않습니다.
""")

practice_rows = ["| 차시 | 현재 실습 | 제작 관리용 출처 쪽 | 원본 실습·예시 |", "|---|---|---|---|"]
for item in catalog:
    practice_rows.append(f"| {item['chapter']} | {item['practice_id']} {item['title']} | {item['source_pdf_pages']} | {item['source_label']} |")
write("practice-source-review.md", f"""# 제작 관리용 실습 대응 기록 · {DATE}

현재 교재는 16차시·41개 실습 카드입니다. 아래 출처 대응은 제작 관리용이며 학생용 본문에 표시하지 않습니다. 원본 과제·데이터·위젯·결과를 유지했고 출처 소개·과거 번호·수정 고지는 본문에서 제외했습니다.

## 과정 개편

1-11차시는 유지했습니다. 12차시의 직접 입력 Chart 3개와 13차시의 자료·API·저장 4개를 분리했습니다. Matplotlib와 Pandas는 14·15차시로 이동했고 16차시는 자율 프로젝트입니다. 코코봇의 2개 실습과 관련 11개 원고 컨테이너·이미지 3개를 제외했습니다. 차시 수는 16개를 유지했습니다.

이전에 정리한 임의 입력값·콘솔 대체 실습·추가 앱 과제는 다시 넣지 않았습니다. 원본이 값을 지정하지 않은 과제는 학생이 직접 입력합니다. 실행 코드 12개·출력·기존 비코코봇 이미지 30개는 이전 학생판과 같습니다. 7쪽에는 사용자 요청의 환각 설명 활동을 추가하고 가상 상황임을 명시했습니다. 실습 카드 41개는 유지합니다.

순서도는 기준 교재의 가족 나이 합(23쪽), 운동 시간 누적(31쪽), 수면 시간 분기(36쪽), 네 학생 영화 관람 조건(39쪽)을 직접 재사용했습니다. 현재 물리 페이지는 각각 23·29·36·42쪽입니다. 네 학생의 영화 조건을 그림과 맞추고 N명 점수 판정·80점 조건은 별도 글 단계로 유지했습니다. 선언은 6각형이며 누적 반복의 10회·합계 55와 15세 관람 경계를 확인했습니다.

원본의 메시지 창, 학생 100명 자료, 학교별 학생 수, 지하철역 API, Matplotlib 여덟 그래프 활동, mon-sun DataFrame을 유지했습니다. 계산기 실습은 두 숫자와 사칙연산 기호를 사용하는 계산기 2로 구성했습니다. API 입력 인증키가 보이는 캡처는 사용하지 않습니다.

## 실습별 대응표

{chr(10).join(practice_rows)}

GUI·API 실습의 새 실행을 주장하지 않습니다. 필요한 학생 자료·API 주소·인증 정보는 수업 환경에서 준비합니다. 과거 대조 기록과 제외한 내용은 previous-reports/20261011-before-no-robot에 보관했습니다.
""")

asset_rows = ["| 파일 | 출처 | 픽셀 크기 | 사용 원고 ID |", "|---|---|---|---|"]
asset_cards = []
for item in assets["items"]:
    if item.get("vector_src"):
        source = f"원본 PDF {item['source_pdf_page']}쪽 순서도 · 인쇄용 벡터와 Canva용 PNG"
    elif item["kind"] == "user-supplied-pdf-embedded-image":
        source = f"원본 PDF {item['pdf_page']}쪽"
    else:
        source = "검증한 코드 실행 결과"
    used = item["used_in"] if isinstance(item["used_in"], list) else [item["used_in"]]
    asset_rows.append(f"| {item['src']} | {source} | {item['width']}×{item['height']} | {', '.join(used)} |")
    asset_cards.append(f'<article><h2>{html.escape(Path(item["src"]).name)}</h2><p>{html.escape(source)}</p><img src="{html.escape(item["src"])}" alt="{html.escape(source)}"><p>{item["width"]} × {item["height"]}</p></article>')
write("asset-audit.md", f"""# 제작 관리용 이미지 출처 · {DATE}

현재 PNG 파일 34개·지면 배치 35곳입니다. 원본 캡처 22개·실행 그래프 7개·실행 표 1개의 기존 파일 30개는 픽셀·출력 폭·비율을 유지했습니다. 원본 순서도 4개는 인쇄용 벡터 PDF 4개와 Canva용 PNG 4개로 준비했습니다. 이 출처 목록은 학생용 본문 밖에서 관리합니다.

벡터 순서도에는 DPI를 적용하지 않습니다. 순서도 PNG는 300dpi 추출이며 metadata의 effectiveDpi는 인쇄 폭에 맞춰 계산한 PNG 대체 파일 정보입니다. 순서도 도형·글꼴·경로·색은 보존했고 crop 밖의 글자와 전체 페이지 회색 배경만 정리했습니다. 상세 확인은 flow-source-review.md와 flow-source-map.json에 있습니다.

{chr(10).join(asset_rows)}
""")
write("asset-review.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><title>현재 교재 PNG 34개</title><style>body{font-family:Malgun Gothic,sans-serif;margin:32px;background:white}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}article{border:1px solid #ccc;padding:16px}img{max-width:100%;height:auto}h2{font-size:18px}</style><h1>앱 개발 16차시 PNG 34개</h1><p>' + DATE + ' · 제작 관리용 캡처·실행 결과·순서도 미리보기. 인쇄 순서도는 별도의 벡터 PDF 4개를 사용합니다.</p><main>' + ''.join(asset_cards) + '</main></html>')

write("apps-edition-review.md", f"""# 앱 개발 16차시 개편 검토 · {DATE}

현재 [학생용 PDF](../../output/pdf/{PDF.name})는 A4 {current_pages}쪽입니다. 이전 학생판 {previous_pages}쪽을 기준으로 코코봇을 제외하고 앱·데이터 과정으로 재구성했습니다.

| 구분 | 이전 | 현재 |
|---|---|---|
| 차시 | 16 | 16 |
| 원고 컨테이너 | 179 | 170 |
| 실습 카드 | 43 | 41 |
| 실행 코드 | 12 | 12 |
| PNG 이미지 파일·배치 | 33·34 | 34·35 |
| 인쇄용 원본 순서도 벡터 PDF | 0 | 4 |
| 순서도 | 4 | 4 |
| PDF 쪽 | {previous_pages} | {current_pages} |

12차시는 직접 입력 Chart, 13차시는 학생 자료·API·저장, 14차시는 Matplotlib, 15차시는 Pandas, 16차시는 자율 프로젝트입니다. 기존 코코봇 차시의 11개 원고 컨테이너·실습 2개·이미지 3개를 제외했고 새 13차시 시작과 12차시 완료 확인을 추가했습니다.

실행 코드·출력과 남은 이미지의 픽셀·출력 폭·비율을 보존했습니다. 학생용 본문의 코코봇·기준 교재 대조·PDF 메타 언급 0, 코드 차이·원고 ID 누락·지면 넘침·목차 오류 0입니다. 목차 링크·책갈피 각각 16개와 주요 글꼴 포함을 확인했습니다.

이번 추가 수정은 7쪽 가상 환각 예시·확인 방법과 순서도 원본 직접 재사용입니다. 선언의 6각형을 유지했고 29쪽 반복의 누적 후 증가·10회 실행·종료 합계 55를 확인했습니다. 순서도는 원본 23·31·36·39쪽에서 가져와 현재 23·29·36·42쪽에 배치했습니다. 기존 31개 래스터의 물리 출력 폭과 픽셀은 유지합니다.

원고 ID 개편 기록은 page-restructure.json, 이전 PDF 지면 대응은 page-compaction-review.md, 상세 자동 검증은 output/pdf/{qa_path.name}에 있습니다. 이전 자료와 제외한 내용은 previous-reports/20261011-before-no-robot에 보관했습니다.
""")

flow_rows = ["| 현재 쪽 | 순서도 | 기준 PDF 쪽 | 인쇄용 벡터 | Canva용 PNG |",
             "|---|---|---|---|---|"]
for item in diagrams:
    flow_rows.append(f"| {page_numbers(new_pages_by_id[item['page_id']])} | {item['alt']} | {item['source_pdf_page']} | {item['vector_src']} | {item['src']} |")
write("flow-source-review.md", f"""# 순서도 직접 재사용·학습 내용 검증 · {DATE}

현재 완성본 output/pdf/{PDF.name}의 순서도 4개는 기준 교재의 네이티브 벡터를 직접 사용했습니다. 재그린 도형이나 PNG를 인쇄 그림으로 사용하지 않습니다. Canva에서 쓸 300dpi PNG를 별도로 준비했습니다.

{chr(10).join(flow_rows)}

원본 PDF는 수정하지 않았습니다. 추출 자산에서 crop 밖의 글자만 제거하고 전체 페이지 회색 배경 색상을 흰색으로 바꿨습니다. 순서도 노드·연결·글꼴·벡터 경로와 색은 보존했습니다. 각 벡터 자산은 1쪽이며 내부 래스터 이미지 객체는 0입니다. PNG·벡터 SHA-256, cropbox, 원고 flowchart 블록 SHA-256을 확인했습니다. 원본 파일을 현재 환경에서 직접 해시 확인했는지 여부는 QA의 sourcePdfHashVerified에 기록합니다. 원본이 없는 다른 컴퓨터에서는 보존 출처 기록과 묶음 자산의 해시 검증을 구분합니다.

## 선언·반복·조건 확인

선언·초기 준비는 원본의 6각형 기호입니다. 원본 기호와 현재 그림을 제작자 및 독립 검토자가 시각 확인했습니다. 자동 검사에서는 자산·원고 해시와 배치 연결을 확인하며 6각형을 영상 인식으로 판정했다고 주장하지 않습니다.

29쪽 반복은 time1=1, total=0에서 시작합니다. time1<=10인 동안 total에 time1을 더하고 time1을 1 증가시킵니다. 누적 추적은 1→1, 2→3, 3→6, 4→10, 5→15, 6→21, 7→28, 8→36, 9→45, 10→55입니다. 10을 포함해 10회 반복한 후 time1=11, total=55에서 종료합니다.

42쪽은 네 학생의 영화 관람 조건입니다. 15세 미만은 관람 불가이며 14·15·16·13세의 결과는 불가·가능·가능·불가입니다. 점수 판정의 N명·80점 활동은 별도 실습 글 단계로 유지했습니다.

## 7쪽 환각 설명

제1차 십자군·『연금술사』 질문에 대한 학습용 가상 오답 2개임을 표시했습니다. 정확한 연도·작가·출간 연도, 질문의 전제와 근거 확인, 맞음·틀림·확인하지 못함 구분, 책임 있는 사용을 한 장에 배치했습니다. 실제 AI 출력 사례가 아니며 사실 확인 근거는 hallucination-source-review.md/json에 보관합니다. 본문 끝은 이전 {old_ethics['y']:g}pt에서 {ethics_layout['y']:g}pt로 변경됐으며 글자·상자 넘침은 0입니다. {current_pages}쪽 전체 렌더링과 해당 지면의 독립 시각 검토를 완료했습니다.

원고·실습·코드를 이 보고서가 수정하지 않습니다. 재생성 절차는 notes.md에 있으며 prepare_source_flowcharts.py는 원본 재추출 때만 사용합니다. 이 문서는 제작 관리용이며 학생용 본문에 출처 메타를 넣지 않습니다.
""")

write("flowchart-canva.md", f"""# Canva 순서도 사용 안내 · {DATE}

현재 순서도 4개는 완성되어 있습니다. 사용자가 원본 교재 순서도를 가져와 활용하도록 요청했으므로 기존의 도형 재제작·편집 가능한 요소 조립 안내 대신 원본 자산을 사용합니다. 독립 인쇄 PDF는 벡터 PDF 4개를 포함하며 Canva용 PNG 4개도 준비했습니다.

{chr(10).join(flow_rows)}

Canva 이미지 입력 시 로컬 coala-book-md/vibe-coding-16/assets/source-flowcharts 폴더를 지정하고 해당 PNG를 넣습니다. 비율을 유지하고 글자·화살표·분기 표시가 잘리지 않게 배치합니다. 원본의 선언은 6각형이고 도형·글꼴·연결을 보존합니다. 이 PNG를 넣는 경로에서는 내부 노드가 각각 편집 가능한 Canva 도형이 되지 않습니다. 독립 PDF의 인쇄 순서도는 PNG가 아닌 네이티브 벡터입니다.

벡터·PNG의 출처와 해시는 flow-source-map.json, 검증은 flow-source-review.md에서 확인합니다. 벡터에는 DPI를 적용하지 않습니다. PNG는 원본에서 300dpi로 추출했습니다. 기준 원고의 논리와 실제 그림을 함께 유지하며 변경할 때는 각 순서도 블록 해시도 맞춥니다.

prepare_source_flowcharts.py는 원본 자산을 다시 추출할 때만 실행하며 원본 PDF·PyMuPDF가 필요합니다. 일상 원고 편집 또는 기존 자산을 쓰는 PDF 재생성 때 실행하지 않습니다. 현재 자산을 사용하는 조판에는 원본 PDF나 PyMuPDF가 필요하지 않습니다.
""")

mapping_rows = ["| 이전 학생판 쪽 | 현재 쪽 | 이전 원고 ID | 상태 |", "|---|---|---|---|"]
for item in mapping:
    mapping_rows.append(f"| {item['previousPage']} | {page_numbers(item['currentPages'])} | {', '.join(item['previousSourceIds'])} | {'제외한 차시' if item['excluded'] else '현재 지면에 대응'} |")
write("page-compaction-review.md", f"""# 과정 개편·페이지 대응 검토 · {DATE}

현재 [학생용 PDF](../../output/pdf/{PDF.name})는 A4 {current_pages}쪽입니다. 이전 학생판 {previous_pages}쪽에서 앱·데이터 중심으로 과정을 개편했습니다. 이전 179쪽→149쪽의 통합 기록은 보관 폴더에 남아 있습니다.

이번 개편은 코코봇 차시를 제외하고 Chart를 12차시 직접 입력·13차시 자료 활용으로 나눕니다. 기존 Matplotlib와 Pandas는 14·15차시로 이동합니다. 새 13차시 시작과 12차시 완료 확인을 추가했습니다.

표는 이전 각 물리 페이지의 원고 ID를 현재 ID에 연결한 결과입니다. 한 원고가 여러 장에 걸친 경우 해당 원고의 현재 전체 쪽을 표시합니다. 제외한 차시는 현재 쪽이 없습니다. 표지·목차도 포함합니다.

{chr(10).join(mapping_rows)}

새 원고 ID: {', '.join(sorted(new_ids))}. 제외한 원고 ID: {', '.join(sorted(removed_ids))}. 상세 매핑은 page-restructure.json과 output/pdf/{qa_path.name}에 있습니다.
""")

example_rows = ["| 차시 | 파일 | 동작 |", "|---|---|---|"]
code_titles = {page["id"]: page.get("title", page["id"]) for page in spec["pages"]}
for item in code_specs:
    example_rows.append(f"| {item['chapter']} | {item['page_id']}.py | {code_titles[item['page_id']]} |")
write("examples/source-based/README.md", f"""# 현재 교재의 Python 실행 예제 · {DATE}

14차시 Matplotlib 7개, 15차시 Pandas 5개 코드를 사용합니다. 데이터·코드·출력은 이전 실제 실행 검증본과 같으며 차시 번호와 파일 이름을 현재 16차시에 맞췄습니다.

Python 3.10 이상에서 requirements.txt의 패키지를 설치한 뒤 각 .py 파일을 실행합니다. 한글 축 제목을 표시하려면 한글 글꼴을 설정합니다. GUI 실습은 사용하는 수업 도구에서 진행합니다.

{chr(10).join(example_rows)}

관리용 실습 출처와 실행 검증은 ../../practice-source-review.md 및 ../../code-results.json에 있습니다. 임의 콘솔 대체 활동과 새 앱 예시는 추가하지 않습니다.
""")
write("examples/README.md", """# 실습 예제

현재 교재의 14차시 Matplotlib·15차시 Pandas 실행 코드는 [source-based](source-based/README.md)에 있습니다. 실행 코드 12개를 사용합니다.

제작 관리용 출처 대응은 [실습 대조 기록](../practice-source-review.md), 검증 결과는 [code-results.json](../code-results.json)에서 확인합니다. index.html과 이전 assets/chXX 화면은 과거 별도 앱 초안입니다.
""")

# Package current inputs only. All old PDFs and excluded images remain archived.
members = set()
for pattern in ("*.md", "*.json"):
    members.update(BOOK.glob(pattern))
members.add(BOOK / "asset-review.html")
members.update(BOOK / item["src"] for item in assets["items"])
members.update(BOOK / item["vector_src"] for item in diagrams)
members.update((BOOK / "examples/source-based").glob("*"))
members.add(BOOK / "examples/README.md")
members.update(ARCHIVE / name for name in
               ("vibe-coding-16-student.json", "code-specs.json", "code-results.json", "source-audit.md"))
with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(members):
        if path.is_file():
            archive.write(path, "vibe-coding-16/" + path.relative_to(BOOK).as_posix())
    for path in (PDF, PDF.with_suffix(".json"), qa_path):
        archive.write(path, "output/pdf/" + path.name)
    for name in ("build_textbook_pdf.py", "finalize_student_manuscript.py", "finalize_textbook_pdf.py",
                 "review_textbook_pdf.py", "report_apps_edition.py", "prepare_source_flowcharts.py"):
        archive.write(ROOT / "scripts" / name, "scripts/" + name)
    archive.writestr("START-HERE.txt", f"""{DATE} 앱 개발 16차시 학생용 완성본

완성 PDF: output/pdf/{PDF.name} (A4 {current_pages}쪽)
원고: vibe-coding-16/book.md 및 ch01.md-ch16.md
과정: 12 직접 입력 Chart / 13 자료·API·저장 / 14 Matplotlib / 15 Pandas / 16 자율 프로젝트
코드: vibe-coding-16/examples/source-based (Python 12개)
이미지: vibe-coding-16/assets (PNG 34개·인쇄 순서도 벡터 PDF 4개)
수정: 7쪽 가상 환각 예시 / 선언 6각형 / 29쪽 반복 합계 55 / 원본 순서도 4개 재사용
검증: output/pdf/{qa_path.name}
구성 안내: vibe-coding-16/curriculum.md

PDF는 바로 열 수 있습니다. 저장소에서 수정하려면 vibe-coding-16 폴더를
coala-book-md/vibe-coding-16에 복사하고 output, scripts도 저장소에 복사합니다.
PDF 재생성에는 Node 앱 파서·Python 패키지·필요 글꼴을 준비합니다.
절차는 vibe-coding-16/notes.md에서 확인합니다.
일반 재생성에는 원본 PDF·PyMuPDF가 필요하지 않습니다.
prepare_source_flowcharts.py는 원본 재추출 때만 쓰며 평소 실행하지 않습니다.

학생용 교재와 별도로 포함한 출처·검증 기록은 제작 관리용입니다.
비교용 이전 metadata·코드 JSON 3개와 수정 근거 문서 1개만 관리 기록으로 포함합니다.
이 묶음에는 이전 완성 PDF·원고와 제외한 코코봇 이미지·실습을 넣지 않았습니다.
""")

with zipfile.ZipFile(bundle) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    packaged_pdfs = [name for name in names if name.startswith("output/pdf/") and name.endswith(".pdf")]
    assert packaged_pdfs == ["output/pdf/" + PDF.name], packaged_pdfs
    assert not any(is_robot_asset(name) for name in names
                   if not name.startswith("vibe-coding-16/previous-reports/"))
    assert sum(name.startswith("vibe-coding-16/assets/") and name.endswith(".png") for name in names) == 34
    assert sum(name.startswith("vibe-coding-16/assets/") and name.endswith(".pdf") for name in names) == 4
    assert "scripts/finalize_student_manuscript.py" in names
    assert "scripts/prepare_source_flowcharts.py" in names
    for diagram in diagrams:
        assert digest(archive.read("vibe-coding-16/" + diagram["vector_src"])) == diagram["vector_sha256"]
        assert digest(archive.read("vibe-coding-16/" + diagram["src"])) == diagram["sha256"]
    assert sum(name.startswith("vibe-coding-16/examples/source-based/") and name.endswith(".py") for name in names) == 12
    assert sum(name.startswith("vibe-coding-16/ch") and name.endswith(".md") for name in names) == 16
    packaged_hash = digest(archive.read("output/pdf/" + PDF.name))
    assert packaged_hash == metadata["pdfSha256"] == qa["pdfSha256"]
    assert json.loads(archive.read("output/pdf/" + PDF.stem + ".json"))["pdfSha256"] == packaged_hash
    assert json.loads(archive.read("output/pdf/" + qa_path.name))["pdfSha256"] == packaged_hash
    assert digest(archive.read("vibe-coding-16/book.md")) == metadata["manuscriptSha256"]

print(json.dumps({"pages": current_pages, "previous_pages": previous_pages,
                  "manuscript_containers": 170, "practice_cards": 41,
                  "code_blocks": 12, "png_assets": 34, "vector_assets": 4, "images": 35, "flowcharts": 4,
                  "bookmarks": 16, "contents_links": contents_links,
                  "pdf_sha256": packaged_hash, "code_hashes_unchanged": True,
                  "image_sizes_unchanged": True, "bundle_bytes": bundle.stat().st_size},
                 ensure_ascii=False))
