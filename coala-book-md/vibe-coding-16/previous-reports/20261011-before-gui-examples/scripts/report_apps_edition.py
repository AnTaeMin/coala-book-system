"""Validate, document and package the current 16-session learner edition.

Run after manuscript assembly, parser validation, PDF generation and full
rendering. This report never changes manuscript, source maps, assets, programs,
renderer or PDF. Historical comparisons remain separate from current checks.
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

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coala-book-md/vibe-coding-16"
PDF = ROOT / "output/pdf/vibe-coding-16-no-pandas.pdf"
QA_INPUT = ROOT / "tmp/pdfs/no-pandas-review/automated-qa.json"
ARCHIVE = BOOK / "previous-reports/20261011-before-no-pandas-divider"
BASELINE = ARCHIVE / "vibe-coding-16-source7.json"
DATE = "2026-10-11"
EDITION = "no-pandas-16-sessions"
FONT_NAMES = ("WantedSans-Regular.ttf", "WantedSans-Medium.ttf",
              "WantedSans-Bold.ttf", "HakgyoansimChilpanjiugaeL.ttf")
REMOVED_ASSETS = {"assets/source-20261006/image-divider.png",
                  "assets/source-20261006/pandas-table.png"}
HALLUCINATION_EXAMPLES = [
    {"topic": "제1차 십자군의 연도",
     "question": "제1차 십자군은 1492년에 시작했나요?",
     "learning_only_wrong_answer": "네, 1492년에 시작했습니다.",
     "verified_fact": "제1차 십자군은 1096~1099년에 진행되었습니다.",
     "source_title": "OpenStax · 13.4 The Crusading Movement",
     "source_url": "https://openstax.org/books/world-history-volume-1/pages/13-4-the-crusading-movement"},
    {"topic": "소설 연금술사의 작가·출간 연도",
     "question": "산티아고가 나오는 소설 『연금술사』는 셰익스피어의 작품인가요?",
     "learning_only_wrong_answer": "네, 셰익스피어가 쓴 작품입니다.",
     "verified_fact": "파울로 코엘료의 소설로, 1988년에 처음 출간되었습니다.",
     "source_title": "Paulo Coelho and Christina Oiticica Foundation · The Alchemist",
     "source_url": "https://fondationpaulocoelho.com/books/paulo-coelho-the-alchemist/"},
]
ACTIVITIES = {
    1: "AI 질문과 답의 검증", 2: "질문 비교·앱 입력 데이터 설계",
    3: "아이디어를 입력·처리·출력으로 나누기",
    4: "가족 나이 합·학생 세 명의 총점", 5: "운동 시간 누적·카페인 입력 반복",
    6: "수면 시간 분류", 7: "학생 점수 판정·영화 관람 조건",
    8: "버튼 색·메시지 창·Field 복사와 삭제",
    9: "누적곱·계산기·Text 추가·구구단",
    10: "Dropdown·Checkbox·RadioButton·진행 막대·두 이미지",
    11: "성적표의 행 추가·셀 값 변경",
    12: "배열·선 그래프·표시 범위·마커·제목과 축 이름",
    13: "막대 높이·나란한 막대 위치·산점도·시드·축과 범례",
    14: "직접 입력한 값의 선 그래프·산점도·막대그래프",
    15: "학생 자료·학교별 학생 수·프로젝트 저장과 불러오기",
    16: "프로젝트 아이디어·UI 설계·실행 확인",
}
REPORTS = [
    "README.md", "notes.md", "canva-production-status.md", "validation-summary.md",
    "pdf-final-review.md", "handover.md", "final-draft.md", "curriculum.md",
    "teacher-guide.md", "print-activities.md", "source-audit.md",
    "practice-source-review.md", "asset-audit.md", "asset-review.html",
    "page-compaction-review.md", "apps-edition-review.md", "flowchart-canva.md",
    "flow-source-review.md", "hallucination-source-review.md", "hallucination-source-review.json",
    "hallucination-page-comparison.json", "graph-first-edition-review.md",
    "graph-first-edition-comparison.json", "page-merge-review.md", "page-merge-comparison.json",
    "calculator-widget-correction.json", "source-reference-review.md",
    "no-pandas-edition-review.md", "no-pandas-edition-comparison.json",
    "examples/README.md", "examples/source-based/README.md",
]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(value):
    return hashlib.sha256(value).hexdigest()


def write(name, text):
    path = BOOK / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def image_signature(item):
    return (item["src"], tuple(item["pixels"]), item["printWidthPt"], item["effectiveDpi"],
            item.get("format"), item.get("vectorSha256"))


def placed_pages(layout):
    result = defaultdict(list)
    for number, page in enumerate(layout, 1):
        for source_id in set([page["id"]] + page.get("includedSources", [])):
            result[source_id].append(number)
    return result


def normalized(text):
    return re.sub(r"\s+", "", text)


def code_signature(item):
    return digest(item["code"].encode("utf-8")), digest((item.get("output") or "").encode("utf-8"))


# All validation precedes report and ZIP writes.
metadata = read_json(PDF.with_suffix(".json"))
baseline = read_json(BASELINE)
qa = read_json(QA_INPUT)
assets = read_json(BOOK / "asset-manifest.json")
old_assets = read_json(ARCHIVE / "asset-manifest.json")
flows = read_json(BOOK / "flow-source-map.json")
old_flows = read_json(ARCHIVE / "flow-source-map.json")
source_reference = read_json(BOOK / "source-reference-review.json")
sources = read_json(BOOK / "source-map.json")
practice_source = read_json(BOOK / "practice-source-map.json")
old_practices = read_json(ARCHIVE / "practice-source-map.json")["practices"]
catalog = practice_source["practices"]
code_specs = read_json(BOOK / "code-specs.json")
codes = read_json(BOOK / "code-results.json")
old_code_specs = read_json(ARCHIVE / "code-specs.json")
old_codes = read_json(ARCHIVE / "code-results.json")
validations = read_json(BOOK / "validation-full.json")
spec = read_json(ROOT / "tmp/pdfs/book-spec.json")
revision = read_json(BOOK / "no-pandas-restructure.json")
manuscript = (BOOK / "book.md").read_text(encoding="utf-8")
current_pages, previous_pages = metadata["pages"], baseline["pages"]
containers = len(spec["pages"])
id_map = revision["old_to_new"]
removed_ids, added_ids = set(revision["removed_pages"]), set(revision["added_pages"])
source_ids = {page["id"] for page in spec["pages"]}
pages_by_id = placed_pages(metadata["layout"])
old_pages_by_id = placed_pages(baseline["layout"])
assert previous_pages == 134
assert current_pages == qa["pages"] == qa["renderedPages"]
assert containers == revision["expected_containers"] == 160
assert len(source_ids) == containers and source_ids <= set(pages_by_id)
assert len(id_map) == 167 and set(id_map) <= set(old_pages_by_id)
if (ARCHIVE / "book.md").is_file():
    assert set(id_map) == set(re.findall(r':::page\{[^\n]*id="([^"]+)"', (ARCHIVE / "book.md").read_text(encoding="utf-8")))
assert removed_ids == {key for key, value in id_map.items() if value is None}
assert len(removed_ids) == 14 and all(value.startswith("ch15-") for value in removed_ids)
assert source_ids == {value for value in id_map.values() if value} | added_ids
assert len(validations) == 17 and validations[0]["pages"] == containers
assert all(value["ok"] and not value["issues"] for value in validations)
assert len(catalog) == metadata["pageTypes"]["practice-opening"] == revision["expected_practices"] == 37
assert len(code_specs) == codes["executed_blocks"] == codes["passed"] == revision["expected_python_blocks"] == 7
assert qa["manuscriptCodeBlocks"] == qa["printedCodeBlocks"] == 7
assert not any(item.get("output") for item in code_specs)
assert not re.search(r"^```(?:text|output)\s*$", manuscript, re.M)
assert revision["expected_output_blocks"] == 0
assert digest((BOOK / "book.md").read_bytes()) == metadata["manuscriptSha256"]
assert digest(PDF.read_bytes()) == metadata["pdfSha256"]
for key in ("outOfPageGlyphs", "missingSourceIds", "contentsErrors", "codeContentDifferences",
            "replacementGlyphPages", "institutionLogoTextPages", "editorialReferencePages",
            "robotReferencePages", "boxOverflows"):
    assert not qa[key], (key, qa[key])

# Retained programs are checked by the explicit old-to-new ID mapping.
executed = {item["page_id"]: item for item in codes["records"]}
previous_executed = {item["page_id"]: item for item in old_codes["records"]}
expected_codes = {id_map[item["page_id"]]: item for item in old_code_specs if id_map.get(item["page_id"])}
current_codes = {item["page_id"]: item for item in code_specs}
assert set(expected_codes) == set(current_codes) == set(executed)
current_code_fences = {}
for page in spec["pages"]:
    for section in page.get("sections", []):
        for code in re.findall(r"```python\s*\n(.*?)\n```", section.get("content", ""), re.S):
            assert page["id"] not in current_code_fences
            current_code_fences[page["id"]] = digest(code.encode("utf-8"))
assert len(current_code_fences) == 7
code_checks = []
for page_id, item in current_codes.items():
    old = expected_codes[page_id]
    code_sha, output_sha = code_signature(item)
    assert code_signature(old) == (code_sha, output_sha)
    assert current_code_fences[page_id] == executed[page_id]["code_sha256"] == code_sha
    assert previous_executed[old["page_id"]]["code_sha256"] == code_sha
    assert executed[page_id]["status"] == "passed"
    path = BOOK / "examples/source-based" / (page_id + ".py")
    assert path.read_text(encoding="utf-8").rstrip() == item["code"].rstrip()
    old_path = ARCHIVE / "examples/source-based" / (old["page_id"] + ".py")
    byte_compared = old_path.is_file()
    if byte_compared:
        assert path.read_bytes() == old_path.read_bytes()
    code_checks.append({"previousId": old["page_id"], "currentId": page_id, "codeSha256": code_sha,
                        "outputSha256": output_sha, "exampleFileSha256": digest(path.read_bytes()),
                        "previousExampleBytesDirectlyCompared": byte_compared})
assert Counter(item["chapter"] for item in code_specs) == {12: 4, 13: 3}
assert sorted(current_code_fences.values()) == sorted(revision["retained_code_sha256"])
assert not any("pandas" in item["code"].lower() for item in code_specs)
requirements = BOOK / "examples/source-based/requirements.txt"
assert "pandas" not in requirements.read_text(encoding="utf-8").lower()

# Keep source practice data and criteria; chapter/practice labels may be renumbered.
practices_by_id = {item["page_id"]: item for item in catalog}
old_practice_by_id = {item["page_id"]: item for item in old_practices}
assert set(practices_by_id) == {id_map[item["page_id"]] for item in old_practices if id_map.get(item["page_id"])}
assert len({item["practice_id"] for item in catalog}) == 37
practice_counts = Counter(item["chapter"] for item in catalog)
assert {number: practice_counts[number] for number in range(12, 17)} == {12: 5, 13: 3, 14: 3, 15: 3, 16: 1}
openings = {page["chapterNumber"]: page for page in spec["pages"] if page["type"] == "chapter-opening"}
assert sorted(openings) == list(range(1, 17))
chapter_titles = {number: page["chapterTitle"] for number, page in openings.items()}
assert {item["chapter"] for item in sources} == set(range(1, 17))

# Active figure additions/removals are explicit; retained pixels and print size match.
asset_by_src = {item["src"]: item for item in assets["items"]}
old_asset_by_src = {item["src"]: item for item in old_assets["items"]}
assert len(asset_by_src) == len(assets["items"])
assert set(old_asset_by_src) - set(asset_by_src) == REMOVED_ASSETS
added_asset_paths = set(asset_by_src) - set(old_asset_by_src)
assert len(added_asset_paths) == 6 and "assets/ch10/two-images.png" in added_asset_paths
save_assets = [asset_by_src[path] for path in sorted(added_asset_paths) if path != "assets/ch10/two-images.png"]
assert len(save_assets) == 5
assert Counter(item["pdf_page"] for item in save_assets) == {119: 2, 124: 1, 125: 1, 126: 1}
assert all(item["chapter"] == 15 for item in save_assets)
assert len(assets["items"]) == 38 and len(metadata["images"]) == qa["images"] == 39
asset_checks = []
for item in assets["items"]:
    path = BOOK / item["src"]
    assert path.is_file() and digest(path.read_bytes()) == item["sha256"], path
    with Image.open(path) as image:
        assert image.size == (item["width"], item["height"])
    if item["src"] in old_asset_by_src:
        assert item["sha256"] == old_asset_by_src[item["src"]]["sha256"]
    if item.get("vector_src"):
        assert digest((BOOK / item["vector_src"]).read_bytes()) == item["vector_sha256"]
        assert len(PdfReader(str(BOOK / item["vector_src"])).pages) == 1
    asset_checks.append({"src": item["src"], "sha256": item["sha256"],
                         "pixels": [item["width"], item["height"]],
                         "status": "added" if item["src"] in added_asset_paths else "retained",
                         "sourcePdfPage": item.get("pdf_page", item.get("source_pdf_page")),
                         "vectorAsset": item.get("vector_src"), "vectorSha256": item.get("vector_sha256")})
retained_placements = [item for item in metadata["images"] if item["src"] in old_asset_by_src]
old_retained_placements = [item for item in baseline["images"] if item["src"] not in REMOVED_ASSETS]
assert len(retained_placements) == len(old_retained_placements) == 33
assert Counter(map(image_signature, retained_placements)) == Counter(map(image_signature, old_retained_placements))
assert {item["src"] for item in metadata["images"]} == set(asset_by_src)
for image in metadata["images"]:
    assert image["sourceId"] in source_ids
    assert image["pixels"] == [asset_by_src[image["src"]]["width"], asset_by_src[image["src"]]["height"]]
vector_assets = [item for item in assets["items"] if item.get("vector_src")]
assert len(vector_assets) == 7
assert Counter(item.get("format", "raster") for item in metadata["images"]) == {
    "native-vector-pdf": 4, "generated-vector-pdf": 1, "source-derived-vector-pdf": 2, "raster": 32}
two_images = asset_by_src["assets/ch10/two-images.png"]
assert two_images["kind"] == "source-derived-vector-illustration"
assert two_images["vector_src"] == "assets/ch10/two-images.pdf"
assert next(item for item in metadata["images"] if item["src"] == two_images["src"])["format"] == "source-derived-vector-pdf"
derived_assets = [item for item in assets["items"] if item["kind"] == "source-derived-vector-illustration"]
assert len(derived_assets) == 2
provenance_records = []
provenance_files = []
for item in derived_assets:
    original = BOOK / item["source_asset"]
    packaged_relative = "provenance/source-assets/" + Path(item["source_asset"]).name
    if not original.is_file():
        original = BOOK / packaged_relative
    assert original.is_file() and digest(original.read_bytes()) == item["source_asset_sha256"]
    provenance_files.append((original, packaged_relative))
    provenance_records.append({"derivedAsset": item["src"], "originalSourceAsset": item["source_asset"],
                               "packagedProvenanceAsset": packaged_relative,
                               "originalSourceSha256": item["source_asset_sha256"],
                               "cropBBoxTopLeftPixels": item["crop_bbox_top_left_px"],
                               "notAnActivePlacement": True})

# Native flow paths and the first-chapter teaching summary remain unchanged.
assert flows["diagrams"] == old_flows["diagrams"] and len(flows["diagrams"]) == qa["flowcharts"] == 4
assert sorted(item["source_pdf_page"] for item in flows["diagrams"]) == [23, 31, 36, 39]
flow_checks = []
for diagram in flows["diagrams"]:
    preview = asset_by_src[diagram["src"]]
    assert preview["sha256"] == diagram["sha256"] and preview["vector_sha256"] == diagram["vector_sha256"]
    fences = re.findall(r"```flowchart\s*\n(.*?)^```\s*$",
                        (BOOK / f"ch{diagram['chapter']:02d}.md").read_text(encoding="utf-8"), re.M | re.S)
    assert len(fences) == 1 and digest(fences[0].encode("utf-8")) == diagram["flowchart_sha256"]
    vector_page = PdfReader(str(BOOK / diagram["vector_src"])).pages[0]
    raster_objects = [value for value in vector_page.get("/Resources", {}).get("/XObject", {}).values()
                      if value.get_object().get("/Subtype") == "/Image"]
    assert not raster_objects
    flow_checks.append({"sourceId": diagram["page_id"], "physicalPages": pages_by_id[diagram["page_id"]],
                        "sourcePdfPage": diagram["source_pdf_page"], "vectorSha256": diagram["vector_sha256"],
                        "previewSha256": diagram["sha256"], "rasterXObjects": 0})
assert flows["declaration_shape"] == "six-sided preparation symbol preserved from source"
trace, total = [], 0
for time1 in range(1, 11):
    total += time1
    trace.append({"time1": time1, "total": total})
assert flows["loop_trace"]["iterations"] == 10 and flows["loop_trace"]["exit"] == {"time1": 11, "total": 55}
assert [age >= 15 for age in [14, 15, 16, 13]] == [False, True, True, False]
summary_map = read_json(BOOK / "intro-summary-map.json")
summary_asset = asset_by_src["assets/ch01/ai-human-summary.png"]
for key in ("src", "vector_src", "sha256", "vector_sha256", "width", "height"):
    assert summary_asset[key] == summary_map[key]
assert summary_map["body_font_pt"] == 14 and summary_map["heading_font_pt"] == 15
assert pages_by_id["ch01-opening"] == [5] and pages_by_id["ch01-ethics"] == [7]
assert metadata["layout"][4] == baseline["layout"][4]
assert metadata["layout"][6] == baseline["layout"][6]

# The source7 equivalence proof is historical provenance, not a claim that this
# deliberately revised learner edition has the previous manuscript/layout.
source_pdf = ROOT / flows["source_pdf"]
source_pdf_checked = source_pdf.is_file()
source_sha = flows["source_sha256"]
assert source_sha == assets["source_sha256"] == practice_source["source_pdf_sha256"] == source_reference["source_sha256"]
assert source_sha == metadata["sourcePdfSha256"]
assert source_sha == "a4aa668621a7c59c36c9666fa1019182d5ed999c9fb8620f2ddcf509840b2729"
assert source_reference["workspace_source_pdf"] == flows["source_pdf"]
assert source_reference["source_pages"] == 158
assert (BOOK / assets["source_pdf"]).resolve() == source_pdf.resolve()
assert (BOOK / practice_source["source_pdf"]).resolve() == source_pdf.resolve()
if source_pdf_checked:
    assert digest(source_pdf.read_bytes()) == source_sha

reader = PdfReader(str(PDF))
assert len(reader.pages) == current_pages and len(reader.outline) == 16
contents_links = sum(len(page.get("/Annots", [])) for page in reader.pages[:3])
assert contents_links == 16
texts = [page.extract_text() or "" for page in reader.pages]
excluded_reference_pages = {name: [number for number, text in enumerate(texts, 1) if re.search(pattern, text, re.I)]
    for name, pattern in {"editorial": r"원본|\bPDF\b", "robot": r"코코봇|로봇|cocobot|robot",
                          "api": r"\bAPI\b|지하철역|공공데이터|인증키",
                          "pandas": r"\bPandas\b|\bSeries\b|\bDataFrame\b", "divider": r"\bDivider\b"}.items()}
assert not any(excluded_reference_pages.values()), excluded_reference_pages
assert not re.search(r"\bPandas\b|\bDivider\b|\bDataFrame\b|\bSeries\b", manuscript, re.I)
embedded_fonts = {}
for page in reader.pages:
    for reference in page["/Resources"].get("/Font", {}).values():
        font = reference.get_object()
        for candidate in [font] + [value.get_object() for value in font.get("/DescendantFonts", [])]:
            descriptor = candidate.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                embedded_fonts[str(candidate.get("/BaseFont"))] = any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
assert embedded_fonts and all(embedded_fonts.values())
hallucination_text = normalized(texts[6])
for required in ("학습용가상오답", "직접확인하기", "책임있는사용", "질문의전제", "연도", "작가"):
    assert required in hallucination_text
for item in HALLUCINATION_EXAMPLES:
    for key in ("question", "learning_only_wrong_answer", "verified_fact"):
        assert normalized(item[key]) in hallucination_text
calculator_sentences = {"ch09-calculator-request": "결과 표시 위젯 fld3에서 계산한 값을 확인합니다.",
                        "ch09-calculator-code": "두 숫자와 선택한 사칙연산을 처리하고 결과를 fld3에 표시합니다."}
calculator_checks = []
for source_id, sentence in calculator_sentences.items():
    assert len(pages_by_id[source_id]) == 1
    physical_page = pages_by_id[source_id][0]
    text = normalized(texts[physical_page - 1])
    assert normalized(sentence) in text and "결과표시위젯txt1" not in text and "결과를txt1에표시" not in text
    calculator_checks.append({"sourceId": source_id, "physicalPage": physical_page, "sentence": sentence})
font_files = [ROOT / "tmp/pdfs/fonts" / name for name in FONT_NAMES]
assert all(path.is_file() for path in font_files)
font_licenses = [path for pattern in ("*LICENSE*", "*license*", "*OFL*", "*COPYING*")
                 for path in (ROOT / "tmp/pdfs/fonts").glob(pattern) if path.is_file()]

mapping = []
for number, page in enumerate(baseline["layout"], 1):
    old_ids = set([page["id"]] + page.get("includedSources", []))
    destination_ids = {id_map.get(value, value) for value in old_ids if value not in removed_ids}
    destination_ids = {value for value in destination_ids if value in pages_by_id}
    destinations = sorted({target for value in destination_ids for target in pages_by_id[value]})
    mapping.append({"previousPage": number, "previousSourceIds": sorted(old_ids),
                    "currentSourceIds": sorted(destination_ids), "currentPages": destinations,
                    "excluded": not destinations, "previousTitle": page["title"]})
comparison = {"date": DATE, "edition": EDITION,
    "baselineMetadata": BASELINE.relative_to(ROOT).as_posix(), "previousPdfPages": previous_pages,
    "currentPdfPages": current_pages, "currentPdfSha256": metadata["pdfSha256"],
    "currentManuscriptSha256": metadata["manuscriptSha256"], "previousManuscriptContainers": len(id_map),
    "currentManuscriptContainers": containers, "previousPracticeCards": len(old_practices),
    "currentPracticeCards": len(catalog), "oldToNewSourceIds": id_map,
    "removedSourceIds": sorted(removed_ids), "addedSourceIds": sorted(added_ids),
    "codeBlocks": 7, "textOutputBlocks": 0, "retainedCodeChecks": code_checks,
    "removedCodeIds": sorted(item["page_id"] for item in old_code_specs if not id_map.get(item["page_id"])),
    "removedAssetPaths": sorted(REMOVED_ASSETS), "addedAssetPaths": sorted(added_asset_paths),
    "activeAssetChecks": asset_checks, "retainedAssetCount": len(asset_by_src) - len(added_asset_paths),
    "retainedImagePlacements": len(retained_placements), "retainedPixelsPrintWidthAndVectorShaUnchanged": True,
    "savedProjectResultPhotoRetainedUnchanged": True, "newSavePhotoSourcePages": [item["pdf_page"] for item in save_assets],
    "derivedIllustrationProvenance": provenance_records,
    "chapterStartPages": metadata["chapterPages"], "previousPhysicalPagesMapping": mapping,
    "summaryPage5Unchanged": True, "hallucinationPage7Unchanged": True,
    "nativeFlowchartChecks": flow_checks, "declarationSixSided": True,
    "loopTrace": trace, "loopExit": {"time1": 11, "total": total},
    "sourcePdf": flows["source_pdf"], "sourceSha256": source_sha,
    "sourceFileHashDirectlyVerified": source_pdf_checked,
    "sourceEquivalenceEvidence": "source-reference-review.json",
    "sourceEquivalenceRecordIsHistorical": True, "studentManuscriptDeliberatelyRevised": True,
    "studentExcludedReferencePages": excluded_reference_pages,
    "calculatorResultWidget": "fld3", "calculatorSentencesChecked": calculator_checks,
    "fontsEmbedded": embedded_fonts, "bookmarks": 16, "contentsLinks": contents_links,
    "bodyFontPt": 14, "headingFontPt": 15, "bodyLeadingPt": 28,
    "checkboxItems": len(re.findall(r"^\s*[-*]\s+\[[ xX]\]", manuscript, re.M)),
    "allCurrentSourceIdsRendered": True, "fullRenderingAutomatedQaPassed": True}

# Preserve management reports before rewriting the current view. The root has
# already archived source files, PDF and assets; never overwrite its archive.
for name in REPORTS:
    path, backup = BOOK / name, ARCHIVE / name
    if path.is_file() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
script_backup = ARCHIVE / "scripts/report_apps_edition.py"
# Root archives the old report script before this edition is authored.
bundle = BOOK.parent / "vibe-coding-16-source-revised.zip"
if bundle.is_file() and not (ARCHIVE / bundle.name).exists():
    shutil.copy2(bundle, ARCHIVE / bundle.name)
qa_path = PDF.with_name(PDF.stem + "-qa.json")
qa.update({"date": DATE, "edition": EDITION, "pdfSha256": metadata["pdfSha256"],
           "manuscriptSha256": metadata["manuscriptSha256"], "manuscriptContainers": containers,
           "practiceCards": len(catalog), "executedCodeBlocks": 7, "executedCodePassed": 7,
           "textOutputBlocks": 0, "uniquePngAssets": len(assets["items"]),
           "vectorAssets": len(vector_assets), "bookmarks": 16, "contentsLinks": contents_links,
           "fontsEmbedded": embedded_fonts, "comparison": comparison})
write_json(qa_path, qa)
write_json(BOOK / "no-pandas-edition-comparison.json", comparison)
write_json(BOOK / "asset-provenance.json", {"date": DATE, "activeDerivedAssets": provenance_records,
    "note": "원래 이미지 보존용이며 인쇄·Canva의 활성 배치 자산 수에 포함하지 않음"})
write_json(BOOK / "calculator-widget-correction.json", {"date": DATE, "resultWidget": "fld3",
    "currentPdfSha256": metadata["pdfSha256"], "checkedSentences": calculator_checks,
    "otherTxt1ExercisesRetained": True, "historicalCorrectionRecord": "previous-reports/20261011-before-no-pandas-divider/calculator-widget-correction.json"})
write_json(BOOK / "hallucination-source-review.json", {"date": DATE, "constructedLearningWrongAnswers": True,
    "actualAiOutputClaimed": False, "examples": HALLUCINATION_EXAMPLES,
    "currentPhysicalPage": pages_by_id["ch01-ethics"][0], "currentPdfSha256": metadata["pdfSha256"],
    "unchangedFromPreviousEdition": True})
for name in ("page-merge-comparison.json", "graph-first-edition-comparison.json", "hallucination-page-comparison.json"):
    write_json(BOOK / name, {"date": DATE, "status": "historical-record-pointer",
        "archivedRecord": "previous-reports/20261011-before-no-pandas-divider/" + name,
        "currentComparison": "no-pandas-edition-comparison.json", "currentPdf": PDF.relative_to(ROOT).as_posix()})

structure = "12차시 Matplotlib 선·마커 → 13차시 Matplotlib 막대·산점도 → 14차시 입력 Chart → 15차시 학생 자료·저장 → 16차시 프로젝트"
counts = f"16차시·{containers}개 원고 컨테이너·37개 실습·7개 Python 코드·4개 순서도"
asset_counts = f"PNG {len(assets['items'])}개·벡터 PDF {len(vector_assets)}개·이미지 배치 {len(metadata['images'])}곳"
current_link = f"[현재 학생용 PDF](../../output/pdf/{PDF.name})"
archive_notice = "직전 source7 134쪽판과 제작 기록은 previous-reports/20261011-before-no-pandas-divider에 보관했습니다. 이전 통합·과정 개편 기록은 현재판의 검증과 구분합니다."
revision_summary = "Matplotlib을 선·마커와 막대·산점도 두 차시로 나누고 입력 Chart를 14차시, 학생 자료·저장을 15차시에 배치했습니다. Pandas 차시의 실습 3개·코드 5개·텍스트 출력 5개·결과 표 이미지 1개를 제외했습니다. Divider를 제외한 두 Image 배치 그림으로 바꾸고 교재의 저장·불러오기 과정 사진 5개를 추가했습니다."
preservation_summary = "남은 Python 코드 7개는 이전 실행 검증본과 코드·실행 해시가 같고, 현재 파일의 내용도 원고와 같습니다. 기존 활성 자산 32개·이미지 배치 33곳의 픽셀·출력 폭·벡터 해시를 보존했습니다. saved-project.png의 사진은 그대로 두고 설명을 실제 화면의 걸음 수·거리 기록에 맞췄습니다."
sources_by_chapter = {item["chapter"]: item for item in sources}
curriculum_rows = ["| 차시 | 주제 | 주요 실습 | 실습 수 | 기준 교재 쪽 |", "|---|---|---|---:|---|"]
for number in range(1, 17):
    curriculum_rows.append(f"| {number} | {chapter_titles[number]} | {ACTIVITIES[number]} | {practice_counts[number]} | {sources_by_chapter[number]['source_pages']} |")
curriculum_table = "\n".join(curriculum_rows)
chapter_page_rows = "\n".join(f"| {number} | {chapter_titles[number]} | {metadata['chapterPages'][str(number)]} |" for number in range(1, 17))
common_review = f"""# 현재 16차시 교재 검토 · {DATE}

