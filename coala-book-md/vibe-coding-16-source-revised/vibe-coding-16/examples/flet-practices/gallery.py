"""Run the textbook's working Flet examples on a real connected Page.

python gallery.py --port 8765 --auto-check
Then open http://127.0.0.1:8765 in a browser. Tests run only after a browser
connects: real controls are mounted and their own event callbacks are exercised.
This does not submit coursework or access the school's cloud project storage.
"""
import argparse
import asyncio
import importlib.util
import json
import os
import platform
import traceback
from datetime import datetime
from pathlib import Path
from importlib.metadata import version

import flet as ft
import flet_charts as fch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
DEST = ROOT/'tmp/pdfs/flet-runtime-review'


def load(name):
    spec = importlib.util.spec_from_file_location('textbook_'+name, HERE/(name+'.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def save_report(records):
    report = {'reviewed_date':'2026-10-27', 'python':platform.python_version(),
              'flet':version('flet'), 'flet_charts':version('flet-charts'),
              'execution':'real-browser-connected-flet-page; real control event callbacks',
              'cloud_project_save_tested':False,
              'tested':len(records), 'passed':sum(r['status']=='passed' for r in records),
              'failed':sum(r['status']=='failed' for r in records), 'records':records}
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST/'gui-results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2,
             default=lambda v: v.item() if hasattr(v,'item') else str(v))+'\n', encoding='utf-8')
    return report


def run():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--auto-check', action='store_true')
    args = parser.parse_args()

    async def main(page: ft.Page):
        page.title = '교재 실습 실행 점검'
        page.scroll = ft.ScrollMode.AUTO
        cases = load('basic').build_cases(page)+load('data').build_cases(page)+load('plots').build_cases(page)
        index = 0
        title = ft.Text(size=22, weight=ft.FontWeight.BOLD)
        status = ft.Text('브라우저 연결 완료. 실제 Flet 화면에서 실습을 실행합니다.', size=16)
        body = ft.Container(height=600, border=ft.Border.all(1, '#CED4DA'), padding=16)
        results = ft.Column()
        records = []

        def select(offset):
            nonlocal index
            index = (index+offset)%len(cases)
            case = cases[index]
            title.value = f'{index+1}/{len(cases)} · {case["id"]} · {case["title"]}'
            body.content = case['control']
            page.update()

        async def check_one(case):
            nonlocal index
            index = cases.index(case)
            body.content = case['control']
            title.value = case['id']+' · '+case['title']
            page.update()
            await asyncio.sleep(.35)
            try:
                evidence = await case['exercise']()
                record = {'id':case['id'], 'title':case['title'], 'status':'passed', 'evidence':evidence}
            except Exception as error:
                traceback.print_exc()
                record = {'id':case['id'], 'title':case['title'], 'status':'failed',
                          'error':str(error), 'traceback':traceback.format_exc()}
            records.append(record)
            save_report(records)
            results.controls.append(ft.Text(('PASS ' if record['status']=='passed' else 'FAIL ')+case['id']+' '+case['title']))
            page.update()

        async def check_all(e=None):
            records.clear()
            results.controls.clear()
            status.value = f'전체 {len(cases)}개 실습을 실제 Page에 차례로 연결하여 점검 중입니다.'
            page.update()
            for case in cases:
                await check_one(case)
            report = save_report(records)
            status.value = f'전체 {report["tested"]}개 · 통과 {report["passed"]}개 · 실패 {report["failed"]}개'
            page.update()
            print(json.dumps({k:report[k] for k in ('tested','passed','failed')}, ensure_ascii=False), flush=True)

        async def current_check(e):
            await check_one(cases[index])

        page.add(ft.Column([
            ft.Text('교재 실습 실행 점검', size=26, weight=ft.FontWeight.BOLD), status,
            ft.Row([ft.Button('이전 실습', on_click=lambda e:select(-1)),
                    ft.Button('다음 실습', on_click=lambda e:select(1)),
                    ft.Button('현재 실습 점검', on_click=current_check),
                    ft.Button('전체 실습 점검', on_click=check_all)], wrap=True),
            title, body, results,
            ft.Text('저장 실습은 로컬 JSON 저장·복원 검사입니다. 수업 사이트의 내 저장소에는 제출하거나 저장하지 않습니다.')
        ]))
        select(0)
        if args.auto_check:
            await asyncio.sleep(1)
            await check_all()

    print(f'Open http://127.0.0.1:{args.port}', flush=True)
    os.environ['FLET_FORCE_WEB_SERVER'] = 'true'
    ft.run(main, view=None, host='127.0.0.1', port=args.port)


if __name__=='__main__':
    run()
