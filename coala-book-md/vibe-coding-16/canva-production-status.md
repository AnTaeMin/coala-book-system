# Canva 전체 교재 제작 상태

기록일: 2026-10-04. 사용자 요청에 따라 앱과 예제를 직접 실행했다.

## 실행 결과

- Canva 앱 서버 http://localhost:8080/app.js 및 예제 서버 http://127.0.0.1:8765/ 모두 HTTP 200.
- 16차시 예제를 새로 실행해 수학 20분·영어 30분을 입력했다. 기록 2개, 합계 50분, 과목별 그래프 20·30분을 확인했다.
- Canva 앱에 원고 붙여넣기 기능을 추가했다. 파일 선택이 어려울 때 기존 원고 검사 경로를 사용한다.
- 최신 book.md 전체 58,927자를 Canva 앱에 입력하고 검사했다. 앱에서 원고 202페이지·8종류를 확인했으며 생성 버튼이 활성화되었다.
- 예상 Canva 배치는 206장이다. 실제 교재 페이지 생성은 0장이다.
- 이미지 21개는 준비되어 있지만 아직 Canva 앱에 연결하지 못했다.

## 원본 디자인 승인과 실제 접근 결과

사용자가 https://www.canva.com/design/DAHRZrtJw9U/edit 의 열람·복제를 승인하고 원본 템플릿 제작 방식을 선택했다. 승인 후 원본을 직접 열었다.

Canva는 **이 디자인을 볼 권한이 없어요.**라고 표시했다. 화면의 현재 로그인 계정은 hagalsa88@thecoala.io다. 사용자의 작업 승인은 받았지만 이 계정에 원본 디자인을 열람할 Canva 권한이 없다. 소유자에게 메시지나 권한 요청은 보내지 않았다.

이전 자동 승인 검토의 대상 확인 문제는 구체적인 사용자 승인으로 해소되었다. 현재 막힌 이유는 Canva 자체의 디자인 접근 권한이다.

## 파일 선택 결과

원고 파일 버튼과 이미지 폴더 입력에서 각각 파일 선택을 기다렸지만 10초 뒤 시간 초과했다. 확장 프로그램의 파일 URL 접근 설정 상태는 확인하지 못했다. 설정 문제로 원인을 단정하지 않는다.

원고는 붙여넣기로 해결했다. 이미지 폴더 선택은 해결되지 않았다. 브라우저·계정 보안 설정을 변경하지 않았다.

## 제작을 이어가기 위한 조건

1. 원본 소유자가 현재 계정에 원본의 편집 권한을 공유하거나 원본을 볼 수 있는 승인된 계정으로 접속해야 한다.
2. 교재 제작용 캔버스 크기와 원본 네이티브 페이지 복제를 확인한다. 현재 앱 미리보기 디자인은 800×600이다.
3. vibe-coding-16 폴더를 앱에서 선택해 이미지 21개를 연결한다.
4. 전체 교재를 생성하고 네이티브 단원·실습 시작 페이지, 6차시 순서도 1개, 글꼴·이미지·페이지 번호를 검수한다.

[교재 스킬](../../skill/coala-canva-textbook/SKILL.md)은 "duplicate the matching Canva source page"를 요구하며, "If the available Canva capabilities cannot duplicate and edit the required native template or flowchart elements, stop and report that exact template fidelity cannot be guaranteed."라고 명시한다. 승인된 원본 제작 경로의 접근 권한이 없어 페이지 생성을 시작하지 않았다.

## 기록

- 원고 검사 화면: C:/Users/Public/Documents/ESTsoft/CreatorTemp/coala-canva-manuscript-ready.png.
- 원본 접근 제한 화면: C:/Users/Public/Documents/ESTsoft/CreatorTemp/coala-canva-source-access.png.
- 실행 근거: direct-execution.json.
