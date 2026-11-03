# 순서도 재사용·검증 · 2026-10-11

순서도 4개는 기준 교재의 네이티브 벡터를 사용합니다. Canva용 300dpi PNG는 별도 미리보기이며 인쇄 PDF의 그림은 래스터가 아닙니다.

| 현재 쪽 | 순서도 | 관리용 출처 쪽 | 벡터 PDF | Canva용 PNG |
|---|---|---|---|---|
| 23 | 가족 나이 합의 변수 준비·값 저장·합계 계산·출력 | 23 | assets/source-flowcharts/ch04-family-flow.pdf | assets/source-flowcharts/ch04-family-flow.png |
| 29 | 운동 시간의 초기값·반복 조건·누적·증가·출력 | 31 | assets/source-flowcharts/ch05-exercise-flow.pdf | assets/source-flowcharts/ch05-exercise-flow.png |
| 36 | 수면 시간의 8시간·5시간 조건 분기 | 36 | assets/source-flowcharts/ch06-sleep-flow.pdf | assets/source-flowcharts/ch06-sleep-flow.png |
| 41 | 네 학생 나이의 반복과 15세 관람 조건 | 39 | assets/source-flowcharts/ch07-movie-flow.pdf | assets/source-flowcharts/ch07-movie-flow.png |

각 자산은 1쪽·래스터 이미지 객체 0이며 PNG·벡터·cropbox·원고 논리 해시를 확인했습니다. 도형·글꼴·연결·경로·색은 보존했고 crop 밖의 글자와 전체 페이지 회색 배경만 정리했습니다. 원본 PDF 자체는 수정하지 않았습니다. 원본 파일의 직접 해시 확인 여부는 QA에 기록합니다.

선언은 6각형입니다. 29쪽 반복은 time1=1·total=0에서 시작해 total에 time1을 더하고 time1을 1 증가시킵니다. 10회 후 time1=11·total=55로 종료합니다. 41쪽 영화 조건은 15세 미만 관람 불가입니다. N명·80점 점수 판정 활동은 별도로 유지합니다.

5쪽의 자체 제작 요약 벡터 1개를 그대로 유지했습니다. 7쪽 가상 오답 내용은 직전 판과 같습니다. 전체 134쪽 조판 검토를 마쳤으며 이 보고서는 원고·그림·코드를 변경하지 않습니다.
