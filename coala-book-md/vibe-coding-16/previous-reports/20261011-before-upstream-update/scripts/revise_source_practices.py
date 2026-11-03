"""Reconcile the manuscript to the source PDF's actual practices, not new demos."""
from pathlib import Path
import re
import json
import shutil
import hashlib

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
ARCHIVE = BOOK / 'previous-reports/20261010-before-practice-review'
ARCHIVE.mkdir(parents=True, exist_ok=True)
for name in ('book.md', 'code-specs.json', 'code-results.json', 'asset-manifest.json', 'pdf-final-review.md'):
    target = ARCHIVE / name
    if not target.exists():
        shutil.copy2(BOOK / name, target)
for suffix in ('.pdf', '.json', '-qa.json'):
    src = ROOT / ('output/pdf/vibe-coding-16-final' + suffix)
    dst = ARCHIVE / src.name
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)

original = (BOOK / 'book.md').read_text(encoding='utf-8')
pattern = re.compile(r'^:::page\{[^\n]+\}\n.*?^:::[ \t]*$', re.M | re.S)
chunks = pattern.findall(original)
order = [re.search(r'id="([^"]+)"', p).group(1) for p in chunks]
pages = dict(zip(order, chunks))
changes = []
catalog = []


def set_page(pid, kind, title, body, attrs=''):
    pages[pid] = f':::page{{type="{kind}" id="{pid}"{attrs}}}\n# {title}\n\n{body.strip()}\n:::'
    changes.append(pid)


def concept(pid, title, sections):
    set_page(pid, 'concept', title, '\n\n'.join(f'## {heading}\n\n{text}' for heading, text in sections), ' layout="basic"')


def steps(pid, title, source_pages, entries):
    set_page(pid, 'step-process', title, '\n\n'.join(f'## {heading}\n\n{text}' for heading, text in entries))
    # Put the source in the first action paragraph, where the parser retains it.
    pages[pid] = pages[pid].replace(entries[0][1], f'원본 PDF {source_pages}쪽의 순서입니다. '+entries[0][1], 1)


def practice(pid, title, source_pages, label, description, checks, tip, kind='원본 실습'):
    set_page(pid, 'practice-opening', title,
        f'원본 PDF {source_pages}쪽 · {label}.\n\n{description}\n\n> [!TIP]\n> {tip}\n\n' +
        '\n'.join('- [ ] '+s for s in checks),
        ' practice="000-0" practice-kind="'+kind+'" platform="알고플로에서 실습하기"')
    catalog.append({'page_id':pid, 'title':title, 'source_pdf_pages':source_pages,
                    'source_label':label, 'source_type': 'numbered-practice' if label.startswith('실습 ') else 'source-worked-example',
                    'completion_criteria': checks})


def insert_before(anchor, pid):
    order.insert(order.index(anchor), pid)


def image_page(pid, title, src, alt, source, width='half', role=None):
    from PIL import Image
    with Image.open(BOOK/src) as im:
        ratio=f'{im.width}:{im.height}'
    role_attr = f' role="{role}"' if role else ''
    concept(pid,title,[('원본 실습 화면',alt+'\n\n'+
        f'::image{{src="{src}" alt="{alt}" ratio="{ratio}" width="{width}"{role_attr} caption="원본 PDF {source}쪽의 실습 화면"}}')])


# Remove invented stand-alone practice cards and repeated, newly authored records.
removed = [pid for pid in order if pid.endswith('-record')]
removed += ['ch03-request','ch04-practice-2','ch07-practice-2','ch16-practice-2']
order = [pid for pid in order if pid not in removed]

concept('book-guide','이 교재를 사용하는 방법',[
    ('원본 실습을 따라 배우기','158쪽 원본 교재의 실습과 문제풀이 예시를 16차시로 재구성했습니다. 각 실습에 원본 PDF 쪽수와 실습 이름을 표시했습니다.'),
    ('입력·동작·결과 확인','책의 조건과 위젯 이름을 먼저 읽습니다. 책에 제시된 값을 입력하고, 실행 결과를 원본 화면과 비교합니다. 입력값이 정해져 있지 않은 과제에서는 학습자가 값을 정합니다.'),
    ('코드와 그림','원본 GUI 화면은 원본에서 추출했습니다. Matplotlib·Pandas 코드는 원본의 데이터와 동작을 유지하고 독립 실행에 필요한 생성 코드 및 오타만 보완했습니다. 새 AI 응답이나 가상 오류 상황은 넣지 않았습니다.')])

# 1–3: original AI/prompt/algorithm tasks, with no made-up AI response.
practice('ch01-practice-1','AI는 어떤 질문을 잘하고, 어려워할까?','8','실습 001-1',
    '일반 지식, 실시간 정보 등 질문 유형에 따라 AI의 답변을 비교해봅시다. 답변을 잘한 질문과 확인이 필요한 질문을 구분합니다. 개인 정보는 실제 개인정보를 입력하지 않고 질문 유형으로만 살펴봅니다.',
    ['서로 다른 질문 유형을 비교했다.','잘 답한 부분과 확인할 부분을 구분했다.','AI 답변의 근거를 확인했다.'],'원본 활동처럼 질문 유형에 따른 차이를 살펴봅니다.')
practice('ch02-practice-1','어떤 질문이 더 좋은 답을 만들까?','10-12','실습 002-1',
    '책의 “공부 계획 알려줘”와 “시험이 2주 남았는데 하루 2시간씩 공부할 수 있어. 효율적인 공부 계획을 짜줘.”를 비교해봅시다. 답변에 상황과 조건이 반영되는지 확인합니다.',
    ['같은 주제의 짧은 질문과 구체적인 질문을 비교했다.','2주와 하루 2시간이라는 조건을 확인했다.','아쉬운 답변은 질문을 다듬어 다시 확인했다.'],'답변의 길이보다 요청한 조건의 반영 여부를 봅니다.')
practice('ch02-practice-2','앱에 필요한 입력 데이터 설계하기','13-15','실습 002-2',
    '원본의 BMI 계산 앱을 기준으로 목적과 입력 데이터를 정해봅시다. 결과를 계산하려면 키와 몸무게가 필요함을 확인하고 입력과 처리의 관계를 정리합니다.',
    ['앱의 목적을 BMI 계산으로 정했다.','필요한 입력을 키와 몸무게로 구분했다.','입력 데이터와 처리 결과의 관계를 설명했다.'],'원본의 입력 데이터 설계 활동이며 건강 판정 기능을 추가하는 과제가 아닙니다.')
concept('ch02-request','책의 질문을 구체적으로 다듬기',[
    ('원본 PDF 10-12쪽','- 짧은 요청: 공부 계획 알려줘.\n- 구체적인 요청: 시험까지 2주, 하루 2시간 공부 조건을 포함합니다.\n- 여행 질문: 2박 3일 부산 여행, 실내 활동 위주라는 조건을 포함합니다.'),
    ('원본 실습의 확인 기준','같은 주제로 질문을 다듬고 결과를 비교합니다. 새로운 앱 제작 요청이나 미리 작성된 AI 답변을 비교 대상으로 삼지 않습니다.')])
