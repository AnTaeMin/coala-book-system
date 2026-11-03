"""Render every final page and audit pagination, glyph bounds, and assets."""
import json
import re
import argparse
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--pdf', type=Path, default=ROOT / 'output/pdf/vibe-coding-16-source7.pdf')
parser.add_argument('--dest', type=Path, default=ROOT / 'tmp/pdfs/apps-review')
args = parser.parse_args()
PDF, DEST = args.pdf.resolve(), args.dest.resolve()
DEST.mkdir(parents=True, exist_ok=True)
metadata = json.loads(PDF.with_suffix('.json').read_text(encoding='utf-8'))
doc = pdfium.PdfDocument(str(PDF))
extracted = []
bad_bounds = []
contacts = []
label_font = ImageFont.truetype('C:/Windows/Fonts/arial.ttf', 16)
for index in range(len(doc)):
    page = doc[index]
    tp = page.get_textpage()
    text = tp.get_text_range()
    extracted.append(text)
    for char in range(tp.count_chars()):
        if not tp.get_text_range(char, 1).strip():
            continue
        l,b,r,t = tp.get_charbox(char)
        if l < -1 or b < -1 or r > page.get_width()+1 or t > page.get_height()+1:
            bad_bounds.append({'page':index+1,'char':tp.get_text_range(char,1),'bounds':[l,b,r,t]})
    bitmap = page.render(scale=110/72)
    image = bitmap.to_pil().convert('RGB')
    image.save(DEST / f'page-{index+1:03d}.png')
    thumb = image.copy(); thumb.thumbnail((220,312))
    tile = Image.new('RGB',(240,342),'#eeeeee');tile.paste(thumb,((240-thumb.width)//2,20))
    ImageDraw.Draw(tile).text((10,3),str(index+1),font=label_font,fill='black')
    contacts.append(tile)
    bitmap.close(); tp.close(); page.close()
for start in range(0,len(contacts),36):
    sheet = Image.new('RGB',(1440,2052),'#eeeeee')
    for j,tile in enumerate(contacts[start:start+36]):
        sheet.paste(tile,((j%6)*240,(j//6)*342))
    sheet.save(DEST / f'contact-{start//36+1:02d}.png')
(DEST/'text.txt').write_text('\n\n'.join(extracted),encoding='utf-8')
source_ids = {p['id'] for p in json.loads((ROOT/'tmp/pdfs/book-spec.json').read_text(encoding='utf-8'))['pages']}
spec = json.loads((ROOT/'tmp/pdfs/book-spec.json').read_text(encoding='utf-8'))
original_code = [code for p in spec['pages'] for s in p.get('sections',[]) for code in re.findall(r'```python\s*\n(.*?)\n```',s.get('content',''),re.S)]
printed_code = []
printed_code_segments = 0
for p in metadata['layout']:
    for block in p['blocks']:
        label = block.get('label', '')
        if not label.startswith('Python'):
            continue
        printed_code_segments += 1
        content = '\n'.join(block['lines'])
        if label == 'Python':
            printed_code.append(content)
        else:
            if not printed_code:
                raise ValueError('Orphan continued code box')
            printed_code[-1] += '\n' + content
normalize = lambda text: re.sub(r'\s+','',text)
code_errors = [i+1 for i,(a,b) in enumerate(zip(original_code,printed_code)) if normalize(a)!=normalize(b)]
if len(original_code) != len(printed_code):
    code_errors.append('block-count-mismatch')
rendered_ids = {p['id'] for p in metadata['layout']}
for p in metadata['layout']:
    rendered_ids.update(p.get('includedSources',[]))
missing = sorted(source_ids-rendered_ids)
toc_errors = []
for ch,number in metadata['chapterPages'].items():
    if metadata['layout'][number-1]['chapter'] != int(ch) or metadata['layout'][number-1]['type'] != 'chapter-opening':
        toc_errors.append(ch)
report = {'pages':len(doc),'renderedPages':len(contacts),'outOfPageGlyphs':bad_bounds,
          'missingSourceIds':missing,'contentsErrors':toc_errors,
          'images':len(metadata['images']),'flowcharts':sum(p['type']=='flowchart' for p in metadata['layout']),
          'manuscriptCodeBlocks':len(original_code),'printedCodeBlocks':len(printed_code),'printedCodeSegments':printed_code_segments,'codeContentDifferences':code_errors,
          'replacementGlyphPages':[i+1 for i,t in enumerate(extracted) if '\ufffd' in t],
          'institutionLogoTextPages':[i+1 for i,t in enumerate(extracted) if '삼육보건' in t],
          'editorialReferencePages':[i+1 for i,t in enumerate(extracted) if re.search(r'원본|\bPDF\b|원 교재|대조 수정판', t, re.I)],
          'robotReferencePages':[i+1 for i,t in enumerate(extracted) if re.search(r'코코봇|cocobot', t, re.I)],
          'boxOverflows':[{'page':i+1,'kind':b['kind']} for i,p in enumerate(metadata['layout']) for b in p['blocks'] if b['y']+b['height']>786]}
(DEST/'automated-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
