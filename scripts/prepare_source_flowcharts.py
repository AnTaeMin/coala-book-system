"""Reuse the supplied textbook's native diagrams without redrawing them.

Requires PyMuPDF for removing only material outside each diagram's crop.
The completed textbook embeds the cropped PDF vectors; PNGs are Canva assets.
"""
from pathlib import Path
import hashlib
import json
import re
import sys
import io
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject, NumberObject

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / 'tmp/pdf-source-tools').is_dir():
    sys.path.insert(0, str(ROOT / 'tmp/pdf-source-tools'))
import pymupdf

BOOK = ROOT / 'coala-book-md/vibe-coding-16'
ASSETS = BOOK / 'assets/source-flowcharts'
ASSETS.mkdir(parents=True, exist_ok=True)
SOURCE = ROOT / json.loads((BOOK/'flow-source-map.json').read_text(encoding='utf-8'))['source_pdf']
SHA = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
CONFIG = [
    ('ch04-family-flow', 4, 23, (243, 360, 862, 1356), 545, '가족 나이 합의 변수 준비·값 저장·합계 계산·출력'),
    ('ch05-exercise-flow', 5, 31, (204, 360, 901, 1356), 540, '운동 시간의 초기값·반복 조건·누적·증가·출력'),
    ('ch06-sleep-flow', 6, 36, (51, 840, 1178, 1524), 330, '수면 시간의 8시간·5시간 조건 분기'),
    ('ch07-movie-flow', 7, 39, (235, 461, 971, 1442), 545, '네 학생 나이의 반복과 15세 관람 조건'),
]

# Match the surrounding lesson to the actual diagrams, retaining the separate
# N-student/80-point practice and all Python programs.
ch4 = BOOK / 'ch04.md'
t = ch4.read_text(encoding='utf-8')
t = t.replace('값 준비, 입력, 처리, 출력이 서로 다른 역할임을 확인합니다.',
              '변수 준비, 나이값 저장, 합계 계산, 결과 출력의 순서를 확인합니다.')
t = t.replace('text: momage, dadage, myage, total 준비',
              'text: momage = 0, dadage = 0, myage = 0, total = 0')
t = t.replace('role: input\n    text: 43, 45, 15 입력',
              'role: process\n    text: momage = 43, dadage = 45, myage = 15')
t = t.replace('입력 나이가 달라지면 처리 식은 유지되고 총합이 달라집니다.',
              '저장하는 나이가 달라지면 계산식은 유지되고 총합이 달라집니다.')
ch4.write_text(t, encoding='utf-8')

movie = ''':::page{type="flowchart" id="ch07-movie-flow" height="1050"}
# 영화 관람의 반복과 분기

학생 네 명의 나이를 입력받고 관람 조건을 판단하는 흐름입니다.

```flowchart
control_structure: loop
nodes:
  - id: start
    role: declaration
    text: i = 0, age = 0
  - id: loop
    role: decision
    text: i < 4인가?
  - id: input
    role: input
    text: 학생 나이 입력
  - id: condition
    role: decision
    text: age < 15인가?
  - id: yes
    role: output
    text: 관람불가 출력
  - id: no
    role: output
    text: 관람가능 출력
  - id: next
    role: process
    text: i = i + 1
connections:
  - from: start
    to: loop
  - from: loop
    to: input
    label: YES
  - from: input
    to: condition
  - from: condition
    to: yes
    label: YES
  - from: condition
    to: no
    label: NO
  - from: yes
    to: next
  - from: no
    to: next
  - from: next
    to: loop
```

반복 상자 안에서 나이 입력·판단·결과 출력을 네 번 수행합니다. age < 15가 참이면 관람불가, 거짓이면 관람가능입니다.
:::'''
ch7 = BOOK / 'ch07.md'
t = ch7.read_text(encoding='utf-8')
t = re.sub(r':::page\{[^\n]*id="ch07-(?:pass|movie)-flow"[^\n]*\}.*?\n:::', movie, t, flags=re.S)
flow = re.search(r':::page\{[^\n]*id="ch07-movie-flow"[^\n]*\}.*?\n:::', t, re.S).group()
steps = re.search(r':::page\{[^\n]*id="ch07-movie-code"[^\n]*\}.*?\n:::', t, re.S).group()
t = t.replace(flow, '').replace(steps, steps + '\n\n' + flow)
t = re.sub(r'\n{4,}', '\n\n', t)
ch7.write_text(t, encoding='utf-8')

revision_path = BOOK / 'page-restructure.json'
revision = json.loads(revision_path.read_text(encoding='utf-8'))
revision['old_to_new']['ch07-pass-flow'] = 'ch07-movie-flow'
revision['original_flow_reuse'] = {'date': '2026-10-11', 'replacement': 'ch07-pass-flow -> ch07-movie-flow',
    'reason': 'Reuse the supplied movie diagram; retain N/80-point practice as written steps.'}
