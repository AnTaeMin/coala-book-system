"""Record the 2026-10-11 page compaction and package current deliverables.

This script changes delivery reports and the ZIP only. It does not revise the
manuscript, examples, assets, or PDF renderer.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coala-book-md/vibe-coding-16"
PDF = ROOT / "output/pdf/vibe-coding-16-student.pdf"
ARCHIVE = BOOK / "previous-reports/20261011-before-page-compaction"
OLD_PDF = ARCHIVE / "vibe-coding-16-final.pdf"
REPORTS = ["README.md", "notes.md", "canva-production-status.md",
           "validation-summary.md", "pdf-final-review.md", "handover.md",
           "final-draft.md", "page-compaction-review.md"]


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(name: str, text: str):
    text = (text.replace("154쪽", f"{current_pages}쪽")
            .replace("25쪽", f"{saved_pages}쪽")
            .replace("179→154", f"{old_pages}→{current_pages}")
            .replace("Canva 앱 추정 185장", f"Canva 앱 추정 {canva_pages}장")
            .replace("vibe-coding-16-compact", PDF.stem)
            .replace("tmp/pdfs/compact-review", "tmp/pdfs/student-review"))
    text += ("\n\n학생용 본문에서는 원본 대조·출처 쪽수·제작 과정과 PDF 안내 문구를 "
             "제외했습니다. 실습 데이터·코드·출력·순서도는 유지했으며, "
             "출처와 제작 기록은 교재 밖의 관리 문서에 보관합니다.\n")
    (BOOK / name).write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def page_list(numbers):
    return ", ".join(str(n) for n in sorted(set(numbers)))


metadata = read_json(PDF.with_suffix(".json"))
old_metadata = read_json(OLD_PDF.with_suffix(".json"))
qa = read_json(ROOT / "tmp/pdfs/student-review/automated-qa.json")
assets = read_json(BOOK / "asset-manifest.json")
codes = read_json(BOOK / "code-results.json")
validations = read_json(BOOK / "validation-full.json")
practices = read_json(BOOK / "practice-source-map.json")["practices"]
current_pages = metadata["pages"]
old_pages = old_metadata["pages"]
saved_pages = old_pages - current_pages
canva_pages = validations[0]["layout"]["canvaPages"]

assert current_pages == qa["pages"] == qa["renderedPages"]
assert 0 < current_pages < old_pages
assert old_metadata["pages"] == 179
assert validations[0]["pages"] == 179 and len(validations) == 17
assert all(v["ok"] and not v["issues"] for v in validations)
assert len(practices) == metadata["pageTypes"]["practice-opening"] == 43
assert codes["executed_blocks"] == codes["passed"] == 12
assert len(assets["items"]) == 33
assert len(metadata["images"]) == qa["images"] == 34
assert qa["flowcharts"] == 4
for key in ("outOfPageGlyphs", "missingSourceIds", "contentsErrors",
            "codeContentDifferences", "replacementGlyphPages",
            "institutionLogoTextPages", "editorialReferencePages", "boxOverflows"):
    assert not qa[key], (key, qa[key])
assert qa["manuscriptCodeBlocks"] == qa["printedCodeBlocks"] == 12
assert metadata["manuscriptSha256"] == hashlib.sha256(
    (BOOK / "book.md").read_bytes()).hexdigest()
assert metadata["pdfSha256"] == hashlib.sha256(PDF.read_bytes()).hexdigest()

reader = PdfReader(str(PDF))
assert len(reader.pages) == current_pages
assert len(reader.outline) == 16
links = sum(len(page.get("/Annots", [])) for page in reader.pages[:3])
assert links == 16
fonts = {}
standard_fonts = set()
for page in reader.pages:
    for reference in page["/Resources"].get("/Font", {}).values():
        font = reference.get_object()
        candidates = [font]
        candidates.extend(v.get_object() for v in font.get("/DescendantFonts", []))
        for value in candidates:
            descriptor = value.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                embedded = any(key in descriptor for key in
                               ("/FontFile", "/FontFile2", "/FontFile3"))
                fonts[str(value.get("/BaseFont"))] = embedded
            elif value.get("/Subtype") == "/Type1":
                standard_fonts.add(str(value.get("/BaseFont")))
assert fonts and all(fonts.values()), fonts

# Preserve the actual image pixels and printed width; compaction must not shrink
# or stretch screenshots and graphs to gain space.
def image_signature(item):
    return (item["src"], tuple(item["pixels"]), item["printWidthPt"],
            item["effectiveDpi"])
assert sorted(map(image_signature, metadata["images"])) == sorted(
    map(image_signature, old_metadata["images"]))

old_pages_by_id = defaultdict(list)
new_pages_by_id = defaultdict(list)
spec = read_json(ROOT / "tmp/pdfs/book-spec.json")
executed_code_hashes = {item["page_id"]: item["code_sha256"]
                        for item in codes["records"]}
current_code_hashes = {}
for page in spec["pages"]:
    for section in page.get("sections", []):
        for code in re.findall(r"```python\s*\n(.*?)\n```",
                               section.get("content", ""), re.S):
            assert page["id"] not in current_code_hashes
            current_code_hashes[page["id"]] = hashlib.sha256(
                code.encode("utf-8")).hexdigest()
assert len(current_code_hashes) == 12
assert current_code_hashes == executed_code_hashes
titles = {page["id"]: page.get("title", page.get("chapterTitle", page["id"]))
          for page in spec["pages"]}
for number, page in enumerate(old_metadata["layout"], 1):
    for source_id in set([page["id"]] + page.get("includedSources", [])):
        old_pages_by_id[source_id].append(number)
        titles.setdefault(source_id, page["title"])
for number, page in enumerate(metadata["layout"], 1):
    for source_id in set([page["id"]] + page.get("includedSources", [])):
        new_pages_by_id[source_id].append(number)
assert all(source_id in new_pages_by_id for source_id in old_pages_by_id)
assert new_pages_by_id["ch01-ai"] == new_pages_by_id["ch01-limits"] == [6]

ARCHIVE.mkdir(parents=True, exist_ok=True)
for name in REPORTS:
    path = BOOK / name
    if path.exists() and not (ARCHIVE / name).exists():
        shutil.copy2(path, ARCHIVE / name)
bundle = ROOT / "coala-book-md/vibe-coding-16-source-revised.zip"
if bundle.exists() and not (ARCHIVE / bundle.name).exists():
    shutil.copy2(bundle, ARCHIVE / bundle.name)

qa.update({"date": "2026-10-11", "fonts": fonts,
           "standardPdfFonts": sorted(standard_fonts),
           "bookmarks": 16, "contentsLinks": links,
           "pdfSha256": metadata["pdfSha256"],
           "manuscriptSha256": metadata["manuscriptSha256"],
           "manuscriptContainers": 179, "previousPdfPages": old_pages,
           "savedPages": saved_pages, "sourcePracticeCards": 43,
           "sourceImages": 25, "uniqueAssets": 33,
           "imagePixelsAndPrintWidthUnchanged": True,
           "executedCodeBlocks": 12, "executedCodePassed": 12,
           "executedCodeHashesUnchanged": True,
           "codeHashes": current_code_hashes,
           "typography": {"bodyPt": 14, "bodyLeadingPt": 28,
                          "sectionHeadingPt": 15, "chapterTitlePt": 25},
           "pageMapping": [{"previousPage": number,
                            "sourceId": page["id"],
                            "currentPages": new_pages_by_id[page["id"]]}
                           for number, page in enumerate(old_metadata["layout"], 1)]})
write_json(PDF.with_name(PDF.stem + "-qa.json"), qa)

write("README.md", """# AI와 함께하는 바이브 코딩 · 학생용 완성본