{current_link}는 A4 {current_pages}쪽입니다. {counts}. {asset_counts}.

## 현재 구성

{structure}

{revision_summary}

{curriculum_table}

## 보존과 확인

{preservation_summary}

표지·목차·책갈피 16개를 확인했고 모든 {containers}개 원고 ID가 인쇄에 포함됩니다. 본문 14pt·소제목 15pt·행간 28pt를 유지했습니다. 전체 {current_pages}쪽 렌더 검사에서 글자 잘림·누락·코드 차이·박스 넘침은 0건입니다. 학생용 본문의 제외 주제·원본 대조·PDF 제작 문구도 0건입니다.

5쪽 요약 그림과 7쪽 역사·문학의 학습용 가상 오답 설명을 유지했습니다. 선언 도형은 육각형이며 누적 반복의 종료 값은 time1=11, total=55입니다. 계산기 2의 결과 위젯은 fld3입니다. 순서도 4개는 기존 네이티브 벡터·PNG 해시를 유지했습니다.

새 저장 사진은 기준 교재 119쪽 2개와 124·125·126쪽 각 1개입니다. 119쪽 표 저장 스위치는 원본의 해당 영역만 보존한 벡터·PNG로 사용하고 다른 네 사진은 원본 이미지입니다. 두 Image 그림과 표 저장 스위치의 원래 사진은 provenance 하위에 따로 보존합니다. 이미지 파일의 해시·픽셀 크기와 현재 지면 배치를 확인했습니다. GUI 저장·불러오기를 이번 검토에서 새로 실행했다고 주장하지 않습니다. 교실에서 실제 입력 기록·프로젝트 이름·재실행 결과를 확인합니다.

