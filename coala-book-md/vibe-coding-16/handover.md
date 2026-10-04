# 원고 사용 및 제작 인계

## 원고 선택

- 최종 초안 전체 원고: book.md. 사용 안내·학습 흐름·기록 양식 포함.
- 차시별 원고: ch01.md~ch16.md. 같은 assets/ 폴더를 공유한다.
- 수업 설계: curriculum.md. 재생성 지침: notes.md. 교사 운영: teacher-guide.md.
- 전체 또는 차시별 파일 중 한 방식을 택해 Canva에 올린다. 둘 다 생성하면 내용이 중복된다.
- 표지, 목차, 단원 구분 페이지는 원고 파서에 지원되지 않아 Canva에서 따로 만든다.
- 차시 시작의 번호는 1~16을 사용한다. 4개 단원 그룹은 curriculum.md를 따른다.
- Canva 생성은 아직 실행하지 않았다. 시각적 배치와 원본 네이티브 템플릿 일치는 미검증이다.

## 준비한 이미지

21개 모두 assets/ch01~ch16에 준비했다. PDF 재사용 3개와 신규 자료 18개다.
출처와 각 파일은 [asset-audit.md](asset-audit.md), 전체 미리보기는 [asset-review.html](asset-review.html)을 참고한다.
신규 자료는 교사의 브라우저 실행 예제 또는 설계 예시이며 학생 작품과 구분한다.
1차시 PDF 캡처는 half, 나머지는 text 너비다. 실제 비율을 전체·차시별 원고에 반영했다.
Canva에 원고와 함께 assets 폴더를 지정하고 생성 후 이미지 누락·자르기·라벨 가독성을 확인한다.

## Canva에서 완성할 순서도

[flowchart-canva.md](flowchart-canva.md)에 노드, 색, 연결, 조건 검수 기준을 준비했다. 최종 Canva 순서도는 아직 미완료다.

- ch06-branch: 대출 수 입력, 3 미만 판단, 가능·불가 출력의 노드 4개와 연결 3개.
- 구조: if-else. 원고의 순서도는 입력 검증 이후의 조건 판단만 표시한다.
- 입력: MAGpWHDxa1c. 판단: MAGpWETGMb4. 출력: MAGpWDtQbCc.
- 분기 컨테이너: MAGpWHT7x4M. skill/coala-canva-textbook/references/flowcharts.md의 if-else 구성을 따른다.
- 글꼴: Hakgyoansim Chilpanjiugae OTF. 노드와 연결은 Canva 네이티브 요소로 완성한다.
- Canva에서 생성되는 회색 작업 영역과 안내를 최종 교재에 남기지 않는다.

## 확인해야 할 항목

- 대상 학년과 수업 시간: 현재 입문자·50분 가정.
- 실제 실습 도구의 위젯 이름, 이벤트 연결 방법, 저장 방식, 그래프 환경.
- Flet 버전과 수업 도구가 사용하는 API. 최신 문서와 동일하다고 가정하지 않는다.
- 루트 수정본과 (11).pdf의 차이. 현재 원고는 읽을 수 있는 flet.pdf를 기반으로 작성했다.
- 기관명, 로고, 실제 인쇄 규격과 축소 비율.
- Canva 생성 뒤 글꼴, 텍스트 넘침, 캡처 가독성, 이미지와 순서도 완성 상태.

## 검증 범위

- 구조·문법·예상 배치는 저장소 검증기로 확인한다. validation-summary.md를 참고한다.
- Python 개념 코드 출력은 code-results.json에 직접 실행한 결과를 기록했다.
- 예시 AI 응답은 집필 예시다. 실제 서비스 대화 기록이 아니다.
- 검증 통과는 실제 생성된 학생 앱의 정상 동작이나 Canva 최종 시각 품질을 보증하지 않는다.

## 최종 초안 상태

원고 202개 페이지 컨테이너, 예상 Canva 206장이다. 이미지 21개가 모두 준비되었으며 실제 파일 비율을 적용했다. 순서도 1개와 표지·목차 등 Canva 마무리 작업은 final-draft.md를 참고한다.
