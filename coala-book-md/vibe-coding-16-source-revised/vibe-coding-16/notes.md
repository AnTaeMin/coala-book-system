# 원고 수정·다른 컴퓨터 전달 · 2026-10-27

현재 Flet 구조 반영본: output/pdf/vibe-coding-16-upstream.pdf, A4 132쪽. 16차시·162개 원고 컨테이너·37개 실습·공통 생성 코드 1개·그리기 코드 7개·4개 순서도. PNG 40개·벡터 PDF 7개·이미지 배치 42곳.

12차시 Matplotlib 선·마커 → 13차시 Matplotlib 막대·산점도 → 14차시 입력 Chart → 15차시 학생 자료·저장 → 16차시 프로젝트

## 다른 컴퓨터에서 준비

최신 저장소를 복제하고 앱 패키지를 설치한 뒤 전달ZIP을 같은 저장소에 덮어씁니다. ZIP의 vibe-coding-16 폴더는 coala-book-md/vibe-coding-16에, canva-app·scripts·output·tmp는 저장소 루트의 같은 위치에 배치합니다. ZIP에 포함한 export-book-spec.cjs도 반드시 canva-app/scripts에 복사합니다.

```powershell
git clone https://github.com/kkh1466/coala-book-system.git
cd coala-book-system
npm --prefix canva-app install
```

반영 기준 커밋은 9723e244e225c4a300b6f251a766b39de46e63f6입니다. 저장소 원본과 수정된 전달 원고를 구분하며 ZIP을 덮어쓴 뒤 일회성 개편 스크립트를 실행하지 않습니다.

## 일반 수정과 재생성

각 chXX.md를 수정한 뒤 book.md를 조립합니다. 기존 데이터·실습 조건·코드·그림 폭을 유지하고 표지·학생 본문에 제작 메모를 넣지 않습니다.

```powershell
python scripts/finalize_student_manuscript.py
$chapters = (Get-ChildItem coala-book-md/vibe-coding-16 -Filter ch??.md).FullName
$validation = node canva-app/scripts/validate.cjs --layout --json coala-book-md/vibe-coding-16/book.md @chapters
[IO.File]::WriteAllText("coala-book-md/vibe-coding-16/validation-full.json", ($validation -join [Environment]::NewLine), [Text.UTF8Encoding]::new($false))
node canva-app/scripts/export-book-spec.cjs coala-book-md/vibe-coding-16/book.md tmp/pdfs/book-spec.json
python scripts/check_practice_code.py --review-date 2026-10-27
python scripts/finalize_textbook_pdf.py --output output/pdf/vibe-coding-16-upstream.pdf --review-date 2026-10-27
python scripts/review_textbook_pdf.py --pdf output/pdf/vibe-coding-16-upstream.pdf --dest tmp/pdfs/current-review
python scripts/audit_current_edition.py --review-date 2026-10-27
```

validation-full.json은 book.md와 16개 차시가 모두 통과한 현재 결과로 갱신한 뒤 보고서를 실행합니다. Node 명령이 실패하면 다음 명령으로 진행하지 않고 오류를 먼저 수정합니다.

restructure_no_pandas.py·restructure_graph_first.py는 과거 원고에서 일회성으로 구조를 변경한 스크립트입니다. 일상 편집에서 다시 실행하면 후속 수정이 지워질 수 있으므로 사용하지 않습니다. prepare_source_flowcharts.py는 원본 자산 재추출 때만 사용하며 일반 PDF 재생성에는 기준 PDF·PyMuPDF가 필요하지 않습니다. 순서도 YAML을 바꿀 때는 대응 flow-source-map 해시도 함께 갱신해야 합니다.

## 환경과 전달 파일

PDF 자체는 설치 없이 열 수 있습니다. 재조판에는 Python의 reportlab·pypdf·Pillow와 원고 파서용 Node.js, 전체 렌더용 도구가 필요합니다. 코드 예제에는 examples/source-based/requirements.txt의 Matplotlib·NumPy를 설치합니다. ZIP의 tmp/pdfs/fonts에는 사용한 비시스템 글꼴 4개를 포함합니다. Windows의 Consolas는 시스템 글꼴을 사용합니다. 현재 비교에 필요한 수정 전 metadata·자산·코드 JSON을 previous-reports/20261027-before-content-code-review에 포함합니다. 과거 PDF·이미지·원고는 전달 ZIP에서 제외합니다.

원본 파일이 없는 컴퓨터에서는 포함 자산·벡터의 해시와 보존 출처 기록을 검사합니다. 로컬에 기준 PDF가 있을 때만 그 파일의 SHA-256도 직접 검증합니다. 원본 기준 파일 동일성 기록은 이전 기준 변경의 증거이며, 이번 16차시 개편이 원고 불변이었다는 뜻이 아닙니다.

Matplotlib을 선·마커와 막대·산점도 두 차시로 나누고 입력 Chart를 14차시, 학생 자료·저장을 15차시에 배치했습니다. Pandas 차시의 실습 3개·코드 5개·텍스트 출력 5개·결과 표 이미지 1개를 제외했습니다. Divider를 제외한 두 Image 배치 그림으로 바꾸고 교재의 저장·불러오기 과정 사진 5개를 추가했습니다. GUI(그래픽 사용자 인터페이스) 구성 설명과 예시를 추가했습니다. 8차시는 Field 복사 화면에서 입력 칸·버튼·표시 영역의 역할을 설명하고, 15차시는118쪽 저장 앱 구성 화면을 사용합니다. 버튼·Field·Text·계산기·Table·Chart·저장 화면의 위젯 위치·이름·역할을 기존 실습에 연결했습니다. 새 실습·코드는 추가하지 않았습니다. 최신 저장소의 공통 설명을GUI수업에 맞게 반영하여 사람과AI의 역할, GUI요청·실행 결과 확인·수정을 기존 개념에서 설명했습니다. 노트북 셀에 코드를 넣고 실행하는 과정과 노트북 화면4개는 이번 수업 방식에 맞지 않아 제외했습니다. 기존162개 원고ID·37개 실습·7개 Python코드·이미지 구성을 유지합니다.

직전 GUI130쪽판과 제작 기록은 previous-reports/20261011-before-upstream-update에 보관했습니다. 이전128쪽 과정 개편판과 source7 기준134쪽판의 기록도 previous-reports에 보존하며 현재판의 검증과 구분합니다.

## 실제 Flet 실습 앱 확인

examples/flet-practices/README.md의 순서로 requirements.txt를 설치하고 gallery.py를 실행합니다. 브라우저가 연결된 실제 Page에서 위젯·계산·표·차트·조건과 반복을 점검합니다. 코드 조각은 독립 실행 파일이 아니라 기존 fig_cht1·ax_cht1에 적용하는 그리기 부분입니다. 코드 자체를 수정하면 대응 code-specs.json도 함께 갱신한 뒤 조립·검증합니다.

현재 실행 결과는 gui-results.json, 현재 종합 검토는 flet-runtime-review.md입니다. 학교 클라우드 저장은 로컬 JSON 저장 검사와 구분합니다.