## 현재 검증 자료

[원고 검증](validation-full.json), [실습 대응](practice-source-map.json), [코드 실행](code-results.json), [현재판 비교](no-pandas-edition-comparison.json), output/pdf/{qa_path.name}.

{archive_notice}
"""
for name in ("no-pandas-edition-review.md", "apps-edition-review.md", "pdf-final-review.md", "final-draft.md"):
    write(name, common_review)
write("README.md", f"""# 바이브 코딩 16차시 교재 · {DATE}

{current_link}: A4 **{current_pages}쪽**. {counts}.

{structure}

- [전체 원고](book.md): ch01.md~ch16.md를 조립한 현재 학생용 내용.
- [차시별 구성](curriculum.md), [교사용 안내](teacher-guide.md).
- [현재판 검토](no-pandas-edition-review.md), [이전→현재 지면 대응](page-compaction-review.md).
- [이미지 미리보기](asset-review.html): {asset_counts}.
- [Python 예제](examples/source-based/README.md): 12차시 4개·13차시 3개.
- 전달 ZIP: ../vibe-coding-16-source-revised.zip.

{revision_summary}

다른 컴퓨터에서는 ZIP의 현재 PDF를 바로 열 수 있습니다. 원고 수정과 재생성 순서는 [notes.md](notes.md)에 있습니다. 기준 파일·출처·검증 기록은 관리 문서에 보관하고 학생용 본문에는 넣지 않습니다.
""")
write("curriculum.md", f"""# 16차시 수업 구성 · {DATE}

