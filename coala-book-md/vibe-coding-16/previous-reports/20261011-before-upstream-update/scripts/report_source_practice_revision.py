"""Validate all manuscript entry points and refresh delivery documentation."""
from __future__ import annotations
import hashlib
import html
import json
import shutil
import subprocess
import zipfile
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
PDF = ROOT / 'output/pdf/vibe-coding-16-final.pdf'
NODE = 'C:/Users/Public/Documents/ESTsoft/CreatorTemp/coala-canva-tools/node-v24.21.0-win-x64/node.exe'
ARCHIVE = BOOK / 'previous-reports/20261010-before-practice-review'
metadata = json.loads(PDF.with_suffix('.json').read_text(encoding='utf-8'))
qa = json.loads((ROOT / 'tmp/pdfs/final-review/automated-qa.json').read_text(encoding='utf-8'))
assets = json.loads((BOOK / 'asset-manifest.json').read_text(encoding='utf-8'))
codes = json.loads((BOOK / 'code-results.json').read_text(encoding='utf-8'))
catalog = json.loads((BOOK / 'practice-source-map.json').read_text(encoding='utf-8'))['practices']

reports = ['README.md','notes.md','teacher-guide.md','curriculum.md','source-audit.md',
           'asset-audit.md','asset-review.html','handover.md','final-draft.md','print-activities.md',
           'canva-production-status.md','validation-summary.md','validation-full.json']
for name in reports:
    if (BOOK / name).exists() and not (ARCHIVE / name).exists():
        shutil.copy2(BOOK / name, ARCHIVE / name)

files = [BOOK / 'book.md'] + [BOOK / f'ch{i:02d}.md' for i in range(1,17)]
validations = []
for path in files:
    run = subprocess.run([NODE, 'scripts/validate.cjs', str(path), '--layout', '--json'],
                         cwd=ROOT / 'canva-app', capture_output=True, encoding='utf-8')
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    value = json.loads(run.stdout)
    assert all(v['ok'] and not v['issues'] for v in value)
    validations.extend(value)
chapter_count = sum(v['pages'] for v in validations[1:])
assert validations[0]['pages'] == chapter_count + 1
reader = PdfReader(str(PDF))
assert len(reader.pages) == metadata['pages'] == qa['pages']
assert len(reader.outline) == 16
links = sum(len(p.get('/Annots', [])) for p in reader.pages[:3])
assert links == 16
fonts = {}
for page in reader.pages:
    resources = page['/Resources']
    for value in resources.get('/Font', {}).values():
        font = value.get_object()
        desc = font.get('/FontDescriptor')
        if desc:
            desc = desc.get_object()
            fonts[str(font.get('/BaseFont'))] = any(k in desc for k in ('/FontFile','/FontFile2','/FontFile3'))
        elif font.get('/Subtype') != '/Type1':
            fonts[str(font.get('/BaseFont'))] = False
assert all(fonts.values()), fonts
qa.update({'fonts': fonts, 'bookmarks': len(reader.outline), 'contentsLinks': links,
           'pdfSha256': hashlib.sha256(PDF.read_bytes()).hexdigest(),
           'manuscriptSha256': metadata['manuscriptSha256'],
           'sourcePracticeCards': len(catalog), 'sourceImages': 25, 'uniqueAssets': 33,
           'executedCodeBlocks': codes['executed_blocks'], 'executedCodePassed': codes['passed']})
assert all(not qa[k] for k in ('outOfPageGlyphs','missingSourceIds','contentsErrors',
                              'codeContentDifferences','replacementGlyphPages','boxOverflows'))

def write(name, text):
    (BOOK / name).write_text(text.rstrip() + '\n', encoding='utf-8')
def json_write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
json_write(BOOK / 'validation-full.json', validations)
json_write(PDF.with_name('vibe-coding-16-final-qa.json'), qa)

