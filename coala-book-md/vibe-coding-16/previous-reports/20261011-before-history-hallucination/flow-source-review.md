# 순서도 직접 재사용·학습 내용 검증 · 2026-10-11

현재 완성본 output/pdf/vibe-coding-16-revised.pdf의 순서도 4개는 기준 교재의 네이티브 벡터를 직접 사용했습니다. 재그린 도형이나 PNG를 인쇄 그림으로 사용하지 않습니다. Canva에서 쓸 300dpi PNG를 별도로 준비했습니다.

| 현재 쪽 | 순서도 | 기준 PDF 쪽 | 인쇄용 벡터 | Canva용 PNG |
|---|---|---|---|---|
| 23 | 가족 나이 합의 변수 준비·값 저장·합계 계산·출력 | 23 | assets/source-flowcharts/ch04-family-flow.pdf | assets/source-flowcharts/ch04-family-flow.png |
| 29 | 운동 시간의 초기값·반복 조건·누적·증가·출력 | 31 | assets/source-flowcharts/ch05-exercise-flow.pdf | assets/source-flowcharts/ch05-exercise-flow.png |
| 36 | 수면 시간의 8시간·5시간 조건 분기 | 36 | assets/source-flowcharts/ch06-sleep-flow.pdf | assets/source-flowcharts/ch06-sleep-flow.png |
| 42 | 네 학생 나이의 반복과 15세 관람 조건 | 39 | assets/source-flowcharts/ch07-movie-flow.pdf | assets/source-flowcharts/ch07-movie-flow.png |

원본 PDF는 수정하지 않았습니다. 추출 자산에서 crop 밖의 글자만 제거하고 전체 페이지 회색 배경 색상을 흰색으로 바꿨습니다. 순서도 노드·연결·글꼴·벡터 경로와 색은 보존했습니다. 각 벡터 자산은 1쪽이며 내부 래스터 이미지 객체는 0입니다. PNG·벡터 SHA-256, cropbox, 원고 flowchart 블록 SHA-256을 확인했습니다. 원본 파일을 현재 환경에서 직접 해시 확인했는지 여부는 QA의 sourcePdfHashVerified에 기록합니다. 원본이 없는 다른 컴퓨터에서는 보존 출처 기록과 묶음 자산의 해시 검증을 구분합니다.

## 선언·반복·조건 확인

선언·초기 준비는 원본의 6각형 기호입니다. 원본 기호와 현재 그림을 제작자 및 독립 검토자가 시각 확인했습니다. 자동 검사에서는 자산·원고 해시와 배치 연결을 확인하며 6각형을 영상 인식으로 판정했다고 주장하지 않습니다.

29쪽 반복은 time1=1, total=0에서 시작합니다. time1<=10인 동안 total에 time1을 더하고 time1을 1 증가시킵니다. 누적 추적은 1→1, 2→3, 3→6, 4→10, 5→15, 6→21, 7→28, 8→36, 9→45, 10→55입니다. 10을 포함해 10회 반복한 후 time1=11, total=55에서 종료합니다.

42쪽은 네 학생의 영화 관람 조건입니다. 15세 미만은 관람 불가이며 14·15·16·13세의 결과는 불가·가능·가능·불가입니다. 점수 판정의 N명·80점 활동은 별도 실습 글 단계로 유지했습니다.

## 7쪽 환각 설명

가상 공지와 잘못된 AI 답변을 비교하는 예시임을 표시했습니다. 시간·장소 차이, 공지·링크의 존재 확인, 맞음·틀림·확인하지 못함 구분, 책임 있는 사용을 한 장에 배치했습니다. 본문 끝은 이전 299pt에서 604pt로 늘어났으며 글자·상자 넘침은 0입니다. 142쪽 전체 렌더링과 해당 지면의 독립 시각 검토를 완료했습니다.

원고·실습·코드를 이 보고서가 수정하지 않습니다. 재생성 절차는 notes.md에 있으며 prepare_source_flowcharts.py는 원본 재추출 때만 사용합니다. 이 문서는 제작 관리용이며 학생용 본문에 출처 메타를 넣지 않습니다.
