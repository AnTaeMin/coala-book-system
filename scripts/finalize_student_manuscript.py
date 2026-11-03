"""Assemble the learner edition while preserving its exercises and code."""
from pathlib import Path
import json
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
RESTRUCTURE = BOOK / 'no-pandas-restructure.json'

GUIDE = ''':::page{type="screenshot-guide" id="book-guide"}
# COALA에 접속하는 방법

## 홈페이지 열기

크롬 주소창에 **thecoala.io**를 입력합니다. 홈페이지 상단의 **다운로드** 메뉴를 누릅니다.

::image{src="assets/coala-access-20261028/homepage.png" alt="thecoala.io 홈페이지와 상단 다운로드 메뉴" ratio="1420:735" width="half" caption="COALA 홈페이지에서 다운로드 메뉴 선택"}

## Web Version에 접속하기

다운로드 화면에서 **Web Version**의 **접속하기**를 누릅니다. 크롬에서 COALA를 엽니다.

::image{src="assets/coala-access-20261028/download.png" alt="다운로드 화면의 Web Version과 Online Book Version 접속하기" ratio="685:448" width="half" caption="실습은 Web Version으로 접속"}

## 학생으로 로그인하기

선생님이 안내한 아이디와 비밀번호를 입력한 뒤 **학생** 버튼을 누릅니다.

::image{src="assets/coala-access-20261028/login.png" alt="아이디와 비밀번호 입력란 및 학생 로그인 버튼" ratio="445:250" width="half" caption="안내받은 계정으로 학생 로그인"}

## 내 강좌에서 수업 입장하기

로그인 후 **내 강좌**에서 안내받은 강좌를 찾습니다. 강좌 오른쪽의 **수업 입장**을 누릅니다.

::image{src="assets/coala-access-20261028/dashboard.png" alt="로그인 후 내 강좌 목록과 수업 입장 버튼" ratio="950:270" width="half" caption="내 강좌에서 수업 입장 선택"}

## 전자책 열기

홈페이지의 다운로드 화면에서 **Online Book Version**의 **접속하기**를 누릅니다. 수정된 표지와 **AI·알고리즘·GUI**로 나뉜 학습 차례를 확인합니다.

::image{src="assets/coala-access-20261028/ebook-preview.png" alt="수정된 표지와 AI·알고리즘 학습 차례를 보여 주는 전자책 예시" ratio="16:9" width="text" caption="수정 교재 화면 예시"}
:::
'''

old = (BOOK / 'book.md').read_text(encoding='utf-8')
baseline = old
front = old.split('---', 2)[1]
front = re.sub(r'^subtitle:.*$', 'subtitle: 16차시 · 개념과 실습', front, flags=re.M)
chapters = []
for n in range(1, 17):
    text = (BOOK / f'ch{n:02d}.md').read_text(encoding='utf-8')
    chapters.append(text[text.index(':::page'):].strip())
new = '---' + front + '---\n\n' + GUIDE + '\n' + '\n\n'.join(chapters) + '\n'

def fences(text, language):
    return re.findall(r'^```' + language + r'\s*\n(.*?)^```\s*$', text, re.M | re.S)

revision = json.loads(RESTRUCTURE.read_text(encoding='utf-8'))
code_specs = json.loads((BOOK / 'code-specs.json').read_text(encoding='utf-8'))
assert [t.rstrip() for t in fences(new, 'python')] == [item['code'].rstrip() for item in code_specs], 'Chapter code must match the current reviewed code specification'
assert len(fences(new, 'output')) == 0

flow_map = BOOK / 'flow-source-map.json'
if flow_map.exists():
    expected_flows = [i['flowchart_sha256'] for i in json.loads(flow_map.read_text(encoding='utf-8'))['diagrams']]
    assert [hashlib.sha256(t.encode('utf-8')).hexdigest() for t in fences(new, 'flowchart')] == expected_flows
else:
    assert fences(baseline, 'flowchart') == fences(new, 'flowchart')
ids = re.findall(r':::page\{[^\n]*id="([^"]+)"', new)
if RESTRUCTURE.exists():
    revision = json.loads(RESTRUCTURE.read_text(encoding='utf-8'))
    expected = {p for p in revision['old_to_new'].values() if p} | set(revision['added_pages'])
    assert set(ids) == expected and len(ids) == revision['expected_containers']
else:
    assert re.findall(r':::page\{[^\n]*id="([^"]+)"', baseline) == ids
    assert len(ids) == 179
assert len(fences(new, 'python')) == len(code_specs) == 8
assert len(fences(new, 'flowchart')) == 4
assert not re.search(r'원본|\bPDF\b|원 교재|대조 수정판|코코봇|cocobot', new, re.I)
assert not re.search(r'\bAPI\b|인증키|지하철역', new, re.I), 'API activity must remain outside this course'
opening_positions = [new.index(f'id="ch{n:02d}-opening"') for n in range(1, 17)]
assert opening_positions == sorted(opening_positions)
assert 'Matplotlib 선 그래프와 마커' in chapters[11]
assert 'Matplotlib 막대그래프와 산점도' in chapters[12]
assert '입력 데이터를 차트로 표현하기' in chapters[13]
assert '자료 활용과 저장·불러오기' in chapters[14]
assert not re.search(r'pandas|DataFrame|Series|Divider|디바이더', new, re.I)
(BOOK / 'book.md').write_text(new, encoding='utf-8')
print(f'Learner manuscript assembled: {len(ids)} containers; retained code verified; diagram sources verified.')
