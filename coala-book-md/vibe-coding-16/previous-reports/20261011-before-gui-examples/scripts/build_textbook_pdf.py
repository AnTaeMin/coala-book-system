"""Typeset the validated 16-session manuscript for A4 printing.

The default foundation proof omits locked Canva templates and flowchart pages.
Those page types require a separately approved production route.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, Color, white
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
FONT_DIR = ROOT / 'tmp/pdfs/fonts'
W, H = A4
LEFT, RIGHT, TOP, BOTTOM = 34.0, 34.0, 99.0, 57.0
WIDTH = W - LEFT - RIGHT
BODY, HEADING, LEADING = 14.0, 15.0, 28.0
INK, INDIGO, GRAY = '#151515', '#1800AD', '#737373'


def fonts():
    for weight in ('Regular', 'Medium', 'Bold'):
        pdfmetrics.registerFont(TTFont('Wanted' + weight, str(FONT_DIR / ('WantedSans-' + weight + '.ttf'))))
    pdfmetrics.registerFont(TTFont('Code', 'C:/Windows/Fonts/consola.ttf'))
    pdfmetrics.registerFont(TTFont('Flow', str(FONT_DIR / 'HakgyoansimChilpanjiugaeL.ttf')))


def plain(text):
    return re.sub(r'\*\*(.*?)\*\*', r'\1', str(text)).replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-')


def text_width(text, font='WantedMedium', size=BODY):
    if font == 'Code':
        return sum(pdfmetrics.stringWidth(c, 'Code' if ord(c) < 128 else 'WantedMedium', size) for c in text)
    return pdfmetrics.stringWidth(text, font, size)


def wrap(text, width, font='WantedMedium', size=BODY, code=False):
    """Keep Latin words intact; allow Korean text to wrap at measured glyph widths."""
    lines = []
    for paragraph in plain(text).split('\n'):
        if not paragraph:
            lines.append('')
            continue
        tokens = list(paragraph) if code else re.findall(r'\S+|\s+', paragraph)
        line = ''
        for token in tokens:
            if line and text_width(line + token, font, size) > width:
                lines.append(line.rstrip())
                line = token if code else token.lstrip()
            else:
                line += token
            if text_width(line, font, size) > width:
                prefix = ''
                for char in line:
                    if prefix and text_width(prefix + char, font, size) > width:
                        lines.append(prefix)
                        prefix = char
                    else:
                        prefix += char
                line = prefix
        if line or not lines:
            lines.append(line.rstrip())
    return lines


class Production:
    def __init__(self, spec):
        self.spec = spec
        self.pages = []
        self.page = None
        self.current_source = None
        self.chapter = 0
        self.images = []
        self.warnings = []
        self.chapters = {p['chapterNumber']: p['chapterTitle'] for p in spec['pages'] if p['type'] == 'chapter-opening'}

    def start(self, source, continued=False):
        self.current_source = source
        continued_count = sum(p['id'] == source['id'] for p in self.pages) if continued else 0
        suffix = (' (계속)' if continued_count == 1 else f' (계속 {continued_count})') if continued else ''
        self.page = {'id': source['id'], 'chapter': self.chapter, 'type': source['type'],
                     'title': source.get('title', source.get('chapterTitle', '')) + suffix,
                     'blocks': [], 'y': TOP}
        self.pages.append(self.page)

    def space(self):
        return H - BOTTOM - self.page['y']

    def next(self):
        self.start(self.current_source, True)

    def add(self, block, gap=12):
        if block['height'] > H - BOTTOM - TOP + .01:
            raise ValueError(f"Oversized {block['kind']} in {self.current_source['id']}: {block['height']}")
        if block['height'] > self.space():
            self.next()
        block['y'] = self.page['y']
        self.page['blocks'].append(block)
        self.page['y'] += block['height'] + gap

    def paragraph(self, text, kind='paragraph', size=BODY, font='WantedMedium', indent=0, bullet=None):
        lines = wrap(text, WIDTH - indent, font, size)
        leading = LEADING if size == BODY else size * 2
        while lines:
            n = int((self.space() - 8) // leading)
            if n < 1 or (n == 1 and len(lines) > 1):
                self.next()
                continue
            part, lines = lines[:n], lines[n:]
            self.add({'kind': kind, 'lines': part, 'font': font, 'size': size, 'leading': leading,
                      'indent': indent, 'bullet': bullet, 'height': len(part) * leading}, gap=7)
            bullet = None

    def heading(self, text):
        if self.space() < 85:
            self.next()
        self.paragraph(text, kind='heading', size=HEADING, font='WantedBold')

    def box(self, text, label, kind='box', color='#F3F5F8', code=False):
        font = 'Code' if code else 'WantedMedium'
        lines = wrap(text, WIDTH - 30, font, BODY, code=code)
        # Keep short console tables together with their column header.
        complete_height = 47 + len(lines) * LEADING
        if label == '실행 결과' and complete_height <= H - BOTTOM - TOP and complete_height > self.space():
            self.next()
        continued = False
        while lines:
            n = int((self.space() - 47) // LEADING)
            if n < 2 and len(lines) > n:
                self.next()
                continue
            if n < 1:
                self.next()
                continue
            part, lines = lines[:n], lines[n:]
            self.add({'kind': kind, 'label': label + (' (계속)' if continued else ''), 'color': color,
                      'lines': part, 'font': font, 'height': 47 + len(part) * LEADING}, gap=15)
            continued = True

    def image(self, attributes):
        src = attributes['src']
        file = (BOOK / src).resolve()
        if not file.is_file() or not file.is_relative_to(BOOK.resolve()):
            raise ValueError(f'Missing or unsafe image: {src}')
        with Image.open(file) as im:
            iw, ih = im.size
        caption = attributes.get('caption', attributes.get('alt', ''))
        ratio = iw / ih
        width = WIDTH * .62 if attributes.get('width') == 'half' else WIDTH
        # Small original captures are kept modest in print, never pretended to be restored.
        if iw < 350:
            width = min(width, iw * .8)
        max_height = H - BOTTOM - TOP - 95
        height = width / ratio
        if height > max_height:
            height, width = max_height, max_height * ratio
        caption_lines = wrap(caption, WIDTH, size=11)
        label = '실행 결과' if attributes.get('role') == 'result' else ''
        total = height + len(caption_lines) * 18 + 12 + (32 if label else 0)
        self.add({'kind': 'image', 'file': str(file), 'src': src, 'width': width, 'imageHeight': height,
                  'label': label, 'caption': caption_lines, 'height': total}, gap=18)
        self.images.append({'src': src, 'pixels': [iw, ih], 'printWidthPt': width,
                            'effectiveDpi': round(iw / (width / 72), 1), 'sourceId': self.current_source['id']})

    def markdown(self, content):
        lines = content.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            if line.startswith('```'):
                language = line[3:].strip()
                i += 1
                code = []
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code.append(lines[i].rstrip())
                    i += 1
                labels = {'prompt': 'AI 요청 예시', 'response': '응답 예시', 'output': '실행 결과', 'python': 'Python'}
                fill = '#EAF1FF' if language in ('prompt', 'response') else '#F3F5F8'
                self.box('\n'.join(code), labels.get(language, language or '코드'), color=fill,
                         code=language not in ('prompt', 'response'))
                i += 1
            elif line.startswith('::image'):
                attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', line))
                self.image(attrs)
                i += 1
            elif line.startswith('>'):
                quoted = []
                while i < len(lines) and lines[i].lstrip().startswith('>'):
                    quoted.append(lines[i].lstrip()[1:].lstrip())
                    i += 1
                label = quoted.pop(0) if quoted and quoted[0].startswith('[!') else '[!TIP]'
                title = '핵심 정리' if 'KEY_POINT' in label else ('확인하기' if 'CAUTION' in label else 'Tip')
                self.box('\n'.join(quoted), title, color='#FFF9D9' if title == '핵심 정리' else '#EAF1FF')
            elif re.match(r'^- (\[.\] )?', line):
                checkbox = line.startswith('- [')
                text = re.sub(r'^- (\[.\] )?', '', line)
                self.paragraph(text, indent=22, bullet='check' if checkbox else 'dot')
                i += 1
            else:
                para = []
                while i < len(lines) and lines[i].strip() and not re.match(r'^(```|::image|>|- )', lines[i].strip()):
                    para.append(lines[i].strip())
                    i += 1
                self.paragraph(' '.join(para))

    def table(self, headers, rows):
        n = len(headers)
        cols = [WIDTH / n] * n
        def row_cells(row):
            return [wrap(text, cols[j] - 24) for j, text in enumerate(row)]
        head = row_cells(headers)
        head_h = max(map(len, head)) * LEADING + 22
        current = []
        total = head_h
        for row in rows:
            cells = row_cells(row)
            height = max(map(len, cells)) * LEADING + 22
            if total + height > self.space():
                if current:
                    self.add({'kind': 'table', 'headers': head, 'rows': current, 'cols': cols, 'headHeight': head_h, 'height': total}, gap=18)
                self.next()
                current, total = [], head_h
            current.append({'cells': cells, 'height': height})
            total += height
        if current:
            self.add({'kind': 'table', 'headers': head, 'rows': current, 'cols': cols, 'headHeight': head_h, 'height': total}, gap=18)

    def regular(self, source):
        self.start(source)
        if source['type'] == 'concept':
            if source.get('introduction'):
                self.paragraph(source['introduction'])
            for section in source['sections']:
                self.heading(section['title'])
                self.markdown(section.get('content', section.get('body', '')))
        elif source['type'] == 'comparison':
            if source.get('introduction'):
                self.paragraph(source['introduction'])
            self.table(source['columns'], source['rows'])
        elif source['type'] == 'step-process':
            for index, step in enumerate(source['steps'], 1):
                self.heading(f"{index:02d}  {step['title']}")
                self.markdown(step['content'])
        elif source['type'] == 'practice-checklist':
            for item in source['items']:
                self.paragraph(item, indent=22, bullet='check')
            if source.get('tip'):
                self.box(source['tip'], '핵심 정리', color='#FFF9D9')
            # Response space makes these pages usable as student worksheets.
            if self.space() >= 150:
                self.add({'kind': 'writing', 'label': '실습 결과 기록',
                          'height': min(self.space() - 8, 230)}, gap=0)
        if source.get('tip') and source['type'] != 'practice-checklist':
            self.box(source['tip'], 'Tip', color='#EAF1FF')
        if source['id'].endswith('-record') and self.space() >= 150:
            self.add({'kind': 'writing', 'label': '입력 · 예상 결과 · 실제 결과 · 수정 내용',
                      'height': min(self.space() - 8, 300)}, gap=0)

    def plan_foundation(self):
        for source in self.spec['pages']:
            if source['type'] == 'chapter-opening':
                self.chapter = source['chapterNumber']
            if source['type'] in ('chapter-opening', 'practice-opening', 'flowchart'):
                continue
            self.regular(source)


def draw_text(c, text, x, top, font='WantedMedium', size=BODY, color=INK):
    c.setFillColor(HexColor(color))
    if font == 'Code':
        runs = re.findall(r'[\x00-\x7f]+|[^\x00-\x7f]+', text)
        for run in runs:
            selected = 'Code' if ord(run[0]) < 128 else 'WantedMedium'
            c.setFont(selected, size)
            c.drawString(x, H - top - size * .84, run)
            x += pdfmetrics.stringWidth(run, selected, size)
    else:
        c.setFont(font, size)
        c.drawString(x, H - top - size * .84, text)


def draw_block(c, b):
    top = b['y']
    kind = b['kind']
    if kind in ('paragraph', 'heading'):
        if b.get('bullet') == 'dot':
            c.setFillColor(HexColor(INDIGO)); c.circle(LEFT + 5, H - top - 7, 2, stroke=0, fill=1)
        elif b.get('bullet') == 'check':
            c.setStrokeColor(HexColor(INDIGO)); c.setLineWidth(.8); c.rect(LEFT + 2, H - top - 12, 10, 10)
        for i, line in enumerate(b['lines']):
            draw_text(c, line, LEFT + b['indent'], top + i * b['leading'], b['font'], b['size'], INDIGO if kind == 'heading' else INK)
    elif kind == 'box':
        c.setFillColor(HexColor(b['color'])); c.setStrokeColor(HexColor('#DDE3EC')); c.setLineWidth(.7)
        c.roundRect(LEFT, H - top - b['height'], WIDTH, b['height'], 9, stroke=1, fill=1)
        draw_text(c, b['label'], LEFT + 15, top + 13, 'WantedBold', 12, INDIGO)
        for i, line in enumerate(b['lines']):
            draw_text(c, line, LEFT + 15, top + 39 + i * LEADING, b['font'])
    elif kind == 'image':
        if b['label']:
            draw_text(c, b['label'], LEFT, top, 'WantedBold', HEADING, INDIGO)
            top += 32
        x = (W - b['width']) / 2
        c.drawImage(b['file'], x, H - top - b['imageHeight'], b['width'], b['imageHeight'], mask='auto', preserveAspectRatio=True)
        top += b['imageHeight'] + 10
        for i, line in enumerate(b['caption']):
            draw_text(c, line, LEFT, top + i * 18, 'WantedMedium', 11, GRAY)
    elif kind == 'table':
        y = top
        for index, row in enumerate([{'cells': b['headers'], 'height': b['headHeight']}] + b['rows']):
            c.setFillColor(HexColor('#EAF1FF' if index == 0 else ('#F8FAFD' if index % 2 == 0 else '#FFFFFF')))
            c.rect(LEFT, H - y - row['height'], WIDTH, row['height'], stroke=0, fill=1)
            x = LEFT
            for j, cells in enumerate(row['cells']):
                for k, line in enumerate(cells):
                    draw_text(c, line, x + 12, y + 11 + k * LEADING, 'WantedBold' if index == 0 else 'WantedMedium', color=INDIGO if index == 0 else INK)
                x += b['cols'][j]
            c.setStrokeColor(HexColor('#DDE3EC')); c.setLineWidth(.65)
            c.line(LEFT, H - y - row['height'], W - RIGHT, H - y - row['height'])
            y += row['height']
    elif kind == 'writing':
        draw_text(c, b['label'], LEFT, top, 'WantedBold', HEADING, INDIGO)
        c.setStrokeColor(HexColor('#CBD3E0')); c.setLineWidth(.65)
        for yy in range(int(top + 48), int(top + b['height']), 35):
            c.line(LEFT, H - yy, W - RIGHT, H - yy)
    else:
        raise ValueError(f'Unsupported block: {kind}')


def render(production, output):
    output.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    c.setTitle(production.spec['title'])
    c.setAuthor('Coala')
    c.setSubject('16차시 학생용 교재 - 현재 수정 원고')
    for number, p in enumerate(production.pages, 1):
        c.setFillColor(white); c.rect(0, 0, W, H, fill=1, stroke=0)
        label = f"{p['chapter']:02d}차시  {production.chapters[p['chapter']]}" if p['chapter'] else '교재 안내'
        draw_text(c, label, LEFT, 24, 'WantedMedium', 10, GRAY)
        c.setStrokeColor(HexColor('#DDE3EC')); c.setLineWidth(.7); c.line(LEFT, H - 46, W - RIGHT, H - 46)
        title = wrap(p['title'], WIDTH, 'WantedBold', HEADING)
        if len(title) > 1:
            raise ValueError(f'Page title requires explicit split: {p["title"]}')
        draw_text(c, title[0], LEFT, 65, 'WantedBold', HEADING, INDIGO)
        for b in p['blocks']:
            draw_block(c, b)
        draw_text(c, 'AI와 함께하는 바이브 코딩', LEFT, H - 30, 'WantedMedium', 9, GRAY)
        c.setFillColor(HexColor(GRAY)); c.setFont('WantedMedium', 10); c.drawRightString(W - RIGHT, 22, str(number))
        c.showPage()
    c.save()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--spec', type=Path, default=ROOT / 'tmp/pdfs/book-spec.json')
    parser.add_argument('--output', type=Path, default=ROOT / 'tmp/pdfs/foundation-proof.pdf')
    args = parser.parse_args()
    fonts()
    spec = json.loads(args.spec.read_text(encoding='utf-8'))
    production = Production(spec)
    production.plan_foundation()
    render(production, args.output)
    report = {'mode': 'foundation-proof', 'pages': len(production.pages),
              'manuscriptSha256': hashlib.sha256((BOOK / 'book.md').read_bytes()).hexdigest(),
              'omittedTypes': ['chapter-opening', 'practice-opening', 'flowchart'],
              'images': production.images, 'layout': production.pages}
    args.output.with_suffix('.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'output': str(args.output), 'pages': len(production.pages), 'images': len(production.images)}))


if __name__ == '__main__':
    main()
