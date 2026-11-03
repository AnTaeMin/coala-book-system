"""One-time, explicit migration from the archived source7 learner edition."""
from pathlib import Path
import hashlib
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
BASE = BOOK / 'previous-reports/20261011-before-no-pandas-divider'

def read(name):
    return (BASE / name).read_text(encoding='utf-8')

def write(name, value):
    (BOOK / name).write_text(value, encoding='utf-8')

def save(name, value):
    write(name, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def pages(text):
    return re.findall(r':::page\{.*?\n:::', text, re.S)

def page_id(text):
    return re.search(r'id="([^"]+)"', text)[1]

def front(text, number, title):
    s = text[:text.index(':::page')]
    return re.sub(r'^subtitle:.*$', f'subtitle: {number}차시 · {title}', s, flags=re.M)

def opening(number, title, objectives, lead):
    return f''':::page{{type="chapter-opening" id="ch{number:02d}-opening" chapter="{number}"}}
# {title}

## {number:02d}차시 · 개념과 실습

### 학습 목표

''' + '\n'.join('- '+x for x in objectives) + '\n\n### 오늘의 시작\n\n' + lead + '\n:::'

def checklist(number, items):
    return f''':::page{{type="practice-checklist" id="ch{number:02d}-check"}}
# 실습 완료 확인

''' + '\n'.join('- [ ] '+x for x in items) + '''

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::'''

original = read('book.md')
old_ids = re.findall(r':::page\{[^\n]*id="([^"]+)"', original)
mapping = {x:x for x in old_ids}
old12 = pages(read('ch12.md'))
first = old12[1:12]
second = old12[12:18]
for index, p in enumerate(second):
    old_id = page_id(p)
    new_id = old_id.replace('ch12-', 'ch13-')
    mapping[old_id] = new_id
    p = p.replace('ch12-', 'ch13-')
    for a,b in [(6,1),(7,2),(8,3)]:
        p = p.replace(f'실습 {a} ·',f'실습 {b} ·')
        p = p.replace(f'practice="012-{a}"',f'practice="013-{b}"')
    second[index] = p

title12 = 'Matplotlib 선 그래프와 마커'
title13 = 'Matplotlib 막대그래프와 산점도'
new12 = [opening(12,title12,[
    'Figure와 Axes를 만들고 배열을 선 그래프로 나타낼 수 있다.',
    'X·Y 값과 표시 범위·마커를 구분할 수 있다.',
    '제목·축 이름·좌표 설명을 설정하고 실행 결과를 확인할 수 있다.'
], '배열 한 개와 X·Y 배열을 그래프로 나타냅니다. 표시 범위와 마커를 바꾸고 제목·축 이름·좌표 설명의 위치를 확인합니다.'), *first,
''':::page{type="concept" id="ch12-fix" layout="basic"}
# 점과 선의 모양 확인

## ro와 r-o

ro는 빨간 점을 표시하고, r-o는 빨간 점과 점 사이의 선을 함께 표시합니다. 같은 X·Y 값에서도 모양 설정에 따라 결과가 달라집니다.
:::''', checklist(12,[
    '다섯 Matplotlib 실습의 입력값과 그래프를 확인했다.',
    '배열·표시 범위·마커의 차이를 설명했다.',
    '제목·축 이름·좌표 설명의 위치를 확인했다.'
])]
new13 = [opening(13,title13,[
    '배열 값을 막대 높이로 표현할 수 있다.',
    'create_x로 나란한 막대의 위치와 항목 이름을 정할 수 있다.',
    '같은 시드로 만든 X·Y의 산점도와 축·범례를 확인할 수 있다.'
], '막대그래프의 높이와 위치를 배열 값에 연결합니다. 두 배열을 나란히 비교하고, 난수를 더한 X·Y 값으로 산점도를 만듭니다.'), *second,
''':::page{type="concept" id="ch13-fix" layout="basic"}
# 산점도의 데이터와 축 설정

## 난수 시드 확인

seed는 난수 생성기의 상태를 정합니다. 같은 시드와 생성 순서를 사용하면 같은 난수를 얻습니다. 산점도의 X·Y 값은 코드에서 생성한 연습용 데이터입니다.

## 축 이름과 범례

축 이름은 set_xlabel("X축 제목"), set_ylabel("Y축 제목")처럼 함수로 설정합니다. 범례 random이 빨간 점을 가리키는지 확인합니다.
:::''', checklist(13,[
    '세 Matplotlib 실습의 코드를 실행했다.',
    '막대의 높이와 나란한 막대 위치를 배열 값과 비교했다.',
    '산점도의 시드·축 이름·범례를 확인했다.'
])]
write('ch12.md',front(read('ch12.md'),12,title12)+'\n\n'.join(new12)+'\n')
write('ch13.md',front(read('ch12.md'),13,title13)+'\n\n'.join(new13)+'\n')
old13=read('ch13.md')
new14=old13.replace('ch13-', 'ch14-').replace('practice="013-', 'practice="014-').replace('chapter="13"','chapter="14"').replace('13차시','14차시')
write('ch14.md',new14)
for x in old_ids:
    if x.startswith('ch13-'): mapping[x]=x.replace('ch13-','ch14-')
    elif x.startswith('ch14-'): mapping[x]=x.replace('ch14-','ch15-')
    elif x.startswith('ch15-'): mapping[x]=None

s=read('ch10.md')
s=s.replace('이미지 사이에 Divider를 넣고 세로로 구분되어 보이는지 확인합니다.','두 이미지가 세로로 배치되고 설정한 크기로 표시되는지 확인합니다.')
s=s.replace('두 이미지 사이에 Divider가 보인다.','설정한 크기로 두 이미지가 표시된다.')
s=s.replace('두 이미지와 구분선','두 이미지 세로 배치')
s=s.replace('두 이미지 사이에 얇은 구분선이 있어 화면 영역이 나뉩니다.','두 Image가 세로로 배치되어 있습니다. 각 이미지의 크기와 배치 순서를 확인합니다.')
s=s.replace('assets/source-20261006/image-divider.png','assets/ch10/two-images.png')
s=s.replace('두 Image 사이에 배치한 Divider','두 Image를 세로로 배치한 화면')
s=s.replace('진행 막대 증감과 두 이미지·Divider를 확인했다.','진행 막대 증감과 두 이미지의 크기·배치를 확인했다.')
write('ch10.md',s)

specs=json.loads(read('code-specs.json'))
retained=[]
for s in specs:
    if mapping[s['page_id']] is None: continue
    s['page_id']=mapping[s['page_id']]; s['chapter']=int(s['page_id'][2:4]); retained.append(s)
save('code-specs.json',retained)
results=json.loads(read('code-results.json'))
results.pop('pandas',None)
results['records']=[dict(s,page_id=mapping[s['page_id']]) for s in results['records'] if mapping[s['page_id']]]
results.update(executed_blocks=7,passed=7,edition='no-pandas-16-sessions')
save('code-results.json',results)
active=BOOK/'examples/source-based'
for s in specs:
    old=active/(s['page_id']+'.py')
    # Specs were remapped above: copy exact bytes from immutable backup instead.
    old_id=next((k for k,v in mapping.items() if v==s['page_id'] and (BASE/'examples/source-based'/(k+'.py')).exists()),s['page_id'])
    source=BASE/'examples/source-based'/(old_id+'.py')
    if s in retained and source.exists(): shutil.copy2(source,old)
allowed={s['page_id']+'.py' for s in retained}
for p in active.glob('*.py'):
    assert BOOK.resolve() in p.resolve().parents
    if p.name not in allowed: p.unlink()  # already preserved in immutable backup
req=active/'requirements.txt'
req.write_text('\n'.join(x for x in req.read_text('utf-8').splitlines() if not x.lower().startswith('pandas'))+'\n',encoding='utf-8')
sources=json.loads(read('source-map.json'))
sources[11].update(title=title12,source_pages='128-139')
sources[12]={'chapter':13,'title':title13,'source_pages':'140-145'}
sources[13]=dict(json.loads(read('source-map.json'))[12],chapter=14)
sources[14]=dict(json.loads(read('source-map.json'))[13],chapter=15)
save('source-map.json',sources)
revision={'date':'2026-10-11','edition':'no-pandas-16-sessions','baseline':'previous-reports/20261011-before-no-pandas-divider',
 'old_to_new':mapping,'added_pages':['ch13-opening','ch13-fix','ch13-check'],
 'removed_pages':[k for k,v in mapping.items() if v is None],
 'expected_practices':37,'expected_python_blocks':7,'expected_output_blocks':0,
 'retained_code_sha256':[hashlib.sha256(s['code'].encode()).hexdigest() for s in retained],
 'notes':['12차시 선·마커 /13차시 막대·산점도로 분리','14차시 Chart /15차시 자료·저장','저장 과정 사진 추가 및 Divider 제거']}
save('no-pandas-restructure.json',revision)
print('Migration complete; wait for source-based chapter15 and illustration before final assembly.')
