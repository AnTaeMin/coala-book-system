'''Verify and package the current Flet-aligned textbook and real callback results.

Run only after code execution, browser-connected GUI checks and full PDF review.
Historical code hashes and page counts are compared rather than imposed on the
new revision. Missing or failed GUI evidence always prevents delivery.
'''
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'coala-book-md/vibe-coding-16'
PDF = ROOT / 'output/pdf/vibe-coding-16-upstream.pdf'
SCREENSHOT = ROOT / 'output/pdf/flet-practice-runtime-check.png'
SITE_SCREENSHOT = ROOT / 'output/pdf/sl42-practice-runtime-check.png'
BASE = BOOK / 'previous-reports/20261027-before-flet-runtime'
SOURCE_URL = 'https://coala-web-v2.coala.services/ko/student/sl42'
ALGORITHM_IDS = {'ch04-family-code', 'ch05-exercise-code', 'ch05-caffeine-code',
                 'ch06-sleep-code', 'ch07-pass-code', 'ch07-movie-code'}
GUI_IDS = {'008-1', '008-2', '008-3', '009-1', '009-2', '009-3', '009-4',
           '010-1', '010-2', '010-3', '010-4', '010-5', '011-1',
           'ch14-practice-1', 'ch14-practice-2', 'ch14-practice-3',
           'ch15-practice-data', 'ch15-practice-school', 'ch15-practice-3'}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def write(name, text):
    (BOOK/name).write_text(text.rstrip()+'\n', encoding='utf-8')


def bundle_names(path):
    with zipfile.ZipFile(path) as archive:
        return archive.namelist()


def code_blocks(text):
    blocks = {}
    for page in re.finditer(r':::page\{[^\n]*id="([^"]+)"[^\n]*\}\n(.*?)(?=\n:::\s*(?:\n|$))', text, re.S):
        code = re.search(r'```python\n(.*?)\n```', page[2], re.S)
        if code:
            assert page[1] not in blocks
            blocks[page[1]] = code[1]
    return blocks


