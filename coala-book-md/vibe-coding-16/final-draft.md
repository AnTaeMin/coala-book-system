# AI와 함께하는 바이브 코딩 · 최종 초안

- 작성일: 2026-10-04.
- 대상·시간: 코딩 입문자, 16차시, 차시당 50분 가정.
- 상태: Canva 제작에 전달할 학생용 원고 최종 초안. Canva 최종 디자인·인쇄본은 아직 아니다.

## 들어 있는 자료

1. book.md: 사용 안내와 학습 흐름, 16차시 본문, 개발·테스트 기록 양식.
2. ch01.md~ch16.md: 차시별 원고. 전체 원고와 차시 본문이 같다.
3. assets/: 원고가 참조하는 이미지 21개. PDF 재사용 3개와 교사 제작 자료 18개.
4. curriculum.md·teacher-guide.md: 수업 설계, 50분 진행, 교사 준비와 평가 예시.
5. examples/: 교재 캡처에 사용한 실행 예제와 조작 방법.
6. asset-review.html·asset-audit.md·asset-manifest.json: 이미지 미리보기와 출처.
7. validation-summary.md·validation-full.json·code-results.json·example-checks.json: 기존 검증 근거.
8. review-report.md·review-browser-checks.json·review-storage-checks.json·canva-production-status.md: 재검토와 실제 제작 상태.
9. flowchart-canva.md·handover.md·notes.md: 순서도 명세, 제작 인계와 재생성 지침.

원고 컨테이너 202개, 예상 Canva 206장이다. 그림의 라벨이 작아지지 않도록 4개 차시의 캡처 페이지가 나뉜다.

## Canva에 전달하기

압축을 풀고 book.md와 assets/를 같은 폴더에 둔다. Coala Book Builder에서 book.md와 해당 폴더를 함께 지정한다.
차시만 제작하려면 chXX.md를 선택한다. 전체와 차시 파일을 동시에 생성하면 본문이 중복된다.
제작용 캔버스는 원고의 coala-portrait 규격을 사용한다. 이전 테스트용 800×600 디자인의 크기를 그대로 교재 규격으로 간주하지 않는다.

## Canva에서 남은 작업

- 6차시 ch06-branch 순서도 1개: flowchart-canva.md에 따라 편집 가능한 네이티브 도형으로 완성한다.
- 표지·목차·단원 구분이 필요하면 원본의 승인된 네이티브 페이지를 복제하여 추가한다. Markdown 앱은 이 페이지 유형을 지원하지 않는다.
- 단원·실습 시작 페이지의 원본 네이티브 템플릿 일치, Wanted Sans와 순서도 글꼴을 확인한다.
- 실제 생성 후 이미지 삽입, 글자 넘침, 페이지 번호를 확인한다.
- 기관명·로고·대상 학년·인쇄 크기와 축소 비율을 확정한다.

[교재 스킬](../../skill/coala-canva-textbook/SKILL.md)의 "A person builds the flowchart in the Canva editor." 규칙 때문에 회색 순서도 작업 영역이 있는 디자인을 최종 교재로 표시하지 않는다. 원고 데이터와 제작 명세는 준비되어 있다.

## 수업 적용 범위

PDF 원본과 신규 자료를 구분했고, AI 답변과 프로젝트 그림은 학습용 예시로 표시했다. 학생은 자신의 실행 증거를 별도로 만든다.
실제 수업 도구의 Flet 버전·위젯 이름·저장·그래프 기능은 교사가 먼저 확인한다. 브라우저 예제 검증을 Flet 실환경 검증으로 해석하지 않는다.
IDE에 열린 수정본 PDF의 차이를 반영한 최종본이라고 주장하지 않는다. 현재 출처와 확인 범위는 asset-audit.md에 기록했다.