practice('ch03-practice-1','내 아이디어를 단계별로 나눠보기','17-18','실습 003-1',
    '원본의 감정 기록 앱 예시를 입력·처리·출력으로 나누어봅시다. 오늘의 기분을 입력하고 감정 상태를 분류한 뒤 결과를 보여주는 순서로 정리합니다.',
    ['입력할 내용을 정리했다.','입력 뒤 처리할 작업을 정리했다.','마지막에 보여줄 결과를 정리했다.'],'감정 분류는 프로그램 구조를 배우기 위한 예시입니다.')

# 4–7: preserve the source algorithms; remove arbitrary numeric datasets.
practice('ch04-practice-1','우리 가족 나이 합 구하기','23-24','실습 004-1',
    '엄마 43살, 아빠 45살, 나 15살의 나이를 더하는 순서도를 만들어봅시다. momage, dadage, myage, total을 사용하고 합계 103을 확인합니다.',
    ['책의 세 나이 43·45·15를 사용했다.','세 나이를 더하는 처리를 연결했다.','총합 103을 확인했다.'],'원본의 “점수” 표현은 가족 나이에 맞게 고쳤습니다.')
steps('ch04-family-code','가족 나이 합 · 원본 문제풀이 순서','23-24',[
    ('변수 준비','momage, dadage, myage, total을 준비합니다.'),('나이 입력','각 변수에 책의 43, 45, 15를 넣습니다.'),('합계 처리','total = momage + dadage + myage로 계산합니다.'),('결과 출력','가족 나이의 총합 103을 보여줍니다.')])
steps('ch04-scores-code','학생 세 명의 총점 · 원본 문제풀이','26',[
    ('변수 준비','s1, s2, s3, total을 준비합니다.'),('점수 입력','세 학생의 점수를 입력하고 정수로 변환합니다. 원본은 입력 점수 세 개를 미리 지정하지 않습니다.'),('총점 계산','total = s1 + s2 + s3으로 더합니다.'),('총점 출력','학생 세 명의 총점수를 출력합니다. 평균 계산 과제와 구분합니다.')])
practice('ch05-practice-1','10일 동안의 운동 시간 누적하기','31-32','실습 005-1',
    '1일차에 1분, 2일차에 2분씩 운동 시간을 늘려 10일차에 10분 운동합니다. 책의 반복 순서도로 1부터 10까지 더하고 총 55분을 확인해봅시다.',
    ['처음 합계를 0분으로 정했다.','1일차부터 10일차까지 반복했다.','총 운동 시간 55분을 확인했다.'],'마지막 10일차를 포함합니다.')
steps('ch05-exercise-code','운동 시간 누적 · 원본 의사코드','31-32',[
    ('처음 값 설정','time1은 1, total은 0에서 시작합니다.'),('조건 확인','time1 <= 10인 동안 반복합니다.'),('시간 누적','total에 time1을 더하고 time1을 1 증가시킵니다.'),('결과 출력','반복이 끝나면 총 운동 시간 55분을 출력합니다.')])
practice('ch05-practice-2','하루 카페인 섭취량 누적하기','27','실습 004-2',
    '책의 카페인 누적 실습을 따라 처음 총량을 0mg으로 정합니다. 음료의 카페인 양을 입력할 때마다 더하고, 입력이 끝나면 총량을 출력합니다. 원본은 각 음료의 입력값을 지정하지 않습니다.',
    ['처음 총 카페인 양을 0mg으로 정했다.','음료 입력을 반복해 총량에 더했다.','입력이 끝났을 때 총량을 출력했다.'],'원본의 하루·일주일 표현을 제목에 맞게 하루로 통일했습니다.')
steps('ch05-caffeine-code','카페인 누적 · 원본 입력 반복','27',[
    ('총량 준비','총 카페인 양을 0mg으로 시작합니다.'),('음료 값 더하기','음료의 카페인 양을 입력하고 현재 총량에 더합니다.'),('입력 반복','더 입력할 내용이 있으면 같은 작업을 반복합니다.'),('최종 총량 출력','입력이 끝나면 누적한 총량을 출력합니다. 50·30·0 같은 새 고정 입력 예시는 사용하지 않습니다.')])
practice('ch06-practice-1','수면 시간에 따른 안내 · 원본 순서도','36','조건문 본문 예시',
    '원본의 수면 시간 순서도를 따라봅시다. 8시간 이상인지 먼저 판단하고, 아니면 5시간 이상인지 판단하여 책의 세 안내 문구 중 하나를 출력합니다.',
    ['8시간 이상 조건을 먼저 확인했다.','그렇지 않을 때 5시간 이상 조건을 확인했다.','충분한 수면·적정 수면·수면 부족의 세 출력을 구분했다.'],'책의 조건문 학습용 규칙입니다.',kind='본문 예시 따라하기')
steps('ch06-sleep-code','수면 시간 · 원본 조건 처리','36',[
    ('입력받기','수면 시간을 입력받습니다. 책은 하나의 고정 입력 시간을 지정하지 않습니다.'),('첫 조건 판단','8시간 이상이면 “충분한 수면입니다”를 출력합니다.'),('다음 조건 판단','8시간 미만일 때 5시간 이상이면 “적정 수면입니다”를 출력합니다.'),('나머지 경우','5시간 미만이면 “수면 부족입니다”를 출력합니다.')])
concept('ch06-fix','책의 조건 검사 순서 읽기',[
    ('원본 PDF 36쪽','8시간 이상인 값은 5시간 이상에도 해당합니다. 원본 순서도는 8시간 조건부터 확인하고, 해당하지 않을 때 다음 조건으로 이동합니다.'),('연결 확인','첫 조건의 NO가 두 번째 조건으로 이어지는지 확인합니다. 각 YES와 마지막 NO는 해당 안내 문구로 연결합니다.')])
practice('ch07-practice-1','입력받은 학생 수만큼 점수 통과 여부 확인','40','실습 007-1',
    '학생 수 N을 정하고 각 학생의 점수를 입력받아봅시다. 원본 기준에 따라 80점 이상이면 PASS, 80점 미만이면 FAIL을 출력합니다. 점수 목록을 세 개로 고정하지 않습니다.',
    ['입력받은 학생 수 N만큼 처리했다.','80점 이상과 미만을 구분했다.','학생마다 PASS 또는 FAIL을 출력했다.'],'원본 38쪽의 60점 설명 예시와 40쪽의 80점 실습 기준을 구분합니다.')
steps('ch07-pass-code','학생 수 N을 사용하는 원본 실습 순서','40',[
    ('학생 수 정하기','처리할 학생 수 N을 입력받고 반복 변수를 0에서 시작합니다.'),('점수 입력','학생 한 명의 점수를 입력받습니다.'),('통과 여부 출력','80점 이상이면 PASS, 80점 미만이면 FAIL을 출력합니다.'),('다음 학생 처리','반복 변수를 1 증가시키고 N명 처리가 끝날 때까지 반복합니다.')])
steps('ch07-movie-code','영화 관람 가능 여부 · 원본 문제풀이','39',[
    ('네 학생의 나이 입력','원본처럼 학생 네 명의 나이를 하나씩 입력받습니다. 별도의 네 나이 목록은 제시하지 않습니다.'),('관람 조건 판단','책에 주어진 15세 이상 조건을 확인합니다.'),('결과 출력','각 학생에 대해 관람가능 또는 관람불가를 출력합니다.'),('네 번 반복','네 학생 모두에게 결과가 출력되었는지 확인합니다.')])

