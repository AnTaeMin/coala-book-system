"""Approved standalone print edition, derived from the validated manuscript.

This edition uses independently typeset vector pages. It does not claim Canva
native template/asset fidelity. The user explicitly accepted that limitation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from collections import Counter
from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

from build_textbook_pdf import (ROOT, BOOK, W, H, LEFT, RIGHT, TOP, BOTTOM,
    WIDTH, BODY, HEADING, LEADING, INK, INDIGO, GRAY, Production, fonts,
    wrap, text_width, draw_text, draw_block)

SHORT_TITLES = [
    'AI와 앱 개발', '질문과 입력', '문제 나누기', '순서도와 변수',
    '반복과 누적', '조건과 분기', '반복 속 조건', '첫 앱 화면',
    '계산과 출력', '선택 위젯', '표와 성적', '차트 시각화',
    '자료와 저장', '그래프 코딩', '데이터 정리', '앱 개선·발표',
]


class FinalProduction(Production):
    def __init__(self, spec):
        super().__init__(spec)
        self.context = None
        self.merges = []

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
        self.paragraph(source.get('body', ''))
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
        heights = {'ch04-family-flow': 450, 'ch05-exercise-flow': 510,
                   'ch06-sleep-flow': 527, 'ch07-pass-flow': 545}
        self.add({'kind': 'flowchart', 'source': source, 'height': heights[source['id']]}, gap=12)
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


def stroke_path(c, points, fill, stroke, close=True):
    p = c.beginPath()
    p.moveTo(points[0][0], H - points[0][1])
    for x, y in points[1:]:
        p.lineTo(x, H - y)
    if close:
        p.close()
    c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke)); c.setLineWidth(1.2)
    c.drawPath(p, stroke=1, fill=int(close))


def arrow(c, points, label=None, label_xy=None):
    c.setStrokeColor(HexColor(GRAY)); c.setFillColor(HexColor(GRAY)); c.setLineWidth(1.1)
    p = c.beginPath(); p.moveTo(points[0][0], H - points[0][1])
    for x, y in points[1:]:
        p.lineTo(x, H - y)
    c.drawPath(p, stroke=1)
    a, b = points[-2], points[-1]
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    wings = [(b[0] - 6 * math.cos(angle + d), b[1] - 6 * math.sin(angle + d)) for d in (-.45, .45)]
    stroke_path(c, [b, wings[0], wings[1]], GRAY, GRAY)
    if label:
        x, y = label_xy
        centered(c, label, x, y, 'Flow', 14, GRAY)


def node(c, role, text, x, y, w, h):
    colors = {'declaration': ('#FFFAB3', '#F3B96B'), 'input': ('#DFF1FE', INDIGO),
              'process': ('#D9FAD3', '#00BF63'), 'output': ('#FFF3E8', '#F3B96B'),
              'decision': ('#FFDEE7', '#FF5757')}
    fill, stroke = colors[role]
    if role == 'decision':
        stroke_path(c, [(x+w/2, y), (x+w, y+h/2), (x+w/2, y+h), (x, y+h/2)], fill, stroke)
        inner = w * .57
    elif role == 'input':
        stroke_path(c, [(x+17, y), (x+w, y), (x+w-17, y+h), (x, y+h)], fill, stroke)
        inner = w - 38
    elif role == 'declaration':
        stroke_path(c, [(x, y), (x+w, y), (x+w, y+h-12), (x+w/2, y+h), (x, y+h-12)], fill, stroke)
        inner = w - 30
    elif role == 'output':
        p = c.beginPath(); p.moveTo(x, H-y); p.lineTo(x+w, H-y); p.lineTo(x+w, H-y-h+8)
        p.curveTo(x+w*.66, H-y-h+26, x+w*.33, H-y-h-10, x, H-y-h+8); p.close()
        c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke)); c.setLineWidth(1.2); c.drawPath(p, fill=1, stroke=1)
        inner = w - 22
    else:
        c.setFillColor(HexColor(fill)); c.setStrokeColor(HexColor(stroke)); c.setLineWidth(1.2)
        c.roundRect(x, H-y-h, w, h, 5, stroke=1, fill=1)
        inner = w - 24
    lines = wrap(text, inner, 'Flow', 14)
    if len(lines) * 28 > h - (24 if role == 'decision' else 16):
        raise ValueError(f'Flow node overflow: {text}')
    top = y + (h - len(lines) * 28) / 2 + 7 - (4 if role == 'output' else 0)
    for i, line in enumerate(lines):
        centered(c, line, x + w/2, top + i*28, 'Flow', 14)


def draw_flow(c, block):
    source = block['source']; sid = source['id']; oy = block['y']; ox = LEFT
    def n(role, text, x, y, w, h):
        node(c, role, text, ox+x, oy+y, w, h)
    def a(points, label=None, xy=None):
        arrow(c, [(ox+x, oy+y) for x,y in points], label, (ox+xy[0], oy+xy[1]) if xy else None)
    if sid == 'ch04-family-flow':
        texts = ['momage, dadage, myage, total 준비', '43, 45, 15 입력',
                 'total = momage + dadage + myage', '나이 총합 103 출력']
        for i, (role, text) in enumerate(zip(['declaration', 'input', 'process', 'output'], texts)):
            n(role, text, 75, i*110, 375, 82)
            if i:
                a([(262.5, (i-1)*110+82), (262.5, i*110)])
    elif sid == 'ch05-exercise-flow':
        n('declaration', 'time1 = 1, total = 0', 105, 0, 310, 60)
        c.setFillColor(HexColor('#EBEBF9')); c.setStrokeColor(HexColor(INDIGO)); c.setLineWidth(1.2)
        c.roundRect(ox+75, H-oy-390, 370, 300, 6, fill=1, stroke=1)
        c.setLineWidth(3.75); c.line(ox+75, H-oy-190, ox+445, H-oy-190)
        centered(c, 'time1 <= 10인가?', ox+260, oy+122, 'Flow', 14)
        n('process', 'total = total + time1', 100, 218, 320, 60)
        n('process', 'time1 = time1 + 1', 100, 310, 320, 60)
        n('output', '총 운동 시간 55분 출력', 110, 432, 300, 68)
        a([(260,60),(260,90)])
        a([(260,150),(260,218)], 'YES', (283,191))
        a([(260,278),(260,310)])
        a([(100,340),(50,340),(50,140),(75,140)])
        a([(445,140),(478,140),(478,465),(410,465)], 'NO', (480,110))
    elif sid == 'ch06-sleep-flow':
        n('input', '수면 시간 입력', 32, 0, 245, 60)
        n('decision', '8시간 이상인가?', 32, 110, 245, 110)
        n('decision', '5시간 이상인가?', 32, 278, 245, 110)
        n('output', '충분한 수면입니다', 345, 130, 180, 72)
        n('output', '적정 수면입니다', 345, 298, 180, 72)
        n('output', '수면 부족입니다', 63, 445, 183, 72)
        a([(154.5,60),(154.5,110)])
        a([(277,165),(345,165)], 'YES', (310,137))
        a([(154.5,220),(154.5,278)], 'NO', (179,239))
        a([(277,333),(345,333)], 'YES', (310,305))
        a([(154.5,388),(154.5,445)], 'NO', (179,407))
    elif sid == 'ch07-pass-flow':
        n('declaration', 'i = 0, N = 학생 수', 65, 0, 240, 60)
        n('output', '전체 처리 완료', 350, 0, 165, 60)
        c.setFillColor(HexColor('#EBEBF9')); c.setStrokeColor(HexColor(INDIGO)); c.setLineWidth(1.2)
        c.roundRect(ox+25, H-oy-535, 480, 450, 6, fill=1, stroke=1)
        c.setLineWidth(3.75); c.line(ox+25, H-oy-145, ox+505, H-oy-145)
        centered(c, 'i < N인가?', ox+265, oy+108, 'Flow', 14)
        n('input', '학생 점수 입력', 150, 173, 230, 54)
        n('decision', '점수가 80\n이상인가?', 160, 262, 210, 104)
        n('output', 'PASS 출력', 58, 395, 170, 56)
        n('output', 'FAIL 출력', 310, 395, 170, 56)
        n('process', 'i = i + 1', 165, 477, 200, 48)
        a([(185,60),(185,85)])
        a([(265,134),(265,173)], 'YES', (292,152))
        a([(265,227),(265,262)])
        a([(160,314),(143,314),(143,395)], 'YES', (116,350))
        a([(370,314),(395,314),(395,395)], 'NO', (420,350))
        a([(143,443),(143,468),(228,468),(228,477)])
        a([(395,443),(395,468),(310,468),(310,477)])
        a([(165,501),(10,501),(10,114),(25,114)])
        a([(505,114),(521,114),(521,30),(515,30)], 'NO', (482,66))
    else:
        raise ValueError(f'Unknown flowchart {sid}')


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
                    draw_flow(c,b)
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


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'output/pdf/vibe-coding-16-apps.pdf')
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
            '순서도는 독립 벡터 도형, 글꼴은 학교안심 칠판지우개 TTF L',
            '원본 캡처의 해상도는 보존하며 화질 복원 또는 재촬영을 주장하지 않음'],
        'layout':production.pages}
    args.output.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('pages','pageTypes','chapterPages')},ensure_ascii=False))


if __name__=='__main__':
    main()