2026-10-11에 학생용 문구를 정리하고 짧은 설명과 표·체크리스트를 같은 지면에 통합하여 PDF를 179쪽에서 154쪽으로 줄였습니다. 차시 시작 아래의 여유 공간에도 바로 이어지는 짧은 개념을 배치했습니다. 기존 6·7쪽은 새 6쪽에 함께 배치했습니다.

- [현재 완성 PDF](../../output/pdf/vibe-coding-16-compact.pdf): A4 154쪽.
- [전체 원고](book.md): 16차시, 원고 페이지 컨테이너 179개. 원고의 구분은 유지하고 PDF 조판에서 합칩니다.
- [페이지 통합 내역과 179→154 대응표](page-compaction-review.md).
- 제작 관리용 [실습 대조 기록](practice-source-review.md), [실습 출처 목록](practice-source-map.json).
- [차시별 구성](curriculum.md), [교사용 안내](teacher-guide.md), [제작 지침](notes.md).
- [이미지 미리보기](asset-review.html): 원본 캡처 25개, 실행 그래프 7개, 실행 표 1개.
- [검증 결과](validation-summary.md), [PDF 검토 기록](pdf-final-review.md).
- [실행 예제](examples/source-based/README.md): Matplotlib·Pandas 코드 12개.

43개 실습·12개 코드·34곳의 이미지 배치·4개 순서도를 보존했습니다. 본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt와 이미지 폭·비율을 유지했습니다. 원고 book.md와 ch01.md-ch16.md는 같은 내용입니다.

