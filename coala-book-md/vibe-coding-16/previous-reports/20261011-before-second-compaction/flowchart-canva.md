# Canva 순서도·요약 그림 안내 · 2026-10-11

현재 순서도 4개와 요약 그림 1개를 준비했습니다. 독립 인쇄 PDF에는 네이티브 벡터 PDF 5개를 사용합니다. Canva에는 같은 이름의 PNG를 입력합니다.

| 현재 쪽 | 순서도 | 관리용 출처 쪽 | 벡터 PDF | Canva용 PNG |
|---|---|---|---|---|
| 23 | 가족 나이 합의 변수 준비·값 저장·합계 계산·출력 | 23 | assets/source-flowcharts/ch04-family-flow.pdf | assets/source-flowcharts/ch04-family-flow.png |
| 29 | 운동 시간의 초기값·반복 조건·누적·증가·출력 | 31 | assets/source-flowcharts/ch05-exercise-flow.pdf | assets/source-flowcharts/ch05-exercise-flow.png |
| 36 | 수면 시간의 8시간·5시간 조건 분기 | 36 | assets/source-flowcharts/ch06-sleep-flow.pdf | assets/source-flowcharts/ch06-sleep-flow.png |
| 42 | 네 학생 나이의 반복과 15세 관람 조건 | 39 | assets/source-flowcharts/ch07-movie-flow.pdf | assets/source-flowcharts/ch07-movie-flow.png |

5쪽 요약 그림은 assets/ch01/ai-human-summary.png를 사용합니다. 순서도는 assets/source-flowcharts 폴더의 PNG 4개를 사용합니다. 비율을 유지하고 글자·화살표·분기가 잘리지 않게 배치합니다. PNG 내부 노드가 각각 편집 가능한 Canva 도형이 되는 것은 아닙니다.

원본 순서도의 선언은 6각형이고 글꼴·노드·연결을 보존합니다. 벡터에는 DPI를 적용하지 않습니다. PNG의 effectiveDpi는 대체 미리보기 파일 정보입니다. 상세 출처·해시는 flow-source-map.json·asset-manifest.json·현재 QA에 있습니다.

prepare_source_flowcharts.py는 원본 재추출 때만 사용하며 원본 PDF·PyMuPDF가 필요하고 일부 원고 문구도 적용합니다. 일상 원고 편집·현재 자산 PDF 재생성에서는 실행하지 않습니다.