# 8: restore the omitted message-window practice and retain original Field task.
practice('ch08-practice-1','버튼 클릭하면 배경색과 글자색 바꾸기','44-46','실습 008-1',
    'Flet 디자이너에 btn1을 추가하고 클릭 이벤트를 작성해봅시다. 책처럼 버튼을 누르면 배경색은 blue, 글자색은 white로 바뀌게 합니다.',
    ['btn1을 화면에 추가했다.','클릭 이벤트에 blue와 white를 지정했다.','클릭 후 배경색과 글자색을 함께 확인했다.'],'원본의 btn1.bgcolor와 btn1.color 역할을 구분합니다.')
practice('ch08-practice-message','버튼 클릭하면 메시지 창 출력하기','49-51','실습 008-2',
    'Field에 “안녕하세요”를 입력하고 Button을 눌러 메시지 창에 입력값이 나타나도록 만들어봅시다. fld1과 btn1을 연결하고 원본의 입력 화면과 알림 창을 비교합니다.',
    ['fld1과 btn1을 화면에 추가했다.','버튼 이벤트가 fld1의 값을 읽는다.','메시지 창에 입력한 인사말이 나타난다.'],'message는 수업 도구 전용 기능이며 독립 Python의 기본 함수가 아닙니다.')
insert_before('ch08-practice-2','ch08-practice-message')
concept('ch08-message-screen','원본의 입력 화면과 메시지 창',[
    ('입력 화면','책처럼 fld1에 안녕하세요를 입력합니다.\n\n::image{src="assets/source-20261010/message-input.png" alt="원본 실습의 안녕하세요 입력창과 Button" ratio="424:247" width="half" caption="원본 PDF 49쪽의 입력 화면"}'),
    ('클릭 결과','버튼을 클릭하면 알림 창에서 같은 입력 내용을 확인합니다.\n\n::image{src="assets/source-20261010/message-dialog.png" alt="원본 실습의 안녕하세요 알림 창" ratio="462:274" width="half" caption="원본 PDF 49쪽의 메시지 창"}')])
insert_before('ch08-practice-2','ch08-message-screen')
practice('ch08-practice-2','Field에 입력한 내용 버튼으로 출력하기','52-53','실습 008-3',
    '원본처럼 fld1에 “안녕”을 입력하고 추가 버튼을 눌러 fld2에 내용을 표시해봅시다. 삭제 버튼을 누르면 두 Field의 내용이 모두 지워지는지 확인합니다.',
    ['fld1·fld2와 추가·삭제 버튼을 배치했다.','추가 후 원본 그림처럼 fld2에 안녕이 보인다.','삭제 후 두 Field의 내용이 지워진다.'],'처음 상태에서 추가 버튼을 한 번 눌러 원본 그림과 비교합니다.')
steps('ch08-request','Field 실습 · 원본 이벤트 설정','52-53',[
    ('UI 배치','fld1, fld2, btn1, btn2를 책의 배치대로 추가합니다.'),('추가 버튼','btn1을 클릭하면 fld1에 입력한 내용을 fld2에 표시하도록 역할과 이벤트를 적습니다.'),('삭제 버튼','btn2를 클릭하면 fld1과 fld2의 내용을 모두 지우도록 적습니다.'),('실행 확인','프로젝트를 생성한 뒤 안녕 입력·추가·삭제를 순서대로 확인합니다.')])

# 9–11: original GUI programs, no substitute console demos or invented faults.
practice('ch09-practice-1','Field에 입력한 두 수의 누적곱 출력','54-55','실습 008-4',
    '책의 화면처럼 fld1에 1, fld2에 6을 넣고 누적 버튼을 눌러봅시다. 1부터 6까지의 곱 720이 fld3에 표시되는지 확인합니다. 다시 누르면 현재 입력으로 결과를 바꿉니다.',
    ['fld1·fld2·fld3과 누적 버튼을 배치했다.','책의 1과 6으로 결과 720을 확인했다.','다시 실행하면 현재 값으로 결과가 바뀐다.'],'곱을 누적할 처음 값은 1입니다.')
steps('ch09-product-code','누적곱 프로그램의 원본 동작','54-55',[
    ('두 수 입력','책의 시작 값 1과 끝 값 6을 각 Field에 입력합니다.'),('버튼 이벤트 설정','두 수 사이의 값을 곱하도록 누적 버튼의 역할을 작성합니다.'),('결과 표시','fld3에서 720을 확인합니다.'),('재실행','새 입력으로 다시 누르면 이전 결과를 현재 계산 결과로 바꿉니다.')])
practice('ch09-practice-2','계산기 프로그램 2','61-62','실습 008-5',
    'fld1과 fld2에 두 숫자를 입력합니다. 연산 버튼을 눌러 +, -, *, /를 차례로 바꾸고 = 버튼으로 계산합니다. 책의 100과 5, 나눗셈을 사용해 결과 20.0을 확인해봅시다.',
    ['두 Field와 연산·계산 버튼을 배치했다.','연산 기호가 순서대로 바뀐다.','100 / 5의 결과 20.0이 보인다.'],'원본의 두 수 계산기를 사용하며 자유 입력 수식을 eval로 실행하지 않습니다.')
steps('ch09-calculator-request','계산기 2 · 원본 위젯과 이벤트','61-62',[
    ('입력 위젯','fld1과 fld2는 각각 계산할 숫자를 받습니다.'),('연산 버튼','btn1을 누르면 연산 기호가 +, -, *, / 순서로 바뀝니다.'),('계산 버튼','btn2를 누르면 현재 기호에 따라 두 값을 계산합니다.'),('결과 확인','원본 62쪽 화면의 결과 표시 위젯 txt1에서 값을 확인합니다. 본문의 세 번째 Field 표현과 캡처를 구분합니다.')])
concept('ch09-calculator-code','책의 두 계산기 예시 구분하기',[
    ('원본 PDF 56-62쪽','원본에는 수식 전체를 입력하는 계산기와 두 수를 입력하는 계산기가 있습니다. 이번 차시는 61-62쪽 계산기 2의 입력·연산·출력을 그대로 따라갑니다.'),('실습 범위','두 숫자와 선택한 사칙연산을 처리합니다. 수식 전체를 eval로 실행하는 예시는 따라쓰기 코드로 넣지 않았습니다.')])
practice('ch09-practice-3','Text에 원하는 내용 추가 프로그램','63-64','실습 008-6',
    'fld1에 내용을 입력하고 추가 버튼을 눌러 txt1에 표시해봅시다. 원본 화면처럼 이전에 표시한 내용과 새로 추가한 내용을 함께 확인합니다.',
    ['fld1·btn1·txt1을 배치했다.','추가 버튼이 fld1의 내용을 txt1에 넣는다.','원본 화면과 추가된 내용을 비교했다.'],'Text 출력과 Field 입력의 역할을 구분합니다.')
