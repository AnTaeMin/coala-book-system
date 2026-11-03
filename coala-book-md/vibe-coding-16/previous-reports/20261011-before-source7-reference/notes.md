# 다음 수정·재생성 관리 지침 · 2026-10-11

## 현재 구성

12차시 Matplotlib → 13차시 입력 Chart → 14차시 학생 자료·저장 → 15차시 Pandas → 16차시 자율 프로젝트

16차시·167개 원고 컨테이너·40개 실습 카드·12개 실행 코드·4개 순서도. PNG 34개·벡터 PDF 5개·전체 배치 35곳. 공공데이터 API 과정·인증키 입력·지하철 API 과제를 다시 넣지 않습니다. 14차시는 학생 자료·학교별 학생 수·저장과 불러오기 3개 실습입니다. 기존 과제·입력값·위젯·코드·결과를 우선하고 새 앱·임의 숫자 과제를 추가하지 않습니다.

## 학생용 내용과 지면

계산기 2의 57·58쪽 결과 위젯 설명 두 문장을 fld3로 바로잡았습니다. 별도의 Text·구구단 실습에서 사용하는 txt1은 유지합니다. 상세 검증은 calculator-widget-correction.json에 있습니다.

학생용 본문에는 원본 대조·출처 쪽수·제작 과정·PDF 안내 문구를 넣지 않습니다. 출처와 검증 기록은 별도 관리 문서에 보관합니다. 캡션은 보이는 내용·입력·동작·결과를 설명합니다. AI 답변의 근거 확인은 학습 내용으로 유지합니다. 7쪽은 역사·문학 질문의 학습용 가상 오답이며 실제 AI 출력으로 소개하지 않습니다. 사실 확인 출처는 hallucination-source-review.md/json에 보관합니다.

5쪽 요약 그림은 assets/ch01/ai-human-summary.pdf를 인쇄 벡터로 사용하고 같은 이름의 PNG를 Canva용으로 준비했습니다. 원본 순서도 4개는 assets/source-flowcharts의 벡터 PDF와 PNG를 사용합니다. 본문 14pt·행간 28pt·소제목 15pt·차시 제목 25pt를 유지합니다. 흰 배경·선명한 글자·둥근 실습 상자를 사용하고 기관 로고·대형 빈 기록칸을 추가하지 않습니다. 짧은 연속 내용은 읽는 순서대로 함께 배치합니다.

## 일상 수정·재생성

각 chXX.md를 수정한 후 전체 원고 조합→파서→조판→전체 렌더링→보고 순서로 진행합니다. 저장소 루트에서 Node 앱 파서·Python 패키지·필요 글꼴을 준비합니다.

```powershell
python scripts/finalize_student_manuscript.py
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/vibe-coding-16-fld3.pdf
python scripts/review_textbook_pdf.py --pdf output/pdf/vibe-coding-16-fld3.pdf --dest tmp/pdfs/fld3-review
python scripts/report_apps_edition.py
```

이전 과정 재편 스크립트나 prepare_source_flowcharts.py는 일상 편집 때 실행하지 않습니다. 후속 수정을 덮어쓸 수 있습니다. prepare_source_flowcharts.py는 원본 순서도 재추출 때만 사용하며 원본 PDF·PyMuPDF가 필요하고 ch04/ch07의 문구도 적용합니다. 현재 포함된 벡터 자산으로 PDF를 만드는 데는 원본 PDF·PyMuPDF가 필요하지 않으며 pypdf를 사용합니다.

flow-source-map.json의 flowchart_sha256와 해당 원고 블록을 일치시킵니다. 논리를 바꾸면 그림·문구·맵을 함께 검토합니다. 보고는 전체 렌더링 검토 이후 실행합니다. 직전 비교 기준은 previous-reports/20261011-before-second-compaction입니다. 묶음에는 이전 metadata·코드 검증 JSON과 수정 근거 문서만 포함합니다. 이전 PDF·이미지·원고는 포함하지 않습니다.

원본 파일이 있으면 해시를 직접 확인하고 없으면 보존 출처 기록과 포함 자산의 해시를 검증합니다. 본문 글꼴은 Wanted Sans·Windows Consolas이며 순서도는 원본 벡터 글자·도형을 보존합니다. Canva 안내는 flowchart-canva.md를 참고합니다.
