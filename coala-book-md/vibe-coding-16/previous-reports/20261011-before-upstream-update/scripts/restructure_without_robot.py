"""Reassign existing app exercises to 16 sessions without robot material."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
ARCHIVE = BOOK / 'previous-reports/20261011-before-no-robot'

def read(name):
    return (ARCHIVE / name).read_text(encoding='utf-8')

def write(name, text):
    (BOOK / name).write_text(text.rstrip() + '\n', encoding='utf-8')

def save_json(name, value):
    write(name, json.dumps(value, ensure_ascii=False, indent=2))

def pages(text):
    return re.findall(r':::page\{[^\n]*\}.*?\n:::', text, re.S)

def page_id(text):
    return re.search(r'\bid="([^"]+)"', text)[1]

def chapter_file(number, title, bodies):
    front = read(f'ch{number:02d}.md').split(':::page', 1)[0]
    front = re.sub(r'^subtitle:.*$', f'subtitle: {number}차시 · {title}', front, flags=re.M)
    return front.rstrip() + '\n\n' + '\n\n'.join(bodies)

def opening(number, title, objectives, body):
    goals = '\n'.join('- ' + text for text in objectives)
    return f''':::page{{type="chapter-opening" id="ch{number:02d}-opening" chapter="{number}"}}
# {title}

## {number}차시 · 개념과 실습

### 학습 목표

{goals}

### 오늘의 시작

{body}
:::'''

def checklist(number, items):
    checks = '\n'.join('- [ ] ' + text for text in items)
    return f''':::page{{type="practice-checklist" id="ch{number:02d}-check"}}
# 실습 완료 확인

{checks}

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::'''

old_pages = pages(read('book.md'))
mapping = {page_id(p): page_id(p) for p in old_pages}
removed = [page_id(p) for p in pages(read('ch15.md'))]
for pid in removed:
    mapping[pid] = None
chart_pages = pages(read('ch12.md'))
split = next(i for i, p in enumerate(chart_pages) if page_id(p) == 'ch12-practice-data')
for p in chart_pages[split:]:
    pid = page_id(p)
    mapping[pid] = pid.replace('ch12-', 'ch13-', 1)
for n in (13, 14):
    for p in pages(read(f'ch{n:02d}.md')):
        pid = page_id(p)
        mapping[pid] = pid.replace(f'ch{n:02d}-', f'ch{n+1:02d}-', 1)

def reassign(text, number):
    pid = page_id(text)
    text = text.replace(f'id="{pid}"', f'id="{mapping[pid]}"', 1)
    text = re.sub(r'\bchapter="\d+"', f'chapter="{number}"', text)
    text = re.sub(r'^## \d+차시 · 개념과 실습$', f'## {number}차시 · 개념과 실습', text, flags=re.M)
    return text

new12 = [opening(12, '입력 데이터를 차트로 표현하기', [
    '선 그래프·막대그래프·산점도의 표현 목적과 축을 구분할 수 있다.',
    '입력창의 값을 버튼 이벤트로 Chart에 연결할 수 있다.',
    '입력값과 그래프를 비교하고 초기화·누적 동작을 확인할 수 있다.',
], '입력값을 선 그래프, 산점도, 막대그래프로 표현합니다. 버튼을 눌렀을 때 그래프가 바뀌는 과정과 초기화·누적 동작을 확인합니다.')]
new12 += chart_pages[1:split]
new12.append(checklist(12, [
    '선 그래프·산점도·막대그래프를 만들었다.',
    '입력값과 그래프의 축·점·막대 높이를 확인했다.',
    '초기화와 입력값 누적 동작을 확인했다.',
]))
new13 = [opening(13, '자료 활용과 저장·불러오기', [
    '학생 자료의 표시 항목을 선택하고 표·차트로 표현할 수 있다.',
    'API 자료의 항목을 표·그래프에 연결하고 상위 5개를 표시할 수 있다.',
    '표 저장 설정과 프로젝트 저장 후 같은 기록을 다시 확인할 수 있다.',
], '학생 자료를 불러와 표와 그래프로 살펴봅니다. API는 프로그램이 다른 서비스와 정보를 주고받는 연결 방식입니다. 자료를 가져온 뒤 저장하고 다시 불러오는 과정까지 확인합니다.')]
for p in chart_pages[split:-1]:
    new13.append(reassign(p, 13))
new13.append(checklist(13, [
    '학생 자료의 표시 항목과 학교별 개수를 확인했다.',
    'API로 가져온 자료의 표·그래프를 확인했다.',
    '저장·불러오기에서 같은 입력 데이터를 확인했다.',
]))
practice_number = 0
for i, p in enumerate(new13):
    if 'type="practice-opening"' in p:
        practice_number += 1
        new13[i] = re.sub(r'\bpractice="[^"]+"', f'practice="013-{practice_number}"', p)
assert practice_number == 4
write('ch12.md', chapter_file(12, '입력 데이터를 차트로 표현하기', new12))
write('ch13.md', chapter_file(13, '자료 활용과 저장·불러오기', new13))
for old_n, new_n, title in [(13, 14, 'Matplotlib 그래프 만들기'), (14, 15, 'Pandas로 데이터 정리하기')]:
    bodies = []
    for p in pages(read(f'ch{old_n:02d}.md')):
        p = reassign(p, new_n)
        p = re.sub(r'\bpractice="\d{3}-(\d+)"', lambda m: f'practice="{new_n:03d}-{m[1]}"', p)
        bodies.append(p)
    write(f'ch{new_n:02d}.md', chapter_file(new_n, title, bodies))
write('ch16.md', read('ch16.md').replace(
    ' 장비가 필요한 기능은 실제 실행 여부를 표시합니다.',
    ' 외부 자료를 사용하는 기능은 실제 연결 결과를 기록합니다.'))
save_json('page-restructure.json', {
    'date': '2026-10-11', 'edition': 'apps-only-16-sessions',
    'baseline': 'previous-reports/20261011-before-no-robot',
    'old_to_new': mapping, 'removed_pages': removed,
    'added_pages': ['ch12-check', 'ch13-opening'],
    'expected_containers': 170, 'expected_practices': 41,
    'expected_images': 31, 'expected_assets': 30,
    'expected_code_blocks': 12, 'expected_flowcharts': 4,
})
current_pages = []
for n in range(1, 17):
    current_pages += pages((BOOK / f'ch{n:02d}.md').read_text(encoding='utf-8'))
by_id = {page_id(p): p for p in current_pages}
source_map = json.loads(read('practice-source-map.json'))
records = []
for record in source_map['practices']:
    pid = mapping[record['page_id']]
    if pid is None:
        continue
    record['page_id'] = pid
    record['chapter'] = int(pid[2:4])
    text = by_id[pid]
    record['practice_id'] = re.search(r'\bpractice="([^"]+)"', text)[1]
    record['title'] = re.search(r'^# (.+)$', text, re.M)[1]
    record['completion_criteria'] = re.findall(r'^- \[ \] (.+)$', text, re.M)
    records.append(record)
order = {page_id(p): i for i, p in enumerate(current_pages)}
source_map['practices'] = sorted(records, key=lambda r: order[r['page_id']])
source_map['reviewed_date'] = '2026-10-11'
source_map['edition'] = 'apps-only-16-sessions'
assert len(records) == 41
save_json('practice-source-map.json', source_map)
code_specs = json.loads(read('code-specs.json'))
for record in code_specs:
    record['page_id'] = mapping[record['page_id']]
    record['chapter'] = int(record['page_id'][2:4])
save_json('code-specs.json', code_specs)
code_results = json.loads(read('code-results.json'))
for record in code_results['records']:
    record['page_id'] = mapping[record['page_id']]
    if 'chapter' in record:
        record['chapter'] = int(record['page_id'][2:4])
code_results['edition'] = 'apps-only-16-sessions'
save_json('code-results.json', code_results)
active_examples = set()
for record in code_specs:
    name = record['page_id'] + '.py'
    active_examples.add(name)
    path = BOOK / 'examples/source-based' / name
    path.write_text(record['code'] + '\n', encoding='utf-8')
for path in (BOOK / 'examples/source-based').glob('*.py'):
    if path.name not in active_examples:
        assert path.resolve().is_relative_to(BOOK.resolve())
        assert (ARCHIVE / 'examples' / path.name).exists()
        path.unlink()
assets = json.loads(read('asset-manifest.json'))
image_uses = {}
for p in current_pages:
    for line in re.findall(r'^::image\{(.+)\}$', p, re.M):
        attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', line))
        image_uses.setdefault(attrs['src'], []).append({'page_id': page_id(p), **attrs})
active_items = []
for item in assets['items']:
    if item['src'] not in image_uses:
        path = BOOK / item['src']
        target = ARCHIVE / item['src']
        assert path.resolve().is_relative_to(BOOK.resolve()) and target.resolve().is_relative_to(BOOK.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            if not target.exists():
                shutil.copy2(path, target)
            assert hashlib.sha256(path.read_bytes()).digest() == hashlib.sha256(target.read_bytes()).digest()
            path.unlink()
        continue
    uses = image_uses[item['src']]
    item['used_in'] = [u['page_id'] for u in uses]
    item['chapter'] = int(uses[0]['page_id'][2:4])
    item['placements'] = [{'page_id': u['page_id'], 'width': u.get('width', 'text'),
                           'caption': u.get('caption', '')} for u in uses]
    item['placement_width'] = uses[0].get('width', 'text')
    active_items.append(item)
assets['items'] = active_items
assets['edition'] = 'apps-only-16-sessions'
assert len(active_items) == 30 and sum(map(len, image_uses.values())) == 31
save_json('asset-manifest.json', assets)
source_chapters = json.loads(read('source-map.json'))
new_ranges = {12: '95-105', 13: '106-127', 14: '128-145', 15: '146-151'}
for record in source_chapters:
    number = record['chapter']
    record['title'] = re.search(r'^# (.+)$', by_id[f'ch{number:02d}-opening'], re.M)[1]
    if number in new_ranges:
        record['source_pages'] = new_ranges[number]
save_json('source-map.json', source_chapters)
print('Restructured sessions 12-15; 41 practices, 12 unchanged examples, 30 assets.')