practice('ch09-practice-4','원하는 단 구구단 출력하기','65-66','실습 008-7',
    'fld1에 원하는 단을 입력하고 버튼을 눌러 txt1에 구구단을 출력해봅시다. 책의 4단 화면과 4 × 1부터 4 × 9까지의 결과를 비교합니다.',
    ['fld1·btn1·txt1을 배치했다.','입력한 단의 구구단이 출력된다.','책의 4단 아홉 줄과 비교했다.'],'버튼 클릭과 반복 출력을 연결합니다.')
steps('ch09-times-code','구구단 실습 · 원본 프로그램 순서','65-66',[
    ('단 입력','책의 화면처럼 fld1에 4를 넣습니다.'),('이벤트 설정','btn1을 눌렀을 때 입력한 단의 구구단을 출력하도록 적습니다.'),('반복 출력','곱하는 수 1부터 9까지의 결과를 txt1에 출력합니다.'),('원본과 대조','4단의 아홉 줄을 책의 결과 화면과 비교합니다.')])
practice('ch10-practice-1','Dropdown을 추가하고 선택한 값 확인','68-70','실습 008-8',
    'fld1에 새 항목을 입력하고 버튼을 눌러 ddl1 목록에 추가해봅시다. 목록에서 항목을 선택하면 선택한 값이 txt1에 출력되는지 확인합니다.',
    ['fld1·ddl1·btn1·txt1을 배치했다.','입력한 항목이 목록에 추가된다.','선택한 값이 txt1에 출력된다.'],'항목 추가 버튼과 Dropdown 선택 이벤트를 각각 설정합니다.')
practice('ch10-practice-2','오늘의 건강습관 체크 프로그램','73-75','실습 009-1',
    '원본의 네 건강습관 Checkbox를 배치해봅시다. 오늘 실천한 항목을 선택하고 결과 확인 버튼으로 선택된 습관의 이름과 개수를 Text에 출력합니다.',
    ['chk1부터 chk4까지 배치했다.','선택한 습관 이름을 출력했다.','선택한 항목의 개수를 함께 출력했다.'],'원본의 체크 활동이며 별도의 건강 점수나 진단 기능을 만들지 않습니다.')
steps('ch10-health-request','건강습관 실습 · 원본 버튼 이벤트','73-75',[
    ('건강습관 선택','원본 화면의 네 항목 중 실천한 항목을 체크합니다.'),('선택값 읽기','btn1은 각 Checkbox의 선택 여부를 읽습니다.'),('이름과 개수 출력','선택한 습관의 이름과 총개수를 Text에 출력합니다.')])
practice('ch10-practice-3','선택한 동아리 소개 프로그램','78-80','실습 009-2',
    '원본의 코딩·방송·미술·과학 동아리를 Radio 그룹에 배치해봅시다. 한 동아리를 선택하고 확인 버튼을 누르면 이름과 안내 내용이 txt1에 표시되게 합니다.',
    ['rad1부터 rad4까지 같은 그룹에 넣었다.','한 동아리만 선택할 수 있다.','선택한 동아리 이름과 안내가 txt1에 보인다.'],'원본 실행 화면의 과학 동아리 선택 상태와 비교합니다.')
practice('ch10-practice-4','ProgressBar 버튼 2개로 증가·감소','82-83','실습 009-3',
    'prg1의 처음 값을 0.0으로 설정해봅시다. 증가 버튼은 0.1을 더하고 감소 버튼은 0.1을 빼도록 설정합니다. 책 81쪽의 범위 0.0부터 1.0을 확인합니다.',
    ['prg1과 두 버튼을 배치했다.','증가·감소에 따라 0.1씩 바뀐다.','0.0부터 1.0 범위를 확인했다.'],'책의 value 범위와 버튼 증감값을 구분합니다.')
practice('ch10-practice-5','Image 구성하기','85-87','실습 009-6',
    '책처럼 Image 두 개를 불러오고 각각 크기를 설정해봅시다. 이미지 사이에 Divider를 넣고 세로로 구분되어 보이는지 확인합니다.',
    ['Image 두 개를 화면에 배치했다.','width와 height로 크기를 설정했다.','두 이미지 사이에 Divider가 보인다.'],'이미지가 보이지 않으면 인터넷 연결과 이미지 주소를 확인합니다.')
practice('ch11-practice-1','학생 성적을 Table에 기록하기','90-92','실습 009-7',
    'fld1부터 fld4까지 학생 이름과 국어·수학·영어 점수를 입력해봅시다. 추가하기 버튼을 누르면 tbl1에 한 행이 기록되는지 원본 화면과 비교합니다. 과목 순서는 캡처에 맞춥니다.',
    ['입력창과 표의 이름·국어·수학·영어 순서를 맞췄다.','추가하기를 누르면 표에 한 행이 기록된다.','입력값과 표의 각 칸을 대조했다.'],'원본 본문의 국어·영어·수학 순서와 캡처의 순서 차이를 바로잡았습니다.')
steps('ch11-request','Table 실습 · 원본 입력과 추가','90-92',[
    ('위젯 배치','fld1부터 fld4, btn1, tbl1을 책의 화면대로 구성합니다.'),('입력창 역할','fld1은 이름, fld2는 국어, fld3은 수학, fld4는 영어로 정합니다.'),('추가 이벤트','btn1은 입력한 네 값을 표의 같은 순서로 추가합니다.'),('화면 대조','원본 화면에 있는 학생1의 100·90·80과 표의 열을 비교합니다.')])
steps('ch11-index-code','행·열 번호를 리스트 위치로 바꾸기','89',[
    ('화면 번호 확인','원본 예시처럼 화면에서 2행을 선택했다고 생각해봅시다.'),('리스트 위치 변환','첫 행의 인덱스는 0, 둘째 행의 인덱스는 1입니다. 선택한 행·열 번호에서 각각 1을 뺍니다.'),('선택한 셀 확인','변환한 행과 열 위치가 원하는 DataCell에 해당하는지 확인합니다.')])
steps('ch11-practice-2','표의 값 변경 · 원본 본문 절차','89',[
    ('행·열 선택','사용자가 값을 넣을 행 번호와 열 번호를 선택합니다.'),('값 입력','Field에 표에 넣을 값을 입력합니다. 88에서 89로 바꾸는 별도 과제는 사용하지 않습니다.'),('인덱스 변환','선택한 번호에서 1을 빼서 리스트 위치로 바꿉니다.'),('변경 반영','선택한 DataCell의 내용을 바꾸고 표에 표시합니다.')])

# 12: restore original saved-data, school-count and subway-API practices.
practice('ch12-practice-1','꺾은선 그래프 만들기','97-99','시각화 프로그램 1',
    'fld1부터 fld5까지 다섯 수치를 입력하고 그래프 그리기 버튼을 눌러봅시다. 책의 실행 화면에 있는 1·2·5·4·5를 사용하고 초기화 버튼의 역할도 확인합니다.',
    ['다섯 Field와 Chart를 구성했다.','책의 입력값이 꺾은선으로 표시된다.','초기화 버튼을 확인했다.'],'원본 그래프의 가로 위치는 입력 순서 0부터 4입니다.',kind='원본 시각화 실습')
