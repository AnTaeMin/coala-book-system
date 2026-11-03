# 바이브 코딩 32차시 교재 · 2026-11-03

현재 16차시 최종 편집본을 각각 1·2부로 나눈 32차시판입니다. 기존 원고와 PDF는 보존합니다.

- [재검토한 학생용 PDF](../../output/pdf/vibe-coding-32-coala-access-reviewed.pdf)
- [전체 원고](book.md), 차시별 원고 ch01.md~ch32.md
- [32차시 수업 구성](curriculum.md), [교사용 안내](teacher-guide.md)
- [분할 대응표·보존 검증](session-split.json)

내용·화면 재검토 결과는 [검토 기록](recheck-review.md)과 [검증 요약](validation-summary.md)을 확인합니다.

기존 162개 원고 컨테이너에 2부 도입 16개를 추가하여 178개가 됩니다. 실습 37개, 공통 생성 코드 1개·그리기 코드 7개, 순서도 4개를 유지합니다. 기존 화면은 보존하고 전자책 미리보기만 현재 32차시 표지·목차로 갱신합니다. 실습 번호는 새 차시에 맞춥니다.

재생성: `python scripts/split_textbook_32.py` → `node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-32/book.md tmp/pdfs/book-spec-32.json` → `python scripts/build_textbook_32_pdf.py` → `python scripts/prepare_textbook_32_preview.py --pdf output/pdf/vibe-coding-32-coala-access-reviewed.pdf` → `python scripts/build_textbook_32_pdf.py`. 저장소 루트에서 실행합니다. 분할 스크립트는 16차시 원고에서 32차시 원고를 다시 만드므로, 32차시 원고에 직접 수정한 내용이 있으면 먼저 보존합니다.
