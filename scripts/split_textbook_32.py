"""Derive a 32-session edition by splitting each current unit into parts 1 and 2.

The current 16-session manuscript and its published outputs are read-only inputs.
Original page IDs, code, diagrams, exercise instructions, and assets are retained.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'coala-book-md/vibe-coding-16'
DEST = ROOT / 'coala-book-md/vibe-coding-32'
DATE = '2026-11-03'

# boundary, short title, (focus, two learning objectives) for each part
PLAN = [
    ('ch01-practice-1', 'AI와 앱 개발',
     ('생성형 AI의 역할과 한계', '생성형 AI와 바이브 코딩의 역할을 설명할 수 있다.', 'AI의 답에서 사람이 확인할 내용을 구분할 수 있다.'),
     ('AI 답변 검증 실습', '질문 유형에 따른 AI 답변의 차이를 비교할 수 있다.', '답변의 근거를 확인하고 활용 여부를 기록할 수 있다.')),
    ('ch02-inputs', '질문과 입력',
     ('프롬프트 구성과 질문 비교', '목적과 상황, 조건을 포함한 프롬프트를 작성할 수 있다.', '모호한 질문과 구체적인 질문의 답변을 비교할 수 있다.'),
     ('앱 입력 데이터와 요청 설계', '앱의 목적에 필요한 입력 데이터를 정할 수 있다.', '입력·버튼 동작·결과를 담아 앱 제작과 수정을 요청할 수 있다.')),
    ('ch03-practice-1', '문제 나누기',
     ('입력·처리·출력과 알고리즘', '문제를 입력·처리·출력으로 구분할 수 있다.', '문제 해결 순서를 단계별로 설명할 수 있다.'),
     ('앱 아이디어의 단계별 설계', '앱 아이디어를 입력·처리·출력으로 설계할 수 있다.', '처리 순서를 확인하고 빠진 단계를 보완할 수 있다.')),
    ('ch04-practice-1', '순서도와 변수',
     ('순서도·자료형·변수', '순서도에서 데이터가 이동하는 과정을 설명할 수 있다.', '문자열과 숫자, 변수 이름과 값을 구분할 수 있다.'),
     ('가족 나이와 학생 총점 계산', '입력한 나이와 점수의 합계를 계산하는 순서를 설명할 수 있다.', '변수와 순서도를 대조하여 계산 결과를 확인할 수 있다.')),
    ('ch05-practice-2', '반복과 누적',
     ('운동 시간 반복·누적', '반복 횟수와 누적 변수의 역할을 설명할 수 있다.', '운동 시간을 반복해서 더하고 결과를 확인할 수 있다.'),
     ('카페인 입력 반복·누적', '반복 입력한 카페인 양의 합계를 구할 수 있다.', '반복 종료 조건과 누적 결과를 확인할 수 있다.')),
    ('ch06-practice-1', '조건과 분기',
     ('조건식과 수면 분류 규칙', '조건식의 참과 거짓에 따른 분기를 설명할 수 있다.', '수면 시간 분류의 기준과 경계값을 구분할 수 있다.'),
     ('조건 처리 구현과 분기 확인', '입력한 수면 시간을 조건에 따라 분류할 수 있다.', '5시간·8시간의 경계값을 넣어 선택되는 안내 문구를 확인할 수 있다.')),
    ('ch07-movie-code', '반복 속 조건',
     ('학생 수만큼 합격 판정', '입력한 학생 수만큼 점수 처리를 반복할 수 있다.', '80점 기준에 따라 PASS와 FAIL을 구분할 수 있다.'),
     ('영화 관람 반복과 분기', '네 학생의 나이를 반복 입력하고 관람 조건을 판단할 수 있다.', '15세 기준의 분기와 반복 흐름을 순서도로 설명할 수 있다.')),
    ('ch08-practice-message', '첫 앱 화면',
     ('기본 위젯과 버튼 색 변경', 'Button·Field·Text의 역할을 구분할 수 있다.', '버튼 클릭에 따른 색 변경을 요청하고 확인할 수 있다.'),
     ('메시지 창과 Field 복사·삭제', '버튼 클릭으로 메시지 창을 표시할 수 있다.', 'Field 입력값의 복사와 삭제 동작을 확인할 수 있다.')),
    ('ch09-practice-3', '계산과 출력',
     ('누적곱과 계산기', '누적곱과 계산기의 입력·처리·출력을 구성할 수 있다.', '계산 결과와 빈칸·문자·0 나누기 처리를 확인할 수 있다.'),
     ('Text 추가와 구구단', 'Text를 추가하여 결과를 누적 출력할 수 있다.', '반복으로 구구단을 출력하고 결과를 확인할 수 있다.')),
    ('ch10-practice-4', '선택 위젯',
     ('Dropdown·Checkbox·RadioButton', '세 선택 위젯의 역할과 선택 방식을 구분할 수 있다.', '선택값에 따른 화면 결과를 확인할 수 있다.'),
     ('ProgressBar와 Image', '진행 막대의 값과 표시 범위를 확인할 수 있다.', '두 이미지를 배치하고 화면 결과를 확인할 수 있다.')),
    ('ch11-index', '표와 성적',
     ('성적표 입력과 행 추가', '입력창의 값을 성적표의 열 순서에 맞출 수 있다.', '학생 성적을 표에 추가하고 입력값과 비교할 수 있다.'),
     ('위치 번호와 셀 값 수정', '화면의 행·열 번호와 리스트 인덱스의 관계를 설명할 수 있다.', '행·열 범위를 확인하고 선택한 셀의 값을 바꿀 수 있다.')),
    ('ch12-practice-colors', '선 그래프·마커',
     ('배열·좌표·선 그래프·표시 범위', 'cht1에 연결된 Figure·Axes에 배열을 선 그래프로 그릴 수 있다.', 'X·Y 좌표와 표시 범위를 실행 결과에서 확인할 수 있다.'),
     ('마커·제목·축 이름', '마커와 선의 표시 방법을 바꿀 수 있다.', '제목·축 이름·좌표 설명을 설정하고 결과를 확인할 수 있다.')),
    ('ch13-practice-4', '막대·산점도',
     ('막대와 나란한 막대그래프', '값을 막대 높이로 나타낼 수 있다.', '나란한 막대의 위치와 항목 이름을 확인할 수 있다.'),
     ('산점도·시드·축 확인', 'X·Y 값의 짝을 산점도로 나타낼 수 있다.', '시드와 축 이름을 확인하고 그림을 해석할 수 있다.')),
    ('ch14-practice-2', '차트 바이브 코딩',
     ('입력값 선 그래프', '입력값을 Chart의 선 그래프로 나타낼 수 있다.', '입력값과 그래프의 축·좌표를 비교할 수 있다.'),
     ('입력값 산점도·막대그래프', '입력값을 산점도와 막대그래프로 나타낼 수 있다.', '새 입력이 이전 값과 함께 누적되는지 확인할 수 있다.')),
    ('ch15-practice-3', '자료와 저장',
     ('학생 자료와 학교별 집계', '학생 자료의 열과 값을 확인할 수 있다.', '학교별 학생 수를 집계하고 결과를 비교할 수 있다.'),
     ('프로젝트 저장·불러오기', '프로젝트와 표의 저장 옵션을 확인할 수 있다.', '저장한 프로젝트를 불러와 입력값과 동작을 비교할 수 있다.')),
    ('ch16-fix', '앱 개선·발표',
     ('자율 프로젝트 설계·구현', '프로그램 아이디어와 입력·처리·출력을 정할 수 있다.', '위젯 역할과 이벤트를 정하여 작은 앱을 구현할 수 있다.'),
     ('동작 검증·기록·발표', '설계와 실행 결과를 비교하고 오류를 수정할 수 있다.', 'AI가 제안한 부분과 직접 확인한 부분, 수정 결과를 구분하여 발표할 수 있다.')),
]


def reviewed_page(page):
    """Apply the evidence-backed corrections found in the detailed recheck."""
    pid = page_id(page)
    if pid == 'ch08-button-before':
        page = page.replace('# 버튼 클릭 전\n', '# 버튼 클릭 전후 비교\n')
    elif pid == 'ch08-button-after':
        page = page.replace('화면의 버튼 상태를 확인해봅시다.',
                            '아래 그림은 배경색 변경을 보여 주는 참고 화면입니다. 그림의 글자는 흰색이 아니므로, 실습에서 지정한 white 적용 여부는 자신의 실행 화면에서 따로 확인합니다.')
        page = page.replace('caption="클릭 후 파란색으로 바뀐 버튼"',
                            'caption="배경색 변경 참고 화면 · 흰 글자 적용은 직접 확인"')
    elif pid == 'ch08-message-screen':
        page = page.replace('버튼을 클릭하면 알림 창에서 같은 입력 내용을 확인합니다.',
                            '아래 그림은 알림 창의 형태를 보여 주는 참고 화면입니다. 위 입력 그림은 “안녕하세요”, 아래 알림 그림은 “안녕하세요!”로 문장부호가 다릅니다. 직접 만든 앱에서는 문장부호까지 입력한 내용 그대로 표시되는지 확인합니다.')
        page = page.replace('alt="안녕하세요가 표시된 알림 창"', 'alt="안녕하세요!가 표시된 참고 알림 창"')
        page = page.replace('caption="입력한 인사말을 표시한 메시지 창"', 'caption="메시지 창 형태 참고 · 문장부호는 입력 그림과 다름"')
    elif pid == 'ch11-practice-2':
        page = page.replace('## 행·열 선택\n\n사용자가 값을 넣을 행 번호와 열 번호를 선택합니다.',
            '## 수정용 위젯 추가\n\n앞 차시의 성적표에 Field 세 개를 추가하고 edit_row(행 번호), edit_column(열 번호), edit_value(변경할 값)로 이름을 정합니다. btn2(셀 변경) 버튼도 추가합니다. 표에는 먼저 학생 기록을 한 행 이상 넣습니다.\n\n'
            '## 행·열 입력\n\nedit_row와 edit_column에 바꿀 셀의 행·열 번호를 1부터 입력합니다.')
        page = page.replace('Field에 표에 넣을 값을 입력합니다.', 'edit_value에 해당 셀에 넣을 값을 입력합니다.')
        page = page.replace('선택한 번호에서 1을 빼서 리스트 위치로 바꿉니다.',
                            'btn2의 클릭 이벤트에서 번호를 숫자로 바꾸고 실제 행·열 범위에 있는지 확인합니다. 번호가 0이거나 범위를 벗어나면 변경하지 않고 안내합니다. 유효한 번호에서 각각 1을 빼서 리스트 위치로 바꿉니다.')
        page = page.replace('선택한 DataCell의 내용을 바꾸고 표에 표시합니다.',
                            'btn2를 누르면 선택한 DataCell의 내용을 edit_value의 값으로 바꾸고 표를 갱신하도록 요청합니다. 과목 점수는 0~100 사이의 숫자인지도 확인합니다.\n\n'
                            '## 실행 확인\n\n선택한 셀만 새 값으로 바뀌고 다른 셀은 유지되는지 확인합니다. 0이나 없는 행·열 번호를 넣었을 때 표가 바뀌지 않는지도 확인합니다.')
    elif pid == 'ch16-portfolio':
        page = page.replace('\n:::', '\n\n## AI 도움과 직접 확인한 내용 발표\n\nAI가 제안한 코드나 아이디어, 내가 직접 실행해 확인한 부분, 수정 전후 결과를 구분하여 설명합니다. 실제 입력과 실행 화면을 근거로 발표합니다.\n:::')
    elif pid == 'ch16-check':
        page = page.replace('- [ ] 위젯 역할·이벤트·실행 결과를 대조했다.',
                            '- [ ] 위젯 역할·이벤트·실행 결과를 대조했다.\n- [ ] AI가 제안한 부분과 직접 확인한 부분, 수정 결과를 구분하여 발표했다.')
    if 'type="practice-checklist"' in page:
        page = page.replace('# 실습 완료 확인\n', '# 1·2부 종합 확인\n')
    return page


CHART_CONTINUITY = {
    24: '23차시에서 만든 cht1·fig_cht1·ax_cht1을 그대로 사용합니다. 같은 X·Y 배열에서 마커와 선을 비교하고 제목·축 이름·좌표 설명을 확인합니다.',
    25: '23차시에서 생성하고 24차시에서 사용한 cht1·fig_cht1·ax_cht1을 그대로 사용합니다. 배열 값을 막대 높이와 위치에 연결합니다.',
    26: '앞 차시와 같은 cht1·fig_cht1·ax_cht1을 사용합니다. 시드로 정한 난수와 X·Y 값으로 산점도를 그리고 축과 범례를 확인합니다.',
}


def read(path):
    return path.read_text(encoding='utf-8')


def pages(text):
    return re.findall(r'^:::page\{[^\n]*\}\n.*?^:::[ \t]*$', text, re.M | re.S)


def page_id(page):
    return re.search(r'\bid="([^"]+)"', page).group(1)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    source_book = read(SOURCE / 'book.md')
    original_pages = pages(source_book)
    original_by_id = {page_id(p): p for p in original_pages}
    front = source_book[:source_book.index(':::page')]
    front = re.sub(r'^subtitle:.*$', 'subtitle: 32차시 · 개념과 실습', front, flags=re.M)
    DEST.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE / 'assets', DEST / 'assets', dirs_exist_ok=True)
    for name in ('flow-source-map.json', 'intro-summary-map.json', 'asset-manifest.json'):
        shutil.copy2(SOURCE / name, DEST / name)

    sessions = []
    chapter_bodies = []
    practice_changes = []
    content_edits = []
    source_hashes = {'book.md': hashlib.sha256((SOURCE / 'book.md').read_bytes()).hexdigest()}
    for old, (boundary, short, part1, part2) in enumerate(PLAN, 1):
        source_path = SOURCE / f'ch{old:02d}.md'
        source_hashes[source_path.name] = hashlib.sha256(source_path.read_bytes()).hexdigest()
        old_pages = pages(read(source_path))
        original_opening = old_pages[0]
        title = re.search(r'^# (.+)$', original_opening, re.M).group(1)
        content = old_pages[1:]
        if old == 2:
            question = next(p for p in content if page_id(p) == 'ch02-practice-1')
            content.remove(question)
            at = next(i for i, p in enumerate(content) if page_id(p) == 'ch02-compare')
            content.insert(at + 1, question)
        split = next(i for i, p in enumerate(content) if page_id(p) == boundary)
        for part, info, body in ((1, part1, content[:split]), (2, part2, content[split:])):
            number = old * 2 - 2 + part
            focus, *objectives = info
            opening_id = f'ch{old:02d}-opening' if part == 1 else f'ch{old:02d}-part2-opening'
            full_title = f'{title} {part}'
            intro = f'이번 차시의 주제는 {focus}입니다.' if part == 1 else f'앞 차시의 내용을 바탕으로 학습을 이어갑니다. 이번 차시는 {focus}에 집중합니다.'
            intro = CHART_CONTINUITY.get(number, intro)
            # Keep the original overview illustration with the first part.
            overview_images = re.findall(r'^::image\{[^\n]+\}$', original_opening, re.M) if part == 1 else []
            opening = (f':::page{{type="chapter-opening" id="{opening_id}" chapter="{number}"}}\n'
                       f'# {full_title}\n\n## {number}차시 · {focus}\n\n### 학습 목표\n\n'
                       + '\n'.join(f'- {o}' for o in objectives)
                       + f'\n\n### 오늘의 시작\n\n{intro}\n'
                       + ('\n' + '\n\n'.join(overview_images) + '\n' if overview_images else '') + ':::')
            practice_count = 0
            renumbered = []
            for page in body:
                corrected = reviewed_page(page)
                if corrected != page:
                    content_edits.append(page_id(page))
                page = corrected
                match = re.search(r'\bpractice="([^"]+)"', page)
                if match:
                    practice_count += 1
                    new_practice = f'{number:03d}-{practice_count}'
                    practice_changes.append({'pageId': page_id(page), 'original': match.group(1), 'current': new_practice})
                    page = page[:match.start(1)] + new_practice + page[match.end(1):]
                renumbered.append(page)
            assembled = '\n\n'.join([opening, *renumbered]) + '\n'
            chapter_front = re.sub(r'^subtitle:.*$', f'subtitle: {number}차시 · {full_title}', front, flags=re.M)
            (DEST / f'ch{number:02d}.md').write_text(chapter_front + assembled, encoding='utf-8')
            chapter_bodies.append(assembled.rstrip())
            sessions.append({'number': number, 'originalChapter': old, 'part': part,
                             'title': full_title, 'shortTitle': f'{short} {part}', 'focus': focus,
                             'objectives': objectives, 'openingId': opening_id,
                             'originalPageIds': ([page_id(original_opening)] if part == 1 else []) + [page_id(p) for p in body],
                             'contentPageIds': [page_id(p) for p in body], 'practiceCount': practice_count})

    result = front + original_by_id['book-guide'] + '\n\n' + '\n\n'.join(chapter_bodies) + '\n'
    (DEST / 'book.md').write_text(result, encoding='utf-8')
    new_pages = pages(result)
    new_by_id = {page_id(p): p for p in new_pages}
    expected_changed = {f'ch{n:02d}-opening' for n in range(1, 17)}
    def normalize_practice(page):
        return re.sub(r'\bpractice="[^"]+"', 'practice="PRESERVED"', page)
    changed_content = [pid for pid, page in original_by_id.items()
                       if pid not in expected_changed and normalize_practice(page) != normalize_practice(new_by_id[pid])]
    assert set(changed_content) == set(content_edits), changed_content
    assert len(new_pages) == 178 and len(new_by_id) == 178
    assert set(original_by_id) <= set(new_by_id)
    assert len(practice_changes) == 37
    for language, count in (('python', 8), ('flowchart', 4)):
        expression = rf'^```{language}\s*\n(.*?)^```\s*$'
        original = re.findall(expression, source_book, re.M | re.S)
        current = re.findall(expression, result, re.M | re.S)
        assert original == current and len(current) == count
    images = lambda text: re.findall(r'^::image\{[^\n]+\}$', text, re.M)
    image_sources = lambda text: re.findall(r'^::image\{src="([^"]+)"', text, re.M)
    assert sorted(image_sources(source_book)) == sorted(image_sources(result))
    for name, digest in source_hashes.items():
        assert hashlib.sha256((SOURCE / name).read_bytes()).hexdigest() == digest
    split_report = {'date': DATE, 'source': '../vibe-coding-16/book.md',
                    'sourceSha256': source_hashes['book.md'], 'sourceFileHashes': source_hashes,
                    'sessions': sessions, 'practiceRenumbering': practice_changes,
                    'reorderedPages': ['ch02-practice-1'],
                    'reviewedContentEdits': content_edits,
                    'preservation': {'originalPageIds': len(original_pages), 'retainedOriginalPageIds': len(original_by_id),
                                     'addedPartOpenings': 16, 'currentPages': len(new_pages),
                                     'practiceCount': 37, 'pythonBlocks': 8, 'flowchartBlocks': 4,
                                     'imagePlacements': len(images(result)), 'changedNonOpeningContent': changed_content,
                                     'unreviewedContentChanges': []}}
    write_json(DEST / 'session-split.json', split_report)
    rows = ['| 차시 | 주제 | 이번 차시 내용 | 기존 차시 |', '|---:|---|---|---:|']
    rows.extend(f'| {s["number"]} | {s["title"]} | {s["focus"]} | {s["originalChapter"]} |' for s in sessions)
    (DEST / 'curriculum.md').write_text('# 32차시 수업 구성 · ' + DATE + '\n\n'
        + '기존 16개 주제를 각각 1·2부로 나눕니다. 기존 1차시는 새 1·2차시, 기존 16차시는 새 31·32차시입니다.\n\n'
        + '\n'.join(rows) + '\n\n실습 37개, 공통 차트 생성 코드 1개와 그리기 코드 7개, 순서도 4개를 유지합니다. 차시별 분량은 개념과 실습의 연결에 따라 다릅니다.\n', encoding='utf-8')
    (DEST / 'teacher-guide.md').write_text('# 32차시 교사용 운영 안내 · ' + DATE + '\n\n'
        + '수업 주제는 기존 명칭 뒤에 1 또는 2를 붙이고, 실제 수업 번호는 1~32차시로 매깁니다. '
        + '각 2부는 앞 1부의 개념을 바탕으로 이어서 진행하고, 본문에서 지정한 프로젝트와 데이터를 사용합니다.\n\n'
        + '1~4차시는 AI와 질문, 5~14차시는 알고리즘, 15~32차시는 GUI·앱 제작입니다. '
        + '23~24차시 선·마커, 25~26차시 막대·산점도, 27~28차시 입력 Chart, 29~30차시 자료·저장, 31~32차시 프로젝트 순서입니다.\n\n'
        + '차시마다 도입의 학습 목표를 확인한 뒤 본문의 입력·처리·출력과 실제 실행 결과를 비교합니다. '
        + '1부 끝에서는 수행한 내용을 정리하고 프로젝트를 보존합니다. 2부에서는 앞 차시의 개념을 확인한 뒤 본문의 예제를 진행합니다. '
        + '단일 실습을 두 차시에 걸쳐 진행하는 주제도 있으므로 실습 개수와 차시 수는 다릅니다.\n\n'
        + '실습 안내 번호는 새 차시에 맞춰 다시 매겼습니다. 본문 페이지 ID와 이미지 경로는 출처 추적을 위해 유지했고, '
        + '대응 관계는 [session-split.json](session-split.json), 세부 수업 구성은 [curriculum.md](curriculum.md)에 있습니다.\n\n'
        + '기존 2차시의 질문 비교 실습은 새 3차시에서 프롬프트 비교 바로 뒤에 배치했습니다. 그 밖의 본문 순서는 유지합니다. '
        + '코드·순서도·결과 화면은 기존 자료를 사용합니다. 재검토에서 참고 화면의 차이를 명시하고, 표 셀 수정의 위젯·이벤트와 AI 도움 구분 발표 안내를 보완했습니다. 실행 예제와 기존 검증 기록은 '
        + '[16차시 원본 안내](../vibe-coding-16/README.md)를 참고합니다.\n', encoding='utf-8')
    (DEST / 'README.md').write_text('# 바이브 코딩 32차시 교재 · ' + DATE + '\n\n'
        + '현재 16차시 최종 편집본을 각각 1·2부로 나눈 32차시판입니다. 기존 원고와 PDF는 보존합니다.\n\n'
        + '- [재검토한 학생용 PDF](../../output/pdf/vibe-coding-32-coala-access-reviewed.pdf)\n'
        + '- [전체 원고](book.md), 차시별 원고 ch01.md~ch32.md\n'
        + '- [32차시 수업 구성](curriculum.md), [교사용 안내](teacher-guide.md)\n'
        + '- [분할 대응표·보존 검증](session-split.json)\n\n'
        + '내용·화면 재검토 결과는 [검토 기록](recheck-review.md)과 [검증 요약](validation-summary.md)을 확인합니다.\n\n'
        + '기존 162개 원고 컨테이너에 2부 도입 16개를 추가하여 178개가 됩니다. 실습 37개, '
        + '공통 생성 코드 1개·그리기 코드 7개, 순서도 4개를 유지합니다. 기존 화면은 보존하고 전자책 미리보기만 현재 32차시 표지·목차로 갱신합니다. 실습 번호는 새 차시에 맞춥니다.\n\n'
        + '재생성: `python scripts/split_textbook_32.py` → '
        + '`node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-32/book.md tmp/pdfs/book-spec-32.json` → '
        + '`python scripts/build_textbook_32_pdf.py` → '
        + '`python scripts/prepare_textbook_32_preview.py --pdf output/pdf/vibe-coding-32-coala-access-reviewed.pdf` → '
        + '`python scripts/build_textbook_32_pdf.py`. 저장소 루트에서 실행합니다. '
        + '분할 스크립트는 16차시 원고에서 32차시 원고를 다시 만드므로, 32차시 원고에 직접 수정한 내용이 있으면 먼저 보존합니다.\n', encoding='utf-8')
    print(json.dumps(split_report['preservation'], ensure_ascii=False))


if __name__ == '__main__':
    main()
