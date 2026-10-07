---
schema_version: 1
title: AI와 함께하는 바이브 코딩
subtitle: 원본 교재 기반 16차시 · 수정 원고
learner_level: 코딩 입문자
language: ko
canvas: coala-portrait
numbering: auto
toc: none
assets_dir: ./assets
---

:::page{type="concept" id="book-guide" layout="basic"}
# 이 교재를 사용하는 방법

## 원본을 따라 배우기

사용자가 제공한 158쪽 앱 개발 PDF의 설명과 실습을 16차시로 재구성했습니다. AI 활용, 알고리즘, GUI, 시각화, 데이터 정리, 코코봇을 순서대로 배웁니다.

## 설명에서 실행까지

책의 예시를 읽고 예상 결과를 적습니다. AI에게 작은 기능을 요청하고, 실제로 실행한 뒤 수정합니다. 요청문과 답변 예시는 수업용으로 재작성했습니다.

## 이미지와 실행 환경

원본 화면에는 출처 쪽수를 표시했습니다. 수정 그래프는 코드를 실행해 새로 제작했습니다. 수업 도구 전용 기능과 독립 Python 예제를 구분하여 사용합니다.
:::

:::page{type="chapter-opening" id="ch01-opening" chapter="1"}
# AI와 함께하는 디지털 시대

## 1차시 · 원본 교재 예시로 배우기

### 학습 목표

- 생성형 AI의 역할과 한계를 설명할 수 있다.
- 사실 확인이 필요한 답변을 구분할 수 있다.
- AI에게 맡길 일과 내가 검증할 일을 정할 수 있다.

### 오늘의 시작

책은 AI가 잘하는 일과 어려워하는 일을 비교하는 활동으로 시작합니다. 바이브 코딩에서도 AI가 코드를 만들고, 사람은 목적과 동작을 확인합니다.
:::

:::page{type="concept" id="ch01-ai" layout="basic"}
# 생성형 AI와 바이브 코딩

## 생성형 AI란?

생성형 AI는 요청에 따라 글, 이미지, 코드 같은 결과물을 만듭니다. 추천 영상이나 번역 등 일상 속 AI와 연결해 생각해봅시다.

## 코드를 만드는 과정

바이브 코딩에서는 원하는 앱을 말로 설명하고 AI가 제안한 코드를 실행합니다. 결과를 직접 확인하고 수정 요청을 반복합니다. 이 표현과 개발 과정 설명은 16차시 수업을 위해 덧붙였습니다.
:::

:::page{type="comparison" id="ch01-limits"}
# AI가 잘하는 일과 확인할 일

입력과 처리 결과를 나란히 비교해봅시다.

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

## 책임 있는 사용

실제 개인정보 대신 가상 데이터를 사용합니다. 다른 사람의 자료를 사용할 때 출처와 이용 조건을 확인합니다. 생성 결과의 오류와 편향을 검토하고, 제출물에서 AI 도움을 받은 부분을 밝힙니다.
:::

