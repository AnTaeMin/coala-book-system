"""Add source-practice GUI examples, preserving the 16-session curriculum."""
from pathlib import Path
import re
import json
import hashlib
import shutil

ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'coala-book-md/vibe-coding-16'
BASE=BOOK/'previous-reports/20261011-before-gui-examples'

def read(name):
    return (BASE/name).read_text(encoding='utf-8')

def write(name,text):
    (BOOK/name).write_text(text,encoding='utf-8')

def replace_once(text,old,new):
    assert text.count(old)==1,old
    return text.replace(old,new,1)

s=read('ch08.md')
s=replace_once(s,'입력과 처리 결과를 나란히 비교해봅시다.','GUI는 화면의 버튼·입력창 등을 통해 프로그램을 사용하는 방식입니다. 화면을 구성하는 각각의 요소를 위젯이라고 합니다.')
s=s.replace('| Field | 글자나 숫자 입력 |','| Field | 글자·숫자 입력 또는 결과 표시 |')
gui8=''':::page{type="concept" id="ch08-gui-example" layout="basic"}
# GUI 구성 예시 · 인사말 앱

## 입력·버튼·결과 배치

인사말 추가·삭제 앱은 입력창, 두 버튼, 결과창으로 구성합니다. 위쪽에서 입력하고, 가운데 버튼으로 동작을 실행한 뒤 아래쪽에서 결과를 확인합니다.

::image{src="assets/source-20261006/field-copy.png" alt="위쪽 fld1 입력창, 가운데 추가·삭제 버튼, 아래쪽 fld2 결과창으로 구성한 인사말 앱" ratio="497:406" width="half" caption="위 입력창 → 추가·삭제 버튼 → 아래 결과창"}

## 위젯 이름과 역할

- fld1: 인사말을 입력하는 Field
- btn1: fld1의 내용을 fld2에 표시하는 ‘추가’ 버튼
- btn2: 두 Field의 내용을 비우는 ‘삭제’ 버튼
- fld2: 추가한 인사말을 보여주는 Field
:::

'''
s=s.replace(':::page{type="practice-opening" id="ch08-practice-1"',gui8+':::page{type="practice-opening" id="ch08-practice-1"')
s=replace_once(s,'프로젝트 이름과 설명을 적습니다.','예를 들어 프로젝트 이름은 ‘인사말 추가·삭제’, 설명은 ‘입력한 인사말을 아래에 표시하고 삭제하는 앱’으로 적습니다.')
s=replace_once(s,'디자이너에서 위젯을 추가하고 이름과 역할을 확인합니다.','Field 두 개와 Button 두 개를 만들고 위쪽 fld1, 가운데 btn1·btn2, 아래쪽 fld2로 배치합니다.')
s=replace_once(s,'각 버튼을 눌렀을 때 바뀔 내용을 적습니다.','btn1은 fld1의 내용을 fld2에 표시하고, btn2는 두 Field를 비우도록 적습니다.')
s=replace_once(s,'코드를 생성하고 버튼을 실제로 눌러 동작을 확인합니다.','‘안녕’을 입력하고 추가 후 fld2의 글자, 삭제 후 두 Field가 비는지 확인합니다.')
s=replace_once(s,'fld1, fld2, btn1, btn2를 추가합니다. 두 Field와 추가·삭제 버튼을 배치합니다.','위쪽에 fld1, 가운데에 btn1(추가)·btn2(삭제), 아래쪽에 fld2를 배치합니다. fld1은 입력, fld2는 입력 내용을 보여주는 결과창으로 정합니다.')
write('ch08.md',s)

s=read('ch09.md')
s=replace_once(s,'시작 값 1과 끝 값 6을 각 Field에 입력합니다.','위쪽 한 줄에 fld1, btn1(누적), fld2를 놓고 아래에 결과창 fld3을 둡니다. fld1에 시작 값 1, fld2에 끝 값 6을 입력합니다.')
s=replace_once(s,'fld1과 fld2는 각각 계산할 숫자를 받습니다.','위쪽에 fld1과 fld2를 나란히 놓아 계산할 두 숫자를 받습니다. 가운데에는 btn1(연산)·btn2(=), 아래쪽에는 결과창 fld3을 배치합니다.')
write('ch09.md',s)

s=read('ch11.md')
s=replace_once(s,'fld1부터 fld4, btn1, tbl1을 화면에 배치합니다.','왼쪽에는 fld1~fld4를 세로로 놓고 그 아래 btn1(추가하기), 오른쪽에는 tbl1을 배치합니다.')
write('ch11.md',s)

