# PDF 재사용 검토 및 이미지 준비 결과

## 검토 범위

- 실제 재사용 출처: ../ai-math/flet.pdf, 155쪽. PDF 페이지 번호 기준이다.
- 53쪽: 입력창·버튼과 인사 알림창을 추출하여 1차시의 입력·동작·테스트 기준을 수정했다.
- 63쪽: 4단 구구단 화면을 추출하여 7차시 입력, 코드 출력, 테스트, 오류 예시를 4단으로 맞췄다.
- 49·56·57·58·60쪽: 버튼·입력·계산 예제가 있지만 현재의 이름 인사 및 2+3 계산 화면과 일치하지 않는다.
- 70·73·77쪽: 선택 위젯 자료가 있지만 코코아 주문 예제의 가격·수량·옵션 결과를 보여주지 않는다.
- 88·89쪽: 표의 셀 위치·값 변경 예제여서 공부 기록의 행 선택 삭제 장면으로 사용할 수 없다.
- 100·103·115·117·119·121·124쪽: 그래프·자료 불러오기·프로젝트 저장 자료가 있다. 공부 기록 두 행을 저장해 새 실행에서 복원하거나 과목별로 합산한 결과와는 다르다.
- 따라서 공통 개념과 수업 구조는 유지하고, 일치하는 캡처 3장은 재사용하며 나머지 18장은 원고의 예제 값에 맞춰 새로 준비했다.
- 루트의 수정본 PDF는 현재 도구에서 본문·이미지가 정상적으로 읽히지 않아 재사용 근거로 삼지 않았다. IDE의 (11).pdf는 작업 폴더에서 확인되지 않았다. 원본 PDF 파일은 수정하지 않았다.

## 준비 상태

- 21개 이미지 경로에 실제 PNG 파일을 준비했다. PDF 3장, 브라우저 실행 캡처 16장, 설계 예시 2장이다.
- 새 실행 자료는 examples/index.html에서 실제로 입력하고 버튼을 눌러 캡처했다. Flet·알고플로의 UI 또는 실제 AI 응답으로 표현하지 않는다.
- 13~16차시의 그림은 교사의 프로젝트 예시다. 학습자는 자신의 기획서와 실행 증거를 별도로 만든다.
- 11차시 첫 이미지는 저장 직후이며, 두 번째 이미지는 새로고침으로 기록 0개인 상태를 확인한 뒤 불러와 복원한 상태다.
- 캡처의 실제 비율을 원고에 반영했다. 새 캡처는 라벨 가독성을 위해 text 너비를 사용하며, 1차시 PDF 캡처는 half를 유지했다.
- 전체 book.md와 ch01.md~ch16.md에 같은 수정 사항을 적용했다.
- [이미지 전체 미리보기](asset-review.html), [출처·크기·해시 기록](asset-manifest.json), [실행 방법과 캡처 입력](examples/README.md).

| 차시 | 파일 | 출처 | 크기(px) | 상태 |
|---:|---|---|---|---|
| 1 | [assets/ch01/before.png](assets/ch01/before.png) | PDF 53쪽 | 849×505 | 준비 완료 |
| 1 | [assets/ch01/after.png](assets/ch01/after.png) | PDF 53쪽 | 937×547 | 준비 완료 |
| 2 | [assets/ch02/result.png](assets/ch02/result.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 3 | [assets/ch03/result.png](assets/ch03/result.png) | 신규 설계 예시 | 1745×777 | 준비 완료 |
| 4 | [assets/ch04/before.png](assets/ch04/before.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 4 | [assets/ch04/after.png](assets/ch04/after.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 5 | [assets/ch05/result.png](assets/ch05/result.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 6 | [assets/ch06/result.png](assets/ch06/result.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 7 | [assets/ch07/result.png](assets/ch07/result.png) | PDF 63쪽 | 1369×721 | 준비 완료 |
| 8 | [assets/ch08/result.png](assets/ch08/result.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 9 | [assets/ch09/result.png](assets/ch09/result.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 10 | [assets/ch10/before.png](assets/ch10/before.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 10 | [assets/ch10/after.png](assets/ch10/after.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 11 | [assets/ch11/before.png](assets/ch11/before.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 11 | [assets/ch11/after.png](assets/ch11/after.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 12 | [assets/ch12/before.png](assets/ch12/before.png) | 신규 실행 캡처 | 1745×828 | 준비 완료 |
| 12 | [assets/ch12/after.png](assets/ch12/after.png) | 신규 실행 캡처 | 1745×828 | 준비 완료 |
| 13 | [assets/ch13/result.png](assets/ch13/result.png) | 신규 설계 예시 | 1745×777 | 준비 완료 |
| 14 | [assets/ch14/result.png](assets/ch14/result.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 15 | [assets/ch15/result.png](assets/ch15/result.png) | 신규 실행 캡처 | 1745×777 | 준비 완료 |
| 16 | [assets/ch16/result.png](assets/ch16/result.png) | 신규 실행 캡처 | 1745×828 | 준비 완료 |

## 순서도

6차시의 대출 판단 순서도 1개는 원고 데이터와 [Canva 제작 명세](flowchart-canva.md)를 준비했다.
Canva 최종 순서도는 아직 만들어지지 않았다. PNG 대체 파일은 만들지 않았다.
[교재 스킬](../../skill/coala-canva-textbook/SKILL.md)의 "A person builds the flowchart in the Canva editor." 규칙에 따라 지정된 네이티브 도형·글꼴·연결선으로 완성해야 한다. 현재 앱은 회색 작업 영역을 생성한다.

## 검증

Markdown 구조와 예상 배치 검사는 validation-summary.md에 기록했다. 실제 Canva 페이지 생성·글꼴·인쇄 가독성 검수는 별도 작업이다.

## 재검토에서 교체한 캡처

12차시 전·후와 16차시 결과 3장을 다시 실행해 캡처했다. 가로 막대 방향, 제목·단위·눈금 범위, 수학·영어 합계를 확인했다. 실제 이미지 비율과 해시를 원고 및 목록에 반영했다.

확장자는 PNG지만 실제로 JPEG인 브라우저 캡처 18장을 PNG로 변환했다. 내용이나 표시 픽셀은 바꾸지 않았으며, 최종 이미지 21개 모두 실제 PNG 형식이다.