:::page{type="practice-opening" id="ch01-practice-1" practice="001-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# AI의 답변 비교하기

일반 지식 질문과 확인이 필요한 최신 정보 질문을 각각 작성해봅시다. 답변의 구체성, 근거, 확인할 점을 비교합니다.

> [!TIP]
> 모르는 사실을 AI 답변만으로 확정하지 않습니다.
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
# 오늘의 완료 확인

- [ ] 두 질문의 차이를 설명할 수 있다.
- [ ] 확인한 근거와 아직 모르는 점을 구분했다.
- [ ] 실제 개인정보를 입력하지 않았다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch01-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

AI가 만든 코드에서도 설명을 믿기 전에 무엇을 확인해야 할까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch02-opening" chapter="2"}
# 좋은 질문이 좋은 답을 만든다

## 2차시 · 원본 교재 예시로 배우기

### 학습 목표

- 프롬프트의 의미를 설명할 수 있다.
- 목적, 대상, 상황, 조건을 담아 요청할 수 있다.
- 앱의 목적에 맞는 입력 데이터를 정할 수 있다.

### 오늘의 시작

같은 AI라도 요청에 담긴 조건에 따라 결과가 달라집니다. 책의 공부 계획과 여행 질문을 앱 제작 요청으로 연결합니다.
:::

:::page{type="concept" id="ch02-prompt" layout="basic"}
# 프롬프트의 구성

## 프롬프트란?

프롬프트는 AI에게 전달하는 질문, 요청, 지시문입니다. 무엇을 만들지, 누구를 위한 것인지, 어떤 조건을 지켜야 하는지 적습니다.

## 책의 공부 계획 예시

공부 계획 알려줘보다 시험이 2주 남았고 하루 2시간 공부할 수 있다는 상황을 함께 알려주면 요청의 범위가 분명해집니다.
:::

:::page{type="comparison" id="ch02-compare"}
# 모호한 요청을 구체적으로 바꾸기

입력과 처리 결과를 나란히 비교해봅시다.

| 모호한 요청 | 구체적인 요청 |
|---|---|
| 추천해줘 | 시험까지 2주, 하루 2시간의 공부 계획을 추천해줘. |
| 여행 추천해줘 | 2박 3일 부산 여행을 실내 활동 위주로 정리해줘. |
| 건강 관리 알려줘 | 대학생이 실천할 수 있는 생활 습관을 알려줘. |
:::

:::page{type="concept" id="ch02-inputs" layout="basic"}
# 앱에 필요한 입력 데이터

## BMI 계산 앱

책의 입력 예시는 키와 몸무게입니다. 결과에 필요한 정보만 받습니다. BMI 계산은 데이터 처리 연습이며 개인의 건강을 진단하는 기능으로 취급하지 않습니다.

## 병원 접수 앱

책은 이름, 증상, 체온을 입력 예시로 듭니다. 수업에서는 가상 이름과 예시 값을 사용하고, 실제 접수나 응급 판단 기능으로 사용하지 않습니다.
:::

:::page{type="practice-opening" id="ch02-practice-1" practice="002-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 같은 주제로 질문 다듬기

책의 공부 계획 질문을 짧은 요청과 구체적인 요청으로 각각 작성합니다. 조건이 답변에 반영되었는지 확인합니다.

> [!TIP]
> 답변이 길어졌다는 이유만으로 더 좋은 답이라고 판단하지 않습니다.
:::

:::page{type="practice-opening" id="ch02-practice-2" practice="002-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 앱 입력 데이터 설계하기

BMI 계산 앱 또는 책에 나온 감정 기록 앱 하나를 골라 목적과 입력 데이터를 적습니다. 입력이 바뀌면 어떤 결과가 달라지는지 설명합니다.

> [!TIP]
> 앱에 필요하지 않은 개인정보는 입력 항목에서 뺍니다.
:::

:::page{type="concept" id="ch02-request" layout="basic"}
# 앱 제작 요청으로 바꿔보기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
키와 몸무게를 입력받는 계산 연습 앱을 설계해줘. 입력 항목과 처리 과정, 출력 항목을 먼저 설명해줘. 빈 입력과 0 이하의 값은 계산하지 않도록 해줘. 건강 진단 문구는 넣지 말아줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="practice-checklist" id="ch02-check"}
# 오늘의 완료 확인

- [ ] 목적과 조건을 구분해 적었다.
- [ ] 입력 항목이 결과와 연결된다.
- [ ] 수정 요청 전후의 차이를 설명했다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch02-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

조건을 너무 많이 한꺼번에 요청하면 무엇을 먼저 확인해야 할까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch03-opening" chapter="3"}
# 문제를 단계별로 나누기

## 3차시 · 원본 교재 예시로 배우기

### 학습 목표

- 알고리즘의 의미를 설명할 수 있다.
- 입력, 처리, 출력을 구분할 수 있다.
- 아이디어를 작은 실행 단계로 나눌 수 있다.

### 오늘의 시작

AI의 아이디어를 실제 앱으로 만들려면 사람이 동작 구조를 정해야 합니다. 책의 라면 끓이기와 감정 기록 예시를 사용합니다.
:::

:::page{type="comparison" id="ch03-ramen"}
# 라면 끓이기로 보는 입력·처리·출력

입력과 처리 결과를 나란히 비교해봅시다.

| 단계 | 책의 예시 |
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

:::page{type="practice-opening" id="ch03-practice-1" practice="003-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 감정 기록 앱의 구조 정하기

책의 감정 기록 앱을 입력, 처리, 출력으로 나누어봅시다. 감정 분류 규칙은 학생이 정한 선택 항목으로 제한하고 심리 진단으로 해석하지 않습니다.

> [!TIP]
> 입력할 내용과 결과 화면을 먼저 정합니다.
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

:::page{type="concept" id="ch03-request" layout="basic"}
# 구조부터 설명해 달라고 요청하기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
오늘의 기분을 선택해서 기록하는 연습 앱을 만들려고 해. 입력, 처리, 출력을 나누어 설명해줘. 아직 코드는 만들지 말고 버튼을 눌렀을 때 바뀌는 화면을 먼저 적어줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="practice-checklist" id="ch03-check"}
# 오늘의 완료 확인

- [ ] 입력, 처리, 출력이 각각 구분되어 있다.
- [ ] 버튼을 눌렀을 때의 변화를 설명했다.
- [ ] 실행 순서에 빠진 단계가 없는지 확인했다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch03-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

처리 단계에 단순히 AI가 알아서 한다고 쓰면 어떤 문제가 생길까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch04-opening" chapter="4"}
# 순서도와 데이터 이해

## 4차시 · 원본 교재 예시로 배우기

### 학습 목표

- 선언, 입력, 처리, 출력의 역할을 구분할 수 있다.
- 문자열과 숫자를 구분할 수 있다.
- 가족 나이와 학생 점수의 합을 구할 수 있다.

### 오늘의 시작

책의 가족 나이 43, 45, 15를 더해봅시다. 그림으로 표현한 동작을 짧은 코드와 연결합니다.
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

입력과 처리 결과를 나란히 비교해봅시다.

| 종류 | 예시 | 사용 방법 |
|---|---|---|
| 문자열 | 이름, 학과, 증상 설명 | 글자로 보관하거나 표시 |
| 정수 | 나이, 점수 | 변환 후 덧셈·비교 |
| 실수 | 키, 체온 | 소수 값을 변환해 계산 |
:::

:::page{type="concept" id="ch04-variables" layout="basic"}
# 변수 이름과 값 맞추기

## 예시 확인하기

원본 21쪽의 scores와 score 불일치를 score로 통일했습니다.

```python
name = "민수"
score = 80
print(name)
print(score)
```

```output
민수
80
```
:::

:::page{type="practice-opening" id="ch04-practice-1" practice="004-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 우리 가족 나이 합 구하기

가상의 가족 나이를 엄마 43살, 아빠 45살, 나 15살로 정하고 합을 구해봅시다. 결과가 103인지 확인합니다.

> [!TIP]
> 원본 문제의 점수라는 표현은 나이로 바로잡았습니다.
:::

:::page{type="concept" id="ch04-family-code" layout="basic"}
# 가족 나이를 더하는 코드

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
momage = 43
dadage = 45
myage = 15
total = momage + dadage + myage
print(f"우리 가족 나이의 총합은 {total}입니다.")
```

```output
우리 가족 나이의 총합은 103입니다.
```
:::

:::page{type="flowchart" id="ch04-family-flow" height="1050"}
# 가족 나이 합의 순서도

값 준비, 입력, 처리, 출력이 서로 다른 역할임을 확인합니다.

```flowchart
control_structure: linear
nodes:
  - id: declare
    role: declaration
    text: momage, dadage, myage, total 준비
  - id: input
    role: input
    text: 43, 45, 15 입력
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

입력 나이가 달라지면 처리 식은 유지되고 총합이 달라집니다.
:::

:::page{type="practice-opening" id="ch04-practice-2" practice="004-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 학생 세 명의 총점 구하기

책의 학생 세 명 점수 합 예시를 사용합니다. 연습 점수는 80, 90, 70으로 정하고 총점 240을 확인합니다. 평균을 구하는 과제와 구분합니다.

> [!TIP]
> 화면의 입력값이 문자열이라면 먼저 숫자로 바꾸어 계산합니다.
:::

:::page{type="concept" id="ch04-scores-code" layout="basic"}
# 문자열 입력을 정수로 바꾸기

## 예시 확인하기

input은 입력 문자열을 반환합니다. 이 예제는 동일한 입력을 재현하기 위해 입력 문자열을 코드에 직접 적었습니다.

```python
s1 = int("80")
s2 = int("90")
s3 = int("70")
print(s1 + s2 + s3)
```

```output
240
```
:::

:::page{type="practice-checklist" id="ch04-check"}
# 오늘의 완료 확인

- [ ] 가족 나이 총합 103을 확인했다.
- [ ] 학생 총점과 평균을 구분한다.
- [ ] 변수 이름이 설명과 코드에서 일치한다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch04-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

문자열 80과 문자열 90을 그대로 붙이면 숫자 덧셈과 어떻게 달라질까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch05-opening" chapter="5"}
# 반복과 누적 이해

## 5차시 · 원본 교재 예시로 배우기

### 학습 목표

- 횟수 반복과 조건 반복을 구분할 수 있다.
- 반복마다 합계를 갱신할 수 있다.
- 10일 운동 시간의 합을 검증할 수 있다.

### 오늘의 시작

책에서는 1일차에 1분, 2일차에 2분, 10일차에 10분 운동합니다. 반복으로 총 운동 시간을 계산해봅시다.
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

입력과 처리 결과를 나란히 비교해봅시다.

| 날짜 | 더할 시간 | 그날까지 합계 |
|---|---|---|
| 1일차 | 1분 | 1분 |
| 2일차 | 2분 | 3분 |
| 3일차 | 3분 | 6분 |
| 9일차 | 9분 | 45분 |
| 10일차 | 10분 | 55분 |
:::

:::page{type="practice-opening" id="ch05-practice-1" practice="005-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 10일 운동 시간 구하기

1부터 10까지의 시간을 더해 총 55분을 출력해봅시다. 합계와 반복 횟수를 각각 확인합니다.

> [!TIP]
> 마지막 10일차가 실제로 포함되는지 확인합니다.
:::

:::page{type="concept" id="ch05-exercise-code" layout="basic"}
# while로 운동 시간 누적하기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
time1 = 1
total = 0
while time1 <= 10:
    total = total + time1
    time1 += 1
print(f"총 운동 시간은 {total}분입니다.")
```

```output
총 운동 시간은 55분입니다.
```
:::

:::page{type="flowchart" id="ch05-exercise-flow" height="1050"}
# 운동 시간 누적 순서도

책의 31쪽 누적 구조를 마지막 날짜까지 따라가봅시다.

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

:::page{type="practice-opening" id="ch05-practice-2" practice="005-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 하루 카페인 양 누적하기

책의 카페인 누적 예시를 하루 기록으로 통일합니다. 계산 연습용 입력 50mg, 30mg, 0mg의 합이 80mg인지 확인합니다. 건강 권고량은 판단하지 않습니다.

> [!TIP]
> 입력 기간이 하루인지 일주일인지 먼저 정합니다.
:::

:::page{type="concept" id="ch05-caffeine-code" layout="basic"}
# 여러 기록을 하나씩 더하기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
caffeine = [50, 30, 0]
total = 0
for amount in caffeine:
    total += amount
print(f"총 카페인 양 {total}mg")
```

```output
총 카페인 양 80mg
```
:::

:::page{type="practice-checklist" id="ch05-check"}
# 오늘의 완료 확인

- [ ] 10일까지 포함해 55분을 구했다.
- [ ] 합계를 반복 안에서 0으로 만들지 않았다.
- [ ] 반복 종료 조건과 입력 기간을 설명했다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch05-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

time1을 증가시키지 않으면 반복은 어떻게 될까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch06-opening" chapter="6"}
# 조건에 따라 결과 나누기

## 6차시 · 원본 교재 예시로 배우기

### 학습 목표

- if, elif, else의 역할을 설명할 수 있다.
- 조건을 검사하는 순서를 정할 수 있다.
- 경계값을 넣어 결과를 확인할 수 있다.

### 오늘의 시작

책의 비 오는 날 우산 예시와 수면 시간 분류로 조건문을 이해합니다. 수면 문구는 책의 분류 규칙을 연습하는 예시이며 건강 판정은 아닙니다.
:::

:::page{type="concept" id="ch06-conditions" layout="basic"}
# 조건문 읽는 방법

## if와 else

if는 조건이 참일 때 실행할 내용을 정합니다. else는 앞의 조건에 해당하지 않을 때 실행할 내용을 정합니다.

## elif와 순서

elif는 앞 조건이 거짓일 때 다음 조건을 검사합니다. 한 번 참인 분기를 선택하면 이어지는 elif와 else는 실행하지 않습니다.
:::

:::page{type="comparison" id="ch06-sleep-rules"}
# 책의 수면 시간 분류 규칙

책 36쪽의 분기 규칙을 그대로 연습합니다. 실제 건강 기준으로 일반화하지 않습니다.

| 수면 시간 | 학습용 출력 |
|---|---|
| 8시간 이상 | 충분한 수면입니다 |
| 5시간 이상, 8시간 미만 | 적정 수면입니다 |
| 5시간 미만 | 수면 부족입니다 |
:::

:::page{type="practice-opening" id="ch06-practice-1" practice="006-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 수면 시간 분류하기

8시간 이상인지 먼저 확인하고, 그렇지 않으면 5시간 이상인지 확인하는 분류를 만듭니다. 4.9, 5, 7.9, 8을 넣어 분기를 확인합니다.

> [!TIP]
> 큰 기준부터 검사하면 겹치는 조건을 정리하기 쉽습니다.
:::

:::page{type="concept" id="ch06-sleep-code" layout="basic"}
# 수면 시간의 세 가지 분기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
hours = 7
if hours >= 8:
    print("충분한 수면입니다")
elif hours >= 5:
    print("적정 수면입니다")
else:
    print("수면 부족입니다")
```

```output
적정 수면입니다
```
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
# 분기 순서 수정 요청하기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
수면 시간이 9인데 적정 수면으로 표시돼. 8시간 이상 조건을 먼저 검사하고, 5시간 이상 조건은 elif로 연결해줘. 4.9, 5, 7.9, 8, 9의 결과를 함께 확인해줘. 책의 분류 연습 문구를 유지해줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="practice-checklist" id="ch06-check"}
# 오늘의 완료 확인

- [ ] 5와 8의 경계값이 올바른 분기로 간다.
- [ ] 조건 검사 순서를 설명할 수 있다.
- [ ] 예시 문구를 실제 건강 판정으로 사용하지 않는다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch06-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

5시간 이상 조건을 가장 먼저 검사하면 8시간은 어느 분기에 들어갈까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch07-opening" chapter="7"}
# 반복과 조건 함께 사용하기

## 7차시 · 원본 교재 예시로 배우기

### 학습 목표

- 반복할 작업과 판단할 조건을 분리할 수 있다.
- 학생 수만큼 결과를 출력할 수 있다.
- 합격 기준과 관람 기준을 구분할 수 있다.

### 오늘의 시작

책에서는 여러 학생의 점수나 나이를 하나씩 확인합니다. 학생을 세는 반복과 각 학생의 조건 판단을 함께 사용합니다.
:::

:::page{type="comparison" id="ch07-roles"}
# 반복과 조건의 서로 다른 역할

입력과 처리 결과를 나란히 비교해봅시다.

| 구조 | 점수 확인 예시 |
|---|---|
| 반복 | 학생 점수를 한 명씩 확인 |
| 조건 | 기준 점수 이상인지 확인 |
| 출력 | 그 학생의 결과를 표시 |
:::

:::page{type="practice-opening" id="ch07-practice-1" practice="007-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 학생 수만큼 PASS·FAIL 확인하기

책 40쪽의 기준은 80점입니다. 연습 점수 79, 80, 100을 순서대로 처리하여 FAIL, PASS, PASS가 나오는지 확인합니다.

> [!TIP]
> 책 38쪽의 60점 예시와 이번 80점 실습 기준을 섞지 않습니다.
:::

:::page{type="concept" id="ch07-pass-code" layout="basic"}
# 80점 기준으로 세 학생 확인하기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
scores = [79, 80, 100]
for score in scores:
    if score >= 80:
        print("PASS")
    else:
        print("FAIL")
```

```output
FAIL
PASS
PASS
```
:::

:::page{type="flowchart" id="ch07-pass-flow" height="1050"}
# 점수 확인의 반복과 분기

각 학생의 결과를 출력한 뒤 학생 수를 한 번 증가시킵니다.

```flowchart
control_structure: loop
nodes:
  - id: start
    role: declaration
    text: i = 0, N = 학생 수
  - id: loop
    role: decision
    text: i < N인가?
  - id: input
    role: input
    text: 학생 점수 입력
  - id: pass
    role: decision
    text: 점수가 80 이상인가?
  - id: yes
    role: output
    text: PASS 출력
  - id: no
    role: output
    text: FAIL 출력
  - id: next
    role: process
    text: i = i + 1
  - id: end
    role: output
    text: 전체 처리 완료
connections:
  - from: start
    to: loop
  - from: loop
    to: input
    label: YES
  - from: input
    to: pass
  - from: pass
    to: yes
    label: YES
  - from: pass
    to: no
    label: NO
  - from: yes
    to: next
  - from: no
    to: next
  - from: next
    to: loop
  - from: loop
    to: end
    label: NO
```

입력 학생 수와 결과 개수가 같아야 합니다.
:::

:::page{type="practice-opening" id="ch07-practice-2" practice="007-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 네 학생의 영화 관람 가능 여부

책 39쪽의 가상 조건은 15세 이상입니다. 14, 15, 16, 13을 넣어 네 결과를 확인합니다. 이는 주어진 문제의 조건을 계산하는 연습입니다.

> [!TIP]
> 15가 관람 가능에 포함되는지 확인합니다.
:::

:::page{type="concept" id="ch07-movie-code" layout="basic"}
# 나이 조건을 반복해서 확인하기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
ages = [14, 15, 16, 13]
for age in ages:
    if age >= 15:
        print("관람 가능")
    else:
        print("관람 불가")
```

```output
관람 불가
관람 가능
관람 가능
관람 불가
```
:::

:::page{type="practice-checklist" id="ch07-check"}
# 오늘의 완료 확인

- [ ] 80점과 15세가 기준에 포함된다.
- [ ] 입력 수와 출력 수가 같다.
- [ ] 각 반복에서 현재 학생의 값을 사용한다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch07-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

여러 학생을 처리할 때 이전 학생의 값이 남아 있으면 어떤 오류가 생길까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch08-opening" chapter="8"}
# Button·Field·Text로 첫 화면 만들기

## 8차시 · 원본 교재 예시로 배우기

### 학습 목표

- GUI와 위젯의 의미를 설명할 수 있다.
- 버튼 이벤트와 입력값을 연결할 수 있다.
- 추가와 삭제 기능을 구분해 확인할 수 있다.

### 오늘의 시작

책의 바이브 프로젝트는 프로젝트 정보, 위젯 역할, 이벤트, 추가 설명을 작성한 뒤 코드를 생성합니다. 화면 구성과 버튼 동작을 따로 설계해봅시다.
:::

:::page{type="comparison" id="ch08-widgets"}
# 기본 위젯의 역할

입력과 처리 결과를 나란히 비교해봅시다.

| 위젯 | 역할 | 책의 이름 |
|---|---|---|
| Button | 눌렀을 때 기능 실행 | btn1 |
| Field | 글자나 숫자 입력 | fld1, fld2 |
| Text | 설명과 결과 표시 | txt1 |
:::

:::page{type="step-process" id="ch08-designer"}
# 책의 바이브 프로젝트 작성 순서

## 프로젝트 정보 정하기

프로젝트 이름과 설명을 적습니다.

## 위젯 역할 정하기

디자이너에서 위젯을 추가하고 이름과 역할을 확인합니다.

## 이벤트 정하기

각 버튼을 눌렀을 때 바뀔 내용을 적습니다.

## 생성 후 실행하기

코드를 생성하고 버튼을 실제로 눌러 동작을 확인합니다.
:::

:::page{type="practice-opening" id="ch08-practice-1" practice="008-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 버튼을 눌러 색 바꾸기

책 44-46쪽의 버튼 예시로 시작합니다. 버튼을 누르면 배경색이 바뀌도록 이벤트를 정합니다. 글자색을 바꿀 때도 배경 위에서 읽히는지 확인합니다.

> [!TIP]
> 버튼의 설명과 클릭 이벤트는 서로 다른 입력입니다.
:::

:::page{type="concept" id="ch08-button-before" layout="basic"}
# 버튼 클릭 전

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

클릭 전에는 밝은 배경의 Button이 보입니다.

::image{src="assets/source-20261006/button-before.png" alt="클릭 전에는 밝은 배경의 Button이 보입니다." ratio="170:84" width="half" caption="원본 PDF 46쪽의 실습 화면"}
:::

:::page{type="concept" id="ch08-button-after" layout="basic"}
# 버튼 클릭 후

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

클릭 후에는 같은 버튼의 배경이 파란색으로 바뀝니다.

::image{src="assets/source-20261006/button-after.png" alt="클릭 후에는 같은 버튼의 배경이 파란색으로 바뀝니다." ratio="183:82" width="half" caption="원본 PDF 46쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch08-practice-2" practice="008-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 입력한 내용을 다른 Field에 표시하기

fld1에 안녕을 입력합니다. 추가 버튼은 fld1의 현재 내용을 fld2에 복사하고, 삭제 버튼은 두 입력창을 모두 비우게 합니다. 이번 실습은 누적 대신 현재 값 표시로 정합니다.

> [!TIP]
> 원본의 추가라는 버튼 이름과 복사·누적 동작을 구분해 설명합니다.
:::

:::page{type="concept" id="ch08-request" layout="basic"}
# Field와 버튼 이벤트 요청하기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
입력창 fld1과 결과창 fld2, 추가 버튼 btn1과 삭제 버튼 btn2를 만들어줘. btn1은 fld1의 현재 내용을 fld2에 복사해줘. btn2는 두 입력창을 모두 비워줘. 빈 입력으로 추가하면 입력 안내를 보여줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="concept" id="ch08-field-copy" layout="basic"}
# 입력값을 복사한 화면

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

위 입력창의 안녕이 추가 버튼을 누른 뒤 아래 입력창에도 표시됩니다.

::image{src="assets/source-20261006/field-copy.png" alt="위 입력창의 안녕이 추가 버튼을 누른 뒤 아래 입력창에도 표시됩니다." ratio="497:406" width="half" caption="원본 PDF 53쪽의 실습 화면"}
:::

:::page{type="concept" id="ch08-platform" layout="basic"}
# 책의 이름과 Python API 구분하기

## 수업 도구의 이름

책의 Field는 디자이너에서 쓰는 이름입니다. Flet Python 코드에서는 TextField와 연결됩니다. btn1, fld1, txt1은 수업 도구에서 지정한 위젯 변수 이름입니다.

## 화면 갱신

값을 바꾸는 코드와 화면에 변경을 반영하는 과정이 연결되어야 합니다. 생성된 코드를 수정할 때는 수업 도구의 실행 구조와 갱신 방식을 확인합니다.
:::

:::page{type="practice-checklist" id="ch08-check"}
# 오늘의 완료 확인

- [ ] 버튼을 실제로 눌러 색 변화를 확인했다.
- [ ] 안녕을 입력해 fld2의 값을 확인했다.
- [ ] 삭제 후 두 입력창이 모두 비워진다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch08-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

버튼을 눌러도 결과가 바뀌지 않으면 위젯 이름과 이벤트 연결 중 무엇을 먼저 살펴볼까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch09-opening" chapter="9"}
# 계산·누적 출력 앱 만들기

## 9차시 · 원본 교재 예시로 배우기

### 학습 목표

- 반복 알고리즘을 GUI 이벤트로 연결할 수 있다.
- 계산 입력을 숫자로 변환할 수 있다.
- 값 교체와 내용 누적을 구분할 수 있다.

### 오늘의 시작

책의 누적곱, 두 수 계산기, Text 누적, 구구단 실습을 연결합니다. 계산은 입력한 숫자와 선택한 연산을 명확히 정해 처리합니다.
:::

:::page{type="practice-opening" id="ch09-practice-1" practice="009-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 두 정수 사이의 누적곱 구하기

시작 1, 끝 6을 입력하고 양 끝을 포함하여 곱합니다. 결과 720을 확인합니다. 버튼을 다시 누르면 이전 결과에 곱하지 않고 새 입력으로 다시 계산합니다.

> [!TIP]
> 곱셈 누적의 처음 값은 0이 아니라 1입니다.
:::

:::page{type="concept" id="ch09-product-code" layout="basic"}
# 1부터 6까지 곱하기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
start, end = 1, 6
product = 1
for number in range(start, end + 1):
    product *= number
print(product)
```

```output
720
```
:::

:::page{type="concept" id="ch09-product" layout="basic"}
# 누적곱 결과 화면

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

시작 1, 끝 6을 입력하고 누적 버튼을 누르면 결과창에 720이 보입니다.

::image{src="assets/source-20261006/product.png" alt="시작 1, 끝 6을 입력하고 누적 버튼을 누르면 결과창에 720이 보입니다." ratio="940:286" width="text" caption="원본 PDF 54쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch09-practice-2" practice="009-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 두 수와 연산 기호로 계산하기

책 61-62쪽의 계산기 2를 만듭니다. 두 숫자와 연산 기호를 분리해서 받고, 100 나누기 5의 결과 20.0을 확인합니다.

> [!TIP]
> 원본 eval 계산기 대신 선택한 사칙연산만 처리합니다.
:::

:::page{type="concept" id="ch09-calculator-request" layout="basic"}
# 계산기 이벤트 작성하기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
입력창 두 개와 연산 선택 버튼, 계산 버튼을 만들어줘. 연산은 +, -, *, / 중 하나만 선택하게 해줘. 숫자로 변환한 두 값에 해당 연산만 적용해줘. eval은 사용하지 말고, 빈 입력·문자·0으로 나누기는 안내해줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="concept" id="ch09-calculator" layout="basic"}
# 두 수 계산기 결과

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

100과 5, 나누기 기호가 표시되고 결과창에는 20.0이 보입니다.

::image{src="assets/source-20261006/calculator.png" alt="100과 5, 나누기 기호가 표시되고 결과창에는 20.0이 보입니다." ratio="452:215" width="half" caption="원본 PDF 61쪽의 실습 화면"}
:::

:::page{type="concept" id="ch09-calculator-code" layout="basic"}
# 선택한 연산만 계산하기

## 예시 확인하기

수식 문자열을 실행하지 않고 책의 계산기 2를 직접 연산하는 방식으로 정리했습니다.

```python
a, b = 100.0, 5.0
op = "/"
if op == "+":
    result = a + b
elif op == "-":
    result = a - b
elif op == "*":
    result = a * b
elif op == "/" and b != 0:
    result = a / b
else:
    result = "계산할 수 없습니다"
print(result)
```

```output
20.0
```
:::

:::page{type="practice-opening" id="ch09-practice-3" practice="009-3" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# Text에 내용 누적하기

책 63-64쪽의 Text 예시처럼 두 문장을 차례로 추가합니다. 이전 문장을 유지하고 새 문장은 다음 줄에 표시합니다.

> [!TIP]
> 값을 덮어쓰는 것과 문자열을 이어 붙이는 것은 다릅니다.
:::

:::page{type="concept" id="ch09-text" layout="basic"}
# Text에 두 문장을 추가한 화면

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

추가한 안녕하세요 저는 코알라입니다와 저는 12살입니다가 두 줄로 표시됩니다.

::image{src="assets/source-20261006/text-append.png" alt="추가한 안녕하세요 저는 코알라입니다와 저는 12살입니다가 두 줄로 표시됩니다." ratio="393:234" width="half" caption="원본 PDF 63쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch09-practice-4" practice="009-4" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 원하는 단 구구단 출력하기

책의 구구단 예시에서 4를 입력합니다. 4 × 1부터 4 × 9까지 아홉 줄을 확인하고, 다음 단을 입력하면 새 결과로 교체합니다.

> [!TIP]
> 반복 범위에 9가 포함되는지 확인합니다.
:::

:::page{type="concept" id="ch09-times-code" layout="basic"}
# 4단의 아홉 줄 출력하기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
dan = 4
for n in range(1, 10):
    print(f"{dan} x {n} = {dan * n}")
```

```output
4 x 1 = 4
4 x 2 = 8
4 x 3 = 12
4 x 4 = 16
4 x 5 = 20
4 x 6 = 24
4 x 7 = 28
4 x 8 = 32
4 x 9 = 36
```
:::

:::page{type="concept" id="ch09-times" layout="basic"}
# 책의 4단 출력 화면

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

입력값 4와 4단의 아홉 줄 결과가 함께 보입니다.

::image{src="assets/source-20261006/times-table.png" alt="입력값 4와 4단의 아홉 줄 결과가 함께 보입니다." ratio="489:257" width="half" caption="원본 PDF 65쪽의 실습 화면"}
:::

:::page{type="practice-checklist" id="ch09-check"}
# 오늘의 완료 확인

- [ ] 누적곱 720과 나눗셈 20.0을 확인했다.
- [ ] 재계산과 문장 누적의 차이를 설명했다.
- [ ] 구구단을 정확히 아홉 줄 출력했다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch09-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

결과가 0이면 누적곱의 시작값을, 결과가 계속 붙으면 초기화 시점을 어떻게 확인할까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch10-opening" chapter="10"}
# 선택 위젯과 진행 표시

## 10차시 · 원본 교재 예시로 배우기

### 학습 목표

- Dropdown, Checkbox, RadioButton의 차이를 설명할 수 있다.
- 선택한 값과 안내를 연결할 수 있다.
- 진행률의 범위를 확인할 수 있다.

### 오늘의 시작

책의 색상 선택, 건강습관 체크, 동아리 소개, 진행 막대 예시로 한 가지 선택과 여러 가지 선택을 비교합니다.
:::

:::page{type="comparison" id="ch10-choice"}
# 선택 방식 비교

입력과 처리 결과를 나란히 비교해봅시다.

| 위젯 | 선택 방식 | 책의 예시 |
|---|---|---|
| Dropdown | 목록에서 하나 | 색상 선택 |
| Checkbox | 항목별 선택·해제 | 건강습관 |
| RadioButton | 같은 그룹에서 하나 | 동아리 소개 |
| ProgressBar | 진행 정도 표시 | 0.1씩 증가·감소 |
:::

:::page{type="practice-opening" id="ch10-practice-1" practice="010-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# Dropdown 항목 추가와 선택

입력한 색상 이름을 목록에 추가하고, 목록에서 빨강을 선택해 선택값이 출력되는지 확인합니다.

> [!TIP]
> 항목 추가와 항목 선택은 별도의 이벤트로 설계합니다.
:::

:::page{type="concept" id="ch10-dropdown" layout="basic"}
# 목록의 선택값 확인하기

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

목록에서 선택한 빨강이 결과 영역에 표시됩니다.

::image{src="assets/source-20261006/dropdown.png" alt="목록에서 선택한 빨강이 결과 영역에 표시됩니다." ratio="334:304" width="half" caption="원본 PDF 68쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch10-practice-2" practice="010-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 오늘의 건강습관 체크

물 충분히 마시기, 운동하기, 아침 식사하기, 7시간 이상 자기의 네 항목을 사용합니다. 선택된 이름과 개수를 보여줍니다. 책의 체크 활동이며 건강 점수나 진단을 만들지 않습니다.

> [!TIP]
> 아무것도 선택하지 않았을 때의 안내도 확인합니다.
:::

:::page{type="concept" id="ch10-health" layout="basic"}
# 책의 건강습관 체크 화면

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

네 가지 습관을 각각 체크하고 확인 버튼을 누르는 화면입니다.

::image{src="assets/source-20261006/health-check.png" alt="네 가지 습관을 각각 체크하고 확인 버튼을 누르는 화면입니다." ratio="235:323" width="half" caption="원본 PDF 73쪽의 실습 화면"}
:::

:::page{type="concept" id="ch10-health-request" layout="basic"}
# 체크된 항목만 출력하기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
Checkbox 네 개와 확인 버튼, 결과 Text를 만들어줘. 체크된 습관 이름과 선택 개수를 보여줘. 선택이 없으면 선택한 항목이 없습니다로 안내해줘. 확인을 반복해도 결과가 중복되지 않게 해줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="practice-opening" id="ch10-practice-3" practice="010-3" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 선택한 동아리 소개

책의 코딩, 방송, 미술, 과학 동아리를 같은 Radio 그룹에 넣습니다. 과학을 선택하면 과학 실험과 탐구 활동 소개가 표시되는지 확인합니다.

> [!TIP]
> 같은 그룹에서 동시에 한 항목만 선택되는지 확인합니다.
:::

:::page{type="concept" id="ch10-club" layout="basic"}
# 한 동아리만 선택한 화면

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

과학 동아리가 선택되고 과학 실험과 탐구 활동 소개가 표시됩니다.

::image{src="assets/source-20261006/club-radio.png" alt="과학 동아리가 선택되고 과학 실험과 탐구 활동 소개가 표시됩니다." ratio="384:240" width="half" caption="원본 PDF 78쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch10-practice-4" practice="010-4" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 진행률 증가·감소

ProgressBar를 0에서 시작합니다. 증가와 감소 버튼으로 0.1씩 바꾸고 결과를 0부터 1 사이로 제한합니다.

> [!TIP]
> 1은 100퍼센트이며 10은 진행률의 정상 범위가 아닙니다.
:::

:::page{type="concept" id="ch10-progress" layout="basic"}
# 진행 막대와 두 버튼

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

진행 막대 아래에 증가와 감소 버튼이 있습니다. 원본 화면은 중간 진행 상태를 보여줍니다.

::image{src="assets/source-20261006/progress.png" alt="진행 막대 아래에 증가와 감소 버튼이 있습니다. 원본 화면은 중간 진행 상태를 보여줍니다." ratio="292:125" width="half" caption="원본 PDF 82쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch10-practice-5" practice="010-5" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# Image와 Divider로 화면 구성

책처럼 이미지 두 개 사이에 구분선을 넣습니다. 수업용으로 허용된 이미지와 주소를 사용하고, 주소가 없거나 불러오지 못했을 때도 확인합니다.

> [!TIP]
> 원본 사진을 복원해 새 사진처럼 소개하지 않습니다.
:::

:::page{type="concept" id="ch10-images" layout="basic"}
# 두 이미지와 구분선

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

두 이미지 사이에 얇은 구분선이 있어 화면 영역이 나뉩니다.

::image{src="assets/source-20261006/image-divider.png" alt="두 이미지 사이에 얇은 구분선이 있어 화면 영역이 나뉩니다." ratio="266:232" width="half" caption="원본 PDF 85쪽의 실습 화면"}
:::

:::page{type="practice-checklist" id="ch10-check"}
# 오늘의 완료 확인

- [ ] 여러 선택과 한 가지 선택이 구분된다.
- [ ] 선택 없음도 결과에 반영된다.
- [ ] 진행률이 0부터 1을 벗어나지 않는다.
- [ ] 이미지 주소와 이용 조건을 확인했다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch10-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

Checkbox를 RadioButton으로 바꾸면 건강습관 체크의 동작이 어떻게 달라질까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch11-opening" chapter="11"}
# 학생 성적을 표로 정리하기

## 11차시 · 원본 교재 예시로 배우기

### 학습 목표

- 표의 행, 열, 셀을 구분할 수 있다.
- 입력 순서와 표 열 순서를 맞출 수 있다.
- 화면 번호와 리스트 인덱스를 연결할 수 있다.

### 오늘의 시작

책의 학생 성적 Table 실습을 사용합니다. 설명과 캡처의 과목 순서가 달라, 이번 원고는 캡처처럼 이름·국어·수학·영어 순서로 통일합니다.
:::

:::page{type="concept" id="ch11-table" layout="basic"}
# DataTable의 구조

## 행과 열

열은 이름, 국어, 수학, 영어처럼 같은 종류의 항목입니다. 행은 학생 한 명의 기록입니다. 셀은 행과 열이 만나는 한 칸입니다.

## Flet 코드와 연결

DataColumn은 열 제목, DataRow는 한 행, DataCell은 한 칸을 구성합니다. 화면에서 보이는 열 이름과 실제 값을 넣는 순서를 맞춥니다.
:::

:::page{type="practice-opening" id="ch11-practice-1" practice="011-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 성적 입력을 표에 추가하기

fld1은 이름, fld2는 국어, fld3는 수학, fld4는 영어로 정합니다. 학생1의 100, 90, 80을 넣고 표의 해당 열에 기록되는지 확인합니다.

> [!TIP]
> 행이 하나 늘어나는 것과 기존 셀이 바뀌는 것은 다릅니다.
:::

:::page{type="concept" id="ch11-table-screen" layout="basic"}
# 책의 학생 성적 Table

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

표 열은 이름, 국어, 수학, 영어입니다. 학생1은 100, 90, 80으로 표시됩니다.

::image{src="assets/source-20261006/student-table.png" alt="표 열은 이름, 국어, 수학, 영어입니다. 학생1은 100, 90, 80으로 표시됩니다." ratio="744:381" width="text" caption="원본 PDF 90쪽의 실습 화면"}
:::

:::page{type="comparison" id="ch11-field-map"}
# 입력창과 표 열 대조

입력과 처리 결과를 나란히 비교해봅시다.

| 입력창 | 표 열 | 연습 입력 |
|---|---|---|
| fld1 | 이름 | 학생1 |
| fld2 | 국어 | 100 |
| fld3 | 수학 | 90 |
| fld4 | 영어 | 80 |
:::

:::page{type="concept" id="ch11-request" layout="basic"}
# 열 순서를 분명히 요청하기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
이름·국어·수학·영어 입력창과 같은 순서의 Table을 만들어줘. 추가 버튼을 누르면 한 학생의 행을 추가해줘. 점수는 0부터 100까지의 정수만 받아줘. 빈 이름이나 잘못된 점수는 행을 추가하지 말아줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="concept" id="ch11-index" layout="basic"}
# 왜 위치 번호에서 1을 뺄까?

## 화면의 번호

사용자는 첫 번째 행을 1행이라고 부릅니다. Python 리스트의 첫 위치는 0입니다. 따라서 화면의 2행은 리스트 위치 1과 대응합니다.

## 확인할 범위

번호를 숫자로 바꾼 뒤 실제 행과 열 범위에 있는지 확인합니다. 번호 0을 허용하면 1을 뺐을 때 -1이 되어 마지막 위치를 가리킬 수 있습니다.
:::

:::page{type="concept" id="ch11-index-code" layout="basic"}
# 두 번째 학생의 수학 점수 찾기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
rows = [["학생1", 100, 90, 80],
        ["학생2", 97, 88, 90]]
row_no, column_no = 2, 3
print(rows[row_no - 1][column_no - 1])
```

```output
88
```
:::

:::page{type="practice-opening" id="ch11-practice-2" practice="011-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 기존 셀의 값 바꾸기

2행 3열의 수학 점수를 88에서 89로 바꿔봅시다. 이름과 다른 과목 값이 그대로인지 확인합니다.

> [!TIP]
> 새 행 추가와 셀 수정에 같은 버튼 동작을 혼합하지 않습니다.
:::

:::page{type="practice-checklist" id="ch11-check"}
# 오늘의 완료 확인

- [ ] 입력 순서와 표 열 순서가 같다.
- [ ] 추가 후 행 수가 하나 늘었다.
- [ ] 2행 3열만 바뀌었다.
- [ ] 0행과 범위를 벗어난 번호를 거부한다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch11-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

국어와 수학 점수가 서로 바뀌었다면 표 제목과 값 목록 중 무엇을 함께 대조해야 할까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch12-opening" chapter="12"}
# 입력 데이터를 차트와 저장으로 연결

## 12차시 · 원본 교재 예시로 배우기

### 학습 목표

- 선 그래프, 막대그래프, 산점도를 구분할 수 있다.
- 표와 차트가 같은 데이터를 쓰는지 확인할 수 있다.
- 프로젝트 저장과 데이터 보관을 구분할 수 있다.

### 오늘의 시작

책의 다섯 값 선 그래프, 키·몸무게 산점도, 입력값 막대그래프를 사용합니다. 저장된 자료를 다시 열어 같은 값이 남아 있는지도 확인합니다.
:::

:::page{type="comparison" id="ch12-charts"}
# 표현 목적에 맞는 그래프

입력과 처리 결과를 나란히 비교해봅시다.

| 그래프 | 표현할 내용 | 축 확인 |
|---|---|---|
| 선 그래프 | 순서에 따른 값 변화 | 입력 순서와 수치 |
| 막대그래프 | 항목별 값 크기 | 항목과 수치 |
| 산점도 | 두 수치의 짝 | X의 값과 Y의 값 |
:::

:::page{type="practice-opening" id="ch12-practice-1" practice="012-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 다섯 입력값을 선으로 표현

책의 실행 화면처럼 1, 2, 5, 4, 5를 입력해 선 그래프를 만듭니다. 원본의 가로 위치는 0부터 4이며 입력 순서를 의미합니다.

> [!TIP]
> 가로 위치와 입력값을 혼동하지 않습니다.
:::

:::page{type="concept" id="ch12-line-screen" layout="basic"}
# 책의 선 그래프 화면

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

다섯 입력값 1, 2, 5, 4, 5와 가로 위치 0부터 4의 선 그래프가 보입니다.

::image{src="assets/source-20261006/line-chart.png" alt="다섯 입력값 1, 2, 5, 4, 5와 가로 위치 0부터 4의 선 그래프가 보입니다." ratio="856:467" width="text" caption="원본 PDF 99쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch12-practice-2" practice="012-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 키와 몸무게의 짝 누적하기

키를 X축, 몸무게를 Y축으로 정합니다. 책의 화면에 보이는 170·75, 180·82, 185·89 세 쌍을 순서대로 입력합니다. 단위는 수업에서 cm와 kg로 명시합니다.

> [!TIP]
> 값을 따로 정렬하면 원래의 키·몸무게 짝이 깨집니다.
:::

:::page{type="concept" id="ch12-scatter-screen" layout="basic"}
# 책의 키·몸무게 산점도

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

현재 입력 185와 89, 이전 입력을 포함한 세 점이 표시됩니다.

::image{src="assets/source-20261006/scatter-chart.png" alt="현재 입력 185와 89, 이전 입력을 포함한 세 점이 표시됩니다." ratio="904:464" width="text" caption="원본 PDF 102쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch12-practice-3" practice="012-3" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 막대그래프 누적과 초기화

책의 90, 80, 70 세 입력값을 누적해 세 막대를 만듭니다. 새로 그리기와 누적하기 중 어떤 동작인지 먼저 정하고 초기화도 확인합니다.

> [!TIP]
> 표와 그래프의 개수 및 값이 같아야 합니다.
:::

:::page{type="concept" id="ch12-bar-screen" layout="basic"}
# 책의 입력값 막대그래프

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

90, 80, 70의 세 막대가 입력 순서대로 보입니다.

::image{src="assets/source-20261006/bar-chart.png" alt="90, 80, 70의 세 막대가 입력 순서대로 보입니다." ratio="480:545" width="half" caption="원본 PDF 105쪽의 실습 화면"}
:::

:::page{type="concept" id="ch12-loaded-data" layout="basic"}
# 자료를 불러올 때 확인할 것

## 표와 차트의 연결

책은 학생 100명의 키·몸무게 자료를 불러와 표와 산점도로 표현합니다. 실제 수업 자료가 제공되는지 확인하고, 사용한 열과 데이터 개수를 기록합니다.

## 공공데이터 API 확장

책의 자치구별 지하철역 예시는 선택 확장입니다. 응답의 열 이름, 집계 기준, 갱신 날짜를 먼저 확인합니다. 자료와 인증 환경이 준비되지 않은 경우 필수 실습으로 두지 않습니다. 인증키는 화면과 제출물에 넣지 않습니다.
:::

:::page{type="practice-opening" id="ch12-practice-4" practice="012-4" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 프로젝트와 데이터 저장 확인

책의 표 저장 설정을 확인한 뒤 입력값 몇 개를 추가하고 프로젝트를 저장합니다. 불러오기에서 같은 프로젝트를 실행해 표와 차트가 유지되는지 비교합니다.

> [!TIP]
> 실행 중 기록, 프로젝트 코드 저장, 표 데이터 저장을 각각 확인합니다.
:::

:::page{type="step-process" id="ch12-save-process"}
# 저장·불러오기 확인 순서

## 표 구성과 저장 옵션 확인

먼저 행·열 구성을 정하고 책의 표 저장 옵션을 확인합니다. 원본 화면에서는 저장 설정 후 행·열 변경이 제한된다고 안내합니다.

## 데이터 추가 후 프로젝트 저장

추가한 행 수와 값 목록을 적고 프로젝트 이름을 정해 저장합니다.

## 불러온 뒤 비교

다시 실행하여 표 값과 차트 점을 비교합니다. 수업 도구의 실제 저장 동작을 확인한 뒤 완료를 판단합니다.
:::

:::page{type="concept" id="ch12-saved" layout="basic"}
# 다시 불러온 책의 프로젝트

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

불러온 프로젝트에 표와 산점도 기록이 함께 표시됩니다. 화면은 저장 동작을 설명하는 원본 예시입니다.

::image{src="assets/source-20261006/saved-project.png" alt="불러온 프로젝트에 표와 산점도 기록이 함께 표시됩니다. 화면은 저장 동작을 설명하는 원본 예시입니다." ratio="744:1282" width="half" caption="원본 PDF 127쪽의 실습 화면"}
:::

:::page{type="practice-checklist" id="ch12-check"}
# 오늘의 완료 확인

- [ ] 세 그래프의 목적과 축을 설명했다.
- [ ] 표와 차트의 입력 개수와 값이 같다.
- [ ] 다시 불러온 기록을 직접 비교했다.
- [ ] 인증키가 캡처에 포함되지 않았다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch12-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

점이 하나만 남는 경우 누적 목록과 그리기 시점 중 무엇을 확인할까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch13-opening" chapter="13"}
# Matplotlib 그래프 만들기

## 13차시 · 원본 교재 예시로 배우기

### 학습 목표

- Figure와 Axes의 역할을 구분할 수 있다.
- 그래프 제목과 축을 함수로 설정할 수 있다.
- 같은 데이터로 결과 이미지와 코드를 대조할 수 있다.

### 오늘의 시작

원본의 배열, 범위, 마커, 나란한 막대, 산점도 예시를 짧은 실행 코드로 정리합니다. 원본 이미지가 코드와 다른 경우 새 실행 결과로 교체합니다.
:::

:::page{type="concept" id="ch13-axes" layout="basic"}
# 그릴 판과 그리는 영역

## Figure와 Axes

plt.subplots는 Figure와 Axes를 함께 만듭니다. Figure는 전체 그림이고 Axes는 실제 데이터를 그리는 영역입니다. 먼저 생성한 뒤 ax.plot처럼 사용합니다.

## Python 예제와 수업 GUI

이 차시 코드는 독립 Python 예제입니다. 책의 fch.MatplotlibChart는 수업 GUI에 그림을 연결하는 부분이며, 단독 예제에 정의 없이 복사하지 않습니다. 생성한 Figure를 GUI에 연결할 때는 해당 수업 도구의 환경을 확인합니다.
:::

:::page{type="practice-opening" id="ch13-practice-1" practice="013-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 한 배열과 두 배열의 차이

한 배열 [1, 2, 3, 4, 5]을 그린 경우와 X·Y 두 배열을 그린 경우를 비교합니다. X축이 자동 위치인지 직접 지정한 값인지 설명합니다.

> [!TIP]
> 배열 한 개를 전달하면 기본 X 위치는 0부터 시작합니다.
:::

:::page{type="concept" id="ch13-one-array" layout="basic"}
# 한 배열을 선으로 표현하기

## 예시 확인하기

원본 131-132쪽의 데이터입니다. 생성과 축 설명을 보완한 코드를 실행한 새 그림입니다.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([1, 2, 3, 4, 5])
ax.set_xlabel("index")
ax.set_ylabel("value")
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-one.png" alt="한 배열을 선으로 표현하기의 코드 실행 결과" ratio="8:5" width="text" role="result" caption="수정 코드를 실제 실행한 결과"}
:::

:::page{type="concept" id="ch13-two-arrays" layout="basic"}
# X와 Y를 직접 지정하기

## 예시 확인하기

원본 133쪽의 두 배열을 그대로 사용했습니다.

```python
import matplotlib.pyplot as plt

x = [15, 25, 35, 45, 55]
y = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-two.png" alt="X와 Y를 직접 지정하기의 코드 실행 결과" ratio="8:5" width="text" role="result" caption="수정 코드를 실제 실행한 결과"}
:::

:::page{type="practice-opening" id="ch13-practice-2" practice="013-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 범위·마커·설명 변경하기

X 1부터 5, Y 5부터 25의 다섯 점을 사용합니다. X 범위 0부터 10, Y 범위 0부터 25를 정하고 파란 선과 더하기 마커로 그려봅시다.

> [!TIP]
> ro는 빨간 점, r-o는 빨간 선과 원형 점입니다.
:::

:::page{type="concept" id="ch13-range" layout="basic"}
# 범위를 지정한 파란 선

## 예시 확인하기

원본 134쪽의 값·모양·범위를 유지하고 Axes 생성을 추가했습니다.

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [5, 10, 15, 20, 25]
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, y, "b-+", clip_on=False)
ax.axis([0, 10, 0, 25])
ax.set_xlabel("x")
ax.set_ylabel("y")
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-range.png" alt="범위를 지정한 파란 선의 코드 실행 결과" ratio="8:5" width="text" role="result" caption="수정 코드를 실제 실행한 결과"}
:::

:::page{type="concept" id="ch13-markers" layout="basic"}
# 빨간 점과 그래프 설명

## 예시 확인하기

원본 136·138쪽의 ro 코드는 선 없이 점만 표시합니다. 같은 코드의 실제 그림으로 교체했습니다.

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

::image{src="assets/source-20261006/plot-markers.png" alt="빨간 점과 그래프 설명의 코드 실행 결과" ratio="8:5" width="text" role="result" caption="수정 코드를 실제 실행한 결과"}
:::

:::page{type="practice-opening" id="ch13-practice-3" practice="013-3" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 한 종류와 두 종류의 막대

책의 2의 거듭제곱 값과 A·B 자료를 사용합니다. 한 자료의 크기 비교와 같은 항목에서 두 자료 비교의 차이를 설명합니다.

> [!TIP]
> 두 막대를 같은 위치에 그리면 한 막대가 다른 막대를 가릴 수 있습니다.
:::

:::page{type="concept" id="ch13-bars" layout="basic"}
# 2의 거듭제곱을 막대로 표현

## 예시 확인하기

원본 140쪽의 값을 유지했습니다. 제곱값이라는 설명은 2의 거듭제곱으로 정리했습니다.

```python
import matplotlib.pyplot as plt

values = [1, 2, 4, 8, 16, 32, 64, 128]
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(range(len(values)), values)
ax.set_xlabel("index")
ax.set_ylabel("value")
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-bars.png" alt="2의 거듭제곱을 막대로 표현의 코드 실행 결과" ratio="8:5" width="text" role="result" caption="수정 코드를 실제 실행한 결과"}
:::

:::page{type="concept" id="ch13-grouped" layout="basic"}
# A와 B의 막대를 나란히 비교

## 예시 확인하기

원본 141-142쪽의 항목과 수치는 유지했습니다. 위치 계산을 단순화하고 실제 범례를 추가했습니다.

```python
import matplotlib.pyplot as plt

topics = ["one", "two", "three", "four", "five"]
a = [35, 80, 84, 83, 50]
b = [73, 80, 77, 40, 86]
x = list(range(len(topics)))
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar([v - 0.2 for v in x], a, 0.4, label="A")
ax.bar([v + 0.2 for v in x], b, 0.4, label="B")
ax.set_xticks(x)
ax.set_xticklabels(topics)
ax.set_ylabel("value")
ax.legend()
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-grouped.png" alt="A와 B의 막대를 나란히 비교의 코드 실행 결과" ratio="8:5" width="text" role="result" caption="수정 코드를 실제 실행한 결과"}
:::

:::page{type="practice-opening" id="ch13-practice-4" practice="013-4" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# NumPy로 산점도 자료 생성

책의 시드 20211206과 X 범위를 유지합니다. Y는 X의 1.5배에 0 이상 50 미만의 난수를 더한 예시 자료입니다. 실제 관측값으로 소개하지 않습니다.

> [!TIP]
> 시드는 난수 생성기의 상태를 정합니다. 시드 자체가 난수를 출력하는 함수는 아닙니다.
:::

:::page{type="concept" id="ch13-scatter" layout="basic"}
# 축 제목을 바로잡은 산점도

## 예시 확인하기

원본 145쪽의 축 제목 대입 오류를 함수 호출로 수정했습니다. rand의 출력은 0 이상 1 미만이며 여기서는 50을 곱합니다.

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(20211206)
x = np.arange(1.1, 100.0, 5.0)
y = x * 1.5 + np.random.rand(len(x)) * 50
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x, y, c="red", alpha=0.5, label="random")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.legend(loc="upper left")
ax.set_title("random")
fig.tight_layout()
plt.show()
```

::image{src="assets/source-20261006/plot-scatter.png" alt="축 제목을 바로잡은 산점도의 코드 실행 결과" ratio="8:5" width="text" role="result" caption="수정 코드를 실제 실행한 결과"}
:::

:::page{type="concept" id="ch13-fix" layout="basic"}
# 그래프 오류를 정확히 요청하기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
산점도의 축 제목이 안 보여. set_xlabel과 set_ylabel에 문자열을 대입한 부분을 함수 호출로 고쳐줘. Figure와 Axes 생성 여부도 확인하고, 기존 X·Y 배열과 시드는 유지해줘. 수정한 코드로 결과 그림을 다시 확인해줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="practice-checklist" id="ch13-check"}
# 오늘의 완료 확인

- [ ] 모든 ax 사용 전에 Figure와 Axes를 만들었다.
- [ ] ro 그림에 불필요한 연결선이 없다.
- [ ] 축 제목은 함수 호출로 설정했다.
- [ ] 코드의 값·범위·범례가 그림과 같다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch13-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

그래프가 다르면 데이터, 그리기 방식, 축 범위 중 어떤 순서로 대조할까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch14-opening" chapter="14"}
# Pandas로 데이터 정리하기

## 14차시 · 원본 교재 예시로 배우기

### 학습 목표

- Series와 DataFrame의 차이를 설명할 수 있다.
- 인덱스, 값, 열 이름을 구분할 수 있다.
- 책의 데이터로 표를 만들고 확인할 수 있다.

### 오늘의 시작

책의 딕셔너리, 혼합 자료 리스트, 학생 정보 표를 그대로 사용합니다. 출력은 수업 전용 message 대신 독립 실행 가능한 print로 바꿉니다.
:::

:::page{type="comparison" id="ch14-formats"}
# 데이터를 보관하는 형식

책 147쪽의 제목은 데이터 파일 형식으로 바로잡았습니다. 이 차시의 필수 실습은 파일 없이 직접 만든 자료로 진행합니다.

| 형식 | 특징 |
|---|---|
| CSV | 구분자로 항목을 나누는 텍스트 자료 |
| Excel | 시트의 행과 열에 정리한 자료 |
| JSON | 키와 값 등의 구조로 표현한 자료 |
:::

:::page{type="comparison" id="ch14-structure"}
# Series와 DataFrame 비교

입력과 처리 결과를 나란히 비교해봅시다.

| 구분 | Series | DataFrame |
|---|---|---|
| 차원 | 1차원 | 2차원 |
| 구조 | 인덱스와 값의 대응 | 행과 열로 이루어진 표 |
| 라벨 | index | index와 columns |
:::

:::page{type="practice-opening" id="ch14-practice-1" practice="014-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 딕셔너리를 Series로 만들기

one, two, three에 각각 1, 2, 3을 연결합니다. 키가 인덱스가 되고 숫자가 값이 되는지 출력으로 확인합니다.

> [!TIP]
> Series에는 서로 다른 종류의 값이 들어갈 수도 있습니다.
:::

:::page{type="concept" id="ch14-series" layout="basic"}
# 딕셔너리의 키와 값 확인하기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
import pandas as pd

ser = pd.Series({"one": 1, "two": 2, "three": 3})
print(ser.to_dict())
print(ser.index.tolist())
print(ser.values.tolist())
```

```output
{'one': 1, 'two': 2, 'three': 3}
['one', 'two', 'three']
[1, 2, 3]
```
:::

:::page{type="concept" id="ch14-mixed" layout="basic"}
# 혼합 자료 리스트의 인덱스와 값

## 예시 확인하기

원본 149쪽의 자료입니다. 출력 형식이 버전에 따라 달라지지 않도록 리스트로 확인합니다.

```python
import pandas as pd

values = ["2022-01-01", 2.14, "song", 1000, True]
sr = pd.Series(values)
print(sr.index.tolist())
print(sr.values.tolist())
```

```output
[0, 1, 2, 3, 4]
['2022-01-01', 2.14, 'song', 1000, True]
```
:::

:::page{type="practice-opening" id="ch14-practice-2" practice="014-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# DataFrame의 행과 열 확인

책 151쪽의 현아와 태민 자료로 표를 만듭니다. 행 이름은 현아·태민, 열 이름은 나이·성별·학년으로 확인합니다.

> [!TIP]
> 원본 설명에 섞인 유상은 코드와 같은 태민으로 바로잡았습니다.
:::

:::page{type="concept" id="ch14-dataframe" layout="basic"}
# 학생 정보 표 만들기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
import pandas as pd

df = pd.DataFrame(
    [[15, "여", "중2"], [17, "남", "고1"]],
    index=["현아", "태민"],
    columns=["나이", "성별", "학년"],
)
print(df.index.tolist())
print(df.columns.tolist())
print(df.loc["태민"].to_dict())
```

```output
['현아', '태민']
['나이', '성별', '학년']
{'나이': 17, '성별': '남', '학년': '고1'}
```
:::

:::page{type="concept" id="ch14-table-result" layout="basic"}
# 실행한 DataFrame을 표로 확인하기

## 예시 확인하기

앞의 코드가 만든 실제 DataFrame을 표 이미지로 출력했습니다. 행 이름과 열 이름은 데이터 값과 구분됩니다.

::image{src="assets/source-20261006/pandas-table.png" alt="현아 15 여 중2와 태민 17 남 고1의 DataFrame" ratio="8:5" width="text" caption="실행한 DataFrame으로 제작한 학습용 표"}
:::

:::page{type="concept" id="ch14-rename" layout="basic"}
# 이름 변경과 값 변경 구분하기

## 인덱스·열 이름 변경

df.index를 학생1·학생2로 바꾸면 행 이름이 달라집니다. df.columns를 연령·남녀·학년으로 바꾸면 열 이름이 달라집니다.

## 데이터는 유지

이름을 바꿔도 15, 17 같은 값이 저절로 바뀌지 않습니다. 라벨 변경과 값 수정을 구분하여 검증합니다.
:::

:::page{type="concept" id="ch14-rename-code" layout="basic"}
# 행 이름과 열 이름 바꾸기

## 예시 확인하기

원본 예시를 실행 가능한 짧은 Python 코드로 정리했습니다.

```python
import pandas as pd

df = pd.DataFrame(
    [[15, "여", "중2"], [17, "남", "고1"]],
    index=["현아", "태민"],
    columns=["나이", "성별", "학년"],
)
df.index = ["학생1", "학생2"]
df.columns = ["연령", "남녀", "학년"]
print(df.index.tolist())
print(df.columns.tolist())
print(df.iloc[0].to_dict())
```

```output
['학생1', '학생2']
['연령', '남녀', '학년']
{'연령': 15, '남녀': '여', '학년': '중2'}
```
:::

:::page{type="practice-checklist" id="ch14-check"}
# 오늘의 완료 확인

- [ ] Series의 index와 values를 각각 확인했다.
- [ ] 현아·태민의 행과 세 열을 맞추었다.
- [ ] 이름 변경 후 데이터 값은 유지된다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch14-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

표에서 행 이름을 바꾸는 일과 나이 값을 바꾸는 일은 어떻게 다를까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch15-opening" chapter="15"}
# 코코봇과 앱 연결하기

## 15차시 · 원본 교재 예시로 배우기

### 학습 목표

- 입력, 클릭, 명령, 동작의 흐름을 설명할 수 있다.
- 거리 입력과 각도 입력을 구분할 수 있다.
- 장비 연결과 실제 동작 확인을 구분해 기록할 수 있다.

### 오늘의 시작

책의 세 버튼 예시를 먼저 읽고, 거리와 각도를 입력하는 예시로 확장합니다. 실제 장비와 연결 환경이 없으면 명령 설계와 입력 검증까지 진행합니다.
:::

:::page{type="concept" id="ch15-robot-flow" layout="basic"}
# 화면의 값을 실제 명령으로 연결

## 기본 흐름

거리나 각도를 입력하고 버튼을 누르면 프로그램이 명령을 전달합니다. 실제 코코봇의 움직임을 관찰하여 요청한 방향과 값에 대응하는지 확인합니다.

## 환경 확인

코코봇 함수 이름, 연결 방식, 거리 단위와 허용 범위는 사용하는 장비·수업 환경에서 확인합니다. 책의 이동 값 100을 근거 없이 100cm로 바꾸지 않습니다.
:::

:::page{type="concept" id="ch15-buttons" layout="basic"}
# 책의 기본 이동·회전 버튼

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

앞으로 100 이동, 왼쪽 90 회전, 오른쪽 90 회전의 세 버튼이 보입니다.

::image{src="assets/source-20261006/cocobot-buttons.png" alt="앞으로 100 이동, 왼쪽 90 회전, 오른쪽 90 회전의 세 버튼이 보입니다." ratio="631:309" width="half" caption="원본 PDF 153쪽의 실습 화면"}
:::

:::page{type="practice-opening" id="ch15-practice-1" practice="015-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 기본 버튼의 동작 설계

앞으로 이동, 왼쪽 회전, 오른쪽 회전의 역할과 연결할 명령을 정합니다. 장비가 있으면 교사가 확인한 공간과 값으로 하나씩 실행합니다.

> [!TIP]
> 세 버튼의 기능을 각각 따로 확인한 뒤 연결합니다.
:::

:::page{type="concept" id="ch15-fields" layout="basic"}
# 거리와 각도를 받는 UI

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

fld1 이동거리와 fld2 회전각도, 이동·왼쪽 회전·오른쪽 회전 버튼이 분리되어 있습니다.

::image{src="assets/source-20261006/cocobot-fields.png" alt="fld1 이동거리와 fld2 회전각도, 이동·왼쪽 회전·오른쪽 회전 버튼이 분리되어 있습니다." ratio="741:652" width="text" caption="원본 PDF 155쪽의 실습 화면"}
:::

:::page{type="comparison" id="ch15-event-map"}
# 입력값과 버튼 매칭

입력과 처리 결과를 나란히 비교해봅시다.

| 버튼 | 읽을 입력 | 명령 역할 |
|---|---|---|
| 앞으로 이동 | fld1 거리 | 앞으로 이동 |
| 왼쪽 회전 | fld2 각도 | 왼쪽 회전 |
| 오른쪽 회전 | fld2 각도 | 오른쪽 회전 |
:::

:::page{type="practice-opening" id="ch15-practice-2" practice="015-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 입력값을 버튼과 연결

책처럼 이동거리 100, 회전각도 90을 입력하는 UI를 설계합니다. 실제 전달 단위와 값은 환경을 확인한 뒤 정하고, 빈 입력과 문자를 거부합니다.

> [!TIP]
> 회전 버튼이 이동거리 입력창을 읽지 않는지 확인합니다.
:::

:::page{type="concept" id="ch15-request" layout="basic"}
# 환경을 확인한 뒤 연결 요청하기

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
거리 입력 fld1과 각도 입력 fld2를 각각 이동과 회전 버튼에 연결해줘. 사용할 코코봇 함수와 거리 단위를 먼저 확인해줘. 함수가 제공되지 않으면 임의로 만들지 말고 전달할 명령 기록만 보여줘. 빈 입력이나 잘못된 숫자는 명령을 보내지 말아줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="concept" id="ch15-inputs" layout="basic"}
# 책의 거리·각도 입력 상태

## 예시 확인하기

원본 교재에 실린 화면입니다. 화면에 보이는 입력값, 위젯 이름과 결과를 함께 읽어봅시다.

이동거리에 100, 회전각도에 90을 입력한 상태입니다. 이 캡처만으로 실제 코코봇 동작이 확인되는 것은 아닙니다.

::image{src="assets/source-20261006/cocobot-input.png" alt="이동거리에 100, 회전각도에 90을 입력한 상태입니다. 이 캡처만으로 실제 코코봇 동작이 확인되는 것은 아닙니다." ratio="582:514" width="half" caption="원본 PDF 157쪽의 실습 화면"}
:::

:::page{type="step-process" id="ch15-verify"}
# 명령과 실제 동작 확인하기

## 연결 상태 확인

수업 도구에서 장비 연결과 명령 함수를 확인합니다.

## 입력과 전달값 확인

거리·각도 입력창을 구분하고 실제 전달되는 값과 단위를 기록합니다.

## 한 기능씩 관찰

이동과 양쪽 회전을 따로 실행합니다. 명령을 보냈다는 기록과 실제 움직임을 관찰한 기록을 구분합니다.
:::

:::page{type="practice-checklist" id="ch15-check"}
# 오늘의 완료 확인

- [ ] 거리와 각도 입력이 맞는 버튼에 연결된다.
- [ ] 함수 이름과 단위를 실제 환경에서 확인했다.
- [ ] 실행하지 못한 항목은 미실행으로 표시했다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch15-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

장비가 움직이지 않으면 입력값, 이벤트, 연결 상태 중 어떤 증거를 남겨야 할까요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::

:::page{type="chapter-opening" id="ch16-opening" chapter="16"}
# 앱 개선과 결과 발표

## 16차시 · 원본 교재 예시로 배우기

### 학습 목표

- 책의 예시를 골라 작은 프로젝트로 완성할 수 있다.
- 문제를 재현하고 수정 결과를 검증할 수 있다.
- AI 도움과 직접 확인한 내용을 구분해 발표할 수 있다.

### 오늘의 시작

책의 자율 프로젝트를 마지막 차시로 확장했습니다. 계산기, 건강습관, 성적표, 차트 중 하나를 골라 작동하는 결과와 검증 기록을 발표합니다.
:::

:::page{type="comparison" id="ch16-projects"}
# 책의 예시에서 프로젝트 고르기

입력과 처리 결과를 나란히 비교해봅시다.

| 예시 | 최소 기능 | 확인할 결과 |
|---|---|---|
| 두 수 계산기 | 수 입력·연산·출력 | 정상 계산과 오류 안내 |
| 건강습관 체크 | 여러 선택·이름·개수 | 선택 없음과 다중 선택 |
| 학생 성적표 | 입력·행 추가·수정 | 열 순서와 행 수 |
| 입력값 차트 | 입력·누적·초기화 | 표와 그림의 값 일치 |
:::

:::page{type="practice-opening" id="ch16-practice-1" practice="016-1" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 한 가지 프로젝트 완성하기

선택한 앱의 핵심 기능 하나를 먼저 완성합니다. 정상 입력과 예외 입력의 결과를 확인한 뒤 개선 기능 하나를 추가합니다.

> [!TIP]
> 기능 수보다 실제 실행 결과가 분명한지 확인합니다.
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
# 재현 가능한 수정 요청

## 예시 확인하기

아래 요청과 답변은 원본 실습을 바탕으로 재작성한 수업용 예시입니다. 실제 AI 응답을 옮긴 기록은 아닙니다.

```prompt
학생 성적표에서 학생1의 국어 100, 수학 90, 영어 80을 넣었는데 수학과 영어가 바뀌어 보여. fld2·fld3·fld4와 열 순서를 대조해 국어·수학·영어로 맞춰줘. 새 행 추가와 기존 행 수정 뒤에도 같은 순서인지 확인해줘.
```

```response
요청을 작은 기능으로 나누어 구현한 뒤, 정해 둔 입력과 예상 결과로 확인합니다.
```
:::

:::page{type="concept" id="ch16-evidence" layout="basic"}
# 결과 이미지를 정직하게 기록하기

## 직접 만든 결과

자기 앱의 실제 입력과 결과가 같이 보이게 캡처합니다. 민감한 정보와 인증키를 빼고, 이전 버전 이미지가 남아 있지 않은지 확인합니다.

## 교재 그림과 구분

앞 차시의 원본 캡처는 학습 자료입니다. 그것을 자신의 완성 앱이나 직접 실행한 증거로 제출하지 않습니다. 오류 수정 전과 후는 같은 입력으로 비교합니다.
:::

:::page{type="practice-opening" id="ch16-practice-2" practice="016-2" practice-kind="바이브 코딩 실습" platform="교실 실습"}
# 개선 결과 발표하기

문제와 사용자, 핵심 기능, 수정 전후, 실제 테스트 결과를 차례로 보여줍니다. 아직 확인하지 못한 기능과 AI 도움을 받은 부분도 함께 설명합니다.

> [!TIP]
> 원본 교재를 참고한 부분과 새로 바꾼 부분을 구분합니다.
:::

:::page{type="concept" id="ch16-portfolio" layout="basic"}
# 포트폴리오에 담을 내용

## 기획과 구현

앱 이름, 사용자, 해결할 문제를 적습니다. 입력, 처리, 출력 설계와 주요 위젯 역할을 넣습니다.

## 검증과 개선

실행 가능한 프로젝트, 정상 입력 결과, 예외 입력 결과, 수정 요청과 재검증 기록을 남깁니다. 장비가 필요한 기능은 실제 실행 여부를 표시합니다.
:::

:::page{type="practice-checklist" id="ch16-check"}
# 오늘의 완료 확인

- [ ] 책의 예시에서 고른 핵심 기능이 작동한다.
- [ ] 정상 입력과 예외 입력을 실행했다.
- [ ] 수정 후 기존 기능도 다시 확인했다.
- [ ] 참고 자료, AI 도움, 미확인 항목을 구분했다.

> [!KEY_POINT]
> 설명이 그럴듯한지보다 입력과 실제 결과가 일치하는지 확인합니다.
:::

:::page{type="concept" id="ch16-record" layout="basic"}
# 내가 확인한 내용을 남기기

## 생각해보기

이번 프로젝트에서 AI의 설명과 실제 결과가 달랐던 부분을 어떻게 해결했나요?

## 개발 기록

- 처음 요청한 내용과 수정한 내용을 구분해 적습니다.
- 정상 입력 한 가지와 예외 입력 한 가지를 기록합니다.
- 예상 결과와 실제 결과를 비교하고 화면 또는 출력 기록을 남깁니다.
:::
