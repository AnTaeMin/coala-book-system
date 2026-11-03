import json
from pathlib import Path
from pypdf import PdfReader
out = Path('tmp/pdfs/audit-20261027/code')
paths = {'source': Path(r'C:/Users/use/Documents/카카오톡 받은 파일/(flet내용 추가)AI와 함께하는 앱 개발  업데이트 수정본(삼육_최종)의 사본 (7).pdf'), 'target': Path('output/pdf/vibe-coding-16-upstream.pdf')}
for label, path in paths.items():
    reader = PdfReader(path)
    data = [{'page':i+1, 'text':p.extract_text() or ''} for i,p in enumerate(reader.pages)]
    (out / (label + '-pages.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    relevant = [p for p in data if any(x in p['text'] for x in ['matplotlib', 'Matplotlib', 'create_x', '20211206', 'set_xlabel'])]
    print(label, 'pages', len(data), 'relevant', [p['page'] for p in relevant])
    (out / (label + '-relevant.txt')).write_text('\n\n'.join('PAGE '+str(p['page'])+'\n'+p['text'] for p in relevant), encoding='utf-8')