def validate(args):
    from PIL import Image
    from pypdf import PdfReader
    metadata = read(PDF.with_suffix('.json'))
    qa = read(args.qa)
    codes, specs = read(BOOK/'code-results.json'), read(BOOK/'code-specs.json')
    assets, gui = read(BOOK/'asset-manifest.json'), read(BOOK/'gui-results.json')
    site = read(BOOK/'sl42-runtime-results.json')
    model, validations = read(ROOT/'tmp/pdfs/book-spec.json'), read(BOOK/'validation-full.json')
    manuscript = (BOOK/'book.md').read_text(encoding='utf-8')
    document = PdfReader(PDF)
    pages = len(document.pages)
    assert pages > 0 and pages == metadata['pages'] == qa['pages'] == qa['renderedPages']
    assert sha(PDF) == metadata['pdfSha256'] == qa['pdfSha256']
    assert sha(BOOK/'book.md') == metadata['manuscriptSha256'] == qa['manuscriptSha256']
    assert len(validations) == 17 and all(v['ok'] and not v['issues'] for v in validations)
    for key in ('outOfPageGlyphs', 'missingSourceIds', 'contentsErrors', 'codeContentDifferences',
                'replacementGlyphPages', 'boxOverflows', 'editorialReferencePages',
                'excludedTopicPages', 'robotReferencePages', 'notebookWorkflowPages'):
        assert not qa[key], (key, qa[key])
    ids = re.findall(r':::page\{[^\n]*id="([^"]+)"', manuscript)
    assert len(ids) == len(set(ids)) == len(model['pages']) == 162
    assert set(ids) == {p['id'] for p in model['pages']}
    assert Counter(p['type'] for p in model['pages'])['practice-opening'] == 37
    assert len(metadata['images']) == qa['images'] == 42
    assert qa['flowcharts'] == 4 and len(document.outline) == 16
    contents = [i for i,p in enumerate(metadata['layout']) if p['type']=='contents']
    links = sum(len(document.pages[i].get('/Annots', [])) for i in contents)
    assert links == 16
    assert qa['manuscriptCodeBlocks'] == qa['printedCodeBlocks'] == len(specs) == 8
    assert codes['executed_blocks'] == codes['passed'] == 8
    assert codes['practice_blocks'] == 7 and codes['setup_blocks'] == 1 and codes['practice_runs'] == 14
    assert codes['reviewed_date'] == gui['reviewed_date'] == args.review_date
    assert codes['fallback']['status']=='passed' and not codes['fallback']['warnings']
    assert codes['chart_binding'] and codes['repeated_updates']
    assert 'flet_charts' in codes['matplotlib_backend']
    assert codes['flet'] == codes['flet_charts'] == gui['flet'] == gui['flet_charts'] == '0.86.0'
    executed = {item['page_id']:item for item in codes['records']}
    printed = code_blocks(manuscript)
    setup = [item for item in specs if item['role']=='generated-chart-setup']
    practices = [item for item in specs if item['role']=='drawing-event-body']
    assert len(setup)==1 and len(practices)==7
    assert {item['page_id'] for item in specs} == set(executed) == set(printed)
    for item in specs:
        path = BOOK/'examples/source-based'/item['file']
        code = path.read_text(encoding='utf-8').rstrip()
        assert code == item['code'] == printed[item['page_id']]
        result = executed[item['page_id']]
        assert hashlib.sha256(code.encode('utf-8')).hexdigest() == result['code_sha256']
        assert result['status']=='passed' and result['chart_binding'] and not result['warnings']
        compile(code, str(path), 'exec')
        if item['role']=='drawing-event-body':
            assert result['draw_count']==2 and result['repeated_updates']
            assert 'plt.subplots' not in code and 'plt.show' not in code
            assert 'ax_cht1.clear()' in code
            assert 'tight_layout' not in code and 'draw_idle' not in code
            assert result['automatic_refresh_outside_logic']
    setup_code = setup[0]['code']
    assert setup_code.index('import flet_charts as fch') < setup_code.index('import matplotlib.pyplot as plt')
    assert 'fig_cht1, ax_cht1 = plt.subplots()' in setup_code
    assert 'figure=fig_cht1' in setup_code and 'fch.MatplotlibChart' in setup_code
    plot_ids = {item['page_id'] for item in practices}
    assert gui['tested']==gui['passed']==len(gui['records'])==32 and gui['failed']==0
    gui_records = {item['id']:item for item in gui['records']}
    assert len(gui_records)==32 and set(gui_records)==GUI_IDS | ALGORITHM_IDS | plot_ids
    assert all(item['status']=='passed' for item in gui['records'])
    assert gui['execution']=='real-browser-connected-flet-page; real control event callbacks'
    assert gui['cloud_project_save_tested'] is False
    assert site['source_url'] == SOURCE_URL
    assert site['tested'] == site['passed'] == 32 and site['failed'] == 0
    assert site['logic_refresh_calls_excluded'] and site['cloud_project_save_tested'] is False
    assert {v['id'] for v in site['cases']} == set(gui_records)
    assert site['program_sha256'] == sha(BOOK/'examples/flet-practices/sl42-runtime-check.py')
    assert SITE_SCREENSHOT.is_file()
    native_logic = read(BOOK/'sl42-code-comparison.json')
    assert native_logic['source_url'] == SOURCE_URL
    assert native_logic['student_example_found'] and native_logic['excluded_calls_absent']
    assert native_logic['rendered_line_graph_verified']
    assert native_logic['student_example'].replace('\r\n','\n') == (BOOK/'examples/source-based/ch12-one-array.py').read_text(encoding='utf-8').rstrip()
    assert SCREENSHOT.is_file()
    assert len(assets['items'])==40
    vectors = [item for item in assets['items'] if item.get('vector_src')]
    assert len(vectors)==7
    for item in assets['items']:
        path = BOOK/item['src']
        assert sha(path)==item['sha256'], path
        with Image.open(path) as image:
            assert image.size==(item['width'], item['height'])
        if item.get('vector_src'):
            assert sha(BOOK/item['vector_src'])==item['vector_sha256']
    old = read(BASE/'vibe-coding-16-upstream.json')
    old_specs = {item['page_id']:item for item in read(BASE/'code-specs.json')}
    new_specs = {item['page_id']:item for item in specs}
    added_code = sorted(set(new_specs)-set(old_specs))
    changed_code = sorted(pid for pid in set(new_specs)&set(old_specs) if new_specs[pid]['code']!=old_specs[pid]['code'])
    assert added_code==[setup[0]['page_id']] and set(changed_code)==plot_ids and len(old_specs)==7
    old_assets = {item['src']:item for item in read(BASE/'asset-manifest.json')['items']}
    new_assets = {item['src']:item for item in assets['items']}
    added_assets = sorted(set(new_assets)-set(old_assets))
    assert added_assets==['assets/ch12/chart-binding.png']
    assert not set(old_assets)-set(new_assets)
    changed_assets = sorted(src for src in set(new_assets)&set(old_assets) if new_assets[src]['sha256']!=old_assets[src]['sha256'])
    expected_plots = {'assets/source-20261006/'+item['result']+'.png' for item in practices}
    assert set(changed_assets)==expected_plots
    assert all((new_assets[src]['width'], new_assets[src]['height'])==(1536,1152) for src in expected_plots)
    for name in ('README.md', 'requirements.txt', 'gallery.py', 'basic.py', 'data.py', 'plots.py'):
        assert (BOOK/'examples/flet-practices'/name).is_file(), name
    return locals()


