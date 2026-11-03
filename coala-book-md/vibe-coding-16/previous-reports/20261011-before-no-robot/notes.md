# 다음 제작·수정에 사용할 지침 · 2026-10-11

이 문서는 제작·검증을 위한 관리 지침입니다. 학생용 교재 본문에 넣지 않습니다.

## 원본과 실습

지정된 루트의 158쪽 앱 개발 PDF를 기준으로 16차시를 유지합니다. practice-source-map.json과 practice-source-review.md의 실습별 출처를 확인하세요.

원본에 있는 과제·데이터·위젯·결과를 우선합니다. 원본이 값을 정하지 않은 경우 임의 고정 입력값이나 테스트 목록을 넣지 않습니다. 가상 AI 응답·오류 이야기·추가 앱 목록·발표 과제를 넣지 않습니다. 설명과 완료 기준은 해당 실습에 필요한 만큼 작성합니다.

Matplotlib·Pandas 코드는 원본 데이터를 유지하고 독립 실행 초기화·출력과 원본 오타만 보완합니다. 변경한 코드는 실행 결과를 확인한 뒤 사용합니다. 원본 GUI의 message, fch와 코코봇 함수는 실제 수업 도구에서 확인합니다.

## 이미지와 지면 통합

asset-manifest.json의 현재 이미지 33개를 사용합니다. source-20261006과 source-20261010 두 폴더가 필요합니다. 원본 픽셀·가로세로 비율·현재 출력 폭을 유지합니다.

삼육보건대 로고를 넣지 않습니다. 흰 배경, 선명한 글자와 도형, 그림자 없는 배치를 사용합니다. 긴 텍스트는 둥근 사각형에 넣습니다. 본문 14pt·행간 28pt·소제목 15pt·단원 제목 25pt를 유지합니다.

같은 차시의 연속된 짧은 개념·표·실습 설명·완료 확인은 읽는 순서를 지켜 한 장에 합칩니다. 차시 시작 아래에 공간이 충분하면 다음 짧은 개념을 함께 배치합니다. 원고 컨테이너 179개는 보존하고 PDF 조판에서 통합합니다. 새로운 실습과 자동 대형 빈 기록칸을 추가하지 않습니다. 실습 카드·차시별 시작·순서도를 구분하고, 내용이 넘치면 글자를 줄이지 않고 페이지를 나눕니다.

현재 학생용 완성본은 A4 149쪽입니다. 기존 6·7쪽은 새 6쪽에 통합했습니다. 다른 대응은 page-compaction-review.md에서 확인합니다.

## PDF와 Canva

현재 PDF는 output/pdf/vibe-coding-16-student.pdf입니다. 저장소 루트에서 다음 순서로 생성·검증합니다. 원고 파서와 필요한 폰트·Python 패키지를 먼저 준비합니다.

```powershell
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/vibe-coding-16-student.pdf
python scripts/review_textbook_pdf.py --pdf output/pdf/vibe-coding-16-student.pdf --dest tmp/pdfs/student-review
python scripts/report_page_compaction.py
```

PDF 폰트는 tmp/pdfs/fonts의 Wanted Sans와 학교안심 칠판지우개, Windows Consolas를 사용합니다. 보고 스크립트는 원고와 예시를 변경하지 않으며, 이전 원본 실습 재작성 스크립트를 실행할 필요가 없습니다.

Canva 제작 시 skill/coala-canva-textbook/SKILL.md를 적용하고 제작 사본을 사용합니다. 네이티브 순서도 규칙은 flowchart-canva.md를 참고하세요. 현재 페이지 통합은 독립 PDF 조판에 적용되어 있습니다.


학생용 본문에서는 원본 대조·출처 쪽수·제작 과정과 PDF 안내 문구를 제외했습니다. 실습 데이터·코드·출력·순서도는 유지했으며, 출처와 제작 기록은 교재 밖의 관리 문서에 보관합니다.