다른 컴퓨터로 옮길 때는 상위 폴더의 vibe-coding-16-source-revised.zip을 사용합니다. 묶음의 START-HERE.txt와 [설치 안내](../../OTHER-PC-SETUP.md)를 참고하세요.

현재 PDF는 사용자가 승인한 독립 배치입니다. Canva에서 원고를 생성할 경우 페이지 수는 다를 수 있습니다. 이전 179쪽 PDF와 previous-reports는 과거 제작 기록입니다.
""")

write("notes.md", """# 다음 제작·수정에 사용할 지침 · 2026-10-11

이 문서는 제작·검증을 위한 관리 지침입니다. 학생용 교재 본문에 넣지 않습니다.

## 원본과 실습

지정된 루트의 158쪽 앱 개발 PDF를 기준으로 16차시를 유지합니다. practice-source-map.json과 practice-source-review.md의 실습별 출처를 확인하세요.

원본에 있는 과제·데이터·위젯·결과를 우선합니다. 원본이 값을 정하지 않은 경우 임의 고정 입력값이나 테스트 목록을 넣지 않습니다. 가상 AI 응답·오류 이야기·추가 앱 목록·발표 과제를 넣지 않습니다. 설명과 완료 기준은 해당 실습에 필요한 만큼 작성합니다.

Matplotlib·Pandas 코드는 원본 데이터를 유지하고 독립 실행 초기화·출력과 원본 오타만 보완합니다. 변경한 코드는 실행 결과를 확인한 뒤 사용합니다. 원본 GUI의 message, fch와 코코봇 함수는 실제 수업 도구에서 확인합니다.

## 이미지와 지면 통합

asset-manifest.json의 현재 이미지 33개를 사용합니다. source-20261006과 source-20261010 두 폴더가 필요합니다. 원본 픽셀·가로세로 비율·현재 출력 폭을 유지합니다.

삼육보건대 로고를 넣지 않습니다. 흰 배경, 선명한 글자와 도형, 그림자 없는 배치를 사용합니다. 긴 텍스트는 둥근 사각형에 넣습니다. 본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt를 유지합니다.

같은 차시의 연속된 짧은 개념·표·실습 설명·완료 확인은 읽는 순서를 지켜 한 장에 합칩니다. 차시 시작 아래에 공간이 충분하면 다음 짧은 개념을 함께 배치합니다. 원고 컨테이너 179개는 보존하고 PDF 조판에서 통합합니다. 새로운 실습과 자동 대형 빈 기록칸을 추가하지 않습니다. 실습 카드·차시별 시작·순서도를 구분하고, 내용이 넘치면 글자를 줄이지 않고 페이지를 나눕니다.