def reports(args, current):
    metadata, codes, gui, assets = (current[key] for key in ('metadata','codes','gui','assets'))
    old, pages = current['old'], current['pages']
    def page_numbers(pid):
        return [i for i,p in enumerate(metadata['layout'],1) if pid in [p['id']]+p.get('includedSources',[])]
    review = {
        'date':args.review_date, 'edition':'flet-chart-context-16-sessions', 'sourceContractUrl':SOURCE_URL,
        'baseline':BASE.relative_to(ROOT).as_posix(), 'previousPdfPages':old['pages'], 'currentPdfPages':pages,
        'currentPdfSha256':sha(PDF), 'currentManuscriptSha256':sha(BOOK/'book.md'),
        'previousChapterPages':old['chapterPages'], 'currentChapterPages':metadata['chapterPages'],
        'chapterPagesUnchanged':metadata['chapterPages']==old['chapterPages'],
        'manuscriptContainers':162, 'practiceCards':37, 'pythonBlocks':8,
        'practiceCodeBlocks':7, 'commonSetupBlocks':1,
        'addedCodeIds':current['added_code'], 'changedCodeIds':current['changed_code'],
        'addedAssets':current['added_assets'], 'changedAssets':current['changed_assets'], 'otherAssetsUnchanged':True,
        'chartContract':{
            'imports':['flet_charts as fch','matplotlib.pyplot as plt'],
            'setup':'fig_cht1, ax_cht1 = plt.subplots(); cht1 = fch.MatplotlibChart(expand=True, figure=fig_cht1)',
            'drawing':'Reuse fig_cht1/ax_cht1/cht1; student examples contain drawing logic only; runtime handles layout and refresh externally',
            'layoutAndRefreshExcludedFromLogic':True,
            'figureInches':[6.4,4.8], 'resultImagePixels':[1536,1152], 'imageRatio':'4:3', 'separatePyplotWindow':False},
        'pythonExecution':{'passedBlocks':8,'practiceBlocks':7,'setupBlocks':1,'practiceRuns':14,'warnings':0,
                           'backend':codes['matplotlib_backend'],'fallbackPassed':True,'figureChartBindingVerified':True,'sameObjectsOnRepeat':True},
        'guiExecution':{'performed':True,'tested':32,'passed':32,'failed':0,'scope':gui['execution'],
                        'guiCases':19,'algorithmCases':6,'plotCases':7,'cloudProjectSaveTested':False,
                        'localJsonSaveLoadTested':True,'resultsSha256':sha(BOOK/'gui-results.json')},
        'sl42Execution':current['site'],
        'nativeLogicView':current['native_logic'],
        'sl42GeneratedSource':'examples/flet-practices/sl42-generated-chart.py',
        'sl42GeneratedSourceSha256':sha(BOOK/'examples/flet-practices/sl42-generated-chart.py'),
        'sl42Screenshot':'output/pdf/'+SITE_SCREENSHOT.name,
        'validation':{'manuscripts':17,'renderedPages':pages,'contentsLinks':current['links'],'bookmarks':16,
                      'pngAssets':40,'vectorAssets':7,'imagePlacements':42,'flowcharts':4},
        'setupPdfPages':page_numbers('ch12-axes'),
        'plotPdfPages':{pid:page_numbers(pid) for pid in current['changed_code']},
        'runtimeScreenshot':'output/pdf/'+SCREENSHOT.name, 'runtimeScreenshotSha256':sha(SCREENSHOT)}
    save(BOOK/'flet-runtime-review.json', review)
    save(BOOK/'upstream-edition-comparison.json', review)
    qa = dict(current['qa']); qa['reviewed_date']=args.review_date
    save(PDF.with_name(PDF.stem+'-qa.json'), qa)
    rows = ['| 코드 | 현재 PDF 쪽 |','|---|---|']
    rows += [f'| {pid} | {", ".join(map(str,page_numbers(pid)))} |' for pid in current['added_code']+current['changed_code']]
    summary = f'''# 실제 Flet 차트 구조 반영 · {args.review_date}

현재 16차시 교재는 A4 **{pages}쪽**입니다. 직전 수정본은 {old['pages']}쪽이었으며 실제 조판 결과에 맞춰 목차와 차시 시작 쪽수를 다시 계산했습니다. 162개 원고 컨테이너, 37개 실습, 순서도 4개를 유지합니다. 차트 연결 예시 그림을 추가하여 PNG 40개·벡터 PDF 7개·이미지 배치 42곳입니다.

## 반영한 코드 구조

[수업 화면]({SOURCE_URL})의 차트 생성 구조에 맞춰 공통 생성 코드 1개와 그리기 실습 7개로 정리했습니다. flet_charts를 pyplot보다 먼저 가져오고, fig_cht1·ax_cht1을 만든 뒤 같은 fig_cht1을 cht1의 figure로 연결합니다.

공통 생성 부분은 앱 구성 때 한 번 실행합니다. 실습 코드는 기존 ax_cht1에 그리며 고정 데이터를 다시 그릴 때 clear로 이전 그림을 지웁니다. 사용자의 요청에 따라 tight_layout·canvas.draw_idle 호출은 학생용 로직 예제 7개에서 제외했습니다. 실행 환경이 로직 밖에서 배치와 화면 갱신을 처리합니다. 이벤트 안에서 새 Figure를 만들거나 별도의 pyplot 창을 여는 코드도 제거했습니다. 14차시 입력 누적은 이전 입력을 유지하는 별도 동작으로 구분합니다.

기본 Figure 크기 6.4×4.8에 맞춰 결과 그림 7개를 **1536×1152, 4:3**으로 다시 만들었습니다. 입력 배열·수치·마커·시드는 유지합니다. 산점도는 글꼴 설정 뒤 기존 Axes를 초기화하며, 해당 한글 글꼴이 없으면 영문 축 이름을 사용합니다.

{chr(10).join(rows)}

## 실행과 인쇄 검증

- 원고 17개와 인쇄 Python 블록 8개: 구조·코드 일치 검사 통과.
- Python {codes['python']}, Flet {codes['flet']}, flet-charts {codes['flet_charts']}, Matplotlib {codes['matplotlib']}, NumPy {codes['numpy']}에서 공통 생성 1개·그리기 7개 통과.
- 같은 Figure·Axes·Chart에서 실습마다 2회씩, 총 14회 실행했습니다. 객체 연결 유지·그래프 수치·축·범례 검사 통과, 경고 0건.
- 실제 Flet Matplotlib 백엔드를 사용했습니다. 한글 글꼴 부재를 모의한 영문 축 대체 검사도 통과했습니다.
- 브라우저가 연결된 실제 Flet Page에 컨트롤을 배치하고 해당 이벤트 콜백을 실행했습니다. **GUI 19개·알고리즘 6개·Matplotlib 실습 7개, 총 32개 모두 통과**했습니다.
- PDF {pages}쪽 전체 렌더 검사에서 글자 경계 초과·원고 누락·코드 차이·박스 넘침은 0건입니다. 목차 링크와 책갈피는 각 16개입니다.

[실제 실행 화면](../../output/pdf/{SCREENSHOT.name})에서 검사 결과를 확인할 수 있습니다.

## sl42 실제 화면에서 확인한 결과

[sl42]({SOURCE_URL})에서 Chart를 추가하고 Python GUI의 전체 코드를 직접 읽어 공통 생성 구조와 대조했습니다. 이 실제 생성 코드는 [원문](examples/flet-practices/sl42-generated-chart.py)에 보관했습니다. 이어서 같은 페이지의 실행 기능으로 점검 앱을 실행했습니다. **학생용 로직에서 배치·갱신 호출을 제외한 최종 코드로도 32개 모두 통과**했습니다. 실제 페이지의 Python은 {current['site']['python']}, Flet과 flet-charts는 {current['site']['flet']}입니다.

[sl42 실제 실행 화면](../../output/pdf/{SITE_SCREENSHOT.name})과 [페이지 실행 기록](sl42-runtime-results.json)을 확인합니다. 로컬 실행과 실제 서비스 페이지 실행을 구분하여 기록했습니다. 점검 앱은 화면에 연결된 실제 위젯의 이벤트 콜백을 호출하며, 모든 항목을 마우스로 하나씩 클릭했다는 의미는 아닙니다.

추가로 sl42의 기본 디자이너에서 생성된 Chart의 **로직 보기**에 교재의 배열 한 개 예제를 직접 넣어 실행했습니다. 배치·갱신 호출이 없는 실제 로직과 선 그래프를 [확인 화면](../../output/pdf/sl42-logic-only-check.png)과 [대조 기록](sl42-code-comparison.json)에 보관했습니다. 현재 sl42에는 이 간단한 예제가 열려 있습니다.

걸음 수·거리 저장 검증은 예제 앱의 **JSON 파일 저장·불러오기**입니다. 로컬 앱에서는 작업 폴더, sl42에서는 브라우저 실행 환경의 파일에 실제로 쓰고 복원했습니다. 학교 계정의 내 저장소 프로젝트 저장·제출은 실행하지 않았습니다.

## 전달 파일

[현재 PDF](../../output/pdf/vibe-coding-16-upstream.pdf), [전체 원고](book.md), [그리기 코드](examples/source-based/README.md), [실행 가능한 Flet 실습](examples/flet-practices/README.md), [코드 검사](code-results.json), [실제 GUI 실행 기록](gui-results.json), [상세 대조](flet-runtime-review.json).

[이전 내용·오류 검토](content-code-review.md)는 직전 검토 기록입니다. 이번 수정 전 자료는 previous-reports/20261027-before-flet-runtime에 보관했습니다.
'''
    write('flet-runtime-review.md', summary)
    pointer = f'''# 현재 교재 검토 · {args.review_date}

현재 PDF는 A4 {pages}쪽입니다. 16차시·162개 원고 컨테이너·37개 실습·공통 차트 생성 코드 1개·그리기 실습 코드 7개·순서도 4개입니다.

[현재 Flet 구조 반영과 실제 실행 검증](flet-runtime-review.md)을 확인합니다. Python 블록 8개와 실제 Flet Page 실습 32개가 검사를 통과했습니다.

수정 전 자료는 previous-reports/20261027-before-flet-runtime에 보관했습니다. [이전 검토](content-code-review.md)와 현재 검증을 구분합니다.
'''
    for name in ('upstream-edition-review.md','pdf-final-review.md','final-draft.md','validation-summary.md','canva-production-status.md','apps-edition-review.md'):
        write(name,pointer)
    write('handover.md',pointer+'\n현재 PDF·원고·실습 파일·검증 자료는 ../vibe-coding-16-source-revised.zip에 있습니다. 재생성은 notes.md 순서를 따릅니다.\n')
    write('README.md',f'''# 바이브 코딩 16차시 교재 · {args.review_date}

[현재 학생용 PDF](../../output/pdf/vibe-coding-16-upstream.pdf): A4 **{pages}쪽**. 16차시·162개 원고 컨테이너·37개 실습·공통 생성 코드 1개·그리기 코드 7개·순서도 4개.

- [현재 수정·검증](flet-runtime-review.md): fig_cht1·ax_cht1·cht1 연결, 실제 Flet Page 실습 32개 실행 결과.
- [전체 원고](book.md), 차시별 원고 ch01.md~ch16.md, [교사용 안내](teacher-guide.md).
- [생성된 앱에서 쓰는 그리기 코드](examples/source-based/README.md), [실행 가능한 Flet 실습 앱](examples/flet-practices/README.md).
- [코드 실행 기록](code-results.json), [GUI 실행 기록](gui-results.json), [실제 실행 화면](../../output/pdf/{SCREENSHOT.name}), [재생성 안내](notes.md).
- 전달 ZIP: ../vibe-coding-16-source-revised.zip.

12차시 선·마커 → 13차시 막대·산점도 → 14차시 입력 Chart → 15차시 자료·저장 → 16차시 프로젝트의 순서를 유지합니다. [이전 내용 검토](content-code-review.md)는 직전 수정본의 기록입니다.
''')
    prior = BOOK/'content-code-review.md'
    text=prior.read_text(encoding='utf-8')
    if not text.startswith('> 이전 검토 기록입니다.'):
        prior.write_text('> 이전 검토 기록입니다. 현재 PDF와 코드·GUI 실행 결과는 [Flet 구조 반영 검토](flet-runtime-review.md)를 확인합니다.\n\n'+text,encoding='utf-8')
    prior_json=read(BOOK/'content-code-review.json')
    prior_json.update(review_status='previous-review',superseded_by='flet-runtime-review.json')
    save(BOOK/'content-code-review.json',prior_json)
    asset_rows=['| 파일 | 픽셀 | 상태 |','|---|---|---|']
    for item in assets['items']:
        status='추가' if item['src'] in current['added_assets'] else ('Flet 실행 결과로 갱신' if item['src'] in current['changed_assets'] else '유지')
        asset_rows.append(f'| {item["src"]} | {item["width"]}×{item["height"]} | {status} |')
    write('asset-audit.md',f'''# 현재 이미지·벡터 검토 · {args.review_date}

PNG 40개·벡터 PDF 7개·이미지 배치 42곳입니다. 기본 Figure 크기에 맞춰 결과 그림 7개를 1536×1152로 다시 만들고 차트 연결 예시를 추가했습니다. 그 밖의 자산은 유지합니다. 실제 파일의 크기·해시와 벡터 해시를 확인했습니다.

{chr(10).join(asset_rows)}

[현재 검증](flet-runtime-review.md), [자산 명세](asset-manifest.json), [미리보기](asset-review.html)를 확인합니다.
''')
    guide=BOOK/'teacher-guide.md'; text=guide.read_text(encoding='utf-8')
    section='\n## 실제 Flet 차트 구조와 실행 검증\n\n'
    if section in text: text=text.split(section,1)[0]
    text += section+f'현재 인쇄본은 {pages}쪽입니다. 차트 생성 코드는 한 번 실행하고 그리기 실습 7개는 기존 fig_cht1·ax_cht1·cht1을 사용합니다. 고정 그림의 다시 그리기와 14차시 입력 누적을 구분합니다. 공통 생성 1개·그리기 7개와 실제 Flet Page 실습 32개를 검증했습니다. 저장 검증은 예제의 로컬 JSON 파일이며 학교 클라우드 저장은 포함하지 않습니다. [현재 검토](flet-runtime-review.md)를 확인합니다.\n'
    text=re.sub(r'현재 인쇄본은 \d+쪽입니다\.',f'현재 인쇄본은 {pages}쪽입니다.',text)
    text=text.replace('GUI·프로젝트 저장 동작은 사용 중인 수업 도구에서 별도로 확인합니다.','GUI 실행 결과는 gui-results.json에 있습니다. 학교 클라우드 프로젝트 저장은 별도로 확인합니다.')
    guide.write_text(text,encoding='utf-8')
    path=BOOK/'source-audit.md';text=path.read_text(encoding='utf-8')
    text=re.sub(r'Python 예제 7개를 다시 실행했습니다\. 산점도 코드와 결과 그림은.*?상세 결과는 content-code-review\.md에 있습니다\.',
                '공통 차트 생성 1개와 그리기 실습 7개를 실제 Flet 구조로 수정하고 결과 그림 7개를 다시 만들었습니다. 현재 검증은 flet-runtime-review.md에 있습니다.',text)
    path.write_text(text,encoding='utf-8')
    return review