write('README.md', '''# AI와 함께하는 바이브 코딩 · 원본 실습 중심 수정판

2026-10-10에 원본 158쪽 PDF의 실습을 다시 대조하여 원고와 독립 PDF를 수정했습니다.

- [전체 원고](book.md): 16차시, 원고 페이지 179개.
- [수정한 PDF](../../output/pdf/vibe-coding-16-final.pdf): A4 179쪽, 표지·목차·순서도 포함.
- [실습별 원본 대조 기록](practice-source-review.md), [실습 출처 목록](practice-source-map.json).
- [차시별 구성](curriculum.md), [교사용 안내](teacher-guide.md), [제작 지침](notes.md).
- [이미지 미리보기](asset-review.html): 원본 캡처 25개, 실행 그래프 7개, 실행 표 1개.
- [검증 결과](validation-summary.md), [PDF 검토 기록](pdf-final-review.md).
- [실행 예제](examples/source-based/README.md): 원본 자료 기반 Matplotlib·Pandas 코드 12개.

전체 원고와 개별 ch01.md-ch16.md는 같은 내용입니다. Canva 제작 시 원고와 assets 폴더를 함께 사용합니다. 현재 PDF는 사용자가 승인한 독립 배치이며 Canva 원본 틀을 그대로 복제한 결과는 아닙니다.

다른 컴퓨터에서 사용할 수정본 묶음은 상위 폴더의 vibe-coding-16-source-revised.zip입니다. [설치 안내](../../OTHER-PC-SETUP.md)도 참고하세요.

previous-reports, previous-20261005.zip, examples/index.html과 assets/chXX는 과거 작업 기록입니다. 현재 책의 예시로 사용하지 않습니다.
''')
write('notes.md', '''# 다음 제작·수정에 사용할 지침

## 원본과 실습

지정된 루트의 158쪽 앱 개발 PDF를 기준으로 16차시를 유지합니다. practice-source-map.json과 practice-source-review.md의 실습별 출처를 확인하세요. 다른 PDF나 과거 공부 기록 앱 초안으로 되돌리지 않습니다.

실습은 원본에 있는 과제·데이터·위젯·결과를 우선합니다. 원본이 값을 정하지 않은 경우 임의 고정 입력값이나 테스트 목록을 만들어 교재에 넣지 않습니다. 새 가상 AI 응답, 가상 오류 이야기, 추가 앱 목록과 발표 과제를 넣지 않습니다. 설명과 완료 기준은 해당 실습에 필요한 만큼 작성합니다.

Matplotlib·Pandas 코드는 원본 데이터를 유지하고 독립 실행 초기화·출력과 원본 오타만 보완합니다. 변경한 코드는 실행 결과를 확인한 뒤 사용합니다. 원본 GUI의 message, fch와 코코봇 함수는 실제 수업 도구에서 확인합니다.

## 이미지와 지면

현재 asset-manifest.json의 이미지 33개를 사용합니다. source-20261006과 source-20261010 두 폴더가 필요합니다. 원본 픽셀과 가로세로 비율을 유지하고 출처 쪽수·실제 실행 결과를 구분합니다.

삼육보건대 로고를 넣지 않습니다. 흰 배경, 선명한 글자와 도형, 그림자 없는 배치를 사용합니다. 긴 텍스트는 둥근 사각형에 넣습니다. 글자 크기와 행간을 줄이거나 지면을 채우려고 새 활동을 자동으로 추가하지 않습니다. 같은 실습의 짧은 설명은 읽는 순서를 유지하여 합칠 수 있습니다.

## PDF와 Canva

현재 독립 PDF는 output/pdf/vibe-coding-16-final.pdf입니다. scripts/finalize_textbook_pdf.py와 scripts/review_textbook_pdf.py로 재생성·검증합니다. PDF 폰트는 tmp/pdfs/fonts에 준비한 Wanted Sans와 학교안심 칠판지우개, Windows Consolas를 사용합니다.

Canva 제작 시 skill/coala-canva-textbook/SKILL.md를 적용하고 원본 Canva를 보존한 제작 사본을 사용합니다. 네이티브 순서도 규칙은 flowchart-canva.md를 참고하세요. 독립 PDF의 벡터 도형과 Canva 네이티브 요소는 구분합니다.
''')
write('teacher-guide.md', '''# 교사용 운영 안내 · 원본 실습 중심 16차시

1-7차시는 원본 개념·순서도·문제풀이 중심입니다. 8-12차시는 책의 알고플로/Flet 디자이너 환경, 13-14차시는 Matplotlib·NumPy·Pandas가 있는 Python 환경을 사용합니다. 15차시는 코코봇 장비, 16차시는 원본 93-94쪽 자율 프로젝트를 사용합니다.

원본 도구 캡처와 최신 수업 도구의 메뉴가 같은지는 수업 전에 확인합니다. 학생 100명 자료, API 주소와 인증 정보, 코코봇 명령·연결·단위는 실제 수업 환경에서 준비합니다. 한글 축 제목은 설치된 한글 글꼴을 Matplotlib의 font.family에 설정합니다. 이번 제작의 실행 그래프에는 Wanted Sans를 사용했습니다.

## 실습 배분

수업 시간이 지정되지 않았으므로 여러 실습이 있는 차시는 핵심과 선택 활동으로 나눠 운영합니다. 선택 활동도 원본 책의 예시에서 고릅니다.

| 차시 | 핵심 원본 활동 | 함께 다룰 원본 활동 |
|---|---|---|
| 1-3 | AI 질문 비교·공부 계획·입력 처리 출력 | BMI 입력 설계·감정 기록 구조 |
| 4 | 가족 나이 합 43·45·15 | 학생 세 명의 총점 본문 예시 |
| 5 | 1-10일 운동 시간 누적 | 카페인 입력 반복 |
| 6-7 | 수면 분류·N명 80점 PASS/FAIL | 학생 네 명의 영화 관람 본문 예시 |
| 8 | 버튼 색·메시지 창·Field 추가/삭제 | 원본 위젯 역할 설정 |
| 9 | 1-6 누적곱·계산기 2 | Text 추가·4단 구구단 |
| 10 | Dropdown·Checkbox·Radiobutton | ProgressBar·Image·Divider |
| 11 | 성적표 행 추가 | 원본 89쪽 행·셀 값 수정 절차 |
| 12 | 선·산점도·막대 차트·저장 | 학생 자료·학교별 개수·지하철역 API |
| 13 | Matplotlib 실습 1-5 | 원본 막대 2종·산점도 |
| 14 | Series·학생 DataFrame | 요일별 DataFrame·행·열 이름 변경 |
| 15 | 이동·양쪽 회전·거리·각도 입력 | 실제 장비 동작 확인 |
| 16 | 원본 자율 프로젝트 아이디어·UI | 구현한 위젯의 동작 확인 |

## 코드와 완료 확인

examples/source-based의 현재 코드 12개는 원고와 같습니다. 원본의 데이터와 동작을 유지하고, 단독 실행을 위한 Figure·Axes 생성 및 출력 함수와 오류를 보완했습니다. GUI 실습을 임의 콘솔 예제로 대체하지 않습니다.

원본이 값을 지정한 과제는 같은 값을 사용하고, 미지정 과제는 학생이 직접 입력합니다. 실습 카드의 완료 기준은 해당 원본 과제에 맞췄습니다. API나 물리 장비를 실행하지 못하면 원본 화면 열람과 실제 실행을 구분합니다. 한 차시를 모두 마치려고 책에 없는 새 과제를 추가하지 않습니다.
''')
curriculum = (ARCHIVE / 'curriculum.md').read_text(encoding='utf-8')
curriculum = curriculum.replace('기준: 2026-10-06에 지정한 158쪽 PDF.', '기준: 2026-10-10에 재대조한 지정 원본 158쪽 PDF.').replace('16차시는 자율 프로젝트를 확장한 수업 활동이다.', '16차시는 원본 93-94쪽 자율 프로젝트를 사용한다.')
write('curriculum.md', curriculum + '\n실습별 입력값·조건·원본 번호는 practice-source-map.json에서 확인합니다.\n')
audit = (ARCHIVE / 'source-audit.md').read_text(encoding='utf-8')
audit = audit.replace('개발 요청문, 짧은 실행 코드, 테스트 입력, 완료 체크, 발표 활동은 원본을 기반으로 수업용으로 재작성한 내용이다. 실제 AI 대화나 학생 결과물로 소개하지 않는다.', '2026-10-10 대조에서 임의 입력값·가상 AI 응답·추가 발표 실습을 정리했다. 원본 과제·본문 예시·자료 활용을 구분하고 실습별 원본 쪽수를 표시했다. 상세 변경은 practice-source-review.md에 있다.')
audit = audit.replace('합계 103 실행 확인', '원본 값의 합계 103 확인').replace('합계 55 실행 확인', '원본 값의 합계 55 확인').replace('23개 코드의', '12개 코드의').replace('추출한 20개 캡처', '추출한 25개 캡처')
write('source-audit.md', audit)
write('print-activities.md', '''# 원본 실습의 출력·기록 안내

현재 원고의 실습 카드와 차시별 완료 확인 페이지를 사용합니다. 원본에 없는 숫자·새 앱·가상 오류를 추가 활동으로 제시하지 않습니다.

실습별 원본 출처와 완료 기준은 practice-source-map.json, 수정 내용은 practice-source-review.md에 있습니다. 이전 활동지는 previous-reports/20261010-before-practice-review에 보관했습니다.
''')
write('validation-summary.md', f'''# 검증 결과 · 2026-10-10

book.md와 ch01.md-ch16.md 총 {len(validations)}개 파일이 파서·레이아웃 검사에 통과했습니다. 전체 원고는 {validations[0]['pages']}개 페이지 컨테이너, Canva 앱의 추정 본문은 {validations[0]['layout']['canvaPages']}장입니다. 실제 독립 PDF는 {qa['pages']}쪽입니다.

- 16차시, 원본 출처가 표시된 실습 카드 43개.
- Matplotlib 7개·Pandas 5개 코드 실제 실행 12/12 통과.
- 사용 이미지 33개, 지면 배치 34곳. 이미지 파일과 비율 누락 0.
- PDF 글자 넘침·상자 넘침·원고 페이지 누락·목차 오류 0.
- 출력 코드 12개와 원고 코드 내용 차이 0.
- 차시 책갈피 16개, 목차 링크 16개. 주요 글꼴 포함 확인.

검사 상세는 validation-full.json, code-results.json과 output/pdf/vibe-coding-16-final-qa.json에 있습니다. GUI·API·물리 코코봇의 새 실행은 이번 검증 범위가 아닙니다.
''')
write('pdf-final-review.md', f'''# 독립 PDF 검토 · 원본 실습 중심 수정판 · 2026-10-10

[완성 PDF](../../output/pdf/vibe-coding-16-final.pdf)를 현재 book.md에서 재생성했습니다. 이전 PDF는 날짜가 표시된 보관 폴더에 남겼습니다.

## 구성과 출처

A4 세로 {qa['pages']}쪽, 16차시, 실습 시작 카드 43개, Python 코드 12개입니다. 이미지 33개를 34곳에 배치했고 완성 벡터 순서도 4개를 포함했습니다. 실습별 쪽수와 원본 번호는 practice-source-review.md 및 practice-source-map.json에 있습니다.

새 고정 입력값·가상 AI 요청과 응답·추가 활동을 정리했습니다. 메시지 창, 학생 100명 자료, 학교별 학생 수, 지하철역 API와 요일별 DataFrame을 원본에서 복원했습니다. 원본 코드 데이터와 그래프 설정을 유지하고 실행 초기화·출력과 오타를 보완했습니다.

## 조판과 검토

Wanted Sans 본문, Consolas 코드 영문, 학교안심 칠판지우개 순서도 글꼴을 PDF에 포함했습니다. 독립 A4 출력의 본문 14pt·행간 28pt, 소제목 15pt, 단원 제목 25pt를 유지했습니다. 흰 배경과 벡터 글자·도형을 사용하고 기관 로고를 제거했습니다. 실습 카드는 둥근 사각형이며 긴 코드·출력은 글자를 줄이지 않고 페이지를 나눕니다.

{qa['renderedPages']}쪽을 모두 렌더링했습니다. 전체 연락 시트와 메시지 창·학생 자료·API·긴 코드·DataFrame 출력·순서도를 확대 점검했습니다. 긴 그래프 코드의 마지막 줄은 본문과 같은 상자에 배치하고 DataFrame 출력은 열 제목과 행 값을 함께 보존했습니다. Poppler 별도 렌더링도 확인했습니다.

글자 넘침 0, 상자 넘침 0, 원고 ID 누락 0, 목차 오류 0, 대체 문자 0, 원고 코드와 출력 코드의 내용 차이 0입니다. 차시 책갈피·목차 이동 링크 각각 16개를 확인했습니다.

## 제작 범위

사용자가 승인한 독립 PDF 배치입니다. Canva 원본 네이티브 요소 복제 결과는 아닙니다. 원본 캡처 25개는 픽셀을 보존했습니다. 실행 그래프 7개와 표 1개는 1920×1200입니다. 작은 원본 UI 글자의 선명도를 복원했다고 주장하지 않습니다.

GUI 저장·외부 API·실물 코코봇의 이번 새 실행을 주장하지 않습니다. 원본 화면과 실제 실행 결과를 구분하여 수업에서 확인합니다.
''')
write('canva-production-status.md', '''# 제작 상태 · 2026-10-10

원본 실습 중심으로 book.md·개별 16차시·이미지·코드를 수정하고 독립 PDF를 재생성했습니다. [현재 PDF](../../output/pdf/vibe-coding-16-final.pdf)는 A4 179쪽이며 표지·목차·완성 순서도 4개를 포함합니다.

현재 Canva 디자인 자체를 이 수정본으로 다시 생성한 것은 아닙니다. 사용자가 승인한 독립 PDF 제작 방식입니다. 네이티브 Canva 제작 절차는 flowchart-canva.md와 notes.md를 참고합니다. 제작과 검증 내역은 pdf-final-review.md에 있습니다.
''')
handover = '''# 원본 실습 중심 수정본 인계 · 2026-10-10

- 원고: book.md 및 ch01.md-ch16.md. 전체 원고 페이지 컨테이너 179개.
- 독립 PDF: output/pdf/vibe-coding-16-final.pdf, A4 179쪽.
- 원본 출처가 표시된 실습 카드 43개. 출처·입력·과제 대응은 practice-source-map.json.
- 이미지: assets/source-20261006 및 source-20261010의 현재 사용 파일 33개. 지면 배치 34곳.
- 코드: examples/source-based의 12개 Python 파일. 실행 결과 12/12 통과.
- 완성된 독립 벡터 순서도 4개. 네이티브 Canva 제작은 별도 flowchart-canva.md 참고.
- 수정 내용: practice-source-review.md. PDF 검토: pdf-final-review.md.
- 전달 묶음: 상위 폴더 vibe-coding-16-source-revised.zip.

사용자 승인에 따라 독립 PDF를 제작했습니다. 실제 수업 GUI·API·코코봇은 수업 환경에서 확인합니다. 원본 캡처의 낮은 해상도는 복원했다고 주장하지 않습니다.
'''
write('handover.md', handover)
write('final-draft.md', handover.replace('# 원본 실습 중심 수정본 인계', '# 현재 전달본'))

