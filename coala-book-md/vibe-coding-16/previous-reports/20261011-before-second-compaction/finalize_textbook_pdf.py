"""Approved standalone print edition, derived from the validated manuscript.

This edition uses independently typeset vector pages. It does not claim Canva
native template/asset fidelity. The user explicitly accepted that limitation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter, Transformation

from build_textbook_pdf import (ROOT, BOOK, W, H, LEFT, RIGHT, TOP, BOTTOM,
    WIDTH, BODY, HEADING, LEADING, INK, INDIGO, GRAY, Production, fonts,
    wrap, text_width, draw_text, draw_block)

SHORT_TITLES = [
    'AI와 앱 개발', '질문과 입력', '문제 나누기', '순서도와 변수',
    '반복과 누적', '조건과 분기', '반복 속 조건', '첫 앱 화면',
    '계산과 출력', '선택 위젯', '표와 성적', '그래프 코딩',
    '차트 바이브 코딩', '자료와 저장', '데이터 정리', '앱 개선·발표',
]


class FinalProduction(Production):
    def __init__(self, spec):
        super().__init__(spec)
        self.context = None
        self.merges = []
        self.flow_sources = {i['page_id']: i for i in json.loads((BOOK/'flow-source-map.json').read_text(encoding='utf-8'))['diagrams']}
        self.summary_asset = json.loads((BOOK/'intro-summary-map.json').read_text(encoding='utf-8'))

    def regular(self, source):
        if source['type'] == 'practice-checklist':
            # Keep the actual completion criteria, without creating another
            # nearly empty page solely for an automatically added writing area.
            self.start(source)
            for item in source['items']:
                self.paragraph(item, indent=22, bullet='check')
            if source.get('tip'):
                self.box(source['tip'], '핵심 정리', color='#FFF9D9')
            return
        if source['type'] != 'concept' or not any(
            '```python' in s.get('content', '') for s in source.get('sections', [])
        ):
            super().regular(source)
            return
        self.start(source)
        if source.get('introduction'):
            self.paragraph(source['introduction'])
        for section in source['sections']:
            content = section.get('content', section.get('body', ''))
            if section['title'] != '예제 코드 실행하기':
                self.heading(section['title'])
            self.markdown(content)
        if source.get('tip'):
            self.box(source['tip'], 'Tip', color='#EAF1FF')

    def image(self, attributes):
        attrs = dict(attributes)
        if attrs.get('src') == self.summary_asset['src']:
            asset = self.summary_asset
            caption = wrap(attrs.get('caption', attrs.get('alt', '')), WIDTH, size=11)
            self.add({'kind': 'vector-image', 'src': asset['src'], 'vectorAsset': asset['vector_src'],
                      'vectorSha256': asset['vector_sha256'], 'printWidthPt': WIDTH,
                      'imageHeight': asset['print_height_pt'], 'caption': caption,
                      'height': asset['print_height_pt']+len(caption)*18+12,
                      'x': LEFT}, gap=18)
            self.images.append({'src': asset['src'], 'pixels': [asset['width'], asset['height']],
                                'printWidthPt': WIDTH, 'effectiveDpi': 300,
                                'sourceId': self.current_source['id'], 'format': 'generated-vector-pdf',
                                'vectorAsset': asset['vector_src'], 'vectorSha256': asset['vector_sha256']})
            return
        if attrs.get('role') == 'result' and 'plot-' in attrs.get('src', ''):
            # The result caption already names the output. Avoid a duplicate
            # heading between its code and graph; keep the image at full width.
            attrs.pop('role', None)
        super().image(attrs)

    def chapter_opening(self, source):
        self.chapter = source['chapterNumber']
        self.context = None
        self.start(source)
        self.page['source'] = source
        self.page['title'] = SHORT_TITLES[self.chapter - 1]
        # The large title has its own upper frame, leaving body typography intact.
        self.page['y'] = 244
        self.heading('학습 목표')
        self.paragraph('이 차시를 마치면 다음을 할 수 있습니다.')
        for item in source['learningObjectives']:
            self.paragraph(item, indent=22, bullet='dot')
        self.page['y'] += 13
        self.heading(source.get('subsectionTitle', '오늘의 시작'))
        self.markdown(source.get('body', ''))
        if self.page is not self.pages[-1] or self.page['type'] != 'chapter-opening':
            raise ValueError('Chapter overflow needs explicit editorial split')

    def practice_opening(self, source):
        self.context = source['id']
        self.start(source)
        self.page['source'] = source
        title_lines = wrap(source['title'], WIDTH - 44, 'WantedBold', HEADING)
        description = wrap(source['description'], WIDTH - 44)
        card_h = 106 + len(title_lines) * 30 + len(description) * LEADING + 26
        self.add({'kind': 'practice', 'source': source, 'titleLines': title_lines,
                  'descriptionLines': description, 'height': card_h}, gap=24)
        if source.get('tip'):
            self.box(source['tip'], 'Tip', color='#EAF1FF')
        self.heading('실습 완료 기준')
        objectives = source.get('objectives', [])
        if not objectives:
            raise ValueError(f'Missing source-specific practice objectives: {source["id"]}')
        for text in objectives:
            self.paragraph(text, indent=22, bullet='check')
        if self.space() >= 95:
            # These lines belong to the objective checklist, not a second lesson.
            self.add({'kind': 'objective-evidence', 'height': min(self.space()-8, 120)}, gap=0)

    def diagram(self, source):
        self.start(source)
        if source.get('introduction'):
            self.paragraph(source['introduction'])
        asset = self.flow_sources[source['id']]
        x0, y0, x1, y1 = asset['crop_bbox_top_left_pt']
        conclusion_h = len(wrap(source.get('conclusion', ''), WIDTH)) * LEADING
        scale = min(WIDTH/(x1-x0), asset['max_print_height_pt']/(y1-y0),
                    (self.space()-conclusion_h-32)/(y1-y0))
        width, height = (x1-x0)*scale, (y1-y0)*scale
        self.add({'kind': 'flowchart', 'source': source, 'height': height,
                  'vectorAsset': asset['vector_src'], 'vectorSha256': asset['vector_sha256'],
                  'printWidthPt': width, 'x': LEFT+(WIDTH-width)/2}, gap=12)
        self.images.append({'src':asset['src'],'pixels':[asset['width'],asset['height']],
            'printWidthPt':width,'effectiveDpi':round(asset['width']/width*72,1),
            'sourceId':source['id'],'format':'native-vector-pdf',
            'vectorAsset':asset['vector_src'],'vectorSha256':asset['vector_sha256']})
        if source.get('conclusion'):
            self.paragraph(source['conclusion'])

    def compact_regular(self, source):
        before = len(self.pages)
        previous = self.pages[-1] if self.pages else None
        self.regular(source)
        added = self.pages[before:]
        for page in added:
            page['context'] = self.context
        # Pack consecutive explanations in one chapter or practice. Earlier
        # editions unnecessarily blocked all pre-practice concept/table merges.
        if previous and len(added) == 1 and previous['chapter'] == self.chapter and previous.get('context') == self.context:
            p = added[0]
            if previous['type'] not in ('cover', 'contents', 'practice-opening', 'flowchart'):
                content_h = p['y'] - TOP
                available = H - BOTTOM - previous['y']
                title_lines = wrap(p['title'], WIDTH, 'WantedBold', HEADING)
                connector_h = len(title_lines) * 30 + 10
                if content_h + connector_h <= available and not any(b['kind'] == 'writing' for b in previous['blocks']):
                    offset = previous['y'] + connector_h - TOP
                    previous['blocks'].append({'kind': 'heading', 'lines': title_lines,
                        'font': 'WantedBold', 'size': HEADING, 'leading': 30, 'indent': 0, 'bullet': None,
                        'height': len(title_lines) * 30, 'y': previous['y'] + 6})
                    for block in p['blocks']:
                        block['y'] += offset
                        previous['blocks'].append(block)
                    previous['y'] += content_h + connector_h
                    previous.setdefault('includedSources', [previous['id']]).append(source['id'])
                    self.pages.pop()
                    self.page = previous
                    self.merges.append([previous['id'], source['id']])

    def plan(self):
        self.pages = [
            {'id': 'cover', 'type': 'cover', 'chapter': 0, 'title': self.spec['title'], 'blocks': []},
            {'id': 'toc-1', 'type': 'contents', 'chapter': 0, 'title': '학습 차례', 'part': 0, 'blocks': []},
            {'id': 'toc-2', 'type': 'contents', 'chapter': 0, 'title': '학습 차례', 'part': 1, 'blocks': []},
        ]
        for source in self.spec['pages']:
            kind = source['type']
            if kind == 'chapter-opening':
                self.chapter_opening(source)
            elif kind == 'practice-opening':
                self.practice_opening(source)
            elif kind == 'flowchart':
                self.diagram(source)
            else:
                self.compact_regular(source)
        self.chapter_pages = {p['chapter']: i for i, p in enumerate(self.pages, 1) if p['type'] == 'chapter-opening'}


def centered(c, text, cx, top, font='WantedBold', size=14, color=INK):
    draw_text(c, text, cx - text_width(text, font, size) / 2, top, font, size, color)


def embed_source_diagrams(production, output):
    reader = PdfReader(output)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    inserted = 0
    summaries = 0
    for index, page in enumerate(production.pages):
        for block in page['blocks']:
            if block['kind'] not in ('flowchart', 'vector-image'):
                continue
            path = BOOK / block['vectorAsset']
            if hashlib.sha256(path.read_bytes()).hexdigest() != block['vectorSha256']:
                raise ValueError(f'Diagram source hash mismatch: {path}')
            source = PdfReader(path).pages[0]
            crop = source.cropbox
            factor = block['printWidthPt'] / float(crop.width)
            image_height = block.get('imageHeight', block['height'])
            transform = (Transformation().translate(-float(crop.left), -float(crop.bottom))
                         .scale(factor).translate(block['x'], H-block['y']-image_height))
            writer.pages[index].merge_transformed_page(source, transform, over=True)
            inserted += block['kind'] == 'flowchart'
            summaries += block['kind'] == 'vector-image'
    assert inserted == 4
    assert summaries == 1
    staged = output.with_name(output.stem+'-staged.pdf')
    writer.write(staged)
    staged.replace(output)


def draw_practice(c, b):
    source = b['source']; top = b['y']
    c.setFillColor(white); c.setStrokeColor(HexColor(INDIGO)); c.setLineWidth(1.1)
    c.roundRect(LEFT, H-top-b['height'], WIDTH, b['height'], 12, fill=1, stroke=1)
    labels = [(source['practiceId'], '#FFFAB3', INDIGO), (source['practiceKind'], INDIGO, '#FFFFFF')]
    x = LEFT+22
    for label, fill, color in labels:
        lw = text_width(label, 'WantedBold', 11) + 24
        c.setFillColor(HexColor(fill)); c.roundRect(x,H-top-49,lw,29,12,fill=1,stroke=0)
        draw_text(c, label,x+12,top+28,'WantedBold',11,color); x += lw+10
    draw_text(c, source.get('platform','교실 실습'), LEFT+22, top+65, 'WantedMedium', 10, GRAY)
    y = top+91
    for line in b['titleLines']:
        draw_text(c,line,LEFT+22,y,'WantedBold',HEADING,INK); y+=30
    y+=13
    for line in b['descriptionLines']:
        draw_text(c,line,LEFT+22,y); y+=LEADING


def draw_cover(c, spec):
    draw_text(c,'16차시 학생용 교재',LEFT,78,'WantedBold',15,INDIGO)
    c.setStrokeColor(HexColor(INDIGO)); c.setLineWidth(2); c.line(LEFT,H-122,W-RIGHT,H-122)
    for i, line in enumerate(['AI와 함께하는','바이브 코딩']):
        draw_text(c,line,LEFT,185+i*83,'WantedBold',42,INK)
    draw_text(c,'요청 · 설계 · 실행 · 확인 · 수정',LEFT,402,'WantedBold',17,INDIGO)
    for i,line in enumerate(['개념을 익히고 실습으로 배우는','Python · Flet · 데이터 · 프로젝트']):
        draw_text(c,line,LEFT,472+i*38,'WantedMedium',20)
    draw_text(c,'작게 만들고 직접 검증하며',LEFT,627,'WantedMedium',17)
    draw_text(c,'나만의 앱으로 완성합니다.',LEFT,665,'WantedMedium',17)
    draw_text(c,'2026 · 16차시 실습 교재',LEFT,755,'WantedMedium',11,GRAY)


def draw_contents(c, production, part):
    draw_text(c,'학습 차례',LEFT,67,'WantedBold',25,INDIGO)
    draw_text(c,'01-08차시 · 코딩과 앱의 기초' if part == 0 else '09-16차시 · 데이터와 프로젝트',LEFT,136,'WantedBold',15)
    y = 205
    for ch in range(part*8+1,part*8+9):
        draw_text(c,f'{ch:02d}',LEFT,y,'WantedBold',17,INDIGO)
        draw_text(c,SHORT_TITLES[ch-1],LEFT+53,y,'WantedMedium',15)
        c.setFont('WantedMedium',14); c.setFillColor(HexColor(GRAY)); c.drawRightString(W-RIGHT,H-y-12,str(production.chapter_pages[ch]))
        c.linkRect('',f'ch{ch:02d}',(LEFT,H-y-35,W-RIGHT,H-y+12),relative=0,thickness=0)
        c.setStrokeColor(HexColor('#DDE3EC')); c.setLineWidth(.65); c.line(LEFT,H-y-35,W-RIGHT,H-y-35)
        y+=65
    draw_text(c,'쪽수는 표지부터 계산합니다.',LEFT,760,'WantedMedium',10,GRAY)


def render_final(production, output):
    output.parent.mkdir(parents=True,exist_ok=True)
    c=canvas.Canvas(str(output),pagesize=(W,H),pageCompression=1)
    c.setTitle(production.spec['title']); c.setAuthor('Coala'); c.setSubject('16차시 바이브 코딩 실습 교재')
    for number,p in enumerate(production.pages,1):
        c.setFillColor(white); c.rect(0,0,W,H,fill=1,stroke=0)
        if p['type']=='cover':
            draw_cover(c,production.spec)
        elif p['type']=='contents':
            draw_contents(c,production,p['part'])
        else:
            label = f"{p['chapter']:02d}차시  {SHORT_TITLES[p['chapter']-1]}" if p['chapter'] else '교재 안내'
            draw_text(c,label,LEFT,24,'WantedMedium',10,GRAY)
            c.setStrokeColor(HexColor('#DDE3EC')); c.setLineWidth(.7); c.line(LEFT,H-46,W-RIGHT,H-46)
            if p['type']=='chapter-opening':
                source=p['source']; title=p['title']
                c.setStrokeColor(HexColor(INDIGO)); c.setLineWidth(1.2)
                c.roundRect(LEFT+18,H-206,WIDTH-18,116,14,fill=0,stroke=1)
                c.setFillColor(HexColor(INDIGO)); c.circle(LEFT+23,H-93,23,fill=1,stroke=0)
                centered(c,str(p['chapter']),LEFT+23,82,'WantedBold',18,'#FFFFFF')
                draw_text(c,title,LEFT+58,112,'WantedBold',25)
                for i,line in enumerate(wrap(source['chapterTitle'],WIDTH-85,'WantedMedium',15)):
                    draw_text(c,line,LEFT+58,158+i*30,'WantedMedium',15,GRAY)
                c.bookmarkPage(f'ch{p["chapter"]:02d}'); c.addOutlineEntry(f'{p["chapter"]:02d} {source["chapterTitle"]}',f'ch{p["chapter"]:02d}',level=0)
            else:
                title=wrap(p['title'],WIDTH,'WantedBold',HEADING)
                if len(title)>1:
                    raise ValueError(f'Page header overflow: {p["title"]}')
                draw_text(c,title[0],LEFT,65,'WantedBold',HEADING,INDIGO)
            for b in p['blocks']:
                if b['kind']=='practice':
                    draw_practice(c,b)
                elif b['kind']=='flowchart':
                    pass  # Insert the preserved source PDF vectors after typesetting.
                elif b['kind']=='vector-image':
                    for i,line in enumerate(b['caption']):
                        draw_text(c,line,LEFT,b['y']+b['imageHeight']+10+i*18,'WantedMedium',11,GRAY)
                elif b['kind']=='objective-evidence':
                    draw_text(c,'완료 기준을 확인한 근거',LEFT,b['y'],'WantedBold',HEADING,INDIGO)
                    c.setStrokeColor(HexColor('#CBD3E0')); c.setLineWidth(.65)
                    for yy in range(int(b['y']+47),int(b['y']+b['height']),35):
                        c.line(LEFT,H-yy,W-RIGHT,H-yy)
                elif b['kind']=='writing' and b.get('question'):
                    draw_text(c,b['label'],LEFT,b['y'],'WantedBold',15,INDIGO)
                    lines=wrap(b['question'],WIDTH)
                    for i,line in enumerate(lines):
                        draw_text(c,line,LEFT,b['y']+37+i*28)
                    c.setStrokeColor(HexColor('#CBD3E0')); c.setLineWidth(.65)
                    for yy in range(int(b['y']+45+len(lines)*28),int(b['y']+b['height']),35):
                        c.line(LEFT,H-yy,W-RIGHT,H-yy)
                else:
                    draw_block(c,b)
        if p['type']!='cover':
            draw_text(c,'AI와 함께하는 바이브 코딩',LEFT,H-30,'WantedMedium',9,GRAY)
            c.setFillColor(HexColor(GRAY));c.setFont('WantedMedium',10);c.drawRightString(W-RIGHT,22,str(number))
        c.showPage()
    c.save()
    embed_source_diagrams(production, output)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'output/pdf/vibe-coding-16-graph-first.pdf')
    args=parser.parse_args()
    archive = BOOK/'previous-reports/20261011-before-page-compaction'
    archive.mkdir(parents=True, exist_ok=True)
    for path in (args.output, args.output.with_suffix('.json'), args.output.with_name(args.output.stem+'-qa.json')):
        if path.exists() and not (archive/path.name).exists():
            shutil.copy2(path, archive/path.name)
    fonts();spec=json.loads((ROOT/'tmp/pdfs/book-spec.json').read_text(encoding='utf-8'))
    production=FinalProduction(spec);production.plan()
    render_final(production,args.output)
    report={'mode':'approved-standalone-print-edition','date':'2026-10-11','pages':len(production.pages),
        'manuscriptSha256':hashlib.sha256((BOOK/'book.md').read_bytes()).hexdigest(),
        'pdfSha256':hashlib.sha256(args.output.read_bytes()).hexdigest(),
        'pageTypes':dict(Counter(p['type'] for p in production.pages)),
        'chapterPages':production.chapter_pages,'images':production.images,'merges':production.merges,
        'limitations':['Canva 원본 틀과 정확히 일치하지 않는 독립 PDF 배치',
            '순서도는 제공 교재에서 추출한 PDF 벡터 도형·글꼴을 그대로 사용',
            '원본 캡처의 해상도는 보존하며 화질 복원 또는 재촬영을 주장하지 않음'],
        'layout':production.pages}
    args.output.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('pages','pageTypes','chapterPages')},ensure_ascii=False))


if __name__=='__main__':
    main()