현재 학생용 완성본은 A4 154쪽입니다. 기존 6·7쪽은 새 6쪽에 통합했습니다. 다른 대응은 page-compaction-review.md에서 확인합니다.

## PDF와 Canva

현재 PDF는 output/pdf/vibe-coding-16-compact.pdf입니다. 저장소 루트에서 다음 순서로 생성·검증합니다. 원고 파서와 필요한 폰트·Python 패키지를 먼저 준비합니다.

```powershell
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/vibe-coding-16-compact.pdf
python scripts/review_textbook_pdf.py --pdf output/pdf/vibe-coding-16-compact.pdf --dest tmp/pdfs/compact-review
python scripts/report_page_compaction.py
```

PDF 폰트는 tmp/pdfs/fonts의 Wanted Sans와 학교안심 칠판지우개, Windows Consolas를 사용합니다. 보고 스크립트는 원고와 예시를 변경하지 않으며, 이전 원본 실습 재작성 스크립트를 실행할 필요가 없습니다.

Canva 제작 시 skill/coala-canva-textbook/SKILL.md를 적용하고 제작 사본을 사용합니다. 네이티브 순서도 규칙은 flowchart-canva.md를 참고하세요. 현재 페이지 통합은 독립 PDF 조판에 적용되어 있습니다.
""")

write("canva-production-status.md", """# 제작 상태 · 2026-10-11

[현재 학생용 완성본](../../output/pdf/vibe-coding-16-compact.pdf)은 A4 154쪽의 독립 PDF입니다. 기존 179쪽에서 25쪽을 줄였고, 6·7쪽을 새 6쪽에 통합했습니다. 16차시·43실습·12코드·이미지 34곳·완성 순서도 4개를 보존했습니다.

본문 글자 크기·행간과 이미지 폭·비율을 유지하며 짧은 연속 내용·표·완료 확인을 함께 배치했습니다. 여유 있는 차시 시작 지면에도 다음 짧은 개념을 합쳤습니다. 자동 대형 빈 기록칸과 중복 코드 안내 제목·그래프 캡션을 정리했습니다.

현재 Canva 디자인 자체를 다시 생성한 것은 아닙니다. 사용자가 승인한 독립 PDF 제작 방식입니다. Canva 제작 절차는 flowchart-canva.md와 notes.md, 페이지 통합과 검증 내역은 page-compaction-review.md 및 pdf-final-review.md에 있습니다.

이전 179쪽 PDF는 previous-reports/20261011-before-page-compaction에 보관했습니다. 현재 전달본은 학생용 파일입니다.
""")

write("validation-summary.md", """# 검증 결과 · 2026-10-11

현재 완성 PDF는 A4 154쪽입니다. 이전 179쪽에서 25쪽을 줄였습니다. 학생용 원고의 제작 메모를 정리한 뒤 book.md와 ch01.md-ch16.md를 다시 검사했습니다.

- 파서·레이아웃 검사 통과 파일 17개. 전체 원고 컨테이너 179개, Canva 앱 추정 185장.
- 독립 PDF 전체 154쪽 렌더링. 글자 넘침·상자 넘침·원고 ID 누락·목차 오류·대체 문자·기관 로고 문구 0.
- 학생용 본문의 원본·PDF 언급 및 제작 메모 노출 0.
- 16차시·43실습·4순서도 유지. 차시 책갈피 16개·목차 링크 16개.
- 코드 12개 보존, 출력 코드와 원고 내용 차이 0. 이전 실행 코드의 SHA-256과 일치, 실제 실행 검증 12/12 통과.
- 이미지 파일 33개·배치 34곳 유지. 이전 PDF와 원본 픽셀·출력 폭 일치.
- 본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt 유지. 주요 글꼴 포함 확인.
- 기존 6·7쪽의 두 원고 ID를 새 6쪽에서 모두 확인.

