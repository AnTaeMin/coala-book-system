"""Execute source examples, synchronize manuscripts, and record provenance."""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import shutil
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
AUDIT = ROOT / 'tmp/pdfs/source-practice-audit'
ARCHIVE = BOOK / 'previous-reports/20261010-before-practice-review'
recipe = json.loads((AUDIT / 'revision-recipe.json').read_text(encoding='utf-8'))
pages, order = recipe['pages'], recipe['order']

font = ROOT / 'tmp/pdfs/fonts/WantedSans-Regular.ttf'
font_manager.fontManager.addfont(str(font))
plt.rcParams['font.family'] = font_manager.FontProperties(fname=str(font)).get_name()
plt.rcParams['axes.unicode_minus'] = False

# Keep editorial comparisons in the review report, outside student activities.
replacements = {
    ' 새 AI 응답이나 가상 오류 상황은 넣지 않았습니다.': '',
    ' 그림으로 표현한 동작을 짧은 코드와 연결합니다.': ' 선언·입력·처리·출력의 순서로 정리합니다.',
    ' 50·30·0 같은 새 고정 입력 예시는 사용하지 않습니다.': '',
    ' 88에서 89로 바꾸는 별도 과제는 사용하지 않습니다.': '',
    ' 새로운 앱 제작 요청이나 미리 작성된 AI 답변을 비교 대상으로 삼지 않습니다.': '',
    '원본 자료를 수업 환경에서 제공받아 사용합니다. 새 가상 100명 자료는 만들지 않습니다.': '원본 학생 자료를 수업 환경에서 제공받아 사용합니다.',
    '새 데이터셋을 만드는 활동이 아니라 불러온 자료를 다른 방식으로 보는 활동입니다.': '앞에서 불러온 자료의 school 열을 사용합니다.',
    ' 새 수치나 현재 통계를 임의로 작성하지 않습니다.': '',
    '원본 PDF의 예시 결과입니다. API 인증 정보가 담긴 입력 화면은 제외하고 표와 그래프 결과만 사용했습니다. 현재 통계나 새 실행 결과를 뜻하지 않습니다.': '원본 PDF 117쪽에 수록된 표와 그래프입니다. 자료를 가져와 자치구별 역 개수 상위 5개를 표시한 예시 결과를 살펴봅니다.',
    '새 프로젝트 목록을 제시하기보다 앞선 원본 실습의 위젯과 기능을 활용합니다.': '앞선 원본 실습의 위젯과 기능을 활용해 UI를 설계합니다.',
    ' 원본에 없는 “수학과 영어가 바뀐 오류” 상황이나 가상 AI 응답을 새 과제로 넣지 않습니다.': '',
    '이 표현과 개발 과정 설명은 16차시 수업을 위해 덧붙였습니다.': '사람이 입력·처리·출력을 설계하고 실행 결과를 확인하는 과정이 중요합니다.',
}
for pid in list(pages):
    for old, new in replacements.items():
        pages[pid] = pages[pid].replace(old, new)

# The extracted XObjects show the input field in /X12 and dialog in /X10.
pages['ch08-message-screen'] = pages['ch08-message-screen'].replace(
    'message-input.png', 'message-TEMP.png').replace(
    'message-dialog.png', 'message-input.png').replace(
    'message-TEMP.png', 'message-dialog.png').replace(
    'ratio="424:247"', 'ratio="462:274"', 1)
pos = pages['ch08-message-screen'].rfind('ratio="462:274"')
pages['ch08-message-screen'] = (pages['ch08-message-screen'][:pos] +
    pages['ch08-message-screen'][pos:].replace('ratio="462:274"', 'ratio="424:247"', 1))