def package(args,current):
    bundle=BOOK.parent/'vibe-coding-16-source-revised.zip'
    assert bundle.is_file(),'Existing archive is required to preserve filtered historical entries'
    replacements={}
    for name in bundle_names(bundle):
        if '/previous-reports/' in name or name.endswith('/delivery-manifest.json'): continue
        path=BOOK/name.removeprefix('vibe-coding-16/') if name.startswith('vibe-coding-16/') else ROOT/name
        if path.is_file(): replacements[name]=path
    additions=[BOOK/'flet-runtime-review.md',BOOK/'flet-runtime-review.json',BOOK/'gui-results.json',BOOK/'code-results.json',
               BOOK/'examples/source-based/chart_setup.py',ROOT/'scripts/audit_current_edition.py',ROOT/'scripts/check_practice_code.py',
               BASE/'vibe-coding-16-upstream.json',BASE/'code-specs.json',BASE/'asset-manifest.json',SCREENSHOT,
               BOOK/'sl42-runtime-results.json',SITE_SCREENSHOT,ROOT/'output/pdf/sl42-chart-code-check.png',
               ROOT/'scripts/build_sl42_runtime_check.py',BOOK/'sl42-code-comparison.json',
               ROOT/'output/pdf/sl42-logic-only-check.png']
    additions += list((BOOK/'examples/flet-practices').glob('*.py'))+list((BOOK/'examples/flet-practices').glob('*.json'))
    additions += [BOOK/'examples/flet-practices'/name for name in ('README.md','requirements.txt')]
    additions += [BOOK/item['src'] for item in current['assets']['items']]
    additions += [BOOK/item['vector_src'] for item in current['assets']['items'] if item.get('vector_src')]
    for path in additions:
        assert path.is_file(),path
        name='vibe-coding-16/'+path.relative_to(BOOK).as_posix() if path.is_relative_to(BOOK) else path.relative_to(ROOT).as_posix()
        replacements[name]=path
    temporary=bundle.with_suffix('.pending.zip')
    with zipfile.ZipFile(bundle) as original,zipfile.ZipFile(temporary,'w',compression=zipfile.ZIP_DEFLATED) as output:
        for item in original.infolist():
            if item.filename in replacements or item.filename in ('START-HERE.txt','vibe-coding-16/delivery-manifest.json'): continue
            output.writestr(item,original.read(item.filename))
        for name,path in sorted(replacements.items()): output.write(path,name)
        output.writestr('START-HERE.txt',f'''{args.review_date} Flet 차트 구조 반영 수정본

PDF: output/pdf/{PDF.name} (A4 {current['pages']}쪽)
원고: vibe-coding-16/book.md 및 ch01.md~ch16.md
현재 검토: vibe-coding-16/flet-runtime-review.md
그리기 코드: vibe-coding-16/examples/source-based (공통 생성1개·그리기7개)
실행 가능한 Flet 실습: vibe-coding-16/examples/flet-practices/README.md
GUI 실행 기록: vibe-coding-16/gui-results.json (32개 통과)
실제 실행 화면: output/pdf/{SCREENSHOT.name}

원고 폴더를 저장소의 coala-book-md/vibe-coding-16에, 나머지는 같은 상대 경로에 복사합니다. notes.md의 현재 순서를 따릅니다. 로컬 JSON 저장·불러오기를 검증했으며 학교 클라우드 프로젝트 저장·제출은 실행하지 않았습니다.
''')
    with zipfile.ZipFile(temporary) as archive:
        assert archive.testzip() is None
        names=archive.namelist(); assert len(names)==len(set(names))
        for name,path in replacements.items(): assert hashlib.sha256(archive.read(name)).hexdigest()==sha(path)
        assert len([n for n in names if n.startswith('vibe-coding-16/examples/source-based/') and n.endswith('.py')])==8
        assert not any(n.startswith('vibe-coding-16/assets/') and 'pandas-table.png' in n for n in names)
        assert not any(n.startswith('vibe-coding-16/examples/') and 'pandas' in n.lower() for n in names)
    temporary.replace(bundle)
    mirror=BOOK.parent/'vibe-coding-16-source-revised'
    if mirror.is_dir():
        for name,path in replacements.items():
            if name.startswith('vibe-coding-16/'):
                target=mirror/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,target)
    save(BOOK/'delivery-manifest.json',{'date':args.review_date,'edition':'flet-chart-context-16-sessions',
         'bundleSha256':sha(bundle),'pdfSha256':sha(PDF),'manuscriptSha256':sha(BOOK/'book.md'),
         'guiResultsSha256':sha(BOOK/'gui-results.json'),'members':len(bundle_names(bundle)),'pdfPages':current['pages']})
    return bundle


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review-date',default='2026-10-27')
    parser.add_argument('--qa',type=Path,default=ROOT/'tmp/pdfs/current-review/automated-qa.json')
    args=parser.parse_args()
    current=validate(args)
    reports(args,current)
    bundle=package(args,current)
    print(json.dumps({'pages':current['pages'],'manuscripts':17,'pythonBlocksPassed':8,'practiceCodeBlocks':7,
          'setupBlocks':1,'practiceRuns':14,'guiPassed':32,'warnings':0,'changedCode':current['changed_code'],
          'addedCode':current['added_code'],'changedAssets':current['changed_assets'],'addedAssets':current['added_assets'],
          'bundle':str(bundle)},ensure_ascii=False))


if __name__=='__main__': main()