practice('ch12-practice-2','키·몸무게 산점도 만들기','100-102','시각화 프로그램 2',
    '두 Field에 키와 몸무게를 입력하고 버튼으로 Chart에 점을 추가해봅시다. 책의 실행 화면에 보이는 170·75, 180·82, 185·89를 대조합니다.',
    ['키와 몸무게를 서로 다른 입력창으로 받는다.','입력한 한 쌍이 점 하나로 표시된다.','누적한 세 쌍을 원본 화면과 비교했다.'],'원본은 현재 값만 표시할지 누적할지 정하도록 안내합니다.',kind='원본 시각화 실습')
practice('ch12-practice-3','입력값 막대그래프 만들기','103-105','시각화 프로그램 3',
    'fld1의 값을 버튼으로 차례로 추가하여 막대그래프로 만들어봅시다. 책에 보이는 90·80·70의 세 막대를 비교합니다.',
    ['입력창·버튼·Chart를 구성했다.','입력한 값을 막대로 표시했다.','90·80·70의 세 막대를 원본과 비교했다.'],'원본 설명처럼 누적할지 현재 자료만 보일지 정합니다.',kind='원본 시각화 실습')
practice('ch12-practice-data','학생 100명 자료 불러와 시각화하기','106-109','저장된 데이터 불러오기',
    '자료 버튼에서 책의 학생 100명 키·몸무게 자료를 불러와봅시다. 표에 표시할 항목을 고르고 키와 몸무게의 두 열을 산점도의 X·Y로 지정합니다.',
    ['학생 100명 자료를 선택했다.','표의 ID·키·몸무게 등 항목을 선택했다.','산점도에 연결할 두 열을 확인했다.'],'원본 자료를 수업 환경에서 제공받아 사용합니다. 새 가상 100명 자료는 만들지 않습니다.',kind='원본 자료 활용')
insert_before('ch12-loaded-data','ch12-practice-data')
steps('ch12-loaded-data','저장된 자료 · 원본 불러오기 순서','106-109',[
    ('자료 선택','자료 버튼에서 학생 100명의 키와 몸무게 자료를 선택합니다.'),('표 항목 선택','책의 ID·키·몸무게 또는 ID·성별·키·몸무게 구성을 살펴봅니다.'),('산점도 설정','X축과 Y축에 쓸 열을 직접 확인합니다. 원본 109쪽의 설명과 화면 축 범위를 대조합니다.')])
image_page('ch12-data-screen','원본 자료의 표시 항목 선택','assets/source-20261010/data-column-select.png','원본의 자료 항목 선택 메뉴입니다. 표시할 열을 선택하고 표와 그래프의 연결을 확인합니다.','107','text')
insert_before('ch12-practice-4','ch12-data-screen')
practice('ch12-practice-school','학교별 학생 수를 막대그래프로 표현','110','저장된 자료 활용 예시',
    '앞에서 불러온 같은 학생 자료를 사용해 학교별 학생 수를 막대그래프로 표시해봅시다. 원본처럼 고등학교와 중학교의 개수를 비교합니다.',
    ['앞의 학생 자료를 그대로 사용했다.','학교 항목별 개수를 집계했다.','고등학교·중학교 막대를 비교했다.'],'새 데이터셋을 만드는 활동이 아니라 불러온 자료를 다른 방식으로 보는 활동입니다.',kind='원본 자료 활용')
insert_before('ch12-practice-4','ch12-practice-school')
image_page('ch12-school-screen','원본의 학교별 개수 막대그래프','assets/source-20261010/school-count-chart.png','원본 학생 자료를 학교 구분별 개수로 표시한 화면입니다.','110','text')
insert_before('ch12-practice-4','ch12-school-screen')
practice('ch12-practice-api','자치구별 지하철역 정보 시각화','111-117','공공데이터 API 활용 예시',
    '원본의 “서울 교통공사 자치구별지하철역정보” 자료를 대상으로 합니다. 역개수·자치구·해당역(호선)을 tbl1에 표시하고 역 개수가 많은 상위 5개 자치구를 cht1에 나타내봅시다.',
    ['원본의 지하철역 자료 구조를 확인했다.','자치구와 역개수를 표·그래프에 연결했다.','상위 5개 자치구를 표시했다.'],'실제 실행에는 수업에서 확인한 API 주소와 인증 정보가 필요합니다. 원본 화면을 자신의 실행 결과로 제출하지 않습니다.',kind='원본 API 실습')
insert_before('ch12-practice-4','ch12-practice-api')
steps('ch12-api-steps','지하철역 API · 원본 실습 순서','112-117',[
    ('자료와 구조 확인','원본에 명시된 자료에서 역개수·자치구·해당역(호선)의 위치를 확인합니다.'),('위젯 구성','btn1, tbl1, cht1을 구성합니다.'),('데이터 가져오기','수업에서 확인한 API로 데이터를 가져와 표와 막대그래프에 연결합니다.'),('상위 5개 표시','원본처럼 역 개수가 많은 자치구 다섯 개만 선택하여 표시합니다. 새 수치나 현재 통계를 임의로 작성하지 않습니다.')])
insert_before('ch12-practice-4','ch12-api-steps')
image_page('ch12-api-screen','원본의 상위 5개 자치구 결과','assets/source-20261010/subway-top5-result.png','원본 PDF의 예시 결과입니다. API 인증 정보가 담긴 입력 화면은 제외하고 표와 그래프 결과만 사용했습니다. 현재 통계나 새 실행 결과를 뜻하지 않습니다.','117','text')
insert_before('ch12-practice-4','ch12-api-screen')
practice('ch12-practice-4','입력받은 데이터 저장·불러오기','118-127','입력 데이터 저장 예시',
    '책의 fld1·fld2, tbl1, cht1, 두 버튼으로 화면을 구성해봅시다. 표 저장 설정 후 데이터를 추가하고 프로젝트를 저장합니다. 불러오기에서 같은 기록이 남아 있는지 확인합니다.',
    ['표 저장 설정을 확인했다.','입력한 표·차트 데이터와 프로젝트를 저장했다.','다시 불러와 같은 기록을 확인했다.'],'표 모양은 표 저장 설정 전에 정한다는 원본 안내를 확인합니다.',kind='원본 저장 실습')

# 13: all eight actual Matplotlib practice objectives, original data/geometry.
practice('ch13-practice-1','Matplotlib 실습 1 · 배열 한 개','131-132','실습 013-1',
    '책의 [1, 2, 3, 4, 5] 배열을 선으로 그려봅시다. 하나의 배열을 전달했을 때 X축이 0부터 4까지의 위치가 되는지 확인합니다.',
    ['책의 배열을 그대로 사용했다.','배열 하나를 plot에 전달했다.','X 위치 0부터 4를 확인했다.'],'원본의 Chart 구성과 생성된 Axes 역할을 연결합니다.',kind='원본 Matplotlib')
practice('ch13-practice-two','Matplotlib 실습 2 · X·Y 배열','133','실습 013-2',
    '책의 a = [15, 25, 35, 45, 55], b = [5, 10, 15, 20, 25]를 X와 Y로 지정해봅시다. 두 배열의 같은 위치 값이 한 점으로 연결됩니다.',
    ['a와 b 배열을 책과 같이 정했다.','a는 X, b는 Y로 연결했다.','다섯 점의 위치를 원본과 비교했다.'],'두 배열의 길이와 값의 짝을 확인합니다.',kind='원본 Matplotlib')