{structure}

{curriculum_table}

총 37개 실습입니다. 출처 쪽수는 교사용 관리 정보입니다. 12차시에서는 배열과 선·마커, 13차시에서는 막대·산점도를 먼저 실행하고, 14차시의 직접 입력 Chart와 15차시의 자료·저장으로 연결합니다. Pandas·공공데이터 API·코코봇 과정과 Divider 내용은 제외했습니다.
""")
write("teacher-guide.md", f"""# 교사용 운영 안내 · {DATE}

{counts}. 현재 인쇄본은 {current_pages}쪽입니다.

{curriculum_table}

## 수업 운영

1~7차시는 질문 검증·문제 분해·순서도·반복과 조건, 8~11차시는 위젯과 표를 다룹니다. 12차시의 다섯 실습은 코드 4개를 사용하며 제목·설명 활동은 앞 그래프를 함께 활용합니다. 13차시의 세 실습은 코드 3개를 사용합니다. 14차시는 입력값·축·누적 여부, 15차시는 자료의 열과 학교별 집계·저장 전후 값, 16차시는 앱 개선과 발표를 확인합니다.

실습의 수치·데이터·조건은 교재의 예시를 사용합니다. AI가 제안한 내용을 실행한 뒤 입력·처리·출력이 맞는지 확인하고, 실행 화면과 바꾼 내용을 저장합니다.

