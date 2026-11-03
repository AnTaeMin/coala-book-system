"""Adapt shared upstream guidance to the existing GUI course, without notebook steps."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
BASE = BOOK / 'previous-reports/20261011-before-upstream-update'
COMMIT = '9723e244e225c4a300b6f251a766b39de46e63f6'
EDITION = 'upstream-gui-16-sessions'


def replace_once(text, before, after):
    assert text.count(before) == 1, before
    return text.replace(before, after, 1)


updates = {
    'ch01.md': [(
        '바이브 코딩에서는 원하는 앱을 말로 설명하고 AI가 제안한 코드를 실행합니다. 결과를 직접 확인하고 수정 요청을 반복합니다. 사람이 입력·처리·출력을 설계하고 실행 결과를 확인하는 과정이 중요합니다.',
        '바이브 코딩은 원하는 앱을 말로 설명하고 AI가 만든 프로그램을 실행하며 고쳐 가는 방식입니다. 사람은 원하는 기능과 입력·처리·출력을 정하고 결과를 확인합니다. AI는 코드를 작성하고 요청에 따라 수정합니다.'
    )],
    'ch02.md': [(
        '같은 주제로 질문을 다듬고 결과를 비교합니다.',
        '같은 주제로 질문을 다듬고 결과를 비교합니다. 앱을 요청할 때도 입력할 값, 버튼의 동작, 화면에 보여 줄 결과를 구체적으로 적습니다.'
    ), (
        '## 답변 확인하기\n\n같은 주제로 질문을 다듬고 결과를 비교합니다. 앱을 요청할 때도 입력할 값, 버튼의 동작, 화면에 보여 줄 결과를 구체적으로 적습니다.\n:::',
        '## 답변 확인하기\n\n같은 주제로 질문을 다듬고 결과를 비교합니다. 앱을 요청할 때도 입력할 값, 버튼의 동작, 화면에 보여 줄 결과를 구체적으로 적습니다.\n\n## 실행 후 수정 요청하기\n\n앱 화면에서 예시 값을 입력하고 버튼을 누른 결과를 확인합니다. 원하는 동작과 다르면 위젯 이름과 바꿀 동작을 적어 수정을 요청한 뒤 다시 실행합니다.\n:::'
    )],
    'ch08.md': [(
        '## 생성 후 실행하기\n\n‘안녕’을 입력하고 추가 후 fld2의 글자, 삭제 후 두 Field가 비는지 확인합니다.',
        '## 생성 후 실행하기\n\n앱 화면에서 ‘안녕’을 입력하고 추가 후 fld2의 글자, 삭제 후 두 Field가 비는지 확인합니다.'
    ), (
        '## 실행 확인\n\n프로젝트를 생성한 뒤 안녕 입력·추가·삭제를 순서대로 확인합니다.\n:::',
        '## 실행 확인\n\n프로젝트를 생성한 뒤 앱 화면에서 안녕 입력·추가·삭제를 순서대로 확인합니다.\n\n## 동작 수정 요청\n\n삭제 뒤 fld2에 글자가 남는다면 “btn2를 누르면 fld1과 fld2의 내용을 모두 지워 줘.”라고 요청합니다. 다시 생성·실행하고 두 Field가 비는지 확인합니다.\n:::'
    )],
}
for name, replacements in updates.items():
    text = (BASE / name).read_text(encoding='utf-8')
    for before, after in replacements:
        text = replace_once(text, before, after)
    (BOOK / name).write_text(text, encoding='utf-8')

manifest = json.loads((BASE / 'asset-manifest.json').read_text(encoding='utf-8'))
manifest['edition'] = EDITION
manifest['upstream_review'] = 'upstream-revision.json'
# All figures remain the previous GUI edition's figures. No notebook images.
(BOOK / 'asset-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
restructure = json.loads((BASE / 'no-pandas-restructure.json').read_text(encoding='utf-8'))
restructure['edition'] = EDITION
(BOOK / 'no-pandas-restructure.json').write_text(json.dumps(restructure, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

paths = ['README.md', 'canva-app/src/builder/image-assets.ts',
         'canva-app/tests/image-assets.test.ts', 'coala-book-md/ai-math2/book.md',
         'coala-book-md/ai-math2/notes.md']
review = {
    'date': '2026-10-11', 'edition': EDITION,
    'repository': 'https://github.com/kkh1466/coala-book-system',
    'branch': 'main', 'commit': COMMIT,
    'commit_url': 'https://github.com/kkh1466/coala-book-system/commit/'+COMMIT,
    'previous_upstream_commit': '032bf19',
    'baseline': 'previous-reports/20261011-before-upstream-update',
    'upstream_source_sha256': {
        path: hashlib.sha256(subprocess.check_output(['git', 'show', COMMIT+':'+path])).hexdigest()
        for path in paths
    },
    'changed_page_ids': ['ch01-ai', 'ch02-request', 'ch08-designer', 'ch08-request'],
    'added_page_ids': [], 'added_assets': [],
    'adopted': ['사람과 AI의 역할', '구체적인 기능·입력·출력 요청',
                '앱 화면에서 실행 결과 확인 후 수정 요청',
                '한글 이미지 경로 NFC 정규화와 회귀 테스트',
                '최신 설치 안내와 PDF 제작 스크립트 전달'],
    'excluded': [{
        'content': '주피터 노트북·코드 셀·AI Chat·현재 셀에 추가 단계와 화면 4개',
        'reason': '사용자 확인: 이 수업에서는 셀에 코드를 넣는 절차를 진행하지 않음'
    }, {
        'content': '노트북에서 실행하는 자기소개·공부 시간 계산 신규 실습',
        'reason': '현재 수업 환경과 기존 교재 실습 중심 구성에 맞추어 기존 실습을 유지'
    }],
    'expected_containers': 162, 'expected_practices': 37,
    'expected_python_blocks': 7, 'expected_output_blocks': 0,
    'expected_png_assets': 39, 'expected_image_placements': 41,
    'expected_vector_assets': 7,
    'student_no_notebook_workflow': True,
}
(BOOK / 'upstream-revision.json').write_text(json.dumps(review, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'changed_pages':review['changed_page_ids'], 'new_pages':0, 'new_images':0}, ensure_ascii=False))