titles = {
    'ch13-one-array': '実習 1 · 배열 한 개의 그래프',
    'ch13-two-arrays': '실습 2 · X·Y 배열 지정',
    'ch13-range': '실습 3 · 선 모양과 표시 범위',
    'ch13-markers': '실습 4 · 빨간 점과 설명',
    'ch13-bars': '실습 6 · 막대그래프 1',
    'ch13-grouped': '실습 7 · 나란한 막대그래프',
    'ch13-scatter': '실습 8 · 산점도',
    'ch14-series': '딕셔너리를 Series로 변환',
    'ch14-mixed': '리스트를 Series로 변환',
    'ch14-dataframe': '현아·태민 자료의 DataFrame',
    'ch14-rename-code': 'DataFrame 행·열 이름 변경',
    'ch14-dict-frame-code': '요일별 열의 DataFrame',
}
titles['ch13-one-array'] = '실습 1 · 배열 한 개의 그래프'
records = []
active_files = set()
for example in recipe['code_specs']:
    pid, code = example['page_id'], example['code']
    capture = io.StringIO()
    def save_result(*args, **kwargs):
        if not example['result']:
            raise RuntimeError('Unexpected plot')
        target = BOOK / 'assets/source-20261006' / (example['result'] + '.png')
        plt.gcf().savefig(target, dpi=240, facecolor='white')
    original_show = plt.show
    plt.show = save_result
    try:
        with contextlib.redirect_stdout(capture):
            namespace = {'__name__': '__main__'}
            exec(compile(code, pid, 'exec'), namespace)
    finally:
        plt.show = original_show
        plt.close('all')
    stdout = capture.getvalue().rstrip()
    example['output'] = stdout or None
    source = recipe['source_codes'][pid]
    lead = f'원본 PDF {source}쪽의 자료와 설정을 사용합니다.' if example['chapter'] == 13 else f'원본 PDF {source}쪽의 자료를 그대로 사용합니다.'
    if pid == 'ch13-scatter':
        lead += ' 축 제목은 함수 호출로 지정하여 원본의 대입 오류를 고쳤습니다.'
    if pid == 'ch14-dataframe':
        lead += ' 본문의 이름 표기를 코드와 같은 태민으로 맞췄습니다.'
    output = f'\n\n```output\n{stdout}\n```' if stdout else ''
    if example['result']:
        output += ('\n\n::image{src="assets/source-20261006/' + example['result'] + '.png" '
                   'alt="' + titles[pid] + ' 코드 실행 결과" ratio="8:5" width="text" role="result" '
                   'caption="원본 PDF ' + source + '쪽의 데이터를 사용한 실제 코드 실행 결과"}')
    pages[pid] = (f':::page{{type="concept" id="{pid}" layout="basic"}}\n# {titles[pid]}\n\n'
                  f'## 원본 예시 따라 실행하기\n\n{lead}\n\n```python\n{code}\n```{output}\n:::\n')
    filename = pid + '.py'
    active_files.add(filename)
    (BOOK / 'examples/source-based' / filename).write_text(code + '\n', encoding='utf-8')
    records.append({'page_id': pid, 'status': 'passed', 'source_pdf_pages': source,
                    'stdout': stdout, 'code_sha256': hashlib.sha256(code.encode()).hexdigest(),
                    'result_asset': example['result']})

# Retire supplemental console examples to a clearly dated archive.
retired = []
for file in (BOOK / 'examples/source-based').glob('*.py'):
    if file.name in active_files:
        continue
    target = (ARCHIVE / 'supplemental-console-examples' / file.name).resolve()
    if not target.is_relative_to(BOOK.resolve()) or not file.resolve().is_relative_to(BOOK.resolve()):
        raise ValueError('Archive path outside book')
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        if target.read_bytes() != file.read_bytes():
            raise ValueError('Different archived file already exists')
        file.unlink()
    else:
        shutil.move(str(file), str(target))
    retired.append(file.name)

front = recipe['frontmatter'].rstrip() + '\n\n'
book_text = front + '\n'.join(pages[pid].rstrip() + '\n' for pid in order)
assert book_text.count('```python') == 12
assert '```prompt' not in book_text and '```response' not in book_text
for forbidden in ('50·30·0', '4.9', '7.9', '88에서 89', '수학과 영어가 바뀐 오류'):
    assert forbidden not in book_text, forbidden
(BOOK / 'book.md').write_text(book_text, encoding='utf-8')
chapters = {i: [] for i in range(1, 17)}
chapter = 0
for pid in order:
    text = pages[pid]
    if 'type="chapter-opening"' in text:
        chapter = int(re.search(r'chapter="(\d+)"', text)[1])
    if chapter:
        chapters[chapter].append(text.rstrip() + '\n')
