---
schema_version: 1
title: AI와 함께하는 바이브 코딩
subtitle: 16차시 · 개념과 실습
learner_level: 코딩 입문자
language: ko
canvas: coala-portrait
numbering: auto
toc: none
assets_dir: ./assets
---

:::page{type="concept" id="book-guide" layout="basic"}
# 이 교재를 사용하는 방법

## 개념을 익히고 실습하기

16차시에 걸쳐 AI 활용, 앱 설계, 프로그래밍, 데이터 시각화를 배웁니다. 각 차시의 학습 목표를 읽고 실습을 진행합니다.

## 입력·동작·결과 확인

실습의 조건과 위젯 이름을 먼저 읽습니다. 예시 값을 입력하고 실행 결과가 예상한 동작과 일치하는지 확인합니다. 입력값이 정해져 있지 않은 과제에서는 직접 값을 정합니다.

## 코드와 실행 화면

코드를 실행하면서 데이터와 처리 순서를 살펴봅니다. 예시 화면의 입력값과 결과를 읽고, 자신의 실행 화면과 확인한 내용을 기록합니다.

## 실습 준비와 Python 예제

알고플로 실습은 교사가 안내한 접속 주소와 계정으로 진행합니다. 위젯을 배치하고 버튼의 역할을 작성한 뒤 앱 화면에서 실행합니다.

12·13차시 예제를 PC에서 실행하려면 Python 3.10 이상을 준비하고, 함께 제공된 examples/source-based 폴더에서 터미널을 엽니다. python -m pip install -r requirements.txt로 필요한 패키지를 설치합니다. python ch12-one-array.py로 예제를 실행하고, 그래프 창을 닫은 뒤 다음 파일을 실행합니다.
:::

:::page{type="chapter-opening" id="ch01-opening" chapter="1"}
# AI와 함께하는 디지털 시대

## 1차시 · 개념과 실습

### 학습 목표

- 생성형 AI의 역할과 한계를 설명할 수 있다.
- 사실 확인이 필요한 답변을 구분할 수 있다.
- AI에게 맡길 일과 내가 검증할 일을 정할 수 있다.

### 오늘의 시작

AI가 잘하는 일과 어려워하는 일을 비교해봅시다. 바이브 코딩에서도 AI가 코드를 만들고, 사람은 목적과 동작을 확인합니다.

::image{src="assets/ch01/ai-human-summary.png" alt="AI는 아이디어와 코드 초안을 제안하고, 사람은 목적·근거·실행 결과를 확인하여 오류를 고칩니다." ratio="2197:792" width="text" caption="AI의 제안과 사람의 검증으로 함께 만드는 앱"}
:::

:::page{type="concept" id="ch01-ai" layout="basic"}
# 생성형 AI와 바이브 코딩

## 생성형 AI란?

생성형 AI는 요청에 따라 글, 이미지, 코드 같은 결과물을 만듭니다. 추천 영상이나 번역 등 일상 속 AI와 연결해 생각해봅시다.

## 코드를 만드는 과정

바이브 코딩은 원하는 앱을 말로 설명하고 AI가 만든 프로그램을 실행하며 고쳐 가는 방식입니다. 사람은 원하는 기능과 입력·처리·출력을 정하고 결과를 확인합니다. AI는 코드를 작성하고 요청에 따라 수정합니다.
:::

:::page{type="comparison" id="ch01-limits"}
# AI가 잘하는 일과 확인할 일

AI 활용 예시와 사람이 확인할 내용을 비교해봅시다.

| 활용할 일 | 사람이 확인할 일 |
|---|---|
| 긴 정보 요약 | 빠진 내용과 왜곡 여부 |
| 아이디어 제안 | 목적에 맞는지 여부 |
| 반복 작업용 코드 작성 | 입력과 실제 실행 결과 |
| 새로운 정보 설명 | 날짜와 공식 근거 |
:::

:::page{type="concept" id="ch01-ethics" layout="basic"}
# AI의 답을 검토하는 태도

## 환각

AI가 사실과 다른 내용을 자신 있게 말하는 현상을 환각이라고 합니다. 자신 있는 말투는 정확성의 증거가 아닙니다.

다음 답변은 환각을 살펴보기 위해 만든 학습용 가상 오답입니다.

## 예시 1 · 십자군의 연도

- 질문: “제1차 십자군은 1492년에 시작했나요?”
- 가상 오답: “네, 1492년에 시작했습니다.”
- 사실 확인: 제1차 십자군은 1096~1099년에 진행되었습니다.

## 예시 2 · 소설 『연금술사』의 작가

- 질문: “산티아고가 나오는 소설 『연금술사』는 셰익스피어의 작품인가요?”
- 가상 오답: “네, 셰익스피어가 쓴 작품입니다.”
- 사실 확인: 파울로 코엘료의 소설로, 1988년에 처음 출간되었습니다.

## 직접 확인하기

질문의 전제부터 살펴보고, 연도와 작가를 역사 자료·작가 소개와 비교합니다. 답변을 맞음·틀림·확인하지 못함으로 나누어 기록합니다.

## 책임 있는 사용

실제 개인정보 대신 가상 데이터를 사용합니다. 다른 사람의 자료를 사용할 때 출처와 이용 조건을 확인합니다. 생성 결과의 오류와 편향을 검토하고, 제출물에서 AI 도움을 받은 부분을 밝힙니다.
:::

