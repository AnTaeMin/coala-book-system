# 다음 제작·수정에 사용할 지침

## 원본과 실습

지정된 루트의 158쪽 앱 개발 PDF를 기준으로 16차시를 유지합니다. practice-source-map.json과 practice-source-review.md의 실습별 출처를 확인하세요. 다른 PDF나 과거 공부 기록 앱 초안으로 되돌리지 않습니다.

실습은 원본에 있는 과제·데이터·위젯·결과를 우선합니다. 원본이 값을 정하지 않은 경우 임의 고정 입력값이나 테스트 목록을 만들어 교재에 넣지 않습니다. 새 가상 AI 응답, 가상 오류 이야기, 추가 앱 목록과 발표 과제를 넣지 않습니다. 설명과 완료 기준은 해당 실습에 필요한 만큼 작성합니다.

Matplotlib·Pandas 코드는 원본 데이터를 유지하고 독립 실행 초기화·출력과 원본 오타만 보완합니다. 변경한 코드는 실행 결과를 확인한 뒤 사용합니다. 원본 GUI의 message, fch와 코코봇 함수는 실제 수업 도구에서 확인합니다.

## 이미지와 지면

현재 asset-manifest.json의 이미지 33개를 사용합니다. source-20261006과 source-20261010 두 폴더가 필요합니다. 원본 픽셀과 가로세로 비율을 유지하고 출처 쪽수·실제 실행 결과를 구분합니다.

삼육보건대 로고를 넣지 않습니다. 흰 배경, 선명한 글자와 도형, 그림자 없는 배치를 사용합니다. 긴 텍스트는 둥근 사각형에 넣습니다. 글자 크기와 행간을 줄이거나 지면을 채우려고 새 활동을 자동으로 추가하지 않습니다. 같은 실습의 짧은 설명은 읽는 순서를 유지하여 합칠 수 있습니다.

## PDF와 Canva

현재 독립 PDF는 output/pdf/vibe-coding-16-final.pdf입니다. scripts/finalize_textbook_pdf.py와 scripts/review_textbook_pdf.py로 재생성·검증합니다. PDF 폰트는 tmp/pdfs/fonts에 준비한 Wanted Sans와 학교안심 칠판지우개, Windows Consolas를 사용합니다.

Canva 제작 시 skill/coala-canva-textbook/SKILL.md를 적용하고 원본 Canva를 보존한 제작 사본을 사용합니다. 네이티브 순서도 규칙은 flowchart-canva.md를 참고하세요. 독립 PDF의 벡터 도형과 Canva 네이티브 요소는 구분합니다.
