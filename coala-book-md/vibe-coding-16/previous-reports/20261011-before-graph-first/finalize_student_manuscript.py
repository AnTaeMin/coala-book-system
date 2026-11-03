"""Assemble the learner edition while preserving its exercises and code."""
from pathlib import Path
import json
import hashlib
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
RESTRUCTURE = BOOK / 'page-restructure.json'
ARCHIVE = BOOK / ('previous-reports/20261011-before-no-robot' if RESTRUCTURE.exists()
                  else 'previous-reports/20261011-before-student-edition')

GUIDE = ''':::page{type="concept" id="book-guide" layout="basic"}
# 이 교재를 사용하는 방법

## 개념을 익히고 실습하기

16차시에 걸쳐 AI 활용, 앱 설계, 프로그래밍, 데이터 시각화를 배웁니다. 각 차시의 학습 목표를 읽고 실습을 진행합니다.

## 입력·동작·결과 확인

실습의 조건과 위젯 이름을 먼저 읽습니다. 예시 값을 입력하고 실행 결과가 예상한 동작과 일치하는지 확인합니다. 입력값이 정해져 있지 않은 과제에서는 직접 값을 정합니다.

## 코드와 실행 화면

코드를 실행하면서 데이터와 처리 순서를 살펴봅니다. 예시 화면의 입력값과 결과를 읽고, 자신의 실행 화면과 확인한 내용을 기록합니다.
:::
'''

old = (BOOK / 'book.md').read_text(encoding='utf-8')
ARCHIVE.mkdir(parents=True, exist_ok=True)
for path in [BOOK / 'book.md', *[
    ROOT / 'output/pdf' / ('vibe-coding-16-compact' + suffix)
    for suffix in ('.pdf', '.json', '-qa.json')
]]:
    if path.exists() and not (ARCHIVE / path.name).exists():
        shutil.copy2(path, ARCHIVE / path.name)
baseline = (ARCHIVE / 'book.md').read_text(encoding='utf-8')
front = old.split('---', 2)[1]
front = re.sub(r'^subtitle:.*$', 'subtitle: 16차시 · 개념과 실습', front, flags=re.M)
chapters = []
for n in range(1, 17):
    text = (BOOK / f'ch{n:02d}.md').read_text(encoding='utf-8')
    chapters.append(text[text.index(':::page'):].strip())
new = '---' + front + '---\n\n' + GUIDE + '\n' + '\n\n'.join(chapters) + '\n'

def fences(text, language):
    return re.findall(r'^```' + language + r'\s*\n(.*?)^```\s*$', text, re.M | re.S)

for language in ('python', 'output'):
    assert fences(baseline, language) == fences(new, language), language
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
assert len(fences(new, 'python')) == 12
assert len(fences(new, 'flowchart')) == 4
assert not re.search(r'원본|\bPDF\b|원 교재|대조 수정판|코코봇|cocobot', new, re.I)
(BOOK / 'book.md').write_text(new, encoding='utf-8')
print(f'Learner manuscript assembled: {len(ids)} containers; code/output unchanged; diagram sources verified.')
