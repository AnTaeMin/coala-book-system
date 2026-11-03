"""Synchronize current curriculum indexes after the explicit lesson migration."""
from pathlib import Path
import json
import re
import hashlib
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
BOOK=ROOT/'coala-book-md/vibe-coding-16'
BASE=BOOK/'previous-reports/20261011-before-no-pandas-divider'

def load(name, base=BOOK):
    return json.loads((base/name).read_text(encoding='utf-8'))

def save(name, value):
    (BOOK/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

revision=load('no-pandas-restructure.json')
mapping=revision['old_to_new']
texts=[(BOOK/f'ch{n:02d}.md').read_text(encoding='utf-8') for n in range(1,17)]
all_text='\n'.join(texts)
parts=re.findall(r':::page\{.*?\n:::',all_text,re.S)
ids=[re.search(r'id="([^"]+)"',p)[1] for p in parts]
expected={v for v in mapping.values() if v}|{'book-guide'}
revision['added_pages']=sorted(set(ids)-expected)
revision['expected_containers']=len(ids)+1
assert revision['expected_containers']==160
save('no-pandas-restructure.json',revision)

catalog=load('practice-source-map.json',BASE)
by_id={v['page_id']:v for v in catalog['practices']}
new=[]
for p in parts:
    if 'type="practice-opening"' not in p: continue
    pid=re.search(r'id="([^"]+)"',p)[1]
    old_id=next(k for k,v in mapping.items() if v==pid and k in by_id)
    item=dict(by_id[old_id]); item['page_id']=pid
    item['chapter']=int(pid[2:4]);item['practice_id']=re.search(r'practice="([^"]+)"',p)[1]
    item['title']=re.search(r'^# (.*)$',p,re.M)[1]
    item['completion_criteria']=re.findall(r'^- \[ \] (.*)$',p,re.M)
    new.append(item)
catalog.update(practices=new,edition='no-pandas-16-sessions',reviewed_date='2026-10-11')
assert len(new)==37
save('practice-source-map.json',catalog)

manifest=load('asset-manifest.json',BASE)
items=[x for x in manifest['items'] if not x['src'].endswith(('pandas-table.png','image-divider.png'))]
for x in items:
    if x.get('chapter') in (12,13,14):
        if x['chapter']==12 and any(p.startswith('ch12-') and p in mapping and mapping[p].startswith('ch13-') for p in x.get('used_in',[])): x['chapter']=13
        elif x['chapter']==13: x['chapter']=14
        elif x['chapter']==14: x['chapter']=15
    if x.get('kind')=='executed-source-code-adaptation':
        spec=next(s for s in load('code-specs.json') if s.get('result')==Path(x['src']).stem)
        x['code']='examples/source-based/'+spec['page_id']+'.py'

src=BOOK/'assets/ch10/two-images.png';vector=src.with_suffix('.pdf')
items.append({'src':'assets/ch10/two-images.png','chapter':10,'width':266,'height':232,'ratio':'266:232',
 'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'kind':'source-derived-vector-illustration',
 'pdf_page':85,'xobject':['/X18','/X9'],'source_asset':'assets/source-20261006/image-divider.png',
 'source_asset_sha256':hashlib.sha256((BASE/'assets/source-20261006/image-divider.png').read_bytes()).hexdigest(),
 'crop_bbox_top_left_px':[[37,10,133,108],[37,118,133,214]],
 'vector_src':'assets/ch10/two-images.pdf','vector_sha256':hashlib.sha256(vector.read_bytes()).hexdigest(),
 'pixel_text_modified':False,'upscaled':False,
 'derivation':'원본 사진 픽셀을 무손실 PDF 이미지로 임베딩하고 사진 영역만 클리핑. 구분선 제외. 새 GUI 실행 화면은 아님.'})
source_pdf=(BOOK/manifest['source_pdf']).resolve(); reader=PdfReader(source_pdf)
for name,page,num in [('save-table-toggle',119,1),('save-table-columns',119,2),('save-project-menu',124,1),('save-project-name',125,1),('load-project-select',126,1)]:
    relative=f'assets/source-20261011/{name}.png'; path=BOOK/relative
    with Image.open(path) as im: w,h=im.size
    native=list(reader.pages[page-1].images)[num-1]
    assert hashlib.sha256(path.read_bytes()).hexdigest()==hashlib.sha256(native.data).hexdigest(),(name,native.name)
    item={'src':relative,'chapter':15,'width':w,'height':h,'ratio':f'{w}:{h}',
      'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'kind':'user-supplied-pdf-embedded-image',
      'pdf_page':page,'xobject':['/'+k for k in native.name.rsplit('.',1)[0].split('.')],
      'pixel_text_modified':False,'upscaled':False,'source_image_index':num}
    if name=='save-table-toggle':
        item.update(src='assets/ch15/save-table-toggle.png',width=208,height=84,ratio='208:84',
          sha256=hashlib.sha256((BOOK/'assets/ch15/save-table-toggle.png').read_bytes()).hexdigest(),
          kind='source-derived-vector-illustration',source_asset=relative,
          source_asset_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
          crop_bbox_top_left_px=[[148,0,356,84]],vector_src='assets/ch15/save-table-toggle.pdf',
          vector_sha256=hashlib.sha256((BOOK/'assets/ch15/save-table-toggle.pdf').read_bytes()).hexdigest(),
          derivation='원본 도구막대를 PDF 이미지로 무손실 임베딩하고 표 저장 옵션 영역만 클리핑. 문자·상태 수정 없음.')
    items.append(item)

placements={}
for p in parts:
    pid=re.search(r'id="([^"]+)"',p)[1]
    for directive in re.findall(r'::image\{([^\n]*)\}',p):
        a=dict(re.findall(r'([\w-]+)="([^"]*)"',directive))
        placements.setdefault(a['src'],[]).append({'page_id':pid,'width':a.get('width','text'),'caption':a.get('caption','')})
for x in items:
    if x['kind']=='user-supplied-pdf-native-vector-crop':
        placements[x['src']]=x['placements']
    x['placements']=placements[x['src']]
    x['used_in']=[v['page_id'] for v in x['placements']]
    x['placement_width']=x['placements'][0]['width']
    if x.get('chapter'): x['chapter']=int(x['used_in'][0][2:4])
assert set(placements)=={x['src'] for x in items}
manifest.update(items=items,reviewed_date='2026-10-11',edition='no-pandas-16-sessions')
save('asset-manifest.json',manifest)
print(json.dumps({'containers':160,'practices':37,'assets':len(items),'placements':sum(len(x['placements']) for x in items),'added_pages':revision['added_pages']},ensure_ascii=False))
