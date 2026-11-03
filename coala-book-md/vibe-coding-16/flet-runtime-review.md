# 실제 Flet 차트 구조 반영 · 2026-10-27

현재 16차시 교재는 A4 **132쪽**입니다. 직전 수정본은 130쪽이었으며 실제 조판 결과에 맞춰 목차와 차시 시작 쪽수를 다시 계산했습니다. 162개 원고 컨테이너, 37개 실습, 순서도 4개를 유지합니다. 차트 연결 예시 그림을 추가하여 PNG 40개·벡터 PDF 7개·이미지 배치 42곳입니다.

## 반영한 코드 구조

[수업 화면](https://coala-web-v2.coala.services/ko/student/sl42)의 차트 생성 구조에 맞춰 공통 생성 코드 1개와 그리기 실습 7개로 정리했습니다. flet_charts를 pyplot보다 먼저 가져오고, fig_cht1·ax_cht1을 만든 뒤 같은 fig_cht1을 cht1의 figure로 연결합니다.

공통 생성 부분은 앱 구성 때 한 번 실행합니다. 실습 코드는 기존 ax_cht1에 그리며 고정 데이터를 다시 그릴 때 clear로 이전 그림을 지웁니다. 사용자의 요청에 따라 tight_layout·canvas.draw_idle 호출은 학생용 로직 예제 7개에서 제외했습니다. 실행 환경이 로직 밖에서 배치와 화면 갱신을 처리합니다. 이벤트 안에서 새 Figure를 만들거나 별도의 pyplot 창을 여는 코드도 제거했습니다. 14차시 입력 누적은 이전 입력을 유지하는 별도 동작으로 구분합니다.

기본 Figure 크기 6.4×4.8에 맞춰 결과 그림 7개를 **1536×1152, 4:3**으로 다시 만들었습니다. 입력 배열·수치·마커·시드는 유지합니다. 산점도는 글꼴 설정 뒤 기존 Axes를 초기화하며, 해당 한글 글꼴이 없으면 영문 축 이름을 사용합니다.

| 코드 | 현재 PDF 쪽 |
|---|---|
| ch12-axes | 84, 85 |
| ch12-markers | 93, 94 |
| ch12-one-array | 87 |
| ch12-range | 91 |
| ch12-two-arrays | 89 |
| ch13-bars | 100 |
| ch13-grouped | 102, 103 |
| ch13-scatter | 105, 106 |

## 실행과 인쇄 검증

- 원고 17개와 인쇄 Python 블록 8개: 구조·코드 일치 검사 통과.
- Python 3.10.11, Flet 0.86.0, flet-charts 0.86.0, Matplotlib 3.10.9, NumPy 2.2.6에서 공통 생성 1개·그리기 7개 통과.
- 같은 Figure·Axes·Chart에서 실습마다 2회씩, 총 14회 실행했습니다. 객체 연결 유지·그래프 수치·축·범례 검사 통과, 경고 0건.
- 실제 Flet Matplotlib 백엔드를 사용했습니다. 한글 글꼴 부재를 모의한 영문 축 대체 검사도 통과했습니다.
- 브라우저가 연결된 실제 Flet Page에 컨트롤을 배치하고 해당 이벤트 콜백을 실행했습니다. **GUI 19개·알고리즘 6개·Matplotlib 실습 7개, 총 32개 모두 통과**했습니다.
- PDF 132쪽 전체 렌더 검사에서 글자 경계 초과·원고 누락·코드 차이·박스 넘침은 0건입니다. 목차 링크와 책갈피는 각 16개입니다.

[실제 실행 화면](../../output/pdf/flet-practice-runtime-check.png)에서 검사 결과를 확인할 수 있습니다.

## sl42 실제 화면에서 확인한 결과

[sl42](https://coala-web-v2.coala.services/ko/student/sl42)에서 Chart를 추가하고 Python GUI의 전체 코드를 직접 읽어 공통 생성 구조와 대조했습니다. 이 실제 생성 코드는 [원문](examples/flet-practices/sl42-generated-chart.py)에 보관했습니다. 이어서 같은 페이지의 실행 기능으로 점검 앱을 실행했습니다. **학생용 로직에서 배치·갱신 호출을 제외한 최종 코드로도 32개 모두 통과**했습니다. 실제 페이지의 Python은 3.14.2, Flet과 flet-charts는 0.86.0입니다.

[sl42 실제 실행 화면](../../output/pdf/sl42-practice-runtime-check.png)과 [페이지 실행 기록](sl42-runtime-results.json)을 확인합니다. 로컬 실행과 실제 서비스 페이지 실행을 구분하여 기록했습니다. 점검 앱은 화면에 연결된 실제 위젯의 이벤트 콜백을 호출하며, 모든 항목을 마우스로 하나씩 클릭했다는 의미는 아닙니다.

추가로 sl42의 기본 디자이너에서 생성된 Chart의 **로직 보기**에 교재의 배열 한 개 예제를 직접 넣어 실행했습니다. 배치·갱신 호출이 없는 실제 로직과 선 그래프를 [확인 화면](../../output/pdf/sl42-logic-only-check.png)과 [대조 기록](sl42-code-comparison.json)에 보관했습니다. 현재 sl42에는 이 간단한 예제가 열려 있습니다.

걸음 수·거리 저장 검증은 예제 앱의 **JSON 파일 저장·불러오기**입니다. 로컬 앱에서는 작업 폴더, sl42에서는 브라우저 실행 환경의 파일에 실제로 쓰고 복원했습니다. 학교 계정의 내 저장소 프로젝트 저장·제출은 실행하지 않았습니다.

## 전달 파일

[현재 PDF](../../output/pdf/vibe-coding-16-upstream.pdf), [전체 원고](book.md), [그리기 코드](examples/source-based/README.md), [실행 가능한 Flet 실습](examples/flet-practices/README.md), [코드 검사](code-results.json), [실제 GUI 실행 기록](gui-results.json), [상세 대조](flet-runtime-review.json).

[이전 내용·오류 검토](content-code-review.md)는 직전 검토 기록입니다. 이번 수정 전 자료는 previous-reports/20261027-before-flet-runtime에 보관했습니다.