for chapter, texts in chapters.items():
    title = re.search(r'^# (.+)$', texts[0], re.M)[1]
    header = re.sub(r'^subtitle:.*$', f'subtitle: {chapter}차시 · {title}', front, flags=re.M)
    (BOOK / f'ch{chapter:02d}.md').write_text(header + '\n'.join(texts), encoding='utf-8')

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
write_json(BOOK / 'code-specs.json', recipe['code_specs'])
write_json(BOOK / 'code-results.json', {
    'reviewed_date': '2026-10-10', 'python': sys.version.split()[0],
    'matplotlib': matplotlib.__version__, 'pandas': pd.__version__, 'numpy': np.__version__,
    'executed_blocks': len(records), 'passed': len(records), 'records': records,
    'gui_practices': '原本 화면 대조 및 절차 작성. GUI/API/코코봇의 새 실행을 주장하지 않음'.replace('原本','원본'),
})
catalog = recipe['catalog']
for row in catalog:
    if row['source_label'].startswith(('실습 ', '원본 실습 ')):
        row['source_type'] = 'source-numbered-practice'
write_json(BOOK / 'practice-source-map.json', {
    'reviewed_date': '2026-10-10', 'source_pdf_sha256': '759455352791ac3818f6757de97fa8f6f4a8ed14cf08e84077477dacae8ed0d5',
    'practices': catalog,
    'note': '4차시 학생 총점, 6차시 수면, 7차시 영화 관람 등은 원본 본문 예시로 구분. 자율 프로젝트는 원본 009-8.',
})

manifest = json.loads((BOOK / 'asset-manifest.json').read_text(encoding='utf-8'))
new_assets = json.loads((AUDIT / 'new-assets.json').read_text(encoding='utf-8'))
items = {i['src']: i for i in manifest['items']}
items.update({i['src']: i for i in new_assets})
used = {}
for pid, text in pages.items():
    if pid not in order:
        continue
    for attributes in re.findall(r'::image\{([^}]+)\}', text):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', attributes))
        used.setdefault(attrs['src'], []).append({'page_id': pid, 'width': attrs.get('width'), 'caption': attrs.get('caption')})
for src, placements in used.items():
    item = items[src]
    file = BOOK / src
    with Image.open(file) as im:
        item['width'], item['height'] = im.size
    item['sha256'] = hashlib.sha256(file.read_bytes()).hexdigest()
    item['used_in'] = [p['page_id'] for p in placements]
    item['placements'] = placements
    item['chapter'] = int(re.search(r'ch(\d+)', placements[0]['page_id'])[1])
    item['placement_width'] = placements[0]['width']
    if item['kind'] != 'user-supplied-pdf-embedded-image':
        item['generated_date'] = '2026-10-10' if 'plot-' in src else item.get('generated_date','2026-10-06')
        item['source_example_only'] = True
manifest['items'] = [items[s] for s in used]
manifest['reviewed_date'] = '2026-10-10'
manifest['active_unique_assets'] = len(used)
manifest['active_placements'] = sum(map(len, used.values()))
write_json(BOOK / 'asset-manifest.json', manifest)

rows = ['| 차시 | 교재 실습 | 원본 PDF 쪽 | 원본 실습·예시 |', '|---|---|---|---|']
for item in catalog:
    rows.append(f"| {item['chapter']} | {item['practice_id']} {item['title']} | {item['source_pdf_pages']} | {item['source_label']} |")