## 저장·불러오기 사진 안내

15차시의 화면 구성은 기준 교재 119쪽, 저장 메뉴·이름 입력·불러오기는 124~126쪽을 활용했습니다. 마지막 재실행 화면은 127쪽의 걸음 수·거리 예시입니다. 첫 활동의 fld1·fld2·tbl1·cht1 화면과 마지막 예시의 UI 이름을 서로 같은 화면으로 설명하지 않습니다. 학생이 만든 프로젝트의 입력 기록을 저장 전후로 비교합니다.

## 확인할 개념

ro는 빨간 점, r-o는 빨간 점과 선입니다. seed는 난수 생성 상태를 정하므로 같은 시드·생성 순서에서 같은 값이 나옵니다. 축 이름은 set_xlabel·set_ylabel로 설정합니다. 계산기 2의 결과 표시는 fld3이며 별도의 Text·구구단 실습의 txt1은 그대로입니다.

7쪽 두 오답은 학습을 위해 구성한 가상 답변으로 실제 AI 출력이라고 설명하지 않습니다. 질문의 전제·연도·작가를 근거와 비교하여 맞음·틀림·미확인을 기록합니다. 누적 반복은 10회 후 time1=11, total=55이며 영화 관람 경계는 15세입니다.

현재 코드 실행 기록은 code-results.json입니다. GUI·프로젝트 저장 동작은 사용 중인 수업 도구에서 별도로 확인합니다.
""")
write("print-activities.md", f"""# 인쇄 활동지 운영 · {DATE}

현재 {current_link}의 37개 실습 카드와 각 차시 완료 확인을 사용합니다. 새 앱·임의 숫자 과제를 추가하지 않습니다.

12차시는 선·마커·축 이름, 13차시는 막대·산점도, 14차시는 직접 입력 Chart, 15차시는 학생 자료·학교별 개수·저장 전후 값, 16차시는 프로젝트 설계·실행을 기록합니다. 실제 실행 화면과 수정한 내용을 저장해 검토합니다.
""")
write("notes.md", f"""# 원고 수정·다른 컴퓨터 전달 · {DATE}

현재 완성본: output/pdf/{PDF.name}, A4 {current_pages}쪽. {counts}. {asset_counts}.

{structure}

## 일반 수정과 재생성

각 chXX.md를 수정한 뒤 book.md를 조립합니다. 기존 데이터·실습 조건·코드·그림 폭을 유지하고 표지·학생 본문에 제작 메모를 넣지 않습니다.

```powershell
python scripts/finalize_student_manuscript.py
$chapters = (Get-ChildItem coala-book-md/vibe-coding-16 -Filter ch??.md).FullName
$validation = node canva-app/scripts/validate.cjs --layout --json coala-book-md/vibe-coding-16/book.md @chapters
[IO.File]::WriteAllText("coala-book-md/vibe-coding-16/validation-full.json", ($validation -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/{PDF.name}
python scripts/review_textbook_pdf.py --pdf output/pdf/{PDF.name} --dest tmp/pdfs/no-pandas-review
python scripts/report_apps_edition.py
```