:::page{type="practice-opening" id="ch01-practice-1" practice="001-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# AI는 어떤 질문을 잘하고, 어려워할까?

일반 지식, 실시간 정보 등 질문 유형에 따라 AI의 답변을 비교해봅시다. 답변을 잘한 질문과 확인이 필요한 질문을 구분합니다. 개인 정보는 실제 개인정보를 입력하지 않고 질문 유형으로만 살펴봅니다.

> [!TIP]
> 질문 유형에 따른 답변의 차이를 살펴봅니다.

- [ ] 서로 다른 질문 유형을 비교했다.
- [ ] 잘 답한 부분과 확인할 부분을 구분했다.
- [ ] AI 답변의 근거를 확인했다.
:::

:::page{type="step-process" id="ch01-procedure"}
# 답변의 근거 찾아보기

## 질문 두 개 정하기

정의나 요약을 묻는 질문과 날짜에 따라 바뀌는 정보를 묻는 질문을 구분합니다.

## 확인할 문장 고르기

답변에서 사실로 제시된 문장 하나를 골라 원문, 공식 안내 또는 교사가 제시한 자료와 비교합니다.

## 활용 여부 결정하기

맞는 내용, 틀린 내용, 확인하지 못한 내용을 나누어 기록합니다.
:::

:::page{type="practice-checklist" id="ch01-check"}
# 실습 완료 확인

- [ ] 질문 유형에 따른 답변을 비교했다.
- [ ] 잘 답한 질문과 확인할 질문을 구분했다.

> [!KEY_POINT]
> 질문과 답변을 바탕으로 직접 확인한 내용을 기록합니다.
:::

:::page{type="chapter-opening" id="ch02-opening" chapter="2"}
# 좋은 질문이 좋은 답을 만든다

## 2차시 · 개념과 실습

### 학습 목표

- 프롬프트의 의미를 설명할 수 있다.
- 목적, 대상, 상황, 조건을 담아 요청할 수 있다.
- 앱의 목적에 맞는 입력 데이터를 정할 수 있다.

### 오늘의 시작

같은 AI라도 요청에 담긴 조건에 따라 결과가 달라집니다. 공부 계획과 여행 질문에 조건을 더하는 방법을 익히고, 앱 제작 요청에도 적용합니다.
:::

:::page{type="concept" id="ch02-prompt" layout="basic"}
# 프롬프트의 구성

## 프롬프트란?

프롬프트는 AI에게 전달하는 질문, 요청, 지시문입니다. 무엇을 만들지, 누구를 위한 것인지, 어떤 조건을 지켜야 하는지 적습니다.

## 공부 계획 예시

공부 계획 알려줘보다 시험이 2주 남았고 하루 2시간 공부할 수 있다는 상황을 함께 알려주면 요청의 범위가 분명해집니다.
:::

:::page{type="comparison" id="ch02-compare"}
# 모호한 요청을 구체적으로 바꾸기

모호한 요청과 구체적인 요청을 비교해봅시다.

| 모호한 요청 | 구체적인 요청 |
|---|---|
| 추천해줘 | 시험까지 2주, 하루 2시간의 공부 계획을 추천해줘. |
| 여행 추천해줘 | 2박 3일 부산 여행을 실내 활동 위주로 정리해줘. |
| 건강 관리 알려줘 | 대학생이 실천할 수 있는 생활 습관을 알려줘. |
:::

:::page{type="concept" id="ch02-inputs" layout="basic"}
# 앱에 필요한 입력 데이터

## BMI 계산 앱

BMI 계산에는 키와 몸무게를 입력합니다. 결과에 필요한 정보만 받습니다. BMI 계산은 데이터 처리 연습이며 개인의 건강을 진단하는 기능으로 취급하지 않습니다.

## 병원 접수 앱

이름, 증상, 체온을 입력 항목으로 설계합니다. 수업에서는 가상 이름과 예시 값을 사용하고, 실제 접수나 응급 판단 기능으로 사용하지 않습니다.
:::

:::page{type="practice-opening" id="ch02-practice-1" practice="002-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# 어떤 질문이 더 좋은 답을 만들까?

“공부 계획 알려줘”와 “시험이 2주 남았는데 하루 2시간씩 공부할 수 있어. 효율적인 공부 계획을 짜줘.”를 비교해봅시다. 답변에 상황과 조건이 반영되는지 확인합니다.

> [!TIP]
> 답변의 길이보다 요청한 조건의 반영 여부를 봅니다.

- [ ] 같은 주제의 짧은 질문과 구체적인 질문을 비교했다.
- [ ] 2주와 하루 2시간이라는 조건을 확인했다.
- [ ] 아쉬운 답변은 질문을 다듬어 다시 확인했다.
:::

:::page{type="practice-opening" id="ch02-practice-2" practice="002-2" practice-kind="실습" platform="알고플로에서 실습하기"}
# 앱에 필요한 입력 데이터 설계하기

BMI 계산 앱의 목적과 입력 데이터를 정해봅시다. 결과를 계산하려면 키와 몸무게가 필요함을 확인하고 입력과 처리의 관계를 정리합니다.

> [!TIP]
> BMI 계산에 필요한 입력 데이터를 설계하는 활동입니다.

- [ ] 앱의 목적을 BMI 계산으로 정했다.
- [ ] 필요한 입력을 키와 몸무게로 구분했다.
- [ ] 입력 데이터와 처리 결과의 관계를 설명했다.
:::

:::page{type="concept" id="ch02-request" layout="basic"}
# 질문을 구체적으로 다듬기

## 요청에 조건 더하기

- 짧은 요청: 공부 계획 알려줘.
- 구체적인 요청: 시험까지 2주, 하루 2시간 공부 조건을 포함합니다.
- 여행 질문: 2박 3일 부산 여행, 실내 활동 위주라는 조건을 포함합니다.

## 답변 확인하기

같은 주제로 질문을 다듬고 결과를 비교합니다. 앱을 요청할 때도 입력할 값, 버튼의 동작, 화면에 보여 줄 결과를 구체적으로 적습니다.

## 실행 후 수정 요청하기

앱 화면에서 예시 값을 입력하고 버튼을 누른 결과를 확인합니다. 원하는 동작과 다르면 위젯 이름과 바꿀 동작을 적어 수정을 요청한 뒤 다시 실행합니다.
:::

:::page{type="practice-checklist" id="ch02-check"}
# 실습 완료 확인

- [ ] 공부 계획의 2주·하루 2시간 조건을 확인했다.
- [ ] BMI 계산에 필요한 키·몸무게 입력을 설계했다.

> [!KEY_POINT]
> 요청한 조건과 답변, 설계한 입력 항목을 직접 확인하고 기록합니다.
:::

:::page{type="chapter-opening" id="ch03-opening" chapter="3"}
# 문제를 단계별로 나누기

## 3차시 · 개념과 실습

### 학습 목표

- 알고리즘의 의미를 설명할 수 있다.
- 입력, 처리, 출력을 구분할 수 있다.
- 아이디어를 작은 실행 단계로 나눌 수 있다.

### 오늘의 시작

AI의 아이디어를 실제 앱으로 만들려면 사람이 동작 구조를 정해야 합니다. 라면 끓이기와 감정 기록을 입력·처리·출력으로 나누어봅시다.
:::

:::page{type="comparison" id="ch03-ramen"}
# 라면 끓이기로 보는 입력·처리·출력

라면 끓이기를 입력·처리·출력의 세 단계로 나누어봅시다.

| 단계 | 라면 끓이기 |
|---|---|
| 입력 | 물, 면, 스프, 냄비 준비 |
| 처리 | 물을 끓이고 재료를 넣어 조리 |
| 출력 | 완성된 라면 |
:::

:::page{type="concept" id="ch03-algorithm" layout="basic"}
# 알고리즘은 해결 절차

## 순서가 필요한 이유

알고리즘은 문제를 해결하기 위한 절차입니다. 필요한 값을 준비하고, 정해 둔 순서로 처리하여 결과를 만듭니다.

## 처리와 출력 구분하기

계산하거나 분류하는 일은 처리입니다. 계산 결과를 화면에 보이게 하는 일은 출력입니다. 같은 문구를 두 단계에 반복해 적지 않습니다.
:::

:::page{type="practice-opening" id="ch03-practice-1" practice="003-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# 내 아이디어를 단계별로 나눠보기

감정 기록 앱을 입력·처리·출력으로 나누어봅시다. 오늘의 기분을 입력하고 감정 상태를 분류한 뒤 결과를 보여주는 순서로 정리합니다.

> [!TIP]
> 감정 분류는 프로그램 구조를 배우기 위한 예시입니다.

- [ ] 입력할 내용을 정리했다.
- [ ] 입력 뒤 처리할 작업을 정리했다.
- [ ] 마지막에 보여줄 결과를 정리했다.
:::

:::page{type="step-process" id="ch03-design"}
# 아이디어를 실행 순서로 만들기

## 입력 정하기

오늘의 기분을 어떤 선택 항목으로 받을지 정합니다.

## 처리 정하기

선택한 항목을 기록하고, 항목에 대응하는 안내를 준비합니다.

## 출력 정하기

선택한 기분과 기록 완료 안내를 보여줍니다.
:::

:::page{type="practice-checklist" id="ch03-check"}
# 실습 완료 확인

- [ ] 감정 기록 앱의 입력·처리·출력을 구분했다.
- [ ] 각 작업의 순서를 정리했다.

> [!KEY_POINT]
> 정리한 입력·처리·출력과 실행 순서를 확인하고 기록합니다.
:::

:::page{type="chapter-opening" id="ch04-opening" chapter="4"}
# 순서도와 데이터 이해

## 4차시 · 개념과 실습

### 학습 목표

- 선언, 입력, 처리, 출력의 역할을 구분할 수 있다.
- 문자열과 숫자를 구분할 수 있다.
- 가족 나이 합과 학생 총점을 구하는 흐름을 설명할 수 있다.

### 오늘의 시작

가족 나이 43, 45, 15를 더해봅시다. 선언·입력·처리·출력의 순서로 정리합니다.
:::

:::page{type="concept" id="ch04-roles" layout="basic"}
# 순서도에서 데이터가 이동하는 과정

## 선언과 변수

변수는 값을 저장하고 다시 사용할 때 붙이는 이름입니다. 이름이나 점수처럼 서로 다른 값을 목적에 맞는 변수로 보관합니다.

## 입력·처리·출력

입력에서는 값을 받습니다. 처리에서는 받은 값을 더하거나 비교합니다. 출력에서는 계산 결과나 안내를 보여줍니다. 순서도에서는 역할에 맞는 도형과 연결선을 사용합니다.
:::

:::page{type="comparison" id="ch04-types"}
# 문자열과 숫자 구분하기

문자열·정수·실수의 예시와 사용 방법을 비교해봅시다.

| 종류 | 예시 | 사용 방법 |
|---|---|---|
| 문자열 | 이름, 학과, 증상 설명 | 글자로 보관하거나 표시 |
| 정수 | 나이, 점수 | 변환 후 덧셈·비교 |
| 실수 | 키, 체온 | 소수 값을 변환해 계산 |
:::

:::page{type="concept" id="ch04-variables" layout="basic"}
# 변수 이름과 값 맞추기

## 이름과 점수 저장하기

name에 민수, score에 80을 저장합니다. 변수 이름을 읽고 어떤 값이 들어 있는지 확인해봅시다.

## 두 변수의 역할

- name은 학생 이름을 보관합니다.
- score는 점수를 보관합니다.
- 변수 이름과 저장한 값을 연결하여 읽어봅시다.
:::

:::page{type="practice-opening" id="ch04-practice-1" practice="004-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# 우리 가족 나이 합 구하기

엄마 43살, 아빠 45살, 나 15살의 나이를 더하는 순서도를 만들어봅시다. momage, dadage, myage, total을 사용하고 합계 103을 확인합니다.

- [ ] 세 나이 43·45·15를 사용했다.
- [ ] 세 나이를 더하는 처리를 연결했다.
- [ ] 총합 103을 확인했다.
:::

:::page{type="step-process" id="ch04-family-code"}
# 가족 나이 합 구하기

## 변수 준비

momage, dadage, myage, total을 준비합니다.

## 나이 입력

각 변수에 43, 45, 15를 넣습니다.

## 합계 처리

total = momage + dadage + myage로 계산합니다.

## 결과 출력

가족 나이의 총합 103을 보여줍니다.
:::

:::page{type="flowchart" id="ch04-family-flow" height="1050"}
# 가족 나이 합의 순서도

변수 준비, 나이값 저장, 합계 계산, 결과 출력의 순서를 확인합니다.

```flowchart
control_structure: linear
nodes:
  - id: declare
    role: declaration
    text: momage = 0, dadage = 0, myage = 0, total = 0
  - id: input
    role: process
    text: momage = 43, dadage = 45, myage = 15
  - id: sum
    role: process
    text: total = momage + dadage + myage
  - id: out
    role: output
    text: 나이 총합 103 출력
connections:
  - from: declare
    to: input
  - from: input
    to: sum
  - from: sum
    to: out
```

저장하는 나이가 달라지면 계산식은 유지되고 총합이 달라집니다.
:::

:::page{type="step-process" id="ch04-scores-code"}
# 학생 세 명의 총점 구하기

## 변수 준비

s1, s2, s3, total을 준비합니다.

## 점수 입력

세 학생의 점수를 하나씩 입력하고 정수로 변환합니다.

## 총점 계산

total = s1 + s2 + s3으로 더합니다.

## 총점 출력

학생 세 명의 총점수를 출력합니다. 평균 계산 과제와 구분합니다.
:::

:::page{type="practice-checklist" id="ch04-check"}
# 실습 완료 확인

- [ ] 43·45·15의 가족 나이 합 103을 확인했다.
- [ ] 학생 세 명의 점수를 더하는 흐름을 설명했다.

> [!KEY_POINT]
> 입력한 나이와 점수, 계산한 합계를 확인하고 기록합니다.
:::

:::page{type="chapter-opening" id="ch05-opening" chapter="5"}
# 반복과 누적 이해

## 5차시 · 개념과 실습

### 학습 목표

- 횟수 반복과 조건 반복을 구분할 수 있다.
- 반복마다 합계를 갱신할 수 있다.
- 10일 운동 시간의 합을 검증할 수 있다.

### 오늘의 시작

1일차에 1분, 2일차에 2분, 10일차에 10분 운동합니다. 반복으로 총 운동 시간을 계산해봅시다.
:::

:::page{type="concept" id="ch05-loops" layout="basic"}
# 같은 처리 여러 번 하기

## 횟수와 조건

횟수가 정해져 있으면 그 횟수만큼 반복합니다. while은 조건이 참인 동안 반복하고 거짓이면 멈춥니다. 조건이 참이 될 때까지 반복한다는 설명과 구분합니다.

## 누적하기

누적은 이전 합계에 새 값을 더해 다시 저장하는 처리입니다. 합계를 0으로 준비하는 일은 반복 시작 전에 한 번만 합니다.
:::

:::page{type="comparison" id="ch05-trace"}
# 운동 시간 누적 따라가기

날짜별 운동 시간과 누적 합계의 변화를 확인해봅시다.

| 날짜 | 더할 시간 | 그날까지 합계 |
|---|---|---|
| 1일차 | 1분 | 1분 |
| 2일차 | 2분 | 3분 |
| 3일차 | 3분 | 6분 |
| 9일차 | 9분 | 45분 |
| 10일차 | 10분 | 55분 |
:::

:::page{type="practice-opening" id="ch05-practice-1" practice="005-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# 10일 동안의 운동 시간 누적하기

1일차에 1분, 2일차에 2분씩 운동 시간을 늘려 10일차에 10분 운동합니다. 반복 순서도로 1부터 10까지 더하고 총 55분을 확인해봅시다.

> [!TIP]
> 마지막 10일차를 포함합니다.

- [ ] 처음 합계를 0분으로 정했다.
- [ ] 1일차부터 10일차까지 반복했다.
- [ ] 총 운동 시간 55분을 확인했다.
:::

:::page{type="step-process" id="ch05-exercise-code"}
# 운동 시간 누적 순서

## 처음 값 설정

time1은 1, total은 0에서 시작합니다.

## 조건 확인

time1 <= 10인 동안 반복합니다.

## 시간 누적

total에 time1을 더하고 time1을 1 증가시킵니다.

## 결과 출력

반복이 끝나면 총 운동 시간 55분을 출력합니다.
:::

:::page{type="flowchart" id="ch05-exercise-flow" height="1050"}
# 운동 시간 누적 순서도

운동 시간을 누적하는 흐름을 마지막 날짜까지 따라가봅시다.

```flowchart
control_structure: loop
nodes:
  - id: start
    role: declaration
    text: time1 = 1, total = 0
  - id: cond
    role: decision
    text: time1 <= 10인가?
  - id: sum
    role: process
    text: total = total + time1
  - id: next
    role: process
    text: time1 = time1 + 1
  - id: out
    role: output
    text: 총 운동 시간 출력
connections:
  - from: start
    to: cond
  - from: cond
    to: sum
    label: YES
  - from: sum
    to: next
  - from: next
    to: cond
  - from: cond
    to: out
    label: NO
```

조건이 거짓이 되면 반복 밖에서 총합을 출력합니다.
:::

:::page{type="practice-opening" id="ch05-practice-2" practice="005-2" practice-kind="실습" platform="알고플로에서 실습하기"}
# 하루 카페인 섭취량 누적하기

하루 동안 마신 음료의 카페인 양을 더해봅시다. 처음 총량을 0mg으로 정합니다. 음료의 카페인 양을 입력할 때마다 더하고, 입력이 끝나면 총량을 출력합니다.

- [ ] 처음 총 카페인 양을 0mg으로 정했다.
- [ ] 음료 입력을 반복해 총량에 더했다.
- [ ] 입력이 끝났을 때 총량을 출력했다.
:::

:::page{type="step-process" id="ch05-caffeine-code"}
# 카페인 섭취량 누적 순서

## 총량 준비

총 카페인 양을 0mg으로 시작합니다.

## 음료 값 더하기

음료의 카페인 양을 입력하고 현재 총량에 더합니다.

## 입력 반복

더 입력할 내용이 있으면 같은 작업을 반복합니다.

## 최종 총량 출력

입력이 끝나면 누적한 총량을 출력합니다.
:::

:::page{type="practice-checklist" id="ch05-check"}
# 실습 완료 확인

- [ ] 1일차부터 10일차까지 총 55분을 확인했다.
- [ ] 카페인 입력을 반복하고 총량을 출력했다.

> [!KEY_POINT]
> 반복한 횟수와 누적한 총량을 확인하고 기록합니다.
:::

:::page{type="chapter-opening" id="ch06-opening" chapter="6"}
# 조건에 따라 결과 나누기

## 6차시 · 개념과 실습

### 학습 목표

- if, elif, else의 역할을 설명할 수 있다.
- 조건을 검사하는 순서를 정할 수 있다.
- 경계값을 넣어 결과를 확인할 수 있다.

### 오늘의 시작

비 오는 날 우산 예시와 수면 시간 분류로 조건문을 이해합니다. 수면 문구는 분류 규칙을 연습하는 예시이며 건강 판정은 아닙니다.
:::

:::page{type="concept" id="ch06-conditions" layout="basic"}
# 조건문 읽는 방법

## if와 else

if는 조건이 참일 때 실행할 내용을 정합니다. else는 앞의 조건에 해당하지 않을 때 실행할 내용을 정합니다.

## elif와 순서

elif는 앞 조건이 거짓일 때 다음 조건을 검사합니다. 한 번 참인 분기를 선택하면 이어지는 elif와 else는 실행하지 않습니다.
:::

:::page{type="comparison" id="ch06-sleep-rules"}
# 수면 시간 분류 규칙

수면 시간에 따라 세 가지 안내 문구를 출력하는 분기 규칙을 연습합니다. 조건문 학습을 위한 규칙으로, 실제 건강 기준으로 일반화하지 않습니다.

| 수면 시간 | 학습용 출력 |
|---|---|
| 8시간 이상 | 충분한 수면입니다 |
| 5시간 이상, 8시간 미만 | 적정 수면입니다 |
| 5시간 미만 | 수면 부족입니다 |
:::

:::page{type="practice-opening" id="ch06-practice-1" practice="006-1" practice-kind="예제 실습" platform="알고플로에서 실습하기"}
# 수면 시간에 따른 안내 만들기

수면 시간을 분류하는 순서도를 만들어봅시다. 8시간 이상인지 먼저 판단하고, 아니면 5시간 이상인지 판단하여 세 안내 문구 중 하나를 출력합니다.

> [!TIP]
> 두 조건을 차례로 검사하고 해당하는 문구 하나를 출력합니다.

- [ ] 8시간 이상 조건을 먼저 확인했다.
- [ ] 그렇지 않을 때 5시간 이상 조건을 확인했다.
- [ ] 충분한 수면·적정 수면·수면 부족의 세 출력을 구분했다.
:::

:::page{type="step-process" id="ch06-sleep-code"}
# 수면 시간에 따른 조건 처리

## 입력받기

수면 시간을 입력받습니다.

## 첫 조건 판단

8시간 이상이면 “충분한 수면입니다”를 출력합니다.

## 다음 조건 판단

8시간 미만일 때 5시간 이상이면 “적정 수면입니다”를 출력합니다.

## 나머지 경우

5시간 미만이면 “수면 부족입니다”를 출력합니다.
:::

:::page{type="flowchart" id="ch06-sleep-flow" height="1050"}
# 수면 시간 조건 순서도

두 조건을 검사하는 순서와 YES, NO 연결을 구분합니다.

```flowchart
control_structure: if-else-if
nodes:
  - id: input
    role: input
    text: 수면 시간 입력
  - id: eight
    role: decision
    text: 8시간 이상인가?
  - id: five
    role: decision
    text: 5시간 이상인가?
  - id: enough
    role: output
    text: 충분한 수면입니다
  - id: normal
    role: output
    text: 적정 수면입니다
  - id: low
    role: output
    text: 수면 부족입니다
connections:
  - from: input
    to: eight
  - from: eight
    to: enough
    label: YES
  - from: eight
    to: five
    label: NO
  - from: five
    to: normal
    label: YES
  - from: five
    to: low
    label: NO
```

잘못된 입력을 검사하는 단계는 이 분류 앞에서 따로 설계합니다.
:::

:::page{type="concept" id="ch06-fix" layout="basic"}
# 조건 검사 순서 읽기

## 큰 기준부터 확인하기

8시간 이상인 값은 5시간 이상에도 해당합니다. 8시간 조건부터 확인하고, 해당하지 않을 때 다음 조건으로 이동합니다.

## 연결 확인

첫 조건의 NO가 두 번째 조건으로 이어지는지 확인합니다. 각 YES와 마지막 NO는 해당 안내 문구로 연결합니다.
:::

:::page{type="practice-checklist" id="ch06-check"}
# 실습 완료 확인

- [ ] 8시간 조건과 5시간 조건의 순서를 확인했다.
- [ ] 세 출력 문구를 올바르게 연결했다.

> [!KEY_POINT]
> 입력한 수면 시간과 선택된 안내 문구를 확인하고 기록합니다.
:::

:::page{type="chapter-opening" id="ch07-opening" chapter="7"}
# 반복과 조건 함께 사용하기

## 7차시 · 개념과 실습

### 학습 목표

- 반복할 작업과 판단할 조건을 분리할 수 있다.
- 학생 수만큼 결과를 출력할 수 있다.
- 합격 기준과 관람 기준을 구분할 수 있다.

### 오늘의 시작

학생 수만큼 반복하며 점수·나이 조건을 판단하고 결과를 출력합니다.
:::

:::page{type="comparison" id="ch07-roles"}
# 반복과 조건의 서로 다른 역할

| 구조 | 점수 확인 예시 |
|---|---|
| 반복 | 학생 점수를 한 명씩 확인 |
| 조건 | 기준 점수 이상인지 확인 |
| 출력 | 그 학생의 결과를 표시 |
:::

:::page{type="practice-opening" id="ch07-practice-1" practice="007-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# 입력받은 학생 수만큼 점수 통과 여부 확인

학생 수 N을 정하고 각 학생의 점수를 입력받아봅시다. 80점 이상이면 PASS, 80점 미만이면 FAIL을 출력합니다. 입력받은 N명 모두에게 결과를 출력합니다.

- [ ] 입력받은 학생 수 N만큼 처리했다.
- [ ] 80점 이상과 미만을 구분했다.
- [ ] 학생마다 PASS 또는 FAIL을 출력했다.
:::

:::page{type="step-process" id="ch07-pass-code"}
# 학생 수 N에 따라 점수 확인하기

## 학생 수 정하기

처리할 학생 수 N을 입력받고 반복 변수를 0에서 시작합니다.

## 점수 입력

학생 한 명의 점수를 입력받습니다.

## 통과 여부 출력

80점 이상이면 PASS, 80점 미만이면 FAIL을 출력합니다.

## 다음 학생 처리

반복 변수를 1 증가시키고 N명 처리가 끝날 때까지 반복합니다.
:::

:::page{type="step-process" id="ch07-movie-code"}
# 영화 관람 가능 여부 확인하기

## 네 학생의 나이 입력

학생 네 명의 나이를 하나씩 입력받습니다.

## 관람 조건 판단

15세 이상 조건을 확인합니다.

## 결과 출력

각 학생에 대해 관람가능 또는 관람불가를 출력합니다.

## 네 번 반복

네 학생 모두에게 결과가 출력되었는지 확인합니다.
:::

:::page{type="flowchart" id="ch07-movie-flow" height="1050"}
# 영화 관람의 반복과 분기

학생 네 명의 나이를 입력받고 관람 조건을 판단하는 흐름입니다.

```flowchart
control_structure: loop
nodes:
  - id: start
    role: declaration
    text: i = 0, age = 0
  - id: loop
    role: decision
    text: i < 4인가?
  - id: input
    role: input
    text: 학생 나이 입력
  - id: condition
    role: decision
    text: age < 15인가?
  - id: yes
    role: output
    text: 관람불가 출력
  - id: no
    role: output
    text: 관람가능 출력
  - id: next
    role: process
    text: i = i + 1
connections:
  - from: start
    to: loop
  - from: loop
    to: input
    label: YES
  - from: input
    to: condition
  - from: condition
    to: yes
    label: YES
  - from: condition
    to: no
    label: NO
  - from: yes
    to: next
  - from: no
    to: next
  - from: next
    to: loop
```

반복 상자 안에서 나이 입력·판단·결과 출력을 네 번 수행합니다. age < 15가 참이면 관람불가, 거짓이면 관람가능입니다.
:::

:::page{type="practice-checklist" id="ch07-check"}
# 실습 완료 확인

- [ ] N명의 점수에 80점 PASS 기준을 적용했다.
- [ ] 네 학생 나이의 15세 관람 조건을 설명했다.

> [!KEY_POINT]
> 입력한 학생 수와 점수·나이, 출력된 결과를 확인하고 기록합니다.
:::

:::page{type="chapter-opening" id="ch08-opening" chapter="8"}
# Button·Field·Text로 첫 화면 만들기

## 8차시 · 개념과 실습

### 학습 목표

- GUI와 위젯의 의미를 설명할 수 있다.
- 버튼 이벤트와 입력값을 연결할 수 있다.
- 메시지 출력과 Field 추가·삭제를 확인할 수 있다.

### 오늘의 시작

바이브 프로젝트에서는 프로젝트 정보, 위젯 역할, 이벤트, 추가 설명을 작성한 뒤 코드를 생성합니다. 화면 구성과 버튼 동작을 따로 설계해봅시다.
:::

:::page{type="comparison" id="ch08-widgets"}
# 기본 위젯의 역할

GUI는 화면의 버튼·입력창 등을 통해 프로그램을 사용하는 방식입니다. 화면을 구성하는 각각의 요소를 위젯이라고 합니다.

| 위젯 | 역할 | 위젯 이름 |
|---|---|---|
| Button | 눌렀을 때 기능 실행 | btn1 |
| Field | 글자·숫자 입력 또는 결과 표시 | fld1, fld2 |
| Text | 설명과 결과 표시 | txt1 |
:::

:::page{type="step-process" id="ch08-designer"}
# 바이브 프로젝트 작성 순서

## 프로젝트 정보 정하기

예를 들어 프로젝트 이름은 ‘인사말 추가·삭제’, 설명은 ‘입력한 인사말을 아래에 표시하고 삭제하는 앱’으로 적습니다.

## 위젯 역할 정하기

Field 두 개와 Button 두 개를 만들고 위쪽 fld1, 가운데 btn1·btn2, 아래쪽 fld2로 배치합니다.

## 이벤트 정하기

btn1은 fld1의 내용을 fld2에 표시하고, btn2는 두 Field를 비우도록 적습니다.

## 생성 후 실행하기

앱 화면에서 ‘안녕’을 입력하고 추가 후 fld2의 글자, 삭제 후 두 Field가 비는지 확인합니다.
:::

:::page{type="concept" id="ch08-gui-example" layout="basic"}
# GUI 구성 예시 · 인사말 앱

## 입력·버튼·결과 배치

인사말 추가·삭제 앱은 입력창, 두 버튼, 결과창으로 구성합니다. 위쪽에서 입력하고, 가운데 버튼으로 동작을 실행한 뒤 아래쪽에서 결과를 확인합니다.

::image{src="assets/source-20261006/field-copy.png" alt="위쪽 fld1 입력창, 가운데 추가·삭제 버튼, 아래쪽 fld2 결과창으로 구성한 인사말 앱" ratio="497:406" width="half" caption="위 입력창 → 추가·삭제 버튼 → 아래 결과창"}

## 위젯 이름과 역할

- fld1: 인사말을 입력하는 Field
- btn1: fld1의 내용을 fld2에 표시하는 ‘추가’ 버튼
- btn2: 두 Field의 내용을 비우는 ‘삭제’ 버튼
- fld2: 추가한 인사말을 보여주는 Field
:::

:::page{type="practice-opening" id="ch08-practice-1" practice="008-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# 버튼 클릭하면 배경색과 글자색 바꾸기

Flet 디자이너에 btn1을 추가하고 클릭 이벤트를 작성해봅시다. 버튼을 누르면 배경색은 blue, 글자색은 white로 바뀌게 합니다.

> [!TIP]
> btn1.bgcolor와 btn1.color의 역할을 구분합니다.

- [ ] btn1을 화면에 추가했다.
- [ ] 클릭 이벤트에 blue와 white를 지정했다.
- [ ] 클릭 후 배경색과 글자색을 함께 확인했다.
:::

:::page{type="concept" id="ch08-button-before" layout="basic"}
# 버튼 클릭 전

## 예시 확인하기

화면의 버튼 상태를 확인해봅시다.

클릭 전에는 밝은 배경의 Button이 보입니다.

::image{src="assets/source-20261006/button-before.png" alt="클릭 전에는 밝은 배경의 Button이 보입니다." ratio="170:84" width="half" caption="클릭 전의 버튼"}
:::

:::page{type="concept" id="ch08-button-after" layout="basic"}
# 버튼 클릭 후

## 예시 확인하기

화면의 버튼 상태를 확인해봅시다.

클릭 후에는 같은 버튼의 배경이 파란색으로 바뀝니다.

::image{src="assets/source-20261006/button-after.png" alt="클릭 후에는 같은 버튼의 배경이 파란색으로 바뀝니다." ratio="183:82" width="half" caption="클릭 후 파란색으로 바뀐 버튼"}
:::

:::page{type="practice-opening" id="ch08-practice-message" practice="008-2" practice-kind="실습" platform="알고플로에서 실습하기"}
# 버튼 클릭하면 메시지 창 출력하기

Field에 “안녕하세요”를 입력하고 Button을 눌러 메시지 창에 입력값이 나타나도록 만들어봅시다. fld1과 btn1을 연결하고 입력한 인사말이 알림 창에 그대로 나타나는지 확인합니다.

> [!TIP]
> message는 수업 도구 전용 기능이며 독립 Python의 기본 함수가 아닙니다.

- [ ] fld1과 btn1을 화면에 추가했다.
- [ ] 버튼 이벤트가 fld1의 값을 읽는다.
- [ ] 메시지 창에 입력한 인사말이 나타난다.
:::

:::page{type="concept" id="ch08-message-screen" layout="basic"}
# 입력 화면과 메시지 창

## 입력 화면

fld1에 안녕하세요를 입력합니다.

::image{src="assets/source-20261010/message-dialog.png" alt="안녕하세요를 입력한 Field와 Button" ratio="462:274" width="half" caption="인사말을 입력한 화면"}

## 클릭 결과

버튼을 클릭하면 알림 창에서 같은 입력 내용을 확인합니다.

::image{src="assets/source-20261010/message-input.png" alt="안녕하세요가 표시된 알림 창" ratio="424:247" width="half" caption="입력한 인사말을 표시한 메시지 창"}
:::

:::page{type="practice-opening" id="ch08-practice-2" practice="008-3" practice-kind="실습" platform="알고플로에서 실습하기"}
# Field에 입력한 내용 버튼으로 출력하기

fld1에 “안녕”을 입력하고 추가 버튼을 눌러 fld2에 내용을 표시해봅시다. 삭제 버튼을 누르면 두 Field의 내용이 모두 지워지는지 확인합니다.

> [!TIP]
> fld2가 비어 있는 상태에서 추가 버튼을 한 번 누르고 표시된 내용을 확인합니다.

- [ ] fld1·fld2와 추가·삭제 버튼을 배치했다.
- [ ] 추가 후 fld2에 안녕이 보인다.
- [ ] 삭제 후 두 Field의 내용이 지워진다.
:::

:::page{type="step-process" id="ch08-request"}
# Field 실습 · 이벤트 설정

## UI 배치

위쪽에 fld1, 가운데에 btn1(추가)·btn2(삭제), 아래쪽에 fld2를 배치합니다. fld1은 입력, fld2는 입력 내용을 보여주는 결과창으로 정합니다.

## 추가 버튼

btn1을 클릭하면 fld1에 입력한 내용을 fld2에 표시하도록 역할과 이벤트를 적습니다.

## 삭제 버튼

btn2를 클릭하면 fld1과 fld2의 내용을 모두 지우도록 적습니다.

## 실행 확인

프로젝트를 생성한 뒤 앱 화면에서 안녕 입력·추가·삭제를 순서대로 확인합니다.

## 동작 수정 요청

삭제 뒤 fld2에 글자가 남는다면 “btn2를 누르면 fld1과 fld2의 내용을 모두 지워 줘.”라고 요청합니다. 다시 생성·실행하고 두 Field가 비는지 확인합니다.
:::

:::page{type="concept" id="ch08-field-copy" layout="basic"}
# 입력값을 복사한 화면

## 예시 확인하기

화면의 입력값과 버튼을 누른 결과를 함께 확인해봅시다.

위 입력창의 안녕이 추가 버튼을 누른 뒤 아래 입력창에도 표시됩니다.

::image{src="assets/source-20261006/field-copy.png" alt="위 입력창의 안녕이 추가 버튼을 누른 뒤 아래 입력창에도 표시됩니다." ratio="497:406" width="half" caption="추가 버튼으로 두 Field에 표시한 인사말"}
:::

:::page{type="concept" id="ch08-platform" layout="basic"}
# 디자이너 이름과 Python 클래스 구분하기

## 수업 도구의 이름

Field는 디자이너에서 쓰는 이름입니다. Flet Python 코드에서는 TextField와 연결됩니다. btn1, fld1, txt1은 수업 도구에서 지정한 위젯 변수 이름입니다.

## 화면 갱신

값을 바꾸는 코드와 화면에 변경을 반영하는 과정이 연결되어야 합니다. 생성된 코드를 수정할 때는 수업 도구의 실행 구조와 갱신 방식을 확인합니다.
:::

:::page{type="practice-checklist" id="ch08-check"}
# 실습 완료 확인

- [ ] 버튼의 blue·white 변경을 확인했다.
- [ ] 입력 인사말을 메시지 창에 표시했다.
- [ ] Field의 내용 추가·삭제를 확인했다.

> [!KEY_POINT]
> 입력한 값, 버튼 동작, 화면에 표시된 결과를 확인하고 기록합니다.
:::

:::page{type="chapter-opening" id="ch09-opening" chapter="9"}
# 계산·누적 출력 앱 만들기

## 9차시 · 개념과 실습

### 학습 목표

- 반복 알고리즘을 GUI 이벤트로 연결할 수 있다.
- 계산 입력을 숫자로 변환할 수 있다.
- 값 교체와 내용 누적을 구분할 수 있다.

### 오늘의 시작

누적곱, 두 수 계산기, Text 누적, 구구단 실습을 연결합니다. 계산은 입력한 숫자와 선택한 연산을 명확히 정해 처리합니다.
:::

:::page{type="practice-opening" id="ch09-practice-1" practice="009-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# Field에 입력한 두 수의 누적곱 출력

fld1에 1, fld2에 6을 넣고 누적 버튼을 눌러봅시다. 1부터 6까지의 곱 720이 fld3에 표시되는지 확인합니다. 다시 누르면 현재 입력으로 결과를 바꿉니다.

> [!TIP]
> 곱을 누적할 처음 값은 1입니다.

- [ ] fld1·fld2·fld3과 누적 버튼을 배치했다.
- [ ] 1과 6을 입력하여 결과 720을 확인했다.
- [ ] 다시 실행하면 현재 값으로 결과가 바뀐다.
:::

:::page{type="step-process" id="ch09-product-code"}
# 누적곱 프로그램의 동작

## 두 수 입력

위쪽 한 줄에 fld1, btn1(누적), fld2를 놓고 아래에 결과창 fld3을 둡니다. fld1에 시작 값 1, fld2에 끝 값 6을 입력합니다.

## 버튼 이벤트 설정

두 입력을 정수로 바꾸고 시작 값부터 끝 값까지 포함하여 곱합니다. 버튼을 누를 때마다 누적값을 1로 초기화합니다. 시작 값이 끝 값보다 크거나 입력이 정수가 아니면 안내를 표시합니다.

## 결과 표시

fld3에서 720을 확인합니다.

## 재실행

새 입력으로 다시 누르면 이전 결과를 현재 계산 결과로 바꿉니다.
:::

:::page{type="concept" id="ch09-product" layout="basic"}
# 누적곱 결과 화면

## 예시 확인하기

시작 1, 끝 6을 입력하고 누적 버튼을 누르면 결과창에 720이 보입니다.

::image{src="assets/source-20261006/product.png" alt="시작 1, 끝 6을 입력하고 누적 버튼을 누르면 결과창에 720이 보입니다." ratio="940:286" width="text" caption="1부터 6까지의 누적곱 결과 720"}
:::

:::page{type="practice-opening" id="ch09-practice-2" practice="009-2" practice-kind="실습" platform="알고플로에서 실습하기"}
# 계산기 프로그램 2

fld1과 fld2에 두 숫자를 입력합니다. 연산 버튼을 눌러 +, -, *, /를 차례로 바꾸고 = 버튼으로 계산합니다. 100과 5를 입력하고 나눗셈을 선택해 결과 20.0을 확인해봅시다.

> [!TIP]
> = 버튼은 연산 버튼에 표시된 현재 기호로 두 수를 계산합니다.

- [ ] 두 Field와 연산·계산 버튼을 배치했다.
- [ ] 연산 기호가 순서대로 바뀐다.
- [ ] 100 / 5의 결과 20.0이 보인다.
:::

:::page{type="step-process" id="ch09-calculator-request"}
# 계산기 2 · 위젯과 이벤트

## 입력 위젯

위쪽에 fld1과 fld2를 나란히 놓아 계산할 두 숫자를 받습니다. 가운데에는 btn1(연산)·btn2(=), 아래쪽에는 결과창 fld3을 배치합니다.

## 연산 버튼

btn1을 누르면 연산 기호가 +, -, *, / 순서로 바뀝니다.

## 계산 버튼

btn2를 누르면 두 입력을 float로 바꾼 뒤 현재 기호에 따라 계산합니다. 빈칸·숫자가 아닌 입력은 안내하고, 나눗셈에서 두 번째 수가 0이면 계산을 중단하고 안내합니다.

## 결과 확인

결과 표시 위젯 fld3에서 계산한 값을 확인합니다.
:::

:::page{type="concept" id="ch09-calculator" layout="basic"}
# 두 수 계산기 결과

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

100과 5, 나누기 기호가 표시되고 결과창에는 20.0이 보입니다.

::image{src="assets/source-20261006/calculator.png" alt="100과 5, 나누기 기호가 표시되고 결과창에는 20.0이 보입니다." ratio="452:215" width="half" caption="100 / 5를 계산한 결과 20.0"}
:::

:::page{type="concept" id="ch09-calculator-code" layout="basic"}
# 입력·연산·결과 연결하기

## 입력값과 연산

두 Field의 문자열을 숫자로 변환하고 사칙연산 기호를 선택합니다. 계산 버튼은 현재 입력과 기호를 읽습니다. 100과 5 외에 빈칸, 문자, 0으로 나누기도 시험하여 오류 안내를 확인합니다.

## 계산 결과 표시

두 숫자와 선택한 사칙연산을 처리하고 결과를 fld3에 표시합니다. 입력 위젯과 결과 위젯의 역할을 구분합니다.
:::

:::page{type="practice-opening" id="ch09-practice-3" practice="009-3" practice-kind="실습" platform="알고플로에서 실습하기"}
# Text에 원하는 내용 추가 프로그램

fld1에 내용을 입력하고 추가 버튼을 눌러 txt1에 표시해봅시다. 이전에 표시한 내용과 새로 추가한 내용을 함께 확인합니다.

> [!TIP]
> Text 출력과 Field 입력의 역할을 구분합니다.

- [ ] fld1·btn1·txt1을 배치했다.
- [ ] 추가 버튼이 fld1의 내용을 txt1에 넣는다.
- [ ] 입력한 내용과 추가된 내용을 비교했다.
:::

:::page{type="concept" id="ch09-text" layout="basic"}
# Text에 두 문장을 추가한 화면

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

추가한 안녕하세요 저는 코알라입니다와 저는 12살입니다가 두 줄로 표시됩니다.

::image{src="assets/source-20261006/text-append.png" alt="추가한 안녕하세요 저는 코알라입니다와 저는 12살입니다가 두 줄로 표시됩니다." ratio="393:234" width="half" caption="Text에 두 문장을 추가한 결과"}
:::

:::page{type="practice-opening" id="ch09-practice-4" practice="009-4" practice-kind="실습" platform="알고플로에서 실습하기"}
# 원하는 단 구구단 출력하기

fld1에 원하는 단을 입력하고 버튼을 눌러 txt1에 구구단을 출력해봅시다. 4를 입력하여 4 × 1부터 4 × 9까지의 결과를 확인합니다.

> [!TIP]
> 버튼 클릭과 반복 출력을 연결합니다.

- [ ] fld1·btn1·txt1을 배치했다.
- [ ] 입력한 단의 구구단이 출력된다.
- [ ] 4단의 아홉 줄을 확인했다.
:::

:::page{type="step-process" id="ch09-times-code"}
# 구구단 실습 · 프로그램 순서

## 단 입력

fld1에 4를 넣습니다.

## 이벤트 설정

btn1을 눌렀을 때 입력한 단의 구구단을 출력하도록 적습니다.

## 반복 출력

곱하는 수 1부터 9까지의 결과를 txt1에 출력합니다.

## 결과 확인

4단의 아홉 줄을 계산한 값과 비교합니다.
:::

:::page{type="concept" id="ch09-times" layout="basic"}
# 4단 출력 화면

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

입력값 4와 4단의 아홉 줄 결과가 함께 보입니다.

::image{src="assets/source-20261006/times-table.png" alt="입력값 4와 4단의 아홉 줄 결과가 함께 보입니다." ratio="489:257" width="half" caption="입력값 4에 대한 구구단 출력"}
:::

:::page{type="practice-checklist" id="ch09-check"}
# 실습 완료 확인

- [ ] 1부터 6까지의 누적곱 720을 확인했다.
- [ ] 계산기 2의 100 / 5 = 20.0을 확인했다.
- [ ] Text 추가와 4단 출력을 확인했다.

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::

:::page{type="chapter-opening" id="ch10-opening" chapter="10"}
# 선택 위젯과 진행 표시

## 10차시 · 개념과 실습

### 학습 목표

- Dropdown, Checkbox, RadioButton의 차이를 설명할 수 있다.
- 선택한 값과 안내를 연결할 수 있다.
- 진행률의 범위를 확인할 수 있다.

### 오늘의 시작

색상 선택, 건강습관 체크, 동아리 소개, 진행 막대 예시로 한 가지 선택과 여러 가지 선택을 비교합니다.
:::

:::page{type="comparison" id="ch10-choice"}
# 선택 방식 비교

선택 위젯과 진행 표시 위젯의 역할과 예시를 비교해봅시다.

| 위젯 | 선택 방식 | 활용 예시 |
|---|---|---|
| Dropdown | 목록에서 하나 | 색상 선택 |
| Checkbox | 항목별 선택·해제 | 건강습관 |
| RadioButton | 같은 그룹에서 하나 | 동아리 소개 |
| ProgressBar | 진행 정도 표시 | 0.1씩 증가·감소 |
:::

:::page{type="practice-opening" id="ch10-practice-1" practice="010-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# Dropdown을 추가하고 선택한 값 확인

fld1에 새 항목을 입력하고 버튼을 눌러 ddl1 목록에 추가해봅시다. 목록에서 항목을 선택하면 선택한 값이 txt1에 출력되는지 확인합니다.

> [!TIP]
> 항목 추가 버튼과 Dropdown 선택 이벤트를 각각 설정합니다.

- [ ] fld1·ddl1·btn1·txt1을 배치했다.
- [ ] 입력한 항목이 목록에 추가된다.
- [ ] 선택한 값이 txt1에 출력된다.
:::

:::page{type="concept" id="ch10-dropdown" layout="basic"}
# 목록의 선택값 확인하기

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

목록에서 선택한 빨강이 결과 영역에 표시됩니다.

::image{src="assets/source-20261006/dropdown.png" alt="목록에서 선택한 빨강이 결과 영역에 표시됩니다." ratio="334:304" width="half" caption="Dropdown에서 선택한 빨강 표시"}
:::

:::page{type="practice-opening" id="ch10-practice-2" practice="010-2" practice-kind="실습" platform="알고플로에서 실습하기"}
# 오늘의 건강습관 체크 프로그램

네 건강습관 Checkbox를 배치해봅시다. 오늘 실천한 항목을 선택하고 결과 확인 버튼으로 선택된 습관의 이름과 개수를 Text에 출력합니다.

> [!TIP]
> Checkbox마다 선택 여부를 확인하여 선택한 습관의 이름과 개수를 구합니다.

- [ ] chk1부터 chk4까지 배치했다.
- [ ] 선택한 습관 이름을 출력했다.
- [ ] 선택한 항목의 개수를 함께 출력했다.
:::

:::page{type="concept" id="ch10-health" layout="basic"}
# 건강습관 체크 화면

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

네 가지 습관을 각각 체크하고 확인 버튼을 누르는 화면입니다.

::image{src="assets/source-20261006/health-check.png" alt="네 가지 습관을 각각 체크하고 확인 버튼을 누르는 화면입니다." ratio="235:323" width="half" caption="건강습관 선택과 결과 확인"}
:::

:::page{type="step-process" id="ch10-health-request"}
# 건강습관 실습 · 버튼 이벤트

## 건강습관 선택

네 항목 중 실천한 항목을 체크합니다.

## 선택값 읽기

btn1은 각 Checkbox의 선택 여부를 읽습니다.

## 이름과 개수 출력

선택한 습관의 이름과 총개수를 Text에 출력합니다.
:::

:::page{type="practice-opening" id="ch10-practice-3" practice="010-3" practice-kind="실습" platform="알고플로에서 실습하기"}
# 선택한 동아리 소개 프로그램

코딩·방송·미술·과학 동아리를 Radio 그룹에 배치해봅시다. 한 동아리를 선택하고 확인 버튼을 누르면 이름과 안내 내용이 txt1에 표시되게 합니다.

> [!TIP]
> 과학 동아리를 선택했을 때 해당 동아리의 안내가 표시되는지 확인합니다.

- [ ] rad1부터 rad4까지 같은 그룹에 넣었다.
- [ ] 한 동아리만 선택할 수 있다.
- [ ] 선택한 동아리 이름과 안내가 txt1에 보인다.
:::

:::page{type="concept" id="ch10-club" layout="basic"}
# 한 동아리만 선택한 화면

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

과학 동아리가 선택되고 과학 실험과 탐구 활동 소개가 표시됩니다.

::image{src="assets/source-20261006/club-radio.png" alt="과학 동아리가 선택되고 과학 실험과 탐구 활동 소개가 표시됩니다." ratio="384:240" width="half" caption="과학 동아리 선택과 활동 소개"}
:::

:::page{type="practice-opening" id="ch10-practice-4" practice="010-4" practice-kind="실습" platform="알고플로에서 실습하기"}
# ProgressBar 버튼 2개로 증가·감소

prg1의 처음 값을 0.0으로 설정합니다. 증가 버튼은 0.1을 더하되 최대 1.0, 감소 버튼은 0.1을 빼되 최소 0.0으로 제한합니다. 양 끝에서 다시 눌러도 범위를 벗어나지 않는지 확인합니다.

> [!TIP]
> 증감 후 소수 첫째 자리로 반올림하고 0.0~1.0 범위로 제한합니다.

- [ ] prg1과 두 버튼을 배치했다.
- [ ] 증가·감소에 따라 0.1씩 바뀐다.
- [ ] 0.0에서 감소, 1.0에서 증가해도 범위를 벗어나지 않는다.
:::

:::page{type="concept" id="ch10-progress" layout="basic"}
# 진행 막대와 두 버튼

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

진행 막대 아래에 증가와 감소 버튼이 있습니다. 화면은 중간 진행 상태를 보여줍니다.

::image{src="assets/source-20261006/progress.png" alt="진행 막대 아래에 증가와 감소 버튼이 있습니다. 화면은 중간 진행 상태를 보여줍니다." ratio="292:125" width="half" caption="진행 막대와 증가·감소 버튼"}
:::

:::page{type="practice-opening" id="ch10-practice-5" practice="010-5" practice-kind="실습" platform="알고플로에서 실습하기"}
# Image 구성하기

Image 두 개를 불러오고 각각 크기를 설정해봅시다. 두 이미지가 세로로 배치되고 설정한 크기로 표시되는지 확인합니다.

> [!TIP]
> 이미지가 보이지 않으면 인터넷 연결과 이미지 주소를 확인합니다.

- [ ] Image 두 개를 화면에 배치했다.
- [ ] width와 height로 크기를 설정했다.
- [ ] 설정한 크기로 두 이미지가 표시된다.
:::

:::page{type="concept" id="ch10-images" layout="basic"}
# 두 이미지 세로 배치

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

두 Image가 세로로 배치되어 있습니다. 각 이미지의 크기와 배치 순서를 확인합니다.

::image{src="assets/ch10/two-images.png" alt="두 Image가 세로로 배치되어 있습니다. 각 이미지의 크기와 배치 순서를 확인합니다." ratio="266:232" width="half" caption="두 Image를 세로로 배치한 화면"}
:::

:::page{type="practice-checklist" id="ch10-check"}
# 실습 완료 확인

- [ ] Dropdown의 항목 추가·선택을 확인했다.
- [ ] Checkbox와 Radio 선택 결과를 확인했다.
- [ ] 진행 막대 증감과 두 이미지의 크기·배치를 확인했다.

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::

:::page{type="chapter-opening" id="ch11-opening" chapter="11"}
# 학생 성적을 표로 정리하기

## 11차시 · 개념과 실습

### 학습 목표

- 표의 행, 열, 셀을 구분할 수 있다.
- 입력 순서와 표 열 순서를 맞출 수 있다.
- 화면 번호와 리스트 인덱스를 연결할 수 있다.

### 오늘의 시작

학생 성적을 이름·국어·수학·영어 순서로 Table에 기록합니다. 입력창과 표의 각 열이 같은 항목을 가리키는지 확인합니다.
:::

:::page{type="concept" id="ch11-table" layout="basic"}
# DataTable의 구조

## 행과 열

열은 이름, 국어, 수학, 영어처럼 같은 종류의 항목입니다. 행은 학생 한 명의 기록입니다. 셀은 행과 열이 만나는 한 칸입니다.

## Flet 코드와 연결

DataColumn은 열 제목, DataRow는 한 행, DataCell은 한 칸을 구성합니다. 화면에서 보이는 열 이름과 실제 값을 넣는 순서를 맞춥니다.
:::

:::page{type="practice-opening" id="ch11-practice-1" practice="011-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# 학생 성적을 Table에 기록하기

fld1부터 fld4까지 학생 이름과 국어·수학·영어 점수를 입력해봅시다. 추가하기 버튼을 누르면 tbl1에 같은 순서로 한 행이 기록되는지 확인합니다.

> [!TIP]
> 입력창의 순서와 표의 이름·국어·수학·영어 열 순서를 맞춥니다.

- [ ] 입력창과 표의 이름·국어·수학·영어 순서를 맞췄다.
- [ ] 추가하기를 누르면 표에 한 행이 기록된다.
- [ ] 입력값과 표의 각 칸을 대조했다.
:::

:::page{type="concept" id="ch11-table-screen" layout="basic"}
# 학생 성적 Table

## 예시 확인하기

화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

표 열은 이름, 국어, 수학, 영어입니다. 학생1은 100, 90, 80으로 표시됩니다.

::image{src="assets/source-20261006/student-table.png" alt="표 열은 이름, 국어, 수학, 영어입니다. 학생1은 100, 90, 80으로 표시됩니다." ratio="744:381" width="text" caption="학생1의 국어·수학·영어 성적 기록"}
:::

:::page{type="comparison" id="ch11-field-map"}
# 입력창과 표 열 대조

각 입력창이 연결되는 표의 열과 예시 값을 확인해봅시다.

| 입력창 | 표 열 | 연습 입력 |
|---|---|---|
| fld1 | 이름 | 학생1 |
| fld2 | 국어 | 100 |
| fld3 | 수학 | 90 |
| fld4 | 영어 | 80 |
:::

:::page{type="step-process" id="ch11-request"}
# Table 실습 · 입력과 추가

## 위젯 배치

왼쪽에는 fld1~fld4를 세로로 놓고 그 아래 btn1(추가하기), 오른쪽에는 tbl1을 배치합니다.

## 입력창 역할

fld1은 이름, fld2는 국어, fld3은 수학, fld4는 영어로 정합니다.

## 추가 이벤트

btn1은 입력한 네 값을 표의 같은 순서로 추가합니다.

## 입력과 표 비교

학생1의 100·90·80 입력값이 표의 국어·수학·영어 열에 맞게 표시되는지 비교합니다.
:::

:::page{type="concept" id="ch11-index" layout="basic"}
# 왜 위치 번호에서 1을 뺄까?

## 화면의 번호

사용자는 첫 번째 행을 1행이라고 부릅니다. Python 리스트의 첫 위치는 0입니다. 따라서 화면의 2행은 리스트 위치 1과 대응합니다.

## 확인할 범위

번호를 숫자로 바꾼 뒤 실제 행과 열 범위에 있는지 확인합니다. 번호 0을 허용하면 1을 뺐을 때 -1이 되어 마지막 위치를 가리킬 수 있습니다.
:::

:::page{type="step-process" id="ch11-index-code"}
# 행·열 번호를 리스트 위치로 바꾸기

## 화면 번호 확인

화면에서 2행을 선택했다고 생각해봅시다.

## 리스트 위치 변환

첫 행의 인덱스는 0, 둘째 행의 인덱스는 1입니다. 선택한 행·열 번호에서 각각 1을 뺍니다.

## 선택한 셀 확인

변환한 행과 열 위치가 원하는 DataCell에 해당하는지 확인합니다.
:::

:::page{type="step-process" id="ch11-practice-2"}
# 표의 값 변경 순서

## 행·열 선택

사용자가 값을 넣을 행 번호와 열 번호를 선택합니다.

## 값 입력

Field에 표에 넣을 값을 입력합니다.

## 인덱스 변환

선택한 번호에서 1을 빼서 리스트 위치로 바꿉니다.

## 변경 반영

선택한 DataCell의 내용을 바꾸고 표에 표시합니다.
:::

:::page{type="practice-checklist" id="ch11-check"}
# 실습 완료 확인

- [ ] Table의 입력과 과목 순서를 맞췄다.
- [ ] 행·열 번호에서 1을 빼는 이유를 설명했다.

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::

:::page{type="chapter-opening" id="ch12-opening" chapter="12"}
# Matplotlib 선 그래프와 마커

## 12차시 · 개념과 실습

### 학습 목표

- Figure와 Axes를 만들고 배열을 선 그래프로 나타낼 수 있다.
- X·Y 값과 표시 범위·마커를 구분할 수 있다.
- 제목·축 이름·좌표 설명을 설정하고 실행 결과를 확인할 수 있다.

### 오늘의 시작

배열 한 개와 X·Y 배열을 그래프로 나타냅니다. 표시 범위와 마커를 바꾸고 제목·축 이름·좌표 설명의 위치를 확인합니다.
:::

:::page{type="concept" id="ch12-axes" layout="basic"}
# 그릴 판과 그리는 영역

## Figure와 Axes

plt.subplots는 Figure와 Axes를 함께 만듭니다. Figure는 전체 그림이고 Axes는 실제 데이터를 그리는 영역입니다. 먼저 생성한 뒤 ax.plot처럼 사용합니다.

## Python 예제와 수업 GUI

Python에서 Matplotlib 코드를 실행하여 그림을 확인합니다. 생성한 Figure를 수업 GUI에 연결할 때는 해당 도구의 fch.MatplotlibChart 설정과 사용 환경을 확인합니다.
:::

:::page{type="practice-opening" id="ch12-practice-1" practice="012-1" practice-kind="Matplotlib 실습" platform="알고플로에서 실습하기"}
# Matplotlib 실습 1 · 배열 한 개

[1, 2, 3, 4, 5] 배열을 선으로 그려봅시다. 하나의 배열을 전달했을 때 X축이 0부터 4까지의 위치가 되는지 확인합니다.

> [!TIP]
> Axes에 plot을 호출하여 데이터를 그립니다.

- [ ] [1, 2, 3, 4, 5] 배열을 사용했다.
- [ ] 배열 하나를 plot에 전달했다.
- [ ] X 위치 0부터 4를 확인했다.
:::

:::page{type="concept" id="ch12-one-array" layout="basic"}
# 실습 1 · 배열 한 개의 그래프

## 예제 코드 실행하기

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3, 4, 5])
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-one.png" alt="실습 1 · 배열 한 개의 그래프 코드 실행 결과" ratio="8:5" width="text" role="result" caption="배열 한 개를 전달한 선 그래프"}
:::

:::page{type="practice-opening" id="ch12-practice-two" practice="012-2" practice-kind="Matplotlib 실습" platform="알고플로에서 실습하기"}
# Matplotlib 실습 2 · X·Y 배열

a = [15, 25, 35, 45, 55], b = [5, 10, 15, 20, 25]를 X와 Y로 지정해봅시다. 두 배열의 같은 위치 값이 한 점의 좌표가 됩니다.

> [!TIP]
> 두 배열의 길이와 값의 짝을 확인합니다.

- [ ] a와 b 배열을 지정했다.
- [ ] a는 X, b는 Y로 연결했다.
- [ ] 다섯 점의 위치를 X·Y 값과 비교했다.
:::

:::page{type="concept" id="ch12-two-arrays" layout="basic"}
# 실습 2 · X·Y 배열 지정

## 예제 코드 실행하기

```python
import matplotlib.pyplot as plt

a = [15, 25, 35, 45, 55]
b = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(a, b)
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-two.png" alt="실습 2 · X·Y 배열 지정 코드 실행 결과" ratio="8:5" width="text" role="result" caption="X·Y 배열을 지정한 선 그래프"}
:::

:::page{type="practice-opening" id="ch12-practice-2" practice="012-3" practice-kind="Matplotlib 실습" platform="알고플로에서 실습하기"}
# Matplotlib 실습 3 · 표시 범위

X는 [1, 2, 3, 4, 5], Y는 [5, 10, 15, 20, 25]로 정합니다. b-+ 모양과 axis([0, 10, 0, 25])를 적용해봅시다.

> [!TIP]
> 값을 바꾸는 것과 표시 범위를 바꾸는 것을 구분합니다.

- [ ] 지정한 X·Y 값을 사용했다.
- [ ] 파란 선과 더하기 마커를 지정했다.
- [ ] X 0-10, Y 0-25 범위를 확인했다.
:::

:::page{type="concept" id="ch12-range" layout="basic"}
# 실습 3 · 선 모양과 표시 범위

## 예제 코드 실행하기

```python
import matplotlib.pyplot as plt

a = [1, 2, 3, 4, 5]
b = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(a, b, "b-+", clip_on=False)
ax.axis([0, 10, 0, 25])
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-range.png" alt="실습 3 · 선 모양과 표시 범위 코드 실행 결과" ratio="8:5" width="text" role="result" caption="파란 선·더하기 마커와 지정한 축 범위"}
:::

:::page{type="practice-opening" id="ch12-practice-colors" practice="012-4" practice-kind="Matplotlib 실습" platform="알고플로에서 실습하기"}
# Matplotlib 실습 4 · 모양과 색

같은 X·Y 배열에 ro를 적용해 빨간 점으로 표시해봅시다. r-o도 비교하여 점만 그리는 경우와 선이 이어지는 경우를 구분합니다.

> [!TIP]
> ro는 빨간 점을 표시하고, r-o는 빨간 점과 점 사이의 선을 함께 표시합니다.

- [ ] 앞 실습의 X·Y 배열을 사용했다.
- [ ] ro가 빨간 점임을 확인했다.
- [ ] r-o와의 선 표시 차이를 설명했다.
:::

:::page{type="concept" id="ch12-markers" layout="basic"}
# 실습 4 · 빨간 점과 설명

## 예제 코드 실행하기

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, "ro", clip_on=False)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("hello")
ax.text(3, 5, "12/19")
ax.axis([0, 10, 0, 25])
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-markers.png" alt="실습 4 · 빨간 점과 설명 코드 실행 결과" ratio="8:5" width="text" role="result" caption="ro로 표시한 빨간 점과 그래프 설명"}
:::

:::page{type="practice-opening" id="ch12-practice-labels" practice="012-5" practice-kind="Matplotlib 실습" platform="알고플로에서 실습하기"}
# Matplotlib 실습 5 · 제목과 설명

같은 그래프에 지정한 x·y 축 이름, hello 제목, 좌표 (3, 5)의 12/19 설명을 확인해봅시다. 앞 실습의 코드와 데이터를 그대로 사용합니다.

> [!TIP]
> 앞 실습의 그래프에서 제목·축 이름·좌표 설명의 위치를 살펴봅니다.

- [ ] x·y 축 이름을 확인했다.
- [ ] hello 제목을 확인했다.
- [ ] (3, 5)의 12/19 설명을 확인했다.
:::

:::page{type="concept" id="ch12-labels-screen" layout="basic"}
# 그래프의 제목·축·좌표 설명

## 설명의 위치 확인

제목 hello, 축 x·y와 좌표 설명 12/19를 확인합니다.

::image{src="assets/source-20261006/plot-markers.png" alt="제목 hello, 축 x·y와 좌표 설명 12/19를 확인합니다." ratio="1920:1200" width="text" caption="제목·축 이름과 좌표 (3, 5)의 12/19 설명"}
:::

:::page{type="concept" id="ch12-fix" layout="basic"}
# 점과 선의 모양 확인

## ro와 r-o

ro는 빨간 점을 표시하고, r-o는 빨간 점과 점 사이의 선을 함께 표시합니다. 같은 X·Y 값에서도 모양 설정에 따라 결과가 달라집니다.
:::

:::page{type="practice-checklist" id="ch12-check"}
# 실습 완료 확인

- [ ] 다섯 Matplotlib 실습의 입력값과 그래프를 확인했다.
- [ ] 배열·표시 범위·마커의 차이를 설명했다.
- [ ] 제목·축 이름·좌표 설명의 위치를 확인했다.

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::

:::page{type="chapter-opening" id="ch13-opening" chapter="13"}
# Matplotlib 막대그래프와 산점도

## 13차시 · 개념과 실습

### 학습 목표

- 배열 값을 막대 높이로 표현할 수 있다.
- create_x로 나란한 막대의 위치와 항목 이름을 정할 수 있다.
- 같은 시드로 만든 X·Y의 산점도와 축·범례를 확인할 수 있다.

### 오늘의 시작

막대그래프의 높이와 위치를 배열 값에 연결합니다. 두 배열을 나란히 비교하고, 난수를 더한 X·Y 값으로 산점도를 만듭니다.
:::

:::page{type="practice-opening" id="ch13-practice-3" practice="013-1" practice-kind="Matplotlib 실습" platform="알고플로에서 실습하기"}
# Matplotlib 실습 1 · 막대그래프 1

[1, 2, 4, 8, 16, 32, 64, 128]을 막대로 그려봅시다. range(len(a))로 X 위치를 만들고 각 높이를 확인합니다.

> [!TIP]
> range(len(a))는 배열 길이만큼 0부터 시작하는 막대 위치를 만듭니다.

- [ ] 2의 거듭제곱 배열을 사용했다.
- [ ] 여덟 값의 막대를 그렸다.
- [ ] 막대 높이와 배열 값을 비교했다.
:::

:::page{type="concept" id="ch13-bars" layout="basic"}
# 실습 1 · 막대그래프 1

## 예제 코드 실행하기

```python
import matplotlib.pyplot as plt

a = [1, 2, 4, 8, 16, 32, 64, 128]
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(range(len(a)), a)
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-bars.png" alt="실습 1 · 막대그래프 1 코드 실행 결과" ratio="8:5" width="text" role="result" caption="2의 거듭제곱 배열을 나타낸 여덟 막대"}
:::

:::page{type="practice-opening" id="ch13-practice-grouped" practice="013-2" practice-kind="Matplotlib 실습" platform="알고플로에서 실습하기"}
# Matplotlib 실습 2 · 막대그래프 2

one부터 five까지의 항목과 value_a·value_b 배열을 사용해봅시다. create_x 함수로 두 막대의 위치를 만들고 중간 위치에 항목 이름을 표시합니다.

> [!TIP]
> create_x는 t, w, n, d로 막대의 가로 위치를 계산합니다.

- [ ] value_a·value_b의 두 값 배열을 사용했다.
- [ ] create_x로 두 막대를 나란히 배치했다.
- [ ] 중간 위치에 one부터 five까지 표시했다.
:::

:::page{type="concept" id="ch13-grouped" layout="basic"}
# 실습 2 · 나란한 막대그래프

## 예제 코드 실행하기

```python
import matplotlib.pyplot as plt

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
plt.show()
```

::image{src="assets/source-20261006/plot-grouped.png" alt="실습 2 · 나란한 막대그래프 코드 실행 결과" ratio="8:5" width="text" role="result" caption="다섯 항목에 나란히 배치한 두 배열의 막대"}
:::

:::page{type="practice-opening" id="ch13-practice-4" practice="013-3" practice-kind="Matplotlib 실습" platform="알고플로에서 실습하기"}
# Matplotlib 실습 3 · 산점도

시드 20211206, X 범위 1.1부터 100.0 미만, 간격 5.0으로 데이터를 만들어봅시다. X의 1.5배에 난수를 더한 Y로 산점도를 만들고 축 이름을 함수 호출로 설정합니다.

> [!TIP]
> seed는 난수 생성의 시작 상태를 정합니다. 같은 시드와 생성 순서를 사용하면 같은 난수를 얻습니다.

- [ ] 지정한 시드와 X 범위를 사용했다.
- [ ] X의 1.5배에 난수를 더해 Y를 만들었다.
- [ ] 축 이름·random 범례·제목을 확인했다.
:::

:::page{type="concept" id="ch13-scatter" layout="basic"}
# 실습 3 · 산점도

## 예제 코드 실행하기

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

fonts = {f.name for f in
         font_manager.fontManager.ttflist}
families = ("Malgun Gothic", "AppleGothic",
            "Noto Sans CJK KR", "Noto Sans KR",
            "NanumGothic", "Wanted Sans")
font_name = next((f for f in families
                  if f in fonts), None)
if font_name:
    plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False

np.random.seed(20211206)
x = np.arange(1.1, 100.0, 5.0)
y = x * 1.5 + np.random.rand(20) * 50
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, c="red", alpha=0.5, label="random")
ax.set_xlabel("X축 제목" if font_name else "X axis")
ax.set_ylabel("Y축 제목" if font_name else "Y axis")
ax.legend(loc="upper left")
ax.set_title("random")
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-scatter.png" alt="실습 3 · 산점도 코드 실행 결과" ratio="8:5" width="text" role="result" caption="난수를 더한 Y값을 표시한 빨간 산점도"}
:::

:::page{type="concept" id="ch13-fix" layout="basic"}
# 산점도의 데이터와 축 설정

## 난수 시드 확인

seed는 난수 생성기의 상태를 정합니다. 같은 시드와 생성 순서를 사용하면 같은 난수를 얻습니다. 산점도의 X·Y 값은 코드에서 생성한 연습용 데이터입니다.

## 축 이름과 범례

축 이름은 set_xlabel, set_ylabel 함수로 설정합니다. 예제는 설치된 한글 글꼴을 찾아 적용합니다. 해당 글꼴이 없으면 축 이름을 X axis·Y axis로 표시합니다. 한글 축 이름을 보려면 families에 적힌 글꼴 중 하나를 설치한 뒤 다시 실행합니다. 범례 random이 빨간 점을 가리키는지 확인합니다.
:::

:::page{type="practice-checklist" id="ch13-check"}
# 실습 완료 확인

- [ ] 세 Matplotlib 실습의 코드를 실행했다.
- [ ] 막대의 높이와 나란한 막대 위치를 배열 값과 비교했다.
- [ ] 산점도의 시드·축 이름·범례를 확인했다.

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::

:::page{type="chapter-opening" id="ch14-opening" chapter="14"}
# 입력 데이터를 차트로 표현하기

## 14차시 · 개념과 실습

### 학습 목표

- 선 그래프·막대그래프·산점도의 표현 목적과 축을 구분할 수 있다.
- 입력창의 값을 버튼 이벤트로 Chart에 연결할 수 있다.
- 입력값과 그래프를 비교하고 초기화·누적 동작을 확인할 수 있다.

### 오늘의 시작

입력값을 선 그래프·산점도·막대그래프로 나타내고 버튼 동작, 초기화·누적을 확인합니다.
:::

:::page{type="comparison" id="ch14-charts"}
# 표현 목적에 맞는 그래프

| 그래프 | 표현할 내용 | 축 확인 |
|---|---|---|
| 선 그래프 | 순서에 따른 값 변화 | 입력 순서와 수치 |
| 막대그래프 | 항목별 값 크기 | 항목과 수치 |
| 산점도 | 두 수치의 짝 | X의 값과 Y의 값 |
:::

:::page{type="practice-opening" id="ch14-practice-1" practice="014-1" practice-kind="시각화 실습" platform="알고플로에서 실습하기"}
# 꺾은선 그래프 만들기

fld1부터 fld5까지 1·2·5·4·5를 입력하고 그래프 그리기 버튼을 눌러봅시다. 초기화 버튼의 역할도 확인합니다.

> [!TIP]
> 그래프의 가로 위치는 입력 순서 0부터 4입니다.

- [ ] 다섯 Field와 Chart를 구성했다.
- [ ] 입력값이 꺾은선으로 표시된다.
- [ ] 초기화 버튼을 확인했다.
:::

:::page{type="concept" id="ch14-line-screen" layout="basic"}
# 선 그래프 화면

## GUI 구성과 실행 예시

왼쪽에 fld1부터 fld5까지 세로로 배치하고 오른쪽에 cht1을 둡니다. 차트 아래에는 btn1(그래프 그리기)과 btn2(초기화)를 나란히 둡니다. 초기화 버튼은 차트의 기록을 비웁니다.

다섯 입력값 1, 2, 5, 4, 5와 가로 위치 0부터 4의 선 그래프가 보입니다.

::image{src="assets/source-20261006/line-chart.png" alt="다섯 입력값 1, 2, 5, 4, 5와 가로 위치 0부터 4의 선 그래프가 보입니다." ratio="856:467" width="text" caption="입력 순서에 따른 다섯 값의 선 그래프"}
:::

:::page{type="practice-opening" id="ch14-practice-2" practice="014-2" practice-kind="시각화 실습" platform="알고플로에서 실습하기"}
# 키·몸무게 산점도 만들기

두 Field에 키와 몸무게를 입력하고 버튼으로 Chart에 점을 추가해봅시다. 170·74, 180·82, 185·89의 세 쌍을 입력하여 점의 위치를 확인합니다.

> [!TIP]
> 버튼을 누를 때마다 이전 점을 유지하고 새 점을 누적하도록 설정합니다.

- [ ] 키와 몸무게를 서로 다른 입력창으로 받는다.
- [ ] 입력한 한 쌍이 점 하나로 표시된다.
- [ ] 누적한 세 쌍의 입력값과 점의 위치를 비교했다.
:::

:::page{type="concept" id="ch14-scatter-screen" layout="basic"}
# 키·몸무게 산점도

## GUI 구성과 실행 예시

왼쪽에 fld1(키)·fld2(몸무게)와 btn1(시각화)을 놓고 오른쪽에 cht1을 둡니다. 산점도의 X값은 키, Y값은 몸무게로 정합니다.

현재 입력 185와 89, 이전 입력을 포함한 세 점이 표시됩니다.

::image{src="assets/source-20261006/scatter-chart.png" alt="현재 입력 185와 89, 이전 입력을 포함한 세 점이 표시됩니다." ratio="904:464" width="text" caption="키·몸무게 세 쌍을 표시한 산점도"}
:::

:::page{type="practice-opening" id="ch14-practice-3" practice="014-3" practice-kind="시각화 실습" platform="알고플로에서 실습하기"}
# 입력값 막대그래프 만들기

fld1의 값을 버튼으로 차례로 추가하여 막대그래프로 만들어봅시다. 90·80·70을 입력하여 세 막대의 높이를 비교합니다.

> [!TIP]
> 버튼을 누를 때마다 이전 막대를 유지하고 새 값을 다음 위치에 누적합니다.

- [ ] 입력창·버튼·Chart를 구성했다.
- [ ] 입력한 값을 막대로 표시했다.
- [ ] 90·80·70의 입력값과 세 막대 높이를 비교했다.
:::

:::page{type="concept" id="ch14-bar-screen" layout="basic"}
# 입력값 막대그래프

## GUI 구성과 실행 예시

위쪽에 fld1, 가운데에 btn1(시각화), 아래쪽에 cht1을 배치합니다.

90, 80, 70의 세 막대가 입력 순서대로 보입니다.

::image{src="assets/source-20261006/bar-chart.png" alt="90, 80, 70의 세 막대가 입력 순서대로 보입니다." ratio="480:545" width="half" caption="90·80·70을 입력 순서대로 표시한 막대그래프"}
:::

:::page{type="practice-checklist" id="ch14-check"}
# 실습 완료 확인

- [ ] 선 그래프·산점도·막대그래프를 만들었다.
- [ ] 입력값과 그래프의 축·점·막대 높이를 확인했다.
- [ ] 초기화와 입력값 누적 동작을 확인했다.
:::

:::page{type="chapter-opening" id="ch15-opening" chapter="15"}
# 자료 활용과 저장·불러오기

## 15차시 · 개념과 실습

### 학습 목표

- 학생 자료의 표시 항목을 선택하고 표·차트로 표현할 수 있다.
- 학교별 학생 수를 집계하여 막대그래프로 비교할 수 있다.
- 걸음 수·이동거리의 표를 저장하고 프로젝트를 불러와 같은 기록을 확인할 수 있다.

### 오늘의 시작

학생 자료의 표시 항목과 학교별 학생 수를 살펴봅니다. 이어서 걸음 수·이동거리를 직접 입력하는 앱을 만들고, 저장한 기록을 다시 불러와 확인합니다.
:::

:::page{type="practice-opening" id="ch15-practice-data" practice="015-1" practice-kind="자료 활용" platform="알고플로에서 실습하기"}
# 학생 100명 자료 불러와 시각화하기

자료 버튼에서 학생 100명 키·몸무게 자료를 불러와봅시다. 표에 표시할 항목을 고르고 키와 몸무게의 두 열을 산점도의 X·Y로 지정합니다.

> [!TIP]
> 수업에서 제공한 학생 자료를 사용합니다.

- [ ] 학생 100명 자료를 선택했다.
- [ ] 표의 ID·키·몸무게 등 항목을 선택했다.
- [ ] 산점도에 연결할 두 열을 확인했다.
:::

:::page{type="step-process" id="ch15-loaded-data"}
# 저장된 자료 불러오기 순서

## 자료 선택

자료 버튼에서 학생 100명의 키와 몸무게 자료를 선택합니다.

## 표 항목 선택

ID·키·몸무게 또는 ID·성별·키·몸무게 구성을 살펴봅니다.

## 산점도 설정

X축과 Y축에 쓸 열을 직접 확인합니다. 선택한 열의 값과 화면의 축 범위가 맞는지 비교합니다.
:::

:::page{type="concept" id="ch15-data-screen" layout="basic"}
# 자료의 표시 항목 선택

## 표시할 열 고르기

자료 항목 선택 메뉴에서 표시할 열을 선택하고 표와 그래프의 연결을 확인합니다.

::image{src="assets/source-20261010/data-column-select.png" alt="자료 항목 선택 메뉴에서 표시할 열을 선택하고 표와 그래프의 연결을 확인합니다." ratio="946:408" width="text" caption="학생 자료에서 표에 표시할 열 선택"}
:::

:::page{type="practice-opening" id="ch15-practice-school" practice="015-2" practice-kind="자료 활용" platform="알고플로에서 실습하기"}
# 학교별 학생 수를 막대그래프로 표현

앞에서 불러온 같은 학생 자료를 사용해 학교별 학생 수를 막대그래프로 표시해봅시다. 고등학교와 중학교의 학생 수를 비교합니다.

> [!TIP]
> 앞에서 불러온 자료의 school 열을 사용합니다.

- [ ] 앞의 학생 자료를 그대로 사용했다.
- [ ] 학교 항목별 개수를 집계했다.
- [ ] 고등학교·중학교 막대를 비교했다.
:::

:::page{type="concept" id="ch15-school-screen" layout="basic"}
# 학교별 학생 수 막대그래프

## 항목별 개수 확인

학생 자료를 학교 구분별 개수로 표시한 화면입니다.

::image{src="assets/source-20261010/school-count-chart.png" alt="학생 자료를 학교 구분별 개수로 표시한 화면입니다." ratio="1020:992" width="text" caption="고등학교·중학교 학생 수 비교"}
:::

:::page{type="practice-opening" id="ch15-practice-3" practice="015-3" practice-kind="저장 실습" platform="알고플로에서 실습하기"}
# 걸음 수·이동거리 저장·불러오기

이번에는 걸음 수와 이동거리를 직접 입력하는 앱을 만들어봅시다. 두 입력 필드, 두 버튼, 표와 산점도로 화면을 구성합니다. 표 저장을 켜고 기록을 추가한 뒤, 프로젝트를 저장하고 다시 불러옵니다.

> [!TIP]
> 표의 두 열을 먼저 정한 뒤 표 저장을 켭니다. 산점도의 X축은 걸음 수, Y축은 이동거리입니다.

- [ ] 걸음 수·이동거리의 표 구성과 저장 설정을 확인했다.
- [ ] 입력한 기록을 표·산점도에 표시하고 프로젝트를 저장했다.
- [ ] 프로젝트를 다시 불러와 같은 기록을 확인했다.
:::

:::page{type="concept" id="ch15-gui-layout" layout="basic"}
# 저장 실습 · GUI 구성 예시

## 여섯 위젯으로 화면 구성

위쪽에 fld1(걸음 수)·fld2(이동거리), 그 아래에 btn1(데이터 추가)·btn2(초기화)를 나란히 놓습니다. 다음에 표 tbl1과 차트 cht1을 세로로 배치합니다.

::image{src="assets/source-20261011/save-gui-layout.png" alt="걸음 수·이동거리 입력창, 데이터 추가·초기화 버튼, 두 열의 표와 차트를 배치한 디자이너 화면" ratio="913:1216" width="half" caption="걸음 수·이동거리 앱의 디자이너 구성"}
:::

:::page{type="concept" id="ch15-save-widgets" layout="basic"}
# 입력 화면과 버튼 동작 정하기

## 위젯 이름과 역할

프로젝트 이름은 ‘걸음수와 이동거리 확인’, 앱 설명은 ‘걸음수와 이동거리를 그래프로 보여주기’로 정합니다.

- fld1: 걸음 수를 입력하는 필드
- fld2: 이동거리를 입력하는 필드
- btn1: ‘데이터 추가’ 버튼
- btn2: ‘초기화’ 버튼
- tbl1: 걸음 수·이동거리를 누적하는 표
- cht1: 두 값의 관계를 보여주는 산점도

## 데이터 추가 버튼

btn1을 누르면 fld1·fld2의 값을 tbl1의 새 행에 추가합니다. 표의 걸음 수를 X값, 이동거리를 Y값으로 사용해 cht1의 산점도를 갱신합니다.

## 초기화 버튼

btn2를 누르면 tbl1과 cht1의 기록을 초기화합니다. 저장·불러오기를 비교하는 동안에는 초기화 버튼을 누르지 않습니다.
:::

:::page{type="concept" id="ch15-save-process" layout="basic"}
# 표 구성과 저장 설정하기

## 먼저 표의 두 열 구성하기

tbl1을 선택하고 ‘걸음 수’와 ‘이동거리’ 두 열을 만듭니다. 입력 기록이 두 열에 한 행씩 추가되도록 설정합니다.

::image{src="assets/source-20261011/save-table-columns.png" alt="tbl1의 걸음 수·이동거리 두 열과 열 추가·행 추가 설정 화면" ratio="1066:286" width="text" caption="표 저장을 켜기 전에 두 열을 정하기"}

## 표 저장 켜기

화면 위쪽의 ‘표 저장’을 켭니다. 프로젝트를 저장할 때 입력한 표의 기록도 함께 저장됩니다. 표 저장을 켠 뒤에는 행·열 개수 변경이 제한되므로 구성을 먼저 마칩니다.

::image{src="assets/ch15/save-table-toggle.png" alt="화면 위쪽의 표 저장 스위치가 켜진 상태" ratio="208:84" width="half" caption="파란색으로 켜진 표 저장 스위치 확인"}
:::

:::page{type="concept" id="ch15-save-menu" layout="basic"}
# 기록을 추가하고 프로젝트 저장하기

## 내 저장소에서 저장 선택

앱을 실행해 걸음 수와 이동거리를 입력하고 ‘데이터 추가’를 누릅니다. 표의 값과 산점도의 점을 확인한 뒤 ‘내 저장소’를 열어 ‘저장’을 선택합니다.

::image{src="assets/source-20261011/save-project-menu.png" alt="내 저장소 메뉴의 저장·다른 이름으로 저장·불러오기 항목" ratio="1115:1366" width="half" caption="내 저장소에서 저장 선택"}
:::

:::page{type="concept" id="ch15-save-name" layout="basic"}
# 프로젝트 이름을 정하고 저장하기

## 저장할 내용 확인

프로젝트 이름에 ‘데이터 저장’을 입력합니다. 화면 구성과 버튼 동작을 확인하고 아래의 ‘저장’을 누릅니다. 불러올 때 찾을 수 있도록 이름을 기억합니다.

::image{src="assets/source-20261011/save-project-name.png" alt="프로젝트 이름 데이터 저장과 저장할 내용, 아래쪽 저장 버튼" ratio="849:1278" width="half" caption="프로젝트 이름을 입력하고 저장 버튼 누르기"}
:::

:::page{type="concept" id="ch15-load-project" layout="basic"}
# 저장한 프로젝트 불러오기

## 같은 이름을 선택하고 열기

‘내 저장소’의 ‘불러오기’를 선택합니다. 목록에서 ‘데이터 저장’을 고르고 오른쪽 아래 ‘열기’를 누릅니다. 불러온 앱을 실행해 표와 산점도의 기록을 확인합니다.

::image{src="assets/source-20261011/load-project-select.png" alt="내 저장소 목록에서 데이터 저장을 선택하고 열기 버튼을 누르는 화면" ratio="1103:1238" width="half" caption="저장한 프로젝트를 선택한 뒤 열기"}
:::

:::page{type="concept" id="ch15-saved" layout="basic"}
# 다시 불러온 프로젝트

## 기록 확인하기

불러온 앱에 걸음 수·이동거리의 표와 산점도가 함께 표시됩니다. 저장하기 전에 기록한 값과 비교합니다. 예를 들어 표의 걸음 수 10·이동거리 15는 산점도의 (10, 15) 점과 대응합니다.

::image{src="assets/source-20261006/saved-project.png" alt="걸음 수·이동거리 입력 기록이 표와 산점도에 남아 있는 불러온 앱" ratio="744:1282" width="half" caption="다시 불러온 걸음 수·이동거리의 표와 산점도"}
:::

:::page{type="practice-checklist" id="ch15-check"}
# 실습 완료 확인

- [ ] 학생 자료의 표시 항목과 학교별 개수를 확인했다.
- [ ] 걸음 수를 X값, 이동거리를 Y값으로 표·산점도에 표시했다.
- [ ] 저장·불러오기 후 같은 입력 기록이 남아 있는지 확인했다.

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::

:::page{type="chapter-opening" id="ch16-opening" chapter="16"}
# 앱 개선과 결과 발표

## 16차시 · 개념과 실습

### 학습 목표

- 앞서 배운 실습을 활용하여 작은 프로젝트를 완성할 수 있다.
- 문제를 재현하고 수정 결과를 검증할 수 있다.
- AI 도움과 직접 확인한 내용을 구분해 발표할 수 있다.

### 오늘의 시작

자율 프로젝트의 아이디어와 UI 설계를 작성합니다. 앞서 배운 위젯으로 프로그램을 만들고 동작 결과를 설명합니다.
:::

:::page{type="concept" id="ch16-projects" layout="basic"}
# 자율 프로젝트 설계

## 프로그램 아이디어

만들고 싶은 프로그램의 아이디어를 작성합니다. 목적과 필요한 입력, 보여줄 결과를 정리합니다.

## UI 설계

UI 설계를 작성합니다. 필요한 위젯을 배치하고 이름과 역할, 버튼을 클릭했을 때 할 일을 적습니다.
:::

:::page{type="practice-opening" id="ch16-practice-1" practice="016-1" practice-kind="실습" platform="알고플로에서 실습하기"}
# 원하는 프로그램을 자유롭게 작성하기

프로그램 아이디어와 UI 설계를 작성해봅시다. 앞에서 배운 위젯으로 화면을 구성하고 버튼 이벤트를 정한 뒤 실행 결과를 확인합니다.

> [!TIP]
> 앞선 실습의 위젯과 기능을 활용해 UI를 설계합니다.

- [ ] 프로그램 아이디어를 적었다.
- [ ] 필요한 위젯과 역할을 정하여 UI를 설계했다.
- [ ] 생성한 프로그램의 동작을 확인했다.
:::

:::page{type="step-process" id="ch16-procedure"}
# 작게 만들고 검증하기

## 성공 기준 정하기

어떤 입력을 넣었을 때 어떤 결과가 보여야 하는지 적습니다.

## 실행 결과 확인

직접 값을 넣고 결과를 기록합니다. 설명만 보고 통과로 표시하지 않습니다.

## 오류 하나 수정

문제 상황, 입력, 예상 결과, 실제 결과를 포함해 수정 요청합니다.

## 다시 확인

수정한 기능과 이전에 정상 동작하던 기능을 다시 실행합니다.
:::

:::page{type="concept" id="ch16-fix" layout="basic"}
# 자율 프로젝트의 입력과 동작 확인

## 설계와 실행 비교

입력창·버튼·결과 위젯의 역할이 자신이 적은 아이디어와 같은지 확인합니다.

## 확인 결과 정리

실행 화면과 확인한 동작을 남깁니다.
:::

:::page{type="concept" id="ch16-evidence" layout="basic"}
# 결과 이미지를 정직하게 기록하기

## 직접 만든 결과

자기 앱의 실제 입력과 결과가 같이 보이게 캡처합니다. 이름·연락처 등 개인정보를 빼고, 이전 버전 이미지가 남아 있지 않은지 확인합니다.

## 수정 전후 기록

오류 수정 전과 후는 같은 입력으로 비교합니다. 직접 실행한 화면과 수정 내용을 함께 저장하여 바뀐 동작을 설명합니다.
:::

:::page{type="concept" id="ch16-portfolio" layout="basic"}
# 포트폴리오에 담을 내용

## 기획과 구현

앱 이름, 사용자, 해결할 문제를 적습니다. 입력, 처리, 출력 설계와 주요 위젯 역할을 넣습니다.

## 검증과 개선

실행 가능한 프로젝트, 정상 입력 결과, 예외 입력 결과, 수정 요청과 재검증 기록을 남깁니다. 불러온 자료의 값과 실행 결과를 기록합니다.
:::

:::page{type="practice-checklist" id="ch16-check"}
# 실습 완료 확인

- [ ] 자율 프로젝트의 아이디어·UI를 작성했다.
- [ ] 위젯 역할·이벤트·실행 결과를 대조했다.

> [!KEY_POINT]
> 입력·동작·결과를 기준으로 직접 확인한 내용을 기록합니다.
:::