review = '''# 원본 실습 대조 수정 기록 · 2026-10-10

158쪽 원본 PDF와 현재 원고를 다시 비교하여 실습의 입력값·동작·결과를 원본 중심으로 수정했습니다. 원본 출처는 각 실습의 첫 페이지에 표시했습니다.

## 정리한 추가 예시

- 학생 총점 80·90·70, 카페인 50·30·0, 학생 판정 79·80·100, 수면 4.9·7.9 등 임의 확인값을 제거했습니다. 원본이 값을 지정하지 않은 과제는 입력값을 미리 지정하지 않습니다.
- 알고리즘과 GUI 실습에 덧붙였던 콘솔 코드 11개를 원본 순서도·위젯 설정 절차로 바꿨습니다. 변수 소개 코드 1개도 설명으로 정리했습니다. 이전 코드는 날짜가 표시된 보관 폴더에 남겼습니다.
- 가상 AI 요청·응답, 가상 오류 이야기, 별도 프로젝트 목록과 추가 발표 실습을 정리했습니다.
- PDF 생성기가 자동으로 넣던 경계값 질문과 추가 활동을 제거했습니다. 실습 첫 페이지는 해당 원본 과제의 완료 기준을 사용합니다.

## 복원한 원본 실습

- 49-51쪽 메시지 창 출력.
- 106-109쪽 학생 100명 키·몸무게 자료와 열 선택.
- 110쪽 학교별 학생 수 막대그래프.
- 111-117쪽 자치구별 지하철역 API와 상위 5개 자치구.
- Matplotlib 실습 1-8의 배열·표시 범위·모양·설명·막대·산점도.
- 150쪽 mon-sun 딕셔너리 DataFrame.

## 보완 범위와 실행 확인

원본 데이터와 과제 동작을 유지했습니다. Matplotlib·Pandas는 독립 실행을 위한 생성 코드, 출력 함수와 원본 오타를 보완했습니다. 12개 코드를 실제 실행하고 그래프 7개를 다시 저장했습니다. 원본 실습 4·5는 같은 코드를 공유합니다. GUI 25개 원본 화면은 PDF에서 추출했습니다. 인증키가 보이는 API 입력 화면은 사용하지 않았습니다.

원본에는 계산기 1의 eval 예시도 있습니다. 교재의 주 실습은 원본 61-62쪽 계산기 2로 구성했습니다. 전체 수업을 16차시로 재구성했으므로 실습 카드 수는 원본 인쇄 번호 개수와 다릅니다. 본문 예시·자료 활용·자율 프로젝트에는 해당 구분을 표시했습니다. 바이브 코딩의 개발 과정과 완료 점검 설명은 수업용 안내입니다.

GUI·API·코코봇 실습은 원본 화면과 절차를 대조했으며 이번에 새로 실행했다고 주장하지 않습니다. API 주소·장비 명령·학생 자료는 수업 환경에서 제공해야 합니다. 원본 캡처의 화질을 복원했다고 주장하지 않습니다.

## 실습별 대조표

'''
(BOOK / 'practice-source-review.md').write_text(review + '\n'.join(rows) + '\n', encoding='utf-8')
(BOOK / 'examples/source-based/README.md').write_text(
    '# 원본 실습 기반 실행 예제\n\n현재 원고에는 Matplotlib 7개, Pandas 5개 코드를 사용합니다.\n'
    '원본 PDF의 데이터와 동작을 유지하고 독립 실행에 필요한 초기화·출력과 오타를 보완했습니다.\n\n'
    'Python 3.10 이상에서 requirements.txt의 패키지를 설치한 뒤 각 .py 파일을 실행합니다.\n'
    'GUI·코코봇 실습은 책의 수업 도구에서 진행하며 이 폴더에 임의 콘솔 대체 실습을 추가하지 않습니다.\n\n'
    '| 파일 | 원본 PDF 쪽 |\n|---|---|\n' + '\n'.join(f"| {x['page_id']}.py | {recipe['source_codes'][x['page_id']]} |" for x in recipe['code_specs']) + '\n', encoding='utf-8')
(BOOK / 'examples/README.md').write_text(
    '# 실습 예제\n\n현재 교재의 실행 코드는 [source-based](source-based/README.md)에 있습니다.\n'
    '원본 실습과의 대응은 [대조 기록](../practice-source-review.md)을 확인하세요.\n'
    'index.html과 이전 assets/chXX 화면은 과거 별도 앱 초안이며 현재 교재 예시로 사용하지 않습니다.\n', encoding='utf-8')
write_json(AUDIT / 'revision-result.json', {
    'manuscript_pages': len(order), 'practice_cards': len(catalog), 'executed_code_blocks': len(records),
    'unique_assets': len(used), 'image_placements': sum(map(len, used.values())),
    'retired_console_files': retired, 'source_pages': 158,
})
print(json.dumps({'pages':len(order),'practices':len(catalog),'codes':len(records),'images':len(used)},ensure_ascii=False))