validation-full.json은 book.md와 16개 차시가 모두 통과한 현재 결과로 갱신한 뒤 보고서를 실행합니다. Node 명령이 실패하면 다음 명령으로 진행하지 않고 오류를 먼저 수정합니다.

restructure_no_pandas.py·restructure_graph_first.py는 과거 원고에서 일회성으로 구조를 변경한 스크립트입니다. 일상 편집에서 다시 실행하면 후속 수정이 지워질 수 있으므로 사용하지 않습니다. prepare_source_flowcharts.py는 원본 자산 재추출 때만 사용하며 일반 PDF 재생성에는 기준 PDF·PyMuPDF가 필요하지 않습니다. 순서도 YAML을 바꿀 때는 대응 flow-source-map 해시도 함께 갱신해야 합니다.

## 환경과 전달 파일

PDF 자체는 설치 없이 열 수 있습니다. 재조판에는 Python의 reportlab·pypdf·Pillow와 원고 파서용 Node.js, 전체 렌더용 도구가 필요합니다. 코드 예제에는 examples/source-based/requirements.txt의 Matplotlib·NumPy를 설치합니다. ZIP의 tmp/pdfs/fonts에는 사용한 비시스템 글꼴 4개를 포함합니다. Windows의 Consolas는 시스템 글꼴을 사용합니다. 이 보고서에 필요한 직전판 metadata·실습·자산·코드 JSON을 archive 상대 경로에 포함하고 과거 PDF·이미지·원고는 포함하지 않습니다.

원본 파일이 없는 컴퓨터에서는 포함 자산·벡터의 해시와 보존 출처 기록을 검사합니다. 로컬에 기준 PDF가 있을 때만 그 파일의 SHA-256도 직접 검증합니다. 원본 기준 파일 동일성 기록은 이전 기준 변경의 증거이며, 이번 16차시 개편이 원고 불변이었다는 뜻이 아닙니다.

{revision_summary}

{archive_notice}
""")
write("validation-summary.md", f"""# 현재 원고·PDF 검증 · {DATE}

{counts}. book.md와 ch01.md~ch16.md 총 17개 파일의 파서·레이아웃 검사를 통과했습니다. 모든 {containers}개 ID가 인쇄에 포함됩니다.

- PDF {current_pages}쪽 전체 렌더 완료, 자동 검사 오류 0건.
- 실습 37개: 12차시 5개·13차시 3개·14차시 3개·15차시 3개·16차시 1개.
- Python 코드 7개, 텍스트 출력 블록 0개. 유지한 코드·실행 기록·예제 파일 검사 통과.
- {asset_counts}. 유지한 기존 33개 배치의 픽셀·출력 폭·비율·벡터 해시 동일.
- 목차 링크·책갈피 각 16개, 주요 글꼴 포함, 본문 14pt·행간 28pt 유지.
- 학생용 원본/PDF 제작 문구·Pandas·Divider·API·코코봇 언급 0건.

현재 비교는 no-pandas-edition-comparison.json, PDF 검증은 output/pdf/{qa_path.name}입니다. 이전 139→134쪽 통합 검사나 원고 전체 동일성 검사를 이번 개편의 조건으로 재사용하지 않습니다.
""")
write("handover.md", f"""# 전달 파일 안내 · {DATE}

- 완성 PDF: output/pdf/{PDF.name}, A4 {current_pages}쪽.
- 원고: book.md와 ch01.md~ch16.md. {counts}.
- 이미지: {asset_counts}. 현재 manifest에 있는 자산만 전달합니다.
- 실행 예제: examples/source-based의 Python 7개와 requirements.txt.
- 검증: output/pdf/{qa_path.name} 및 no-pandas-edition-comparison.json.
- 전달 ZIP: ../vibe-coding-16-source-revised.zip.

{structure}

다른 컴퓨터에서 PDF를 바로 열거나 ZIP의 vibe-coding-16 폴더를 coala-book-md/vibe-coding-16에 배치하고 output·scripts·tmp/pdfs/fonts를 같은 저장소 위치에 복사합니다. START-HERE.txt와 notes.md에 재생성 순서가 있습니다. Pandas 예제·표 이미지와 기존 Divider 활성 배치, 이전 완성 PDF는 현재 전달본에서 제외했습니다. 두 파생 그림의 원래 사진은 provenance에 따로 보존합니다.
""")
write("canva-production-status.md", f"""# 제작 상태 · {DATE}

현재 완성본은 {current_link}, A4 {current_pages}쪽의 독립 PDF입니다. {counts}. {asset_counts}.

{revision_summary}

원고·활성 자산·완성 PDF·검증 자료를 ZIP에 포함했습니다. Canva 원본 디자인과 동일한 틀이라고 주장하지 않습니다. Canva용 PNG 미리보기와 독립 인쇄용 벡터 PDF를 구분합니다. 세부 검토는 no-pandas-edition-review.md에 있습니다.
""")
write("source-reference-review.md", f"""# 기준 교재 파일·출처 검증 · {DATE}

현재 기준 파일은 {flows['source_pdf']}이며 158쪽입니다. SHA-256: `{source_sha}`.

source-reference-review.json은 이전 기준 파일과 이 파일의 158쪽 공백 정규화 본문·현재 당시 UI 이미지 21개·순서도 4개를 대조한 보존 기록입니다. 이 증거의 학생판 수치와 원고 불변 판정은 당시 source7판을 설명합니다. 현재판은 16차시를 재편하고 사진을 추가했으므로 당시 학생판 불변 판정을 현재판에 적용하지 않습니다.

현재 기준 파일·asset-manifest·practice-source-map·flow-source-map·조판 metadata의 SHA가 일치합니다. 로컬 원본 파일 해시 직접 검사: {source_pdf_checked}. 원본이 없는 컴퓨터에서는 포함된 PNG·벡터 PDF의 해시와 출처 기록을 확인합니다. 일반 PDF 재생성에는 기준 PDF가 필요하지 않습니다.

현재판의 변경·보존 검증은 no-pandas-edition-comparison.json입니다.
""")
write("source-audit.md", f"""# 현재 교재 출처·수정 근거 · {DATE}

{counts}. {structure}

{curriculum_table}

## 포함한 내용의 수정 근거

학습 예시·수치·조건은 기준 교재의 실습을 사용했습니다. 12차시 128~139쪽과 13차시 140~145쪽의 Matplotlib 예시를 분리했습니다. 14차시는 95~105쪽 Chart, 15차시는 106~110·118~127쪽 자료·저장을 사용합니다. 저장 화면은 119·124·125·126·127쪽을 사용합니다. 127쪽 결과는 걸음 수·거리 기록 화면으로 설명합니다.

ro와 r-o의 점·선 차이, 난수 시드, 축 설정 함수와 계산기 결과 위젯 fld3를 정확한 개념으로 안내했습니다. 역사·문학의 학습용 가상 오답은 근거 확인 활동이며 실제 AI 출력이라고 설명하지 않습니다. 새 독립 앱·데이터 실습은 추가하지 않았습니다.

## 코드와 이미지 검증

{preservation_summary}

현재 제외 내용은 Pandas·공공데이터 API·코코봇·Divider입니다. 기존 두 Image 사진은 선을 제외하고 원본 사진 영역을 활용한 벡터로 대체했습니다. 추가 저장 사진 5개는 기준 교재의 화면 자산입니다. 자세한 해시·출처·지면 대응은 현재 비교 JSON에 있습니다. 이전 오류 검토·통합 근거는 보관 폴더에 남겼습니다.
""")
practice_rows = ["| 차시 | 실습 | 원고 ID | 기준 교재 쪽 |", "|---:|---|---|---|"]
for item in catalog:
    practice_rows.append(f"| {item['chapter']} | {item['practice_id']} | {item['page_id']} | {item.get('source_pdf_pages', item.get('source_pages', 'practice-source-map.json 참고'))} |")
write("practice-source-review.md", f"""# 현재 실습·기준 교재 대응 · {DATE}