insert_before('ch13-two-arrays','ch13-practice-two')
practice('ch13-practice-2','Matplotlib 실습 3 · 표시 범위','134','실습 013-3',
    'X는 [1, 2, 3, 4, 5], Y는 [5, 10, 15, 20, 25]로 정합니다. 책처럼 b-+ 모양과 axis([0, 10, 0, 25])를 적용해봅시다.',
    ['원본의 X·Y 값을 사용했다.','파란 선과 더하기 마커를 지정했다.','X 0-10, Y 0-25 범위를 확인했다.'],'값을 바꾸는 것과 표시 범위를 바꾸는 것을 구분합니다.',kind='원본 Matplotlib')
practice('ch13-practice-colors','Matplotlib 실습 4 · 모양과 색','136','실습 013-4',
    '책의 같은 X·Y 배열에 ro를 적용해 빨간 점으로 표시해봅시다. 원본 안내의 r-o도 비교하여 점만 그리는 경우와 선이 이어지는 경우를 구분합니다.',
    ['원본 배열을 유지했다.','ro가 빨간 점임을 확인했다.','r-o와의 선 표시 차이를 설명했다.'],'원본 코드 ro와 연결선 그림의 차이는 실행 결과를 기준으로 바로잡았습니다.',kind='원본 Matplotlib')
insert_before('ch13-markers','ch13-practice-colors')
practice('ch13-practice-labels','Matplotlib 실습 5 · 제목과 설명','137-138','실습 013-5',
    '원본에서 같은 그래프에 지정한 x·y 축 이름, hello 제목, 좌표 (3, 5)의 12/19 설명을 확인해봅시다. 앞 실습의 코드와 데이터를 그대로 사용합니다.',
    ['x·y 축 이름을 확인했다.','hello 제목을 확인했다.','(3, 5)의 12/19 설명을 확인했다.'],'원본 실습 4와 5의 코드는 같고, 이번에는 설명 글자에 집중합니다.',kind='원본 Matplotlib')
insert_before('ch13-practice-3','ch13-practice-labels')
image_page('ch13-labels-screen','원본 실습의 제목·축·좌표 설명','assets/source-20261006/plot-markers.png','원본 136·138쪽의 동일한 코드로 만든 수정 결과입니다. 제목 hello, 축 x·y와 좌표 설명 12/19를 확인합니다.','138','text')
pages['ch13-labels-screen']=pages['ch13-labels-screen'].replace('원본 PDF 138쪽의 실습 화면','원본 136·138쪽 코드를 오류 수정하여 실행한 결과')
insert_before('ch13-practice-3','ch13-labels-screen')
practice('ch13-practice-3','Matplotlib 실습 6 · 막대그래프 1','140','원본 실습 014-6',
    '책의 [1, 2, 4, 8, 16, 32, 64, 128]을 막대로 그려봅시다. range(len(a))로 X 위치를 만들고 각 높이를 확인합니다.',
    ['2의 거듭제곱 배열을 사용했다.','여덟 값의 막대를 그렸다.','막대 높이와 배열 값을 비교했다.'],'원본의 실습 번호와 제목 오기는 이 교재에서 차시 순서에 맞게 정리했습니다.',kind='원본 Matplotlib')
practice('ch13-practice-grouped','Matplotlib 실습 7 · 막대그래프 2','141-142','원본 실습 014-7',
    'one부터 five까지의 항목과 책의 value_a·value_b 배열을 사용해봅시다. 원본 create_x 함수로 두 막대의 위치를 만들고 중간 위치에 항목 이름을 표시합니다.',
    ['원본의 두 값 배열을 유지했다.','create_x로 두 막대를 나란히 배치했다.','중간 위치에 one부터 five까지 표시했다.'],'원본의 t, w, n, d 위치 계산을 유지합니다.',kind='원본 Matplotlib')
insert_before('ch13-grouped','ch13-practice-grouped')
practice('ch13-practice-4','Matplotlib 실습 8 · 산점도','144-145','원본 실습 014-8',
    '책의 시드 20211206, X 범위 1.1부터 100.0 미만, 간격 5.0을 유지해봅시다. X의 1.5배에 난수를 더한 Y로 산점도를 만들고 축 이름을 함수 호출로 설정합니다.',
    ['책의 시드와 X 범위를 사용했다.','책의 Y 생성식을 사용했다.','축 이름·random 범례·제목을 확인했다.'],'원본의 seed·rand 설명과 축 이름 대입 오류만 바로잡았습니다.',kind='원본 Matplotlib')
concept('ch13-fix','원본 그래프에서 바로잡은 코드',[
    ('원본 PDF 136·138쪽','ro는 빨간 점입니다. 코드가 ro일 때 점을 이어 그린 그림은 코드와 다르므로 실제 실행 그림을 사용했습니다.'),
    ('원본 PDF 144-145쪽','seed는 난수 생성기의 상태를 정합니다. 축 이름은 set_xlabel("X축 제목"), set_ylabel("Y축 제목")처럼 함수로 설정합니다. 생성 데이터는 원본 예제이며 실제 관측 자료가 아닙니다.')])

# 14: restore the omitted dictionary DataFrame, preserve all source data.
practice('ch14-practice-1','Series · 원본 딕셔너리와 리스트','148-149','Pandas 본문 예시',
    'one·two·three 딕셔너리와 [2022-01-01, 2.14, song, 1000, True] 리스트로 Series를 만들어봅시다. 원본처럼 Series, index, values를 각각 확인합니다.',
    ['원본 딕셔너리와 리스트를 사용했다.','Series 전체를 출력했다.','index와 values를 구분했다.'],'독립 Python 실행에서는 원본 message를 print로 바꿉니다.',kind='본문 예시 따라하기')
practice('ch14-practice-dict','DataFrame · 요일별 열 만들기','150','Pandas 본문 예시',
    '원본의 mon부터 sun까지 딕셔너리를 DataFrame으로 바꿔봅시다. 딕셔너리의 키가 열 이름, 각 리스트가 해당 열의 값이 되는지 확인합니다.',
    ['원본의 일곱 열 데이터를 사용했다.','DataFrame으로 변환했다.','열 이름과 각 행 값을 확인했다.'],'원본의 tue 배열 [2, 9, 6, 23]을 그대로 유지합니다. 달력 날짜로 재해석하지 않습니다.',kind='본문 예시 따라하기')
insert_before('ch14-practice-2','ch14-practice-dict')
insert_before('ch14-practice-2','ch14-dict-frame-code')
practice('ch14-practice-2','DataFrame · 행·열 이름 지정과 변경','151','Pandas 본문 예시',
    '현아 [15, 여, 중2]와 태민 [17, 남, 고1] 자료를 사용해봅시다. 행·열 이름을 확인하고 책처럼 행은 학생1·학생2, 열은 연령·남녀·학년으로 바꿉니다.',
    ['현아·태민의 원본 자료를 사용했다.','행 이름과 열 이름을 구분했다.','학생1·학생2와 연령·남녀·학년으로 변경했다.'],'본문의 유상 표기는 코드와 같은 태민으로 고쳤습니다.',kind='본문 예시 따라하기')

