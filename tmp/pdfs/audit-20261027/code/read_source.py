import hashlib,json
from pathlib import Path
src=Path(r'C:/Users/use/Documents/카카오톡 받은 파일/(flet내용 추가)AI와 함께하는 앱 개발  업데이트 수정본(삼육_최종)의 사본 (7).pdf')
data=json.loads(Path('tmp/pdfs/source7-review/new-source.json').read_text(encoding='utf-8'))
assert data['sha256']==hashlib.sha256(src.read_bytes()).hexdigest()
for p in range(128,146):
    print('PAGE',p)
    print(data['texts'][p-1])