검사 상세는 validation-full.json, code-results.json, output/pdf/vibe-coding-16-compact-qa.json에 있습니다. 코드·GUI·API·물리 코코봇을 새로 실행한 변경은 없습니다. 이번 검증은 학생용 문구 정리, 지면 통합과 PDF 출력 검증입니다.
""")

write("pdf-final-review.md", """# 독립 PDF 검토 · 학생용 완성본 · 2026-10-11

[현재 완성 PDF](../../output/pdf/vibe-coding-16-compact.pdf)는 A4 154쪽입니다. 이전 179쪽에서 25쪽을 줄였습니다. 요청한 기존 6·7쪽의 생성형 AI·바이브 코딩과 AI의 한계를 새 6쪽에 함께 배치했습니다.

## 보존한 내용

원고 컨테이너 179개와 16차시, 실습 카드 43개, Python 코드 12개를 보존했습니다. 이미지 33개를 34곳에 배치하고 벡터 순서도 4개를 유지했습니다. 실습 출처는 제작 관리용 practice-source-review.md와 practice-source-map.json에 보관합니다.

같은 차시의 짧은 개념·표·설명과 완료 체크리스트를 합쳤습니다. 차시 시작 지면에 공간이 충분하면 바로 다음 개념을 함께 배치했습니다. 중복 코드 안내 제목·그래프 캡션을 간결하게 정리하고 자동 대형 빈 기록칸을 제거했습니다. 실습 과제·데이터·코드·실행 출력은 유지했습니다. 전체 기존→현재 페이지 대응은 page-compaction-review.md에 있습니다.

## 조판과 검증

본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt를 유지했습니다. Wanted Sans, Consolas 코드 글꼴과 학교안심 칠판지우개 순서도 글꼴을 PDF에 포함했습니다. 흰 배경과 벡터 글자·도형, 둥근 실습 상자를 사용합니다. 원본 이미지의 픽셀·출력 폭·가로세로 비율은 이전 PDF와 같습니다.

154쪽을 모두 렌더링했습니다. 자동 검사에서 글자 넘침·상자 넘침·원고 ID 누락·목차 오류·대체 문자·기관 로고 문구·코드 내용 차이는 모두 0입니다. 학생용 본문의 원본·PDF 언급과 제작 메모 노출도 0입니다. 실행 코드 12개의 SHA-256이 이전 실행본과 같고, 목차 링크·차시 책갈피 각각 16개와 글꼴 포함을 확인했습니다.

## 제작 범위

사용자가 승인한 독립 PDF 배치입니다. 페이지 통합은 독립 PDF 조판에서 적용합니다. 원본 캡처의 해상도를 보존하며 작은 UI 글자의 화질을 복원했다고 주장하지 않습니다. GUI 저장·외부 API·실물 코코봇의 새 실행을 주장하지 않습니다.

이전 179쪽 PDF는 보존했고 현재 전달 파일은 학생용 파일입니다. 이전 PDF·안내 문서·ZIP은 previous-reports/20261011-before-page-compaction에 보관했습니다.
""")

handover = """# 학생용 완성본 인계 · 2026-10-11

- 현재 독립 PDF: output/pdf/vibe-coding-16-compact.pdf, A4 154쪽.
- 원고: book.md 및 ch01.md-ch16.md. 16차시·페이지 컨테이너 179개 보존.
- 실습: 실습 카드 43개. 제작 관리용 출처는 practice-source-map.json에 보관.
- 이미지: assets/source-20261006 및 source-20261010의 현재 파일 33개·배치 34곳.
- 코드: examples/source-based의 Python 12개. 기존 실제 실행 12/12 통과.
- 순서도: 독립 벡터 4개. Canva 제작은 flowchart-canva.md 참고.
- 통합 내역: page-compaction-review.md. PDF 검토: pdf-final-review.md.
- PDF 메타데이터·QA: output/pdf/vibe-coding-16-compact.json 및 vibe-coding-16-compact-qa.json.
- 전달 ZIP: 상위 폴더 vibe-coding-16-source-revised.zip.