s=read('ch14.md')
parts=re.findall(r':::page\{.*?\n:::',s,re.S)
layouts={
 'ch14-line-screen':'왼쪽에 fld1부터 fld5까지 세로로 배치하고 오른쪽에 cht1을 둡니다. 차트 아래에는 btn1(그래프 그리기)과 btn2(초기화)를 나란히 둡니다. 초기화 버튼은 차트의 기록을 비웁니다.',
 'ch14-scatter-screen':'왼쪽에 fld1(키)·fld2(몸무게)와 btn1(시각화)을 놓고 오른쪽에 cht1을 둡니다. 산점도의 X값은 키, Y값은 몸무게로 정합니다.',
 'ch14-bar-screen':'위쪽에 fld1, 가운데에 btn1(시각화), 아래쪽에 cht1을 배치합니다.'
}
for p in parts:
 pid=re.search(r'id="([^"]+)"',p)[1]
 if pid not in layouts: continue
 new=p.replace('## 예시 확인하기','## GUI 구성과 실행 예시').replace('화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.',layouts[pid])
 s=s.replace(p,new)
write('ch14.md',s)

s=read('ch15.md')
gui15=''':::page{type="concept" id="ch15-gui-layout" layout="basic"}
# 저장 실습 · GUI 구성 예시

## 여섯 위젯으로 화면 구성

위쪽에 fld1(걸음 수)·fld2(이동거리), 그 아래에 btn1(데이터 추가)·btn2(초기화)를 나란히 놓습니다. 다음에 표 tbl1과 차트 cht1을 세로로 배치합니다.

::image{src="assets/source-20261011/save-gui-layout.png" alt="걸음 수·이동거리 입력창, 데이터 추가·초기화 버튼, 두 열의 표와 차트를 배치한 디자이너 화면" ratio="913:1216" width="half" caption="걸음 수·이동거리 앱의 디자이너 구성"}
:::

'''
s=s.replace(':::page{type="concept" id="ch15-save-widgets" layout="basic"}',gui15+':::page{type="concept" id="ch15-save-widgets" layout="basic"}')
write('ch15.md',s)
asset=BOOK/'assets/source-20261011/save-gui-layout.png'
shutil.copy2(ROOT/'tmp/pdfs/save-review/source7-page-118-image-1.png',asset)

revision=json.loads(read('no-pandas-restructure.json'))
revision['edition']='gui-examples-16-sessions'
revision['added_pages']+=['ch08-gui-example','ch15-gui-layout']
revision['expected_containers']=162
write('no-pandas-restructure.json',json.dumps(revision,ensure_ascii=False,indent=2)+'\n')

manifest=json.loads(read('asset-manifest.json'))
manifest['items'].append({'src':'assets/source-20261011/save-gui-layout.png','chapter':15,
 'width':913,'height':1216,'ratio':'913:1216','sha256':hashlib.sha256(asset.read_bytes()).hexdigest(),
 'kind':'user-supplied-pdf-embedded-image','pdf_page':118,'xobject':['/X16','/X4'],
 'pixel_text_modified':False,'upscaled':False})
placement={}
for n in range(1,17):
 text=(BOOK/f'ch{n:02d}.md').read_text('utf-8')
 for p in re.findall(r':::page\{.*?\n:::',text,re.S):
  pid=re.search(r'id="([^"]+)"',p)[1]
  for raw in re.findall(r'::image\{([^\n]*)\}',p):
   a=dict(re.findall(r'([\w-]+)="([^"]*)"',raw))
   placement.setdefault(a['src'],[]).append({'page_id':pid,'width':a.get('width','text'),'caption':a.get('caption','')})
for item in manifest['items']:
 if item['kind']=='user-supplied-pdf-native-vector-crop': continue
 item['placements']=placement[item['src']]
 item['used_in']=[p['page_id'] for p in item['placements']]
 item['placement_width']=item['placements'][0]['width']
manifest.update(edition='gui-examples-16-sessions',reviewed_date='2026-10-11')
write('asset-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
changed=[]
for n in [8,9,11,14,15]:
 old={re.search(r'id="([^"]+)"',p)[1]:p for p in re.findall(r':::page\{.*?\n:::',read(f'ch{n:02d}.md'),re.S)}
 for p in re.findall(r':::page\{.*?\n:::',(BOOK/f'ch{n:02d}.md').read_text('utf-8'),re.S):
  pid=re.search(r'id="([^"]+)"',p)[1]
  if pid in old and old[pid]!=p: changed.append(pid)
record={'date':'2026-10-11','edition':'gui-examples-16-sessions','baseline':'previous-reports/20261011-before-gui-examples',
 'added_page_ids':['ch08-gui-example','ch15-gui-layout'],'changed_page_ids':changed,
 'added_asset':'assets/source-20261011/save-gui-layout.png','added_asset_source_pdf_page':118,
 'new_placement':{'src':'assets/source-20261006/field-copy.png','page_id':'ch08-gui-example'},
 'expected_containers':162,'expected_practices':37,'expected_python_blocks':7,'expected_output_blocks':0,
 'notes':['기존 실습의 배치·위젯 이름·역할·버튼 동작을 설명','계산기 결과fld3과 표fld1~fld4 역할을 구분','저장 디자이너사진은 실행결과사진과 용도를 구분']}
write('gui-examples-revision.json',json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'containers':162,'assets':len(manifest['items']),'placements':sum(len(x['placements']) for x in manifest['items']),'changed':changed},ensure_ascii=False))
