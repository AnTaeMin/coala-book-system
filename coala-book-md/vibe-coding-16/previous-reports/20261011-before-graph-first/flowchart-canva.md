# Canva 순서도 사용 안내 · 2026-10-11

현재 순서도 4개는 완성되어 있습니다. 사용자가 원본 교재 순서도를 가져와 활용하도록 요청했으므로 기존의 도형 재제작·편집 가능한 요소 조립 안내 대신 원본 자산을 사용합니다. 독립 인쇄 PDF는 벡터 PDF 4개를 포함하며 Canva용 PNG 4개도 준비했습니다.

| 현재 쪽 | 순서도 | 기준 PDF 쪽 | 인쇄용 벡터 | Canva용 PNG |
|---|---|---|---|---|
| 23 | 가족 나이 합의 변수 준비·값 저장·합계 계산·출력 | 23 | assets/source-flowcharts/ch04-family-flow.pdf | assets/source-flowcharts/ch04-family-flow.png |
| 29 | 운동 시간의 초기값·반복 조건·누적·증가·출력 | 31 | assets/source-flowcharts/ch05-exercise-flow.pdf | assets/source-flowcharts/ch05-exercise-flow.png |
| 36 | 수면 시간의 8시간·5시간 조건 분기 | 36 | assets/source-flowcharts/ch06-sleep-flow.pdf | assets/source-flowcharts/ch06-sleep-flow.png |
| 42 | 네 학생 나이의 반복과 15세 관람 조건 | 39 | assets/source-flowcharts/ch07-movie-flow.pdf | assets/source-flowcharts/ch07-movie-flow.png |

Canva 이미지 입력 시 로컬 coala-book-md/vibe-coding-16/assets/source-flowcharts 폴더를 지정하고 해당 PNG를 넣습니다. 비율을 유지하고 글자·화살표·분기 표시가 잘리지 않게 배치합니다. 원본의 선언은 6각형이고 도형·글꼴·연결을 보존합니다. 이 PNG를 넣는 경로에서는 내부 노드가 각각 편집 가능한 Canva 도형이 되지 않습니다. 독립 PDF의 인쇄 순서도는 PNG가 아닌 네이티브 벡터입니다.

벡터·PNG의 출처와 해시는 flow-source-map.json, 검증은 flow-source-review.md에서 확인합니다. 벡터에는 DPI를 적용하지 않습니다. PNG는 원본에서 300dpi로 추출했습니다. 기준 원고의 논리와 실제 그림을 함께 유지하며 변경할 때는 각 순서도 블록 해시도 맞춥니다.

prepare_source_flowcharts.py는 원본 자산을 다시 추출할 때만 실행하며 원본 PDF·PyMuPDF가 필요합니다. 일상 원고 편집 또는 기존 자산을 쓰는 PDF 재생성 때 실행하지 않습니다. 현재 자산을 사용하는 조판에는 원본 PDF나 PyMuPDF가 필요하지 않습니다.