기존 6·7쪽을 새 6쪽에 통합했습니다. 같은 차시의 짧은 연속 내용과 표·완료 확인을 합쳐 총 25쪽을 줄였습니다. 글자 크기·행간과 이미지 폭·비율을 유지했고 새 예시와 실습을 추가하지 않았습니다.

이전 179쪽 PDF는 보존했습니다. 현재 전달본은 학생용 파일입니다. 이전 PDF·안내 문서·ZIP은 previous-reports/20261011-before-page-compaction에 있습니다.

다른 컴퓨터에서는 ZIP 안 START-HERE.txt를 확인하세요. PDF는 바로 열 수 있습니다. 원고·이미지·코드를 수정할 경우 저장소의 coala-book-md/vibe-coding-16에 복사합니다.
"""
write("handover.md", handover)
write("final-draft.md", handover.replace("# 학생용 완성본 인계", "# 현재 전달본 · 학생용 완성본"))

merge_rows = ["| 이전 쪽 | 현재 쪽 | 함께 배치한 내용 |",
              "|---|---|---|"]
for page in metadata["layout"]:
    included = page.get("includedSources", [])
    if not included:
        continue
    before = sorted({n for source_id in included
                     for n in old_pages_by_id[source_id]})
    after = sorted({n for source_id in included
                    for n in new_pages_by_id[source_id]})
    title = " · ".join(titles[source_id] for source_id in included)
    merge_rows.append(f"| {page_list(before)} | {page_list(after)} | {title} |")

mapping_rows = ["| 이전 PDF 쪽 | 현재 PDF 쪽 | 원고 ID | 이전 지면 제목 |",
                "|---|---|---|---|"]
for number, page in enumerate(old_metadata["layout"], 1):
    title = page["title"].replace("|", "／")
    mapping_rows.append(f"| {number} | {page_list(new_pages_by_id[page['id']])} | "
                        f"{page['id']} | {title} |")
write("page-compaction-review.md", """# 페이지 통합 검토 · 2026-10-11

현재 [학생용 완성 PDF](../../output/pdf/vibe-coding-16-compact.pdf)는 A4 154쪽입니다. 기존 179쪽에서 25쪽을 줄였습니다. 요청한 **기존 6·7쪽 → 현재 6쪽** 통합을 반영했습니다.

## 통합 기준

같은 차시에서 연속되는 짧은 개념과 표, 실습 설명과 완료 체크리스트를 읽는 순서대로 합쳤습니다. 차시 시작 아래의 여유 공간에도 바로 다음 짧은 개념을 함께 배치했습니다. 중복 코드 안내 제목과 그래프 캡션을 간결하게 정리하고 자동 대형 빈 기록칸을 제거했습니다. 내용이 넘치는 경우 다음 장에 이어 배치합니다.

원고 179개 컨테이너·16차시·43실습·12코드·34곳의 이미지 배치·4순서도는 보존했습니다. 본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt와 이미지 픽셀·폭·비율도 유지했습니다. 원고를 합치거나 새 실습을 추가하지 않고 PDF 지면을 통합했습니다.

원고 ID 누락·코드 내용 차이·글자 및 상자 넘침·목차 오류는 0입니다. PDF 전체 154쪽 렌더링, 폰트 포함, 목차 링크 16개와 차시 책갈피 16개를 확인했습니다. 자세한 자동 검사 결과는 output/pdf/vibe-coding-16-compact-qa.json에 있습니다.

학생용 본문의 원본·PDF 언급과 제작 메모를 정리했습니다. 기존 실습 데이터와 실행 코드의 SHA-256은 유지했고 출처와 이전 대조 기록은 관리 문서에 보관합니다.

## 함께 배치한 원고

한 원고가 여러 장에 걸치는 경우 아래 표는 해당 원고의 현재 전체 쪽 범위를 표시합니다. 통합 조합 수와 절감 쪽수는 계속 페이지의 배치에 따라 다릅니다.

