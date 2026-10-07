# 다른 컴퓨터에서 이어서 작업하기

2026-10-07 기준. 최신 16차시 교재의 원고, 이미지, 예제 코드와 Canva 앱 소스는 이 저장소의 **feat/python-vibe-sample** 브랜치에 있다.

## 1. 저장소 받기

Git을 설치한 컴퓨터의 터미널에서 실행한다.

```powershell
git clone --branch feat/python-vibe-sample --single-branch https://github.com/AnTaeMin/coala-book-system.git
cd coala-book-system
```

이미 받은 저장소라면 변경 사항을 먼저 저장하거나 커밋한 뒤 다음을 실행한다.

```powershell
git fetch origin
git switch feat/python-vibe-sample
git pull --ff-only origin feat/python-vibe-sample
```

저장소가 비공개인 경우 접근 권한이 있는 GitHub 계정으로 로그인한다. 파일 경로는 복제한 폴더를 기준으로 사용한다. 이전 컴퓨터의 C: 드라이브 경로를 그대로 사용할 필요는 없다.

## 2. 작업 파일 확인

- 원고: `coala-book-md/vibe-coding-16/book.md`
- 차시별 원고: 같은 폴더의 `ch01.md`부터 `ch16.md`
- 현재 이미지 28개: `coala-book-md/vibe-coding-16/assets/source-20261006/`
- 이미지 미리보기: 같은 교재 폴더의 `asset-review.html`을 브라우저로 연다.
- 원본 출처·수정 사항: 같은 교재 폴더의 `source-audit.md`
- 제작 조건: 같은 교재 폴더의 `notes.md`
- 원본 PDF: 저장소 루트의 `(flet내용 추가)AI와 함께하는 앱 개발  업데이트 수정본(삼육_최종)의 사본.pdf`
- 원고·이미지 배포 묶음: `coala-book-md/vibe-coding-16-source-revised.zip`

원고와 assets의 상대 경로를 유지한다. ZIP만 받으면 원고·이미지·예제 코드를 사용할 수 있지만, Canva 앱 소스와 제작 스킬까지 이어서 작업하려면 저장소를 복제한다.

## 3. Canva 앱 설치와 원고 검증

프로젝트의 요구 사항은 Node.js 22 또는 24와 npm 11이다. Node.js 설치 후 터미널을 다시 열어 버전을 확인한다.

```powershell
node --version
npm --version
cd canva-app
npm ci
npm run validate -- ../coala-book-md/vibe-coding-16/book.md --layout
```

원고 검증은 Canva 로그인 없이 실행할 수 있다. 현재 검사 기준은 원고 컨테이너 183개, 예상 Canva 본문 190장, 이미지 파일 28개다. 표지와 목차는 이 본문 수에 포함되지 않는다.

## 4. Canva 연결과 실행

새 컴퓨터에서는 해당 Canva 계정으로 로그인하고 앱을 연결한다. 로그인 정보와 로컬 .env는 저장소에 포함하지 않는다.

```powershell
npx @canva/cli login
npx @canva/cli apps link
npm start
```

Canva Developer Portal에서 사용할 앱의 Development URL을 `http://localhost:8080`으로 설정하고 `canva:design:content:read`, `canva:design:content:write` 권한을 확인한다. 기존 앱을 사용할 수 있는 계정이면 그 앱을 선택한다.

앱 미리보기에서 현재 `book.md`를 선택하고 이미지가 있는 교재 폴더를 함께 선택한다. 원본 디자인은 보존하고 제작 사본에서 진행한다. 자세한 절차는 저장소 README.md와 교재 notes.md를 따른다.

기존 제작 사본: https://www.canva.com/design/DAHXGrp6T5Q/LJk3hNHWt6oKX2ACnx_87w/edit

**기존 Canva 디자인과 209쪽 PDF에는 이번 PDF 기반 수정 원고가 아직 반영되지 않았다.** 다른 컴퓨터에서 이번 원고를 재생성한 뒤 표지·목차·순서도 4개와 실제 배치를 확인하고 PDF를 새로 내보낸다. 작은 원본 캡처의 해상도 한계도 인쇄 검토 때 확인한다.

## 5. Python 예제 실행

예제 검증에 사용한 환경은 Python 3.10.11이다. 이 버전 계열의 Python을 사용할 때 저장소 루트에서 가상 환경을 만들고 확인된 라이브러리 버전을 설치할 수 있다.

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r coala-book-md/vibe-coding-16/examples/source-based/requirements.txt
.venv\Scripts\python.exe coala-book-md/vibe-coding-16/examples/source-based/ch04-family-code.py
.venv\Scripts\python.exe coala-book-md/vibe-coding-16/examples/source-based/ch13-scatter.py
```

Python 실행 명령이 다른 컴퓨터에서는 해당 Python 실행 파일을 사용한다. Matplotlib 예제는 그래프 창을 표시한다. 이 예제들은 독립 Python 코드이며, 알고플로 GUI 생성·저장이나 실제 코코봇 연결을 대신하지 않는다. 해당 플랫폼과 장비 설정은 수업 환경에서 확인한다.

## 6. 에이전트에게 이어서 요청하기

아래처럼 저장소 안의 파일을 지정한다.

```text
skill/coala-canva-textbook/SKILL.md를 따라
coala-book-md/vibe-coding-16/book.md와 notes.md를 참고해 작업해줘.
source-audit.md의 원본 오류 수정 사항과 assets/source-20261006의 이미지 28개를 유지해줘.
삼육보건대 로고를 넣지 말고 흰 배경·그림자 제거·긴 프롬프트의 둥근 사각형 배치를 적용해줘.
현재 원고를 기준으로 Canva 제작 사본에 반영하고 실제 배치와 출력 결과를 확인해줘.
```

작업 상태와 남은 항목은 `coala-book-md/vibe-coding-16/canva-production-status.md` 및 `handover.md`에 있다.