총 37개 실습입니다. Matplotlib은 12차시 5개와 13차시 3개로 나누었고, 14차시 Chart 3개·15차시 자료와 저장 3개·16차시 프로젝트 1개를 사용합니다. 실습 수치·조건과 그래프 코드 7개를 유지했습니다.

{chr(10).join(practice_rows)}

출처 정보는 관리용입니다. 이전 Pandas 실습 3개를 현재 실습 표·완성본·전달 예제에서 제외했습니다. 자세한 대응은 practice-source-map.json과 no-pandas-restructure.json입니다.
""")
asset_rows = ["| 파일 | 픽셀 | 출처 쪽 | 현재 상태 |", "|---|---|---|---|"]
asset_cards = []
for item in assets["items"]:
    record = next(value for value in asset_checks if value["src"] == item["src"])
    caption = item.get("caption") or next((value.get("caption", "") for value in item.get("placements", []) if value.get("caption")), item["src"])
    asset_rows.append(f"| {item['src']} | {item['width']}×{item['height']} | {record['sourcePdfPage'] or '실행/자체 제작'} | {record['status']} |")
    asset_cards.append(f'<article><h2>{html.escape(caption)}</h2><img src="{html.escape(item["src"])}"><p>{item["width"]}×{item["height"]} · {html.escape(item["src"])}</p></article>')
write("asset-audit.md", f"""# 현재 이미지·벡터 검토 · {DATE}

{asset_counts}. {preservation_summary}

{chr(10).join(asset_rows)}

순서도 4개·요약 1개·두 Image 그림 1개·표 저장 스위치 그림 1개는 인쇄에 벡터 PDF를 사용합니다. 벡터의 effectiveDpi는 Canva용 PNG 대체 파일의 정보이며 인쇄 벡터에 DPI를 적용하지 않습니다. 이전 Divider·Pandas 표 PNG는 활성 manifest에서 제외했습니다. Divider 원래 사진과 표 저장 스위치 원래 사진은 provenance에만 포함합니다. 저장 결과 사진은 유지했고 과정 사진 5개만 추가했습니다.
""")
write("asset-review.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><title>현재 교재 이미지</title><style>body{font-family:Malgun Gothic,sans-serif;margin:32px;background:white}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}article{border:1px solid #ccc;padding:16px}img{max-width:100%;height:auto}h2{font-size:18px}</style><h1>현재 16차시 교재 이미지</h1><p>' + html.escape(asset_counts) + ' · 관리용 미리보기</p><main>' + ''.join(asset_cards) + '</main></html>')
flow_rows = "\n".join(f"| {item['sourceId']} | {item['sourcePdfPage']} | {', '.join(map(str, item['physicalPages']))} |" for item in flow_checks)
write("flow-source-review.md", f"""# 현재 순서도 검토 · {DATE}

원본 도형 경로·글꼴을 보존한 네이티브 벡터 4개를 유지했습니다. PNG는 Canva용 미리보기이고 인쇄에는 벡터 PDF를 사용합니다. 선언은 육각형, 운동 누적은 10회 후 time1=11·total=55, 영화 조건은 15세 이상입니다.

| 원고 ID | 기준 교재 쪽 | 현재 인쇄 쪽 |
|---|---:|---|
{flow_rows}

기존 벡터·PNG·flowchart YAML 해시가 모두 같습니다. 자산 재추출은 이번 개편에서 수행하지 않았습니다. 새 원본 파일 기준과 이전 자산의 동등성은 source-reference-review.json에 보관되어 있습니다.
""")
write("flowchart-canva.md", "# Canva 순서도 자산\n\nflow-source-map.json의 PNG 4개를 사용합니다. 현재 인쇄용 벡터 PDF도 같은 그림의 네이티브 도형을 포함합니다. PNG와 벡터 자산은 전달 ZIP에 포함합니다. 일상 원고 편집에서 prepare_source_flowcharts.py를 다시 실행하지 않습니다.")
hallu_rows = "\n\n".join(f"- {item['topic']}: {item['verified_fact']} [근거]({item['source_url']})." for item in HALLUCINATION_EXAMPLES)
write("hallucination-source-review.md", f"""# 7쪽 가상 오답의 사실 확인 · {DATE}

두 답변은 환각을 살펴보기 위해 만든 학습용 가상 오답이며 실제 AI 출력이 아닙니다. 현재 학생용 7쪽의 안내·질문·오답·사실·직접 확인·책임 있는 사용을 유지했습니다.

{hallu_rows}

현재판에서는 이 지면을 바꾸지 않았습니다. 웹 근거와 제작 메모는 관리 문서에만 보관합니다.
""")
mapping_rows = ["| 이전 쪽 | 현재 쪽 | 이전 원고 ID → 현재 ID |", "|---:|---|---|"]
for item in mapping:
    mapping_rows.append(f"| {item['previousPage']} | {', '.join(map(str, item['currentPages'])) or '제외'} | {', '.join(item['previousSourceIds'])} → {', '.join(item['currentSourceIds']) or '제외'} |")
write("page-compaction-review.md", f"""# 직전판→현재판 지면 대응 · {DATE}

이전 source7판 {previous_pages}쪽 → 현재판 {current_pages}쪽입니다. 이번에는 차시 분리·이동·Pandas 제외·저장 사진 추가를 적용했으므로 단순 페이지 통합으로 설명하지 않습니다. 167개 이전 ID 중 14개를 제외하고 7개를 추가하여 현재 {containers}개 ID를 사용합니다.

{chr(10).join(mapping_rows)}

현재 비교 자료는 no-pandas-restructure.json과 no-pandas-edition-comparison.json입니다. 예전 139→134쪽 5쌍 통합 기록은 이전판의 이력으로 보관했습니다.
""")
for name, title in (("page-merge-review.md", "이전 지면 통합 기록"), ("graph-first-edition-review.md", "이전 과정 개편 기록")):
    write(name, f"# {title} 안내 · {DATE}\n\n현재 학생용 PDF는 output/pdf/{PDF.name}, {current_pages}쪽입니다. 이번 검토는 no-pandas-edition-review.md와 no-pandas-edition-comparison.json입니다.\n\n이전 상세 기록은 previous-reports/20261011-before-no-pandas-divider/{name}에 보존했습니다. 예전 과정 ID mapping이나 통합 계획을 현재 원고에 다시 적용하지 않습니다.")
example_rows = ["| 차시 | 파일 | 학습 내용 |", "|---:|---|---|"]
page_titles = {page["id"]: page.get("title", page["id"]) for page in spec["pages"]}
for item in code_specs:
    example_rows.append(f"| {item['chapter']} | {item['page_id']}.py | {page_titles[item['page_id']]} |")
write("examples/source-based/README.md", f"""# 현재 교재의 Python 실행 예제 · {DATE}

12차시 선·마커 코드 4개, 13차시 막대·산점도 코드 3개입니다. 데이터·코드·실행 검증 해시를 보존했습니다. Pandas 프로그램은 현재 전달본에서 제외했습니다.

requirements.txt의 Matplotlib·NumPy를 설치하고 각 .py 파일을 실행합니다. 한글 축 제목에는 한글 글꼴 설정이 필요합니다.