""" + "\n".join(merge_rows) + """

## 전체 179→154쪽 대응표

이전 각 물리 페이지를 같은 원고 ID의 현재 지면에 대응했습니다. 같은 원고의 본문과 계속 페이지는 현재 범위를 함께 표시합니다. 표지·목차도 포함합니다.

""" + "\n".join(mapping_rows))

# Include only active manuscript, assets, source examples and current PDF.
members = set()
for extension in ("*.md", "*.json"):
    members.update(BOOK.glob(extension))
members.add(BOOK / "asset-review.html")
members.update(BOOK / item["src"] for item in assets["items"])
members.update((BOOK / "examples/source-based").glob("*"))
members.add(BOOK / "examples/README.md")
with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(members):
        if path.is_file():
            archive.write(path, "vibe-coding-16/" + path.relative_to(BOOK).as_posix())
    for path in (PDF, PDF.with_suffix(".json"),
                 PDF.with_name(PDF.stem + "-qa.json")):
        archive.write(path, "output/pdf/" + path.name)
    for name in ("build_textbook_pdf.py", "finalize_textbook_pdf.py",
                 "review_textbook_pdf.py", "report_page_compaction.py",
                 "finalize_student_manuscript.py"):
        archive.write(ROOT / "scripts" / name, "scripts/" + name)
    archive.writestr("START-HERE.txt", f"""2026-10-11 학생용 완성본

현재 완성본: output/pdf/{PDF.name} (A4 {current_pages}쪽)
원고: vibe-coding-16/book.md 및 ch01.md-ch16.md
통합 내역과 쪽수 대응: vibe-coding-16/page-compaction-review.md
제작 관리용 실습 대조: vibe-coding-16/practice-source-review.md
이미지: vibe-coding-16/assets의 source-20261006, source-20261010
코드: vibe-coding-16/examples/source-based (Python 12개)
검증: output/pdf/{PDF.stem}-qa.json

PDF는 바로 열 수 있습니다. 저장소에서 수정하려면 vibe-coding-16 폴더를
coala-book-md/vibe-coding-16에 복사하고 output, scripts도 저장소에 복사합니다.
PDF 재생성에는 Node 앱 파서, Python 패키지와 필요한 글꼴을 준비합니다.
절차: vibe-coding-16/notes.md
이번 ZIP에는 이전 179쪽 final PDF와 과거 기록을 넣지 않았습니다.
학생용 교재 본문과 별도로 포함한 출처·검증 문서는 제작 관리용입니다.
""")

with zipfile.ZipFile(bundle) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert "output/pdf/" + PDF.name in names
    assert not any("vibe-coding-16-final.pdf" in name for name in names)
    assert not any("vibe-coding-16-compact.pdf" in name for name in names)
    packaged_hash = hashlib.sha256(archive.read("output/pdf/" + PDF.name)).hexdigest()
    assert packaged_hash == metadata["pdfSha256"] == qa["pdfSha256"]
    assert json.loads(archive.read("output/pdf/" + PDF.stem + ".json"))["pdfSha256"] == packaged_hash
    assert json.loads(archive.read("output/pdf/" + PDF.stem + "-qa.json"))["pdfSha256"] == packaged_hash
    assert sum(name.startswith("vibe-coding-16/assets/") for name in names) == 33
    assert sum(name.startswith("vibe-coding-16/examples/source-based/")
               and name.endswith(".py") for name in names) == 12
    assert sum(name.startswith("vibe-coding-16/ch") and name.endswith(".md")
               for name in names) == 16

print(json.dumps({"pages": current_pages, "previous_pages": old_pages, "saved_pages": saved_pages,
                  "bookmarks": 16, "contents_links": links, "fonts": fonts,
                  "mapping_rows": len(qa["pageMapping"]),
                  "pdf_sha256": packaged_hash,
                  "code_hashes_unchanged": True,
                  "bundle_bytes": bundle.stat().st_size}, ensure_ascii=False))
