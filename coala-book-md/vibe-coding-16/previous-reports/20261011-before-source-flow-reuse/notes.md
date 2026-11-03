# 다음 제작·수정에 사용할 관리 지침 · 2026-10-11

## 현재 16차시 구조

1-11차시는 유지합니다. 12차시에는 직접 입력한 값의 선 그래프·키와 몸무게 산점도·막대그래프를, 13차시에는 학생 자료·학교별 학생 수·공공데이터 API·저장과 불러오기를 둡니다. 14차시는 Matplotlib, 15차시는 Pandas, 16차시는 자율 프로젝트입니다. 코코봇 장비 실습은 추가하지 않습니다.

실습 카드 41개, 원고 컨테이너 170개, 실행 코드 12개, 순서도 4개, 이미지 30개·배치 31곳을 유지합니다. 원본 과제·데이터·위젯·결과를 우선하고 임의 숫자 예시·가상 AI 대화·새 앱 과제를 추가하지 않습니다. 원본이 입력값을 정하지 않은 활동은 학생이 직접 입력하도록 둡니다.

## 학생용 문구와 조판

학생용 본문에는 기준 교재의 대조·출처 쪽수·과거 실습 번호·제작 과정·PDF 안내를 넣지 않습니다. 이미지 캡션은 보이는 입력과 동작·결과를 설명합니다. 오류 정정 고지는 정확한 개념 설명으로 바꿉니다. 출처와 수정 근거는 practice-source-review.md, practice-source-map.json, source-audit.md에서 관리합니다. AI 답변의 근거 확인처럼 학습에 필요한 자료 비교 활동은 유지합니다.

본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt와 현재 이미지 픽셀·출력 폭·비율을 유지합니다. 흰 배경·선명한 글자와 도형·둥근 실습 상자를 사용하고 삼육보건대 로고를 넣지 않습니다. 연속된 짧은 설명·표·완료 확인을 읽는 순서대로 함께 배치합니다. 차시 시작 아래에 충분한 공간이 있으면 다음 개념을 함께 놓습니다. 대형 빈 기록칸과 반복 안내를 자동으로 추가하지 않습니다.

## 생성과 검증

현재 학생용 PDF는 output/pdf/vibe-coding-16-apps.pdf, A4 142쪽입니다. 원고·metadata의 차시 번호와 예제 파일 이름을 함께 유지합니다. Node 앱 파서·Python 패키지·필요 글꼴을 준비한 뒤 저장소 루트에서 실행합니다.

```powershell
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/vibe-coding-16-apps.pdf
python scripts/review_textbook_pdf.py --pdf output/pdf/vibe-coding-16-apps.pdf --dest tmp/pdfs/apps-review
python scripts/report_apps_edition.py
```

보고 스크립트는 조판과 전체 렌더링 검증 이후에 실행합니다. 이전 학생판과의 비교 기준은 previous-reports/20261011-before-no-robot입니다. PDF 글꼴은 Wanted Sans·학교안심 칠판지우개·Windows Consolas입니다. Canva 제작은 skill/coala-canva-textbook/SKILL.md와 flowchart-canva.md를 참고하고, 현재 독립 PDF의 쪽수와 Canva 자동 생성 쪽수를 구분합니다.
