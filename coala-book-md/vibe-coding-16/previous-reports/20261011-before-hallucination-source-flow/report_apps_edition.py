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


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coala-book-md/vibe-coding-16"
PDF = ROOT / "output/pdf/vibe-coding-16-apps.pdf"
ARCHIVE = BOOK / "previous-reports/20261011-before-no-robot"
BASELINE = ARCHIVE / "vibe-coding-16-student.json"
QA_INPUT = ROOT / "tmp/pdfs/apps-review/automated-qa.json"
DATE = "2026-10-11"
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
    "page-compaction-review.md", "apps-edition-review.md",
]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(name: str, value: str):
    (BOOK / name).write_text(value.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(value: bytes):
    return hashlib.sha256(value).hexdigest()


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
assert len(assets["items"]) == 30
assert len(metadata["images"]) == qa["images"] == 31
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
assert sorted(map(signature, metadata["images"])) == sorted(map(signature, old_images))
for item in assets["items"]:
    path = BOOK / item["src"]
    assert path.is_file(), path
    expected = item.get("sha256")
    if expected:
        assert digest(path.read_bytes()) == expected, path

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
ARCHIVE.mkdir(parents=True, exist_ok=True)
for name in REPORTS:
    path = BOOK / name
    if path.exists() and not (ARCHIVE / name).exists():
        shutil.copy2(path, ARCHIVE / name)
for relative in ("examples/README.md", "examples/source-based/README.md"):
    path = BOOK / relative
    backup = ARCHIVE / relative
    if path.exists() and not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
bundle = ROOT / "coala-book-md/vibe-coding-16-source-revised.zip"
if bundle.exists() and not (ARCHIVE / bundle.name).exists():
    shutil.copy2(bundle, ARCHIVE / bundle.name)

qa.update({"date": DATE, "edition": "apps-16-sessions", "manuscriptContainers": 170,
           "previousPdfPages": previous_pages, "savedPages": saved_pages,
           "practiceCards": 41, "uniqueAssets": 30, "sourceImages": 22,
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
- [이미지 미리보기](asset-review.html): 사용 파일 30개·배치 31곳.
- [실행 예제](examples/source-based/README.md): 14차시 Matplotlib 7개·15차시 Pandas 5개.
- 제작 관리용 [실습 대조 기록](practice-source-review.md), [실습 출처 목록](practice-source-map.json).

{chapter_table_text}

실습 카드 41개·코드 12개·순서도 4개를 포함합니다. 학생용 본문에는 원본 대조·출처 쪽수·제작 과정·PDF 안내 문구를 넣지 않습니다. 출처와 검증 기록은 별도 관리 문서에 보관합니다.

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

이 문서는 교사용 관리 안내입니다. 출처·제작·검증 메모는 학생용 본문 밖에서 관리합니다.
""")

write("notes.md", f"""# 다음 제작·수정에 사용할 관리 지침 · {DATE}

## 현재 16차시 구조

1-11차시는 유지합니다. 12차시에는 직접 입력한 값의 선 그래프·키와 몸무게 산점도·막대그래프를, 13차시에는 학생 자료·학교별 학생 수·공공데이터 API·저장과 불러오기를 둡니다. 14차시는 Matplotlib, 15차시는 Pandas, 16차시는 자율 프로젝트입니다. 코코봇 장비 실습은 추가하지 않습니다.

실습 카드 41개, 원고 컨테이너 170개, 실행 코드 12개, 순서도 4개, 이미지 30개·배치 31곳을 유지합니다. 원본 과제·데이터·위젯·결과를 우선하고 임의 숫자 예시·가상 AI 대화·새 앱 과제를 추가하지 않습니다. 원본이 입력값을 정하지 않은 활동은 학생이 직접 입력하도록 둡니다.

## 학생용 문구와 조판

학생용 본문에는 기준 교재의 대조·출처 쪽수·과거 실습 번호·제작 과정·PDF 안내를 넣지 않습니다. 이미지 캡션은 보이는 입력과 동작·결과를 설명합니다. 오류 정정 고지는 정확한 개념 설명으로 바꿉니다. 출처와 수정 근거는 practice-source-review.md, practice-source-map.json, source-audit.md에서 관리합니다. AI 답변의 근거 확인처럼 학습에 필요한 자료 비교 활동은 유지합니다.

본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt와 현재 이미지 픽셀·출력 폭·비율을 유지합니다. 흰 배경·선명한 글자와 도형·둥근 실습 상자를 사용하고 삼육보건대 로고를 넣지 않습니다. 연속된 짧은 설명·표·완료 확인을 읽는 순서대로 함께 배치합니다. 차시 시작 아래에 충분한 공간이 있으면 다음 개념을 함께 놓습니다. 대형 빈 기록칸과 반복 안내를 자동으로 추가하지 않습니다.

## 생성과 검증

현재 학생용 PDF는 output/pdf/{PDF.name}, A4 {current_pages}쪽입니다. 원고·metadata의 차시 번호와 예제 파일 이름을 함께 유지합니다. Node 앱 파서·Python 패키지·필요 글꼴을 준비한 뒤 저장소 루트에서 실행합니다.

```powershell
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/{PDF.name}
python scripts/review_textbook_pdf.py --pdf output/pdf/{PDF.name} --dest tmp/pdfs/apps-review
python scripts/report_apps_edition.py
```

보고 스크립트는 조판과 전체 렌더링 검증 이후에 실행합니다. 이전 학생판과의 비교 기준은 previous-reports/20261011-before-no-robot입니다. PDF 글꼴은 Wanted Sans·학교안심 칠판지우개·Windows Consolas입니다. Canva 제작은 skill/coala-canva-textbook/SKILL.md와 flowchart-canva.md를 참고하고, 현재 독립 PDF의 쪽수와 Canva 자동 생성 쪽수를 구분합니다.
""")

write("canva-production-status.md", f"""# 제작 상태 · 앱 개발 16차시 · {DATE}

[현재 학생용 완성본](../../output/pdf/{PDF.name})은 A4 {current_pages}쪽의 독립 PDF입니다. 이전 학생판 {previous_pages}쪽에서 과정 개편과 지면 통합을 반영했습니다. 16차시·41실습·12코드·31곳 이미지 배치·4순서도를 포함합니다.

12차시는 직접 입력 Chart, 13차시는 자료·API·저장, 14차시는 Matplotlib, 15차시는 Pandas, 16차시는 자율 프로젝트입니다. 코코봇 장비 실습과 이미지 3개는 제외했습니다. 학생용 본문의 출처·제작 메모는 관리 문서로 분리했습니다.

사용자가 승인한 독립 PDF 제작 방식입니다. Canva 디자인 자체를 이 개편본으로 다시 생성한 것은 아닙니다. Canva 제작 절차는 notes.md와 flowchart-canva.md를 참고합니다. 이전 학생판과 제외한 자료는 previous-reports/20261011-before-no-robot에 보관했습니다.
""")

write("validation-summary.md", f"""# 검증 결과 · 앱 개발 16차시 · {DATE}

현재 학생용 PDF는 A4 {current_pages}쪽입니다. book.md와 ch01.md-ch16.md 총 17개 파일이 파서·레이아웃 검사에 통과했습니다. 원고 컨테이너 170개, Canva 앱 추정 {canva_pages}장입니다.

- 16차시·41개 실습 카드·4개 벡터 순서도 유지.
- 12차시 3실습, 13차시 4실습, 14차시 8실습, 15차시 3실습, 16차시 1실습.
- 코드 12개와 출력 유지. 이전 실행본의 코드 SHA-256과 일치, 출력 코드 내용 차이 0.
- 이미지 파일 30개·배치 31곳. 이전 학생판의 비코코봇 이미지와 픽셀·출력 폭·비율 일치.
- {current_pages}쪽 전체 렌더링. 글자·상자 넘침, 원고 ID 누락, 목차 오류, 대체 문자 0.
- 학생용 본문의 코코봇·기준 교재 대조·PDF 안내 문구 노출 0.
- 목차 링크 16개·차시 책갈피 16개·주요 글꼴 포함 확인.

검사 상세는 validation-full.json, code-results.json과 output/pdf/{qa_path.name}에 있습니다. 코드·GUI·외부 API를 새로 실행한 변경은 없습니다. 실행 코드의 동일성과 현재 PDF 출력·지면·내용 보존을 검증했습니다.
""")

write("pdf-final-review.md", f"""# 독립 PDF 검토 · 앱 개발 16차시 학생용 완성본 · {DATE}

[현재 완성 PDF](../../output/pdf/{PDF.name})는 A4 {current_pages}쪽입니다. 이전 학생판은 {previous_pages}쪽이며, 지면 대응은 page-compaction-review.md에 기록했습니다.

## 과정과 내용

코코봇 차시를 제외하고 12차시의 Chart 활동을 직접 입력과 자료 활용으로 나눴습니다. Matplotlib는 14차시, Pandas는 15차시로 이동했고 16차시는 자율 프로젝트입니다. 170개 원고 컨테이너·41개 실습 카드·12개 코드·4개 순서도를 포함합니다.

이미지 파일 30개를 31곳에 배치했습니다. 남은 이미지의 픽셀·출력 폭·비율은 이전 학생판과 같고, 실행 코드와 출력도 변경하지 않았습니다. 학생용 본문에는 원본 대조·출처 쪽수·오류 수정 고지·제작 과정·PDF 안내를 넣지 않습니다.

## 조판과 검증

본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt를 유지했습니다. Wanted Sans·Consolas·학교안심 칠판지우개 글꼴을 PDF에 포함했습니다. 흰 배경·벡터 글자와 도형·둥근 실습 상자를 사용하고, 연속된 짧은 개념·표·완료 확인을 함께 배치합니다.

{current_pages}쪽을 모두 렌더링했습니다. 자동 검사에서 글자·상자 넘침·원고 ID 누락·목차 오류·대체 문자·코드 내용 차이는 0입니다. 코코봇·기준 교재 대조·PDF 메타 언급은 학생용 본문에서 0입니다. 목차 링크·책갈피 각각 16개와 주요 글꼴 포함을 확인했습니다.

## 제작 범위

사용자가 승인한 독립 PDF 배치입니다. 원본 캡처의 낮은 해상도를 복원했다거나 GUI·외부 API를 새로 실행했다고 주장하지 않습니다. 출처와 이전 대조 기록은 관리 문서에 보관하며, 이전 학생판과 제외한 차시는 previous-reports/20261011-before-no-robot에 있습니다.
""")

handover = f"""# 앱 개발 16차시 학생용 완성본 인계 · {DATE}

- 학생용 PDF: output/pdf/{PDF.name}, A4 {current_pages}쪽.
- 원고: book.md 및 ch01.md-ch16.md, 컨테이너 170개·16차시.
- 실습: 41개 카드. 12차시 직접 입력 Chart, 13차시 자료·API·저장.
- 14차시 Matplotlib·15차시 Pandas·16차시 자율 프로젝트.
- 실행 코드: examples/source-based의 Python 12개. 데이터·코드·출력 유지.
- 이미지: assets/source-20261006 및 source-20261010의 현재 파일 30개·배치 31곳.
- 순서도: 독립 벡터 4개.
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

현재 본문의 출처 쪽수·과거 실습 번호·제작 과정·원본 오류 고지는 제거했고 정확한 개념과 실습 동작 설명으로 정리했습니다. 출처 대응은 practice-source-map.json 및 practice-source-review.md에 있습니다. 임의 고정 입력값·가상 AI 응답·새 앱 예시는 추가하지 않습니다.

## 포함한 내용의 수정 근거
{corrections}

## 코드와 이미지 검증

Matplotlib 7개·Pandas 5개 코드는 이전 실제 실행본과 SHA-256이 같습니다. 출력 데이터도 유지했고 차시 번호와 파일 이름만 새 구조에 맞췄습니다. 실행 환경과 결과는 code-results.json에 보존했습니다. 이번 과정 개편에서 GUI·외부 API를 새로 실행했다고 주장하지 않습니다.

현재 이미지 30개는 원본 캡처 22개·실행 그래프 7개·실행 표 1개입니다. 이전 학생판의 비코코봇 이미지와 원본 픽셀·출력 폭·비율이 일치합니다. 작은 UI 캡처의 선명도를 복원했다고 주장하지 않습니다. PDF의 종이 배경·기관 로고·그림자를 전체 이미지로 붙이지 않습니다.
""")

practice_rows = ["| 차시 | 현재 실습 | 제작 관리용 출처 쪽 | 원본 실습·예시 |", "|---|---|---|---|"]
for item in catalog:
    practice_rows.append(f"| {item['chapter']} | {item['practice_id']} {item['title']} | {item['source_pdf_pages']} | {item['source_label']} |")
write("practice-source-review.md", f"""# 제작 관리용 실습 대응 기록 · {DATE}

현재 교재는 16차시·41개 실습 카드입니다. 아래 출처 대응은 제작 관리용이며 학생용 본문에 표시하지 않습니다. 원본 과제·데이터·위젯·결과를 유지했고 출처 소개·과거 번호·수정 고지는 본문에서 제외했습니다.

## 과정 개편

1-11차시는 유지했습니다. 12차시의 직접 입력 Chart 3개와 13차시의 자료·API·저장 4개를 분리했습니다. Matplotlib와 Pandas는 14·15차시로 이동했고 16차시는 자율 프로젝트입니다. 코코봇의 2개 실습과 관련 11개 원고 컨테이너·이미지 3개를 제외했습니다. 차시 수는 16개를 유지했습니다.

이전에 정리한 임의 입력값·가상 AI 응답·콘솔 대체 실습·추가 앱 과제는 다시 넣지 않았습니다. 원본이 값을 지정하지 않은 과제는 학생이 직접 입력합니다. 실행 코드 12개·출력·비코코봇 이미지는 이전 학생판과 같습니다.

원본의 메시지 창, 학생 100명 자료, 학교별 학생 수, 지하철역 API, Matplotlib 여덟 그래프 활동, mon-sun DataFrame을 유지했습니다. 계산기 실습은 두 숫자와 사칙연산 기호를 사용하는 계산기 2로 구성했습니다. API 입력 인증키가 보이는 캡처는 사용하지 않습니다.

## 실습별 대응표

{chr(10).join(practice_rows)}

GUI·API 실습의 새 실행을 주장하지 않습니다. 필요한 학생 자료·API 주소·인증 정보는 수업 환경에서 준비합니다. 과거 대조 기록과 제외한 내용은 previous-reports/20261011-before-no-robot에 보관했습니다.
""")

asset_rows = ["| 파일 | 출처 | 픽셀 크기 | 사용 원고 ID |", "|---|---|---|---|"]
asset_cards = []
for item in assets["items"]:
    source = f"원본 PDF {item['pdf_page']}쪽" if item["kind"] == "user-supplied-pdf-embedded-image" else "검증한 코드 실행 결과"
    used = item["used_in"] if isinstance(item["used_in"], list) else [item["used_in"]]
    asset_rows.append(f"| {item['src']} | {source} | {item['width']}×{item['height']} | {', '.join(used)} |")
    asset_cards.append(f'<article><h2>{html.escape(Path(item["src"]).name)}</h2><p>{html.escape(source)}</p><img src="{html.escape(item["src"])}" alt="{html.escape(source)}"><p>{item["width"]} × {item["height"]}</p></article>')
write("asset-audit.md", f"""# 제작 관리용 이미지 출처 · {DATE}

현재 사용 파일 30개·지면 배치 31곳입니다. 원본 캡처 22개, 실행 그래프 7개, 실행 표 1개를 사용합니다. 코코봇 이미지 3개를 제외했고 남은 이미지의 픽셀·출력 폭·비율은 이전 학생판과 같습니다. 이 출처 목록은 학생용 본문 밖에서 관리합니다.

{chr(10).join(asset_rows)}
""")
write("asset-review.html", '<!doctype html><html lang="ko"><meta charset="utf-8"><title>현재 교재 이미지 30개</title><style>body{font-family:Malgun Gothic,sans-serif;margin:32px;background:white}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}article{border:1px solid #ccc;padding:16px}img{max-width:100%;height:auto}h2{font-size:18px}</style><h1>앱 개발 16차시 이미지 30개</h1><p>' + DATE + ' · 제작 관리용 원본 캡처·실행 결과 미리보기</p><main>' + ''.join(asset_cards) + '</main></html>')

write("apps-edition-review.md", f"""# 앱 개발 16차시 개편 검토 · {DATE}

현재 [학생용 PDF](../../output/pdf/{PDF.name})는 A4 {current_pages}쪽입니다. 이전 학생판 {previous_pages}쪽을 기준으로 코코봇을 제외하고 앱·데이터 과정으로 재구성했습니다.

| 구분 | 이전 | 현재 |
|---|---|---|
| 차시 | 16 | 16 |
| 원고 컨테이너 | 179 | 170 |
| 실습 카드 | 43 | 41 |
| 실행 코드 | 12 | 12 |
| 이미지 파일·배치 | 33·34 | 30·31 |
| 순서도 | 4 | 4 |
| PDF 쪽 | {previous_pages} | {current_pages} |

12차시는 직접 입력 Chart, 13차시는 학생 자료·API·저장, 14차시는 Matplotlib, 15차시는 Pandas, 16차시는 자율 프로젝트입니다. 기존 코코봇 차시의 11개 원고 컨테이너·실습 2개·이미지 3개를 제외했고 새 13차시 시작과 12차시 완료 확인을 추가했습니다.

실행 코드·출력과 남은 이미지의 픽셀·출력 폭·비율을 보존했습니다. 학생용 본문의 코코봇·기준 교재 대조·PDF 메타 언급 0, 코드 차이·원고 ID 누락·지면 넘침·목차 오류 0입니다. 목차 링크·책갈피 각각 16개와 주요 글꼴 포함을 확인했습니다.

원고 ID 개편 기록은 page-restructure.json, 이전 PDF 지면 대응은 page-compaction-review.md, 상세 자동 검증은 output/pdf/{qa_path.name}에 있습니다. 이전 자료와 제외한 내용은 previous-reports/20261011-before-no-robot에 보관했습니다.
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
members.update((BOOK / "examples/source-based").glob("*"))
members.add(BOOK / "examples/README.md")
with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(members):
        if path.is_file():
            archive.write(path, "vibe-coding-16/" + path.relative_to(BOOK).as_posix())
    for path in (PDF, PDF.with_suffix(".json"), qa_path):
        archive.write(path, "output/pdf/" + path.name)
    for name in ("build_textbook_pdf.py", "finalize_textbook_pdf.py", "review_textbook_pdf.py", "report_apps_edition.py"):
        archive.write(ROOT / "scripts" / name, "scripts/" + name)
    archive.writestr("START-HERE.txt", f"""{DATE} 앱 개발 16차시 학생용 완성본

완성 PDF: output/pdf/{PDF.name} (A4 {current_pages}쪽)
원고: vibe-coding-16/book.md 및 ch01.md-ch16.md
과정: 12 직접 입력 Chart / 13 자료·API·저장 / 14 Matplotlib / 15 Pandas / 16 자율 프로젝트
코드: vibe-coding-16/examples/source-based (Python 12개)
이미지: vibe-coding-16/assets (현재 사용 30개)
검증: output/pdf/{qa_path.name}
구성 안내: vibe-coding-16/curriculum.md

PDF는 바로 열 수 있습니다. 저장소에서 수정하려면 vibe-coding-16 폴더를
coala-book-md/vibe-coding-16에 복사하고 output, scripts도 저장소에 복사합니다.
PDF 재생성에는 Node 앱 파서·Python 패키지·필요 글꼴을 준비합니다.
절차는 vibe-coding-16/notes.md에서 확인합니다.

학생용 교재와 별도로 포함한 출처·검증 기록은 제작 관리용입니다.
이 묶음에는 이전 PDF와 제외한 코코봇 이미지·실습을 넣지 않았습니다.
""")

with zipfile.ZipFile(bundle) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    packaged_pdfs = [name for name in names if name.endswith(".pdf")]
    assert packaged_pdfs == ["output/pdf/" + PDF.name], packaged_pdfs
    assert not any(is_robot_asset(name) for name in names)
    assert sum(name.startswith("vibe-coding-16/assets/") for name in names) == 30
    assert sum(name.startswith("vibe-coding-16/examples/source-based/") and name.endswith(".py") for name in names) == 12
    assert sum(name.startswith("vibe-coding-16/ch") and name.endswith(".md") for name in names) == 16
    packaged_hash = digest(archive.read("output/pdf/" + PDF.name))
    assert packaged_hash == metadata["pdfSha256"] == qa["pdfSha256"]
    assert json.loads(archive.read("output/pdf/" + PDF.stem + ".json"))["pdfSha256"] == packaged_hash
    assert json.loads(archive.read("output/pdf/" + qa_path.name))["pdfSha256"] == packaged_hash
    assert digest(archive.read("vibe-coding-16/book.md")) == metadata["manuscriptSha256"]

print(json.dumps({"pages": current_pages, "previous_pages": previous_pages,
                  "manuscript_containers": 170, "practice_cards": 41,
                  "code_blocks": 12, "assets": 30, "images": 31, "flowcharts": 4,
                  "bookmarks": 16, "contents_links": contents_links,
                  "pdf_sha256": packaged_hash, "code_hashes_unchanged": True,
                  "image_sizes_unchanged": True, "bundle_bytes": bundle.stat().st_size},
                 ensure_ascii=False))