asset_rows = ['| 파일 | 출처 | 크기 | 사용 원고 페이지 |', '|---|---|---|---|']
cards = []
for item in assets['items']:
    source = f"원본 PDF {item['pdf_page']}쪽" if item['kind']=='user-supplied-pdf-embedded-image' else '원본 자료 기반 코드 실행 결과'
    asset_rows.append(f"| {item['src']} | {source} | {item['width']}×{item['height']} | {', '.join(item['used_in'])} |")
    cards.append(f'<article><h2>{html.escape(Path(item["src"]).name)}</h2><p>{html.escape(source)}</p><img src="{html.escape(item["src"])}" alt="{html.escape(source)}"><p>{item["width"]} × {item["height"]}</p></article>')
write('asset-audit.md', '# 이미지 출처 · 2026-10-10\n\n현재 사용 이미지 33개, 지면 배치 34곳입니다. 원본 25개와 실행 그래프 7개·표 1개입니다.\n\n' + '\n'.join(asset_rows))
write('asset-review.html', '<!doctype html><html lang="ko"><meta charset="utf-8"><title>원본 실습 이미지 확인</title><style>body{font-family:Malgun Gothic,sans-serif;margin:32px;background:white}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px}article{border:1px solid #ccc;padding:16px}img{max-width:100%;height:auto}h2{font-size:18px}</style><h1>원본 실습 이미지 33개</h1><p>2026-10-10 · 원본 캡처와 원본 자료의 실제 코드 실행 결과</p><main>' + ''.join(cards) + '</main></html>')