# 15–16: original robot tasks and ONE original free-project practice.
practice('ch15-practice-1','코코봇 이동·회전 시켜보기','153-154','코코봇 프로그램 예시',
    '책의 세 버튼으로 앞으로 이동, 왼쪽 90도 회전, 오른쪽 90도 회전을 실행하는 프로그램을 설계해봅시다. 실제 동작은 수업의 장비 연결 환경에서 확인합니다.',
    ['세 버튼에 책의 역할을 지정했다.','이동과 양쪽 회전을 각각 연결했다.','실행 또는 미실행 상태를 구분했다.'],'이동 값 100의 단위는 장비 환경에서 확인합니다.',kind='원본 코코봇 실습')
practice('ch15-practice-2','입력받은 거리·각도로 코코봇 움직이기','155-157','코코봇 프로그램 예시',
    'fld1은 이동거리, fld2는 회전각도로 구성해봅시다. 책의 화면처럼 이동거리 100과 회전각도 90을 입력하고 각 버튼이 해당 입력을 읽도록 설정합니다.',
    ['거리와 각도 입력창을 구분했다.','이동 버튼은 거리 값을 읽는다.','회전 버튼은 각도 값을 읽는다.'],'책에 없는 코코봇 함수를 만들어 넣지 않고 수업에서 제공한 명령을 사용합니다.',kind='원본 코코봇 실습')
steps('ch15-request','코코봇 · 원본 위젯 역할 설정','154-156',[
    ('프로젝트 정보','원본처럼 코코봇 이동과 회전 기능을 프로젝트 설명에 적습니다.'),('입력창 역할','fld1은 이동거리, fld2는 회전각도로 역할을 정합니다.'),('버튼 역할','앞으로 이동, 왼쪽 회전, 오른쪽 회전의 세 역할을 각 버튼에 적습니다.'),('환경 연결','실제 수업에서 제공한 명령과 장비 연결을 확인하고 실행합니다.')])
practice('ch16-practice-1','원하는 프로그램을 자유롭게 작성하기','93-94','실습 009-8',
    '원본 자율 프로젝트 활동을 따라 프로그램 아이디어와 UI 설계를 작성해봅시다. 앞에서 배운 위젯으로 화면을 구성하고 버튼 이벤트를 정한 뒤 실행 결과를 확인합니다.',
    ['프로그램 아이디어를 적었다.','원본 양식처럼 UI를 설계했다.','생성한 프로그램의 동작을 확인했다.'],'새 프로젝트 목록을 제시하기보다 앞선 원본 실습의 위젯과 기능을 활용합니다.')
concept('ch16-projects','자율 프로젝트 · 원본 작성 양식',[
    ('원본 PDF 93쪽','만들고 싶은 프로그램의 아이디어를 작성합니다. 목적과 필요한 입력, 보여줄 결과를 정리합니다.'),('원본 PDF 94쪽','UI 설계를 작성합니다. 필요한 위젯을 배치하고 이름과 역할, 버튼을 클릭했을 때 할 일을 적습니다.')])
concept('ch16-fix','자율 프로젝트의 입력과 동작 확인',[
    ('원본 설계와 대조','입력창·버튼·결과 위젯의 역할이 자신이 적은 아이디어와 같은지 확인합니다.'),('확인 결과 정리','실행 화면과 확인한 동작을 남깁니다. 원본에 없는 “수학과 영어가 바뀐 오류” 상황이나 가상 AI 응답을 새 과제로 넣지 않습니다.')])

# Source-specific checks; no newly added boundary-value worksheets.
check_map={
 1:['원본 실습의 질문 유형을 비교했다.','잘 답한 질문과 확인할 질문을 구분했다.'],
 2:['공부 계획의 2주·하루 2시간 조건을 확인했다.','BMI 계산에 필요한 키·몸무게 입력을 설계했다.'],
 3:['감정 기록 앱의 입력·처리·출력을 구분했다.','각 작업의 순서를 정리했다.'],
 4:['43·45·15의 가족 나이 합 103을 확인했다.','학생 세 명의 점수를 더하는 흐름을 설명했다.'],
 5:['1일차부터 10일차까지 총 55분을 확인했다.','카페인 입력을 반복하고 총량을 출력했다.'],
 6:['8시간 조건과 5시간 조건의 순서를 확인했다.','원본의 세 출력 문구를 올바르게 연결했다.'],
 7:['N명의 점수에 80점 PASS 기준을 적용했다.','네 학생 나이의 15세 관람 조건을 설명했다.'],
 8:['버튼의 blue·white 변경을 확인했다.','입력 인사말을 메시지 창에 표시했다.','Field 추가·삭제를 원본과 비교했다.'],
 9:['1부터 6까지의 누적곱 720을 확인했다.','계산기 2의 100 / 5 = 20.0을 확인했다.','Text 추가와 4단 출력을 원본과 비교했다.'],
 10:['Dropdown의 항목 추가·선택을 확인했다.','Checkbox와 Radio 선택 결과를 확인했다.','진행 막대 증감과 두 이미지·Divider를 확인했다.'],
 11:['원본 Table의 입력과 과목 순서를 맞췄다.','행·열 번호에서 1을 빼는 이유를 설명했다.'],
 12:['책의 선·산점도·막대그래프를 따라 만들었다.','학생 자료의 표시 항목과 학교별 개수를 확인했다.','API 실습은 실제 실행과 원본 결과 열람을 구분했다.','저장·불러오기에서 입력 데이터를 확인했다.'],
 13:['원본 여덟 Matplotlib 실습을 대조했다.','배열·범위·마커·글자·막대 위치를 확인했다.','산점도의 시드와 축 이름을 확인했다.'],
 14:['원본 Series 자료의 index·values를 구분했다.','요일별 열과 현아·태민 DataFrame을 만들었다.','원본의 행·열 이름 변경을 확인했다.'],
 15:['책의 이동·양쪽 회전 버튼을 설계했다.','거리 100·각도 90 입력과 버튼을 맞췄다.','장비 실행 여부를 실제로 구분했다.'],
 16:['원본 자율 프로젝트의 아이디어·UI를 작성했다.','위젯 역할·이벤트·실행 결과를 대조했다.'],
}
for ch,items in check_map.items():
    set_page(f'ch{ch:02d}-check','practice-checklist','원본 실습의 완료 확인',
        '\n'.join('- [ ] '+v for v in items)+'\n\n> [!KEY_POINT]\n> 책의 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.')

