"""Build a crisp vector summary and a Canva-ready PNG for the first lesson."""
from pathlib import Path
import hashlib
import json

import pypdfium2 as pdfium
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

from build_textbook_pdf import BOOK, WIDTH, INK, INDIGO, fonts


HEIGHT = 190.0
DEST = BOOK / 'assets/ch01'
DEST.mkdir(parents=True, exist_ok=True)
fonts()
pdf_path = DEST / 'ai-human-summary.pdf'
c = canvas.Canvas(str(pdf_path), pagesize=(WIDTH, HEIGHT), pageCompression=1)
c.setTitle('AI의 제안과 사람의 검증')
c.setAuthor('Coala')
c.setFillColor(white)
c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)


def text(value, x, top, bold=False, size=14, color=INK):
    c.setFillColor(HexColor(color))
    c.setFont('WantedBold' if bold else 'WantedMedium', size)
    c.drawString(x, HEIGHT-top-size, value)


gap = 18
card_width = (WIDTH-gap)/2
roles = [
    ('AI의 제안', ['아이디어·코드 초안 제안', '요청에 맞게 결과 만들기', '답변은 사실 확인이 필요'], '#EEF2FF'),
    ('사람의 검증', ['목적과 동작 정하기', '근거·실행 결과 확인', '오류를 고치고 다시 확인'], '#EFFAF5'),
]
for index, (title, lines, fill) in enumerate(roles):
    x = index*(card_width+gap)
    c.setFillColor(HexColor(fill))
    c.setStrokeColor(HexColor(INDIGO if index == 0 else '#16704F'))
    c.setLineWidth(.9)
    c.roundRect(x+.5, HEIGHT-153, card_width-1, 151, 10, fill=1, stroke=1)
    # Simple role icons, rather than algorithm/flowchart symbols.
    c.setFillColor(white)
    c.roundRect(x+16, HEIGHT-43, 25, 25, 6, fill=1, stroke=0)
    c.setStrokeColor(HexColor(INDIGO if index == 0 else '#16704F'))
    c.setLineWidth(1.5)
    if index == 0:
        c.roundRect(x+21, HEIGHT-37, 15, 13, 3, fill=0, stroke=1)
        c.line(x+24, HEIGHT-37, x+24, HEIGHT-40)
        c.line(x+24, HEIGHT-40, x+28, HEIGHT-37)
        for dot_x in (25, 29, 33):
            c.setFillColor(HexColor(INDIGO)); c.circle(x+dot_x, HEIGHT-30.5, .8, fill=1, stroke=0)
    else:
        path = c.beginPath()
        path.moveTo(x+21, HEIGHT-30); path.lineTo(x+27, HEIGHT-36); path.lineTo(x+36, HEIGHT-24)
        c.drawPath(path, stroke=1)
    text(title, x+50, 18, bold=True, size=15, color=INDIGO if index == 0 else '#16704F')
    for i, line in enumerate(lines):
        text(line, x+18, 56+i*28)

message = 'AI에게 맡길 일과 내가 검증할 일을 구분합니다.'
c.setFont('WantedMedium', 14)
message_width = c.stringWidth(message, 'WantedMedium', 14)
text(message, (WIDTH-message_width)/2, 167)
c.showPage(); c.save()
document = pdfium.PdfDocument(str(pdf_path))
page = document[0]
bitmap = page.render(scale=300/72)
preview = bitmap.to_pil().convert('RGB')
png_path = pdf_path.with_suffix('.png')
preview.save(png_path, dpi=(300, 300))
width, height = preview.size
bitmap.close(); page.close(); document.close()
record = {
    'src': 'assets/ch01/ai-human-summary.png', 'chapter': 1,
    'page_id': 'ch01-opening', 'width': width, 'height': height,
    'ratio': f'{width}:{height}', 'sha256': hashlib.sha256(png_path.read_bytes()).hexdigest(),
    'vector_src': 'assets/ch01/ai-human-summary.pdf',
    'vector_sha256': hashlib.sha256(pdf_path.read_bytes()).hexdigest(),
    'kind': 'self-authored-vector-learning-summary', 'used_in': ['ch01-opening'],
    'placement_width': 'text',
    'caption': 'AI의 제안과 사람의 검증으로 함께 만드는 앱',
    'placements': [{'page_id': 'ch01-opening', 'width': 'text',
                    'caption': 'AI의 제안과 사람의 검증으로 함께 만드는 앱'}],
    'body_font_pt': 14, 'heading_font_pt': 15,
    'print_width_pt': WIDTH, 'print_height_pt': HEIGHT,
    'pixel_text_modified': False, 'upscaled': False,
}
(BOOK/'intro-summary-map.json').write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
manifest_path = BOOK/'asset-manifest.json'
if manifest_path.is_file():
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if any(item['src'] == record['src'] for item in manifest['items']):
        manifest['items'] = [record if item['src'] == record['src'] else item for item in manifest['items']]
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(record, ensure_ascii=False))