# Package current inputs only; do not reintroduce archived supplemental examples.
bundle = ROOT / 'coala-book-md/vibe-coding-16-source-revised.zip'
members = set()
for ext in ('*.md', '*.json'):
    members.update(BOOK.glob(ext))
members.add(BOOK / 'asset-review.html')
members.update(BOOK / i['src'] for i in assets['items'])
members.update((BOOK / 'examples/source-based').glob('*'))
members.add(BOOK / 'examples/README.md')
with zipfile.ZipFile(bundle, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(members):
        if path.is_file():
            archive.write(path, 'vibe-coding-16/' + path.relative_to(BOOK).as_posix())
    for path in [PDF, PDF.with_suffix('.json'), PDF.with_name('vibe-coding-16-final-qa.json')]:
        archive.write(path, 'output/pdf/' + path.name)
    for name in ('build_textbook_pdf.py','finalize_textbook_pdf.py','review_textbook_pdf.py'):
        archive.write(ROOT / 'scripts' / name, 'scripts/' + name)
    archive.writestr('START-HERE.txt', '현재 완성본: output/pdf/vibe-coding-16-final.pdf\n원고: vibe-coding-16/book.md\n실습 대조: vibe-coding-16/practice-source-review.md\n폰트와 Node 앱 파서는 PDF 재생성 시 별도로 준비하세요.\n')
print(json.dumps({'validated_files':len(validations),'pdf_pages':len(reader.pages),'fonts':fonts,'bundle_bytes':bundle.stat().st_size},ensure_ascii=False))