# Existing explanatory chapter introductions must describe the restored source work.
intro_changes={
 'ch04-opening':('가족 나이와 학생 점수의 합을 구할 수 있다.','가족 나이 합과 학생 총점의 원본 흐름을 설명할 수 있다.'),
 'ch08-opening':('추가와 삭제 기능을 구분해 확인할 수 있다.','메시지 출력과 Field 추가·삭제를 확인할 수 있다.'),
 'ch12-opening':('표와 차트가 같은 데이터를 쓰는지 확인할 수 있다.','학생 자료와 공공데이터의 표·차트를 확인할 수 있다.'),
 'ch14-opening':('책의 데이터로 표를 만들고 확인할 수 있다.','요일별 열과 학생 정보 표를 만들 수 있다.'),
 'ch16-opening':('책의 자율 프로젝트를 마지막 차시로 확장했습니다. 계산기, 건강습관, 성적표, 차트 중 하나를 골라 작동하는 결과와 검증 기록을 발표합니다.','원본 93-94쪽 자율 프로젝트의 아이디어와 UI 설계를 따라 작성합니다. 앞서 배운 위젯으로 프로그램을 만들고 동작 결과를 설명합니다.'),
}
for pid,(a,b) in intro_changes.items():
    assert a in pages[pid],pid
    pages[pid]=pages[pid].replace(a,b)

# Renumber the restructured practice sequence while retaining each source label.
chapter=0;counts={};catalog_map={x['page_id']:x for x in catalog}
for pid in order:
    chunk=pages.get(pid)
    if chunk is None: # calendar code is inserted after executable outputs exist.
        continue
    m=re.search(r'type="chapter-opening".*?chapter="(\d+)"',chunk)
    if m:chapter=int(m.group(1))
    if 'type="practice-opening"' in chunk:
        counts[chapter]=counts.get(chapter,0)+1
        number=f'{chapter:03d}-{counts[chapter]}'
        pages[pid]=re.sub(r'practice="[^"]+"',f'practice="{number}"',chunk,1)
        catalog_map[pid]['chapter']=chapter;catalog_map[pid]['practice_id']=number

# Restore source code data and only the minimum independent-execution setup.
specs=json.loads((BOOK/'code-specs.json').read_text(encoding='utf-8'))
kept=[s for s in specs if s['chapter'] in (13,14)]
by_id={s['page_id']:s for s in kept}
by_id['ch13-one-array']['code']='import matplotlib.pyplot as plt\n\nfig, ax = plt.subplots(figsize=(8, 5))\nax.plot([1, 2, 3, 4, 5])\nfig.tight_layout()\nplt.show()'
by_id['ch13-two-arrays']['code']='import matplotlib.pyplot as plt\n\na = [15, 25, 35, 45, 55]\nb = [5, 10, 15, 20, 25]\nfig, ax = plt.subplots(figsize=(8, 5))\nax.plot(a, b)\nfig.tight_layout()\nplt.show()'
by_id['ch13-range']['code']='import matplotlib.pyplot as plt\n\na = [1, 2, 3, 4, 5]\nb = [5, 10, 15, 20, 25]\nfig, ax = plt.subplots(figsize=(8, 5))\nax.plot(a, b, "b-+", clip_on=False)\nax.axis([0, 10, 0, 25])\nfig.tight_layout()\nplt.show()'
by_id['ch13-bars']['code']='import matplotlib.pyplot as plt\n\na = [1, 2, 4, 8, 16, 32, 64, 128]\nfig, ax = plt.subplots(figsize=(8, 5))\nax.bar(range(len(a)), a)\nfig.tight_layout()\nplt.show()'
by_id['ch13-grouped']['code']='''import matplotlib.pyplot as plt

topics = ["one", "two", "three", "four", "five"]
value_a = [35, 80, 84, 83, 50]
value_b = [73, 80, 77, 40, 86]

def create_x(t, w, n, d):
    return [t * x + w * n for x in range(d)]

value_a_x = create_x(2, 0.8, 1, 5)
value_b_x = create_x(2, 0.8, 2, 5)
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(value_a_x, value_a)
ax.bar(value_b_x, value_b)
middle_x = [(a + b) / 2
            for a, b in zip(value_a_x, value_b_x)]
ax.set_xticks(middle_x)
ax.set_xticklabels(topics)
fig.tight_layout()
plt.show()'''
by_id['ch13-scatter']['code']=by_id['ch13-scatter']['code'].replace('len(x)', '20').replace('set_xlabel("X")','set_xlabel("X축 제목")').replace('set_ylabel("Y")','set_ylabel("Y축 제목")')
by_id['ch14-series']['code']='import pandas as pd\n\ndict_data = {"one": 1, "two": 2, "three": 3}\nser = pd.Series(dict_data)\nprint(ser)'
by_id['ch14-mixed']['code']='import pandas as pd\n\nlist_data = ["2022-01-01", 2.14, "song", 1000, True]\nsr = pd.Series(list_data)\nprint(sr)\nprint(sr.index)\nprint(sr.values)'
dataframe='''import pandas as pd

df = pd.DataFrame(
    [[15, "여", "중2"], [17, "남", "고1"]],
    index=["현아", "태민"],
    columns=["나이", "성별", "학년"],
)'''
by_id['ch14-dataframe']['code']=dataframe+'\nprint(df)\nprint(df.index)\nprint(df.columns)'
by_id['ch14-rename-code']['code']=dataframe+'\ndf.index = ["학생1", "학생2"]\ndf.columns = ["연령", "남녀", "학년"]\nprint(df)\nprint(df.index)\nprint(df.columns)'
kept.append({'chapter':14,'page_id':'ch14-dict-frame-code','code':'''import pandas as pd

dict_data = {
    "mon": [1, 8, 15, 22],
    "tue": [2, 9, 6, 23],
    "wed": [3, 10, 17, 24],
    "thu": [4, 11, 18, 25],
    "fri": [5, 12, 19, 26],
    "sat": [6, 13, 20, 27],
    "sun": [7, 14, 21, 28],
}
df = pd.DataFrame(dict_data)
print(type(df))
print(df)''','output':None,'result':None})

source_codes={'ch13-one-array':'131-132','ch13-two-arrays':'133','ch13-range':'134',
 'ch13-markers':'136-138','ch13-bars':'140','ch13-grouped':'141-142','ch13-scatter':'145',
 'ch14-series':'148','ch14-mixed':'149','ch14-dataframe':'151','ch14-rename-code':'151','ch14-dict-frame-code':'150'}
concept('ch04-variables','변수 이름과 값 맞추기',[
    ('원본 PDF 21쪽','책의 변수 예시는 name에 민수, score에 80을 저장합니다. 원본의 scores·score 혼용과 스마트 따옴표를 바로잡았습니다.'),
    ('두 변수의 역할','- name은 학생 이름을 보관합니다.\n- score는 점수를 보관합니다.\n- 변수 이름과 저장한 값을 연결하여 읽어봅시다.')])

# Write a staging recipe, then the execution script replaces source code pages
# with real stdout / generated plots before writing the full manuscript.
recipe={'frontmatter':original.split(':::page',1)[0].replace('원본 교재 기반 16차시 · 수정 원고','원본 실습 중심 16차시 · 대조 수정판'),
        'order':order,'pages':pages,'code_specs':kept,'source_codes':source_codes,
        'catalog':sorted(catalog,key=lambda x:order.index(x['page_id'])),
        'removed_pages':removed,'rewritten_pages':changes}
(ROOT/'tmp/pdfs/source-practice-audit/revision-recipe.json').write_text(json.dumps(recipe,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'practices':len(catalog),'removed_pages':len(removed),'rewritten_pages':len(changes),'code_blocks':len(kept)},ensure_ascii=False))