revision_path.write_text(json.dumps(revision, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

items = []
for sid, chapter, number, bbox, max_height, alt in CONFIG:
    reader = PdfReader(SOURCE)
    source_page = reader.pages[number-1]
    changed = []
    def whiten_background(obj):
        stream = ContentStream(obj, reader)
        for i, (args, op) in enumerate(stream.operations):
            if (op in (b'rg', b'RG') and len(args)==3
                    and all(abs(float(a)-b)<.0001 for a,b in zip(args, (.9725,.9765,.9804)))
                    and any(next_op==b're' and list(map(float,next_args))==[0.,0.,1587.,2245.]
                            for next_args,next_op in stream.operations[i+1:i+8])):
                stream.operations[i] = ([NumberObject(1)]*3, op)
                changed.append(op.decode())
        obj._data = stream.get_data()
        obj.pop(NameObject('/Filter'), None)
        obj.pop(NameObject('/DecodeParms'), None)
        for child in obj.get('/Resources', {}).get('/XObject', {}).values():
            form = child.get_object()
            if form.get('/Subtype') == '/Form':
                whiten_background(form)
    for child in source_page['/Resources'].get('/XObject', {}).values():
        obj = child.get_object()
        if obj.get('/Subtype') == '/Form':
            whiten_background(obj)
    assert changed == ['RG','rg'], (number, changed)
    writer = PdfWriter(); writer.add_page(source_page)
    buffer = io.BytesIO(); writer.write(buffer)
    doc = pymupdf.open(stream=buffer.getvalue(), filetype='pdf')
    # Remove only text outside the crop; preserve every native diagram path.
    page = doc[0]
    box = pymupdf.Rect(bbox)
    outer = page.rect
    margins = [pymupdf.Rect(0,0,outer.width,box.y0),
               pymupdf.Rect(0,box.y1,outer.width,outer.height),
               pymupdf.Rect(0,box.y0,box.x0,box.y1),
               pymupdf.Rect(box.x1,box.y0,outer.width,box.y1)]
    for rect in margins:
        page.add_redact_annot(rect, fill=(1,1,1))
    page.apply_redactions(images=0, graphics=0, text=0)
    page.set_cropbox(box)
    vector = ASSETS / (sid + '.pdf')
    preview = ASSETS / (sid + '.png')
    doc.save(vector, garbage=4, deflate=True)
    page.get_pixmap(dpi=300, alpha=False).save(preview)
    image = pymupdf.Pixmap(preview)
    fences = re.findall(r'```flowchart\s*\n(.*?)^```\s*$', (BOOK/f'ch{chapter:02d}.md').read_text(encoding='utf-8'), re.M|re.S)
    assert len(fences)==1
    items.append({'page_id':sid,'chapter':chapter,'source_pdf_page':number,
        'crop_bbox_top_left_pt':list(bbox),'vector_src':vector.relative_to(BOOK).as_posix(),
        'src':preview.relative_to(BOOK).as_posix(),'vector_sha256':SHA(vector),
        'sha256':SHA(preview),'width':image.width,'height':image.height,
        'ratio':f'{image.width}:{image.height}','max_print_height_pt':max_height,
        'kind':'user-supplied-pdf-native-vector-crop','alt':alt,
        'background':'full-page background changed to white; external text removed; all diagram paths/colors unchanged',
        'flowchart_sha256':hashlib.sha256(fences[0].encode('utf-8')).hexdigest()})
    doc.close()
mapping = {'source_pdf':str(SOURCE.relative_to(ROOT)).replace('\\','/'),
           'source_sha256':SHA(SOURCE),'date':'2026-10-11','diagrams':items,
           'declaration_shape':'six-sided preparation symbol preserved from source',
           'loop_trace':{'start':{'time1':1,'total':0},'condition':'time1 <= 10',
                         'updates':['total = total + time1','time1 += 1'],
                         'iterations':10,'exit':{'time1':11,'total':55}}}
(BOOK/'flow-source-map.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
manifest_path = BOOK/'asset-manifest.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
manifest['items'] = [i for i in manifest['items'] if not i['src'].startswith('assets/source-flowcharts/')]
for item in items:
    manifest['items'].append({**item,'pdf_page':item['source_pdf_page'],'used_in':[item['page_id']],
        'placement_width':'full','placements':[{'page_id':item['page_id'],'width':'full','caption':item['alt']}],
        'pixel_text_modified':False,'upscaled':False})
manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared 4 native vector diagrams and 300-dpi Canva images; retained all practice programs.')
