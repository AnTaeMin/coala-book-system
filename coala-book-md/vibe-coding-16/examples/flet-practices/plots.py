"""Mount the seven textbook drawing bodies on their real Flet chart controls."""
import sys
from pathlib import Path
import flet as ft

BOOK = Path(__file__).resolve().parents[2]
ROOT = BOOK.parents[1]


def build_cases(page):
    import json
    sys.path.insert(0, str(ROOT/'scripts'))
    from check_practice_code import check_semantics
    specs = json.loads((BOOK/'code-specs.json').read_text(encoding='utf-8'))
    setup = next(s['code'] for s in specs if s['role']=='generated-chart-setup')
    cases = []
    for spec in specs:
        if spec['role'] != 'drawing-event-body':
            continue
        ns = {}
        exec(compile(setup, 'chart_setup.py', 'exec'), ns)
        figure, axes, chart = ns['fig_cht1'], ns['ax_cht1'], ns['cht1']
        compiled = compile(spec['code'], spec['file'], 'exec')

        def redraw(e=None, ns=ns, compiled=compiled):
            exec(compiled, ns)
            # The learning examples contain only drawing logic. The runtime
            # refreshes the bound chart after that logic has completed.
            ns['fig_cht1'].tight_layout()
            ns['fig_cht1'].canvas.draw_idle()
            page.update()

        async def exercise(ns=ns, figure=figure, axes=axes, chart=chart,
                           redraw=redraw, pid=spec['page_id']):
            identities = (id(figure), id(axes), id(chart))
            redraw()
            first = (len(axes.lines), len(axes.patches), len(axes.collections))
            semantics = check_semantics(pid, axes, ns)
            redraw()
            assert identities == (id(ns['fig_cht1']), id(ns['ax_cht1']), id(ns['cht1']))
            assert chart.figure is figure and axes in figure.axes
            assert first == (len(axes.lines), len(axes.patches), len(axes.collections))
            return {'chart_binding':True, 'repeat_redraw':True,
                    'automatic_refresh_outside_logic':True, 'semantics':semantics}

        cases.append({'id':spec['page_id'], 'title':spec['page_id'],
                      'control':ft.Column([ft.Button('그래프 다시 그리기', on_click=redraw),
                                           ft.Container(content=chart, height=430, expand=True)], expand=True),
                      'exercise':exercise, 'figure':figure})
    return cases
