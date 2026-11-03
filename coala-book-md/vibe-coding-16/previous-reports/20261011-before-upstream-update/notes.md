# 원고 수정·다른 컴퓨터 전달 · 2026-10-11

현재 완성본: output/pdf/vibe-coding-16-gui.pdf, A4 130쪽. 16차시·162개 원고 컨테이너·37개 실습·7개 Python 코드·4개 순서도. PNG 39개·벡터 PDF 7개·이미지 배치 41곳.

12차시 Matplotlib 선·마커 → 13차시 Matplotlib 막대·산점도 → 14차시 입력 Chart → 15차시 학생 자료·저장 → 16차시 프로젝트

## 일반 수정과 재생성

각 chXX.md를 수정한 뒤 book.md를 조립합니다. 기존 데이터·실습 조건·코드·그림 폭을 유지하고 표지·학생 본문에 제작 메모를 넣지 않습니다.

```powershell
python scripts/finalize_student_manuscript.py
$chapters = (Get-ChildItem coala-book-md/vibe-coding-16 -Filter ch??.md).FullName
$validation = node canva-app/scripts/validate.cjs --layout --json coala-book-md/vibe-coding-16/book.md @chapters
[IO.File]::WriteAllText("coala-book-md/vibe-coding-16/validation-full.json", ($validation -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/finalize_textbook_pdf.py --output output/pdf/vibe-coding-16-gui.pdf
python scripts/review_textbook_pdf.py --pdf output/pdf/vibe-coding-16-gui.pdf --dest tmp/pdfs/gui-review
python scripts/report_apps_edition.py
```

validation-full.json은 book.md와 16개 차시가 모두 통과한 현재 결과로 갱신한 뒤 보고서를 실행합니다. Node 명령이 실패하면 다음 명령으로 진행하지 않고 오류를 먼저 수정합니다.

restructure_no_pandas.py·restructure_graph_first.py는 과거 원고에서 일회성으로 구조를 변경한 스크립트입니다. 일상 편집에서 다시 실행하면 후속 수정이 지워질 수 있으므로 사용하지 않습니다. prepare_source_flowcharts.py는 원본 자산 재추출 때만 사용하며 일반 PDF 재생성에는 기준 PDF·PyMuPDF가 필요하지 않습니다. 순서도 YAML을 바꿀 때는 대응 flow-source-map 해시도 함께 갱신해야 합니다.

## 환경과 전달 파일

PDF 자체는 설치 없이 열 수 있습니다. 재조판에는 Python의 reportlab·pypdf·Pillow와 원고 파서용 Node.js, 전체 렌더용 도구가 필요합니다. 코드 예제에는 examples/source-based/requirements.txt의 Matplotlib·NumPy를 설치합니다. ZIP의 tmp/pdfs/fonts에는 사용한 비시스템 글꼴 4개를 포함합니다. Windows의 Consolas는 시스템 글꼴을 사용합니다. 이 보고서에 필요한 직전판 metadata·실습·자산·코드 JSON을 archive 상대 경로에 포함하고 과거 PDF·이미지·원고는 포함하지 않습니다.

원본 파일이 없는 컴퓨터에서는 포함 자산·벡터의 해시와 보존 출처 기록을 검사합니다. 로컬에 기준 PDF가 있을 때만 그 파일의 SHA-256도 직접 검증합니다. 원본 기준 파일 동일성 기록은 이전 기준 변경의 증거이며, 이번 16차시 개편이 원고 불변이었다는 뜻이 아닙니다.

Matplotlib을 선·마커와 막대·산점도 두 차시로 나누고 입력 Chart를 14차시, 학생 자료·저장을 15차시에 배치했습니다. Pandas 차시의 실습 3개·코드 5개·텍스트 출력 5개·결과 표 이미지 1개를 제외했습니다. Divider를 제외한 두 Image 배치 그림으로 바꾸고 교재의 저장·불러오기 과정 사진 5개를 추가했습니다. GUI(그래픽 사용자 인터페이스) 구성 설명과 예시를 추가했습니다. 8차시는 Field 복사 화면에서 입력 칸·버튼·표시 영역의 역할을 설명하고, 15차시는118쪽 저장 앱 구성 화면을 사용합니다. 버튼·Field·Text·계산기·Table·Chart·저장 화면의 위젯 위치·이름·역할을 기존 실습에 연결했습니다. 새 실습·코드는 추가하지 않았습니다.

직전128쪽판과 제작 기록은 previous-reports/20261011-before-gui-examples에 보관했습니다. source7 기준134쪽판은 previous-reports/20261011-before-no-pandas-divider에 있으며 이전 통합·과정 개편 기록은 현재판의 검증과 구분합니다.