{chr(10).join(example_rows)}

실행 검증은 ../../code-results.json, 실습 대응은 ../../practice-source-review.md에 있습니다.
""")
write("examples/README.md", "# 실습 예제\n\n현재 12·13차시의 Python 그래프 코드 7개는 [source-based](source-based/README.md)에 있습니다. 실행 검증은 [code-results.json](../code-results.json)을 확인합니다. index.html과 옛 assets/chXX 화면은 이전 별도 앱 초안입니다.")

# Only active figures and current programs are packaged. Historical management
# JSON supports rechecking retained subsets without shipping retired materials.
members = set()
for pattern in ("*.md", "*.json"):
    members.update(BOOK.glob(pattern))
members.add(BOOK / "asset-review.html")
members.update(BOOK / item["src"] for item in assets["items"])
members.update(BOOK / item["vector_src"] for item in vector_assets)
members.update(BOOK / "examples/source-based" / (item["page_id"] + ".py") for item in code_specs)
members.update({requirements, BOOK / "examples/source-based/README.md", BOOK / "examples/README.md"})
archive_dependencies = ("vibe-coding-16-source7.json", "asset-manifest.json", "flow-source-map.json",
                        "code-specs.json", "code-results.json", "practice-source-map.json", "source-audit.md")
members.update(ARCHIVE / name for name in archive_dependencies if name not in ("code-specs.json", "code-results.json"))
script_names = ("build_textbook_pdf.py", "finalize_student_manuscript.py", "finalize_textbook_pdf.py",
                "review_textbook_pdf.py", "report_apps_edition.py", "prepare_source_flowcharts.py",
                "prepare_intro_summary.py", "restructure_no_pandas.py")
with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(members):
        assert path.is_file(), path
        archive.write(path, "vibe-coding-16/" + path.relative_to(BOOK).as_posix())
    for path in (PDF, PDF.with_suffix(".json"), qa_path):
        archive.write(path, "output/pdf/" + path.name)
    for path, packaged_relative in provenance_files:
        archive.write(path, "vibe-coding-16/" + packaged_relative)
    baseline_prefix = "vibe-coding-16/" + ARCHIVE.relative_to(BOOK).as_posix() + "/"
    retained_baseline_specs = [item for item in old_code_specs if id_map.get(item["page_id"])]
    retained_baseline_results = dict(old_codes)
    retained_baseline_results.pop("pandas", None)
    retained_baseline_results.update(executed_blocks=7, passed=7,
        records=[item for item in old_codes["records"] if id_map.get(item["page_id"])],
        scope="Retained Matplotlib programs only; historical Pandas programs omitted from portable bundle")
    archive.writestr(baseline_prefix + "code-specs.json", json.dumps(retained_baseline_specs, ensure_ascii=False, indent=2) + "\n")
    archive.writestr(baseline_prefix + "code-results.json", json.dumps(retained_baseline_results, ensure_ascii=False, indent=2) + "\n")
    for name in script_names:
        archive.write(ROOT / "scripts" / name, "scripts/" + name)
    for path in font_files + list(set(font_licenses)):
        archive.write(path, "tmp/pdfs/fonts/" + path.name)
    archive.writestr("START-HERE.txt", f"""{DATE} 16차시 학생용 완성본

완성 PDF: output/pdf/{PDF.name} (A4 {current_pages}쪽)
원고: vibe-coding-16/book.md 및 ch01.md~ch16.md ({containers}개 컨테이너·37실습)
구성: {structure}
Python 예제: 7개 / 텍스트 출력 블록: 0개
자산: {asset_counts}
검증: output/pdf/{qa_path.name}

PDF는 바로 열 수 있습니다. 원고를 수정하려면 vibe-coding-16 폴더를
coala-book-md/vibe-coding-16에, output·scripts·tmp는 같은 저장소 위치에 복사합니다.
notes.md의 조립→검증→조판→전체 렌더→보고 순서를 따릅니다.
기존 저장소의 canva-app 파서와 Node 패키지도 필요합니다.
일반 재조판에는 원본 PDF·PyMuPDF가 필요하지 않습니다.
Windows Consolas와 Python/Node/렌더 도구 환경은 notes.md를 확인합니다.
일회성 restructure 스크립트와 원본 재추출은 일상 편집에서 실행하지 않습니다.

비교용 이전 JSON과 관리 문서는 포함하며 이전 PDF·원고·Pandas 코드·표 이미지는
포함하지 않습니다. 이전 코드 JSON도 유지한 Matplotlib7개만 담습니다.
원래 사진2개는 provenance에만 보존하며 현재 코드7개와 활성 자산을 사용합니다.
""")
with zipfile.ZipFile(bundle) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert len(names) == len(set(names))
    assert [name for name in names if name.startswith("output/pdf/") and name.endswith(".pdf")] == ["output/pdf/" + PDF.name]
    assert sum(name.startswith("vibe-coding-16/assets/") and name.endswith(".png") for name in names) == len(assets["items"])
    assert sum(name.startswith("vibe-coding-16/assets/") and name.endswith(".pdf") for name in names) == len(vector_assets)
    assert {name for name in names if name.startswith("vibe-coding-16/examples/source-based/") and name.endswith(".py")} == {
        "vibe-coding-16/examples/source-based/" + item["page_id"] + ".py" for item in code_specs}
    assert sum(name.startswith("vibe-coding-16/ch") and name.endswith(".md") for name in names) == 16
    assert not any("pandas-table.png" in name for name in names)
    assert not any(name.startswith("vibe-coding-16/assets/") and "image-divider.png" in name for name in names)
    for path, packaged_relative in provenance_files:
        assert digest(archive.read("vibe-coding-16/" + packaged_relative)) == digest(path.read_bytes())
    assert len(json.loads(archive.read(baseline_prefix + "code-specs.json"))) == 7
    for item in assets["items"]:
        assert digest(archive.read("vibe-coding-16/" + item["src"])) == item["sha256"]
        if item.get("vector_src"):
            assert digest(archive.read("vibe-coding-16/" + item["vector_src"])) == item["vector_sha256"]
    for path in font_files:
        assert digest(archive.read("tmp/pdfs/fonts/" + path.name)) == digest(path.read_bytes())
    packaged_hash = digest(archive.read("output/pdf/" + PDF.name))
    assert packaged_hash == metadata["pdfSha256"] == qa["pdfSha256"]
    assert json.loads(archive.read("output/pdf/" + PDF.stem + ".json"))["pdfSha256"] == packaged_hash
    assert json.loads(archive.read("output/pdf/" + qa_path.name))["pdfSha256"] == packaged_hash
    assert digest(archive.read("vibe-coding-16/book.md")) == metadata["manuscriptSha256"]
print(json.dumps({"pages": current_pages, "previous_pages": previous_pages,
    "manuscript_containers": containers, "practice_cards": len(catalog), "code_blocks": 7,
    "text_output_blocks": 0, "png_assets": len(assets["items"]), "vector_assets": len(vector_assets),
    "images": len(metadata["images"]), "flowcharts": 4, "bookmarks": 16, "contents_links": contents_links,
    "pdf_sha256": packaged_hash, "book_sha256": metadata["manuscriptSha256"],
    "bundle_sha256": digest(bundle.read_bytes()), "bundle_bytes": bundle.stat().st_size,
    "bundle_entries": len(names), "retained_code_hashes_unchanged": True,
    "retained_image_pixels_and_print_widths_unchanged": True}, ensure_ascii=False))
