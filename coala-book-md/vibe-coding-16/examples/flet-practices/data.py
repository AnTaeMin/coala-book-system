"""Real Flet 0.86 applications for textbook charts, data and algorithms.

The gallery must mount each returned control on a real Page before awaiting its
exercise. Exercises call the same handlers wired to visible buttons and verify
the resulting real controls and Matplotlib artists. Nothing here creates a
stand-in Page. The project persistence case saves a local JSON model; it does
not claim to test Coala's cloud project store.
"""
from __future__ import annotations

import asyncio
from collections import Counter
import hashlib
import json
import math
from pathlib import Path

import flet as ft
import flet_charts as fch
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[4]
MANIFEST = Path(__file__).with_name("data-cases.json")


def _finite(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("유한한 숫자를 입력하세요.")
    return result


def _text_rows(values):
    return [ft.DataRow(cells=[ft.DataCell(ft.Text(str(value))) for value in row])
            for row in values]


def _layout(*controls):
    return ft.Column(list(controls), spacing=12, width=760,
                     scroll=ft.ScrollMode.AUTO)


def _chart_view(chart, height=320):
    # A fixed-height parent bounds the chart's expand=True inside scrolling UI.
    return ft.Container(content=chart, width=700, height=height)


def _case(case_id, title, control, exercise, **extra):
    return {"id": case_id, "title": title, "control": control,
            "exercise": exercise, **extra}


def _line_case(page):
    fields = [ft.TextField(label=f"fld{i + 1}", value=str(value), width=130)
              for i, value in enumerate([1, 2, 5, 4, 5])]
    message = ft.Text()
    fig_cht1, ax_cht1 = plt.subplots()
    cht1 = fch.MatplotlibChart(expand=True, figure=fig_cht1)
    cht1.height = 320
    identity = id(fig_cht1)

    def draw(e=None):
        try:
            values = [_finite(field.value) for field in fields]
        except ValueError:
            message.value = "다섯 칸에 숫자를 입력하세요."
        else:
            ax_cht1.clear()
            ax_cht1.plot(values)
            fig_cht1.tight_layout()
            fig_cht1.canvas.draw_idle()
            message.value = "입력 순서 0~4의 다섯 값을 표시했습니다."
        page.update()

    def clear(e=None):
        ax_cht1.clear()
        fig_cht1.canvas.draw_idle()
        message.value = "그래프 기록을 초기화했습니다."
        page.update()

    control = _layout(ft.Row(fields, wrap=True),
                      ft.Row([ft.Button("그래프 그리기", on_click=draw),
                              ft.Button("초기화", on_click=clear)]), message, _chart_view(cht1))

    async def exercise():
        for field, value in zip(fields, [1, 2, 5, 4, 5]):
            field.value = str(value)
        draw()
        assert list(ax_cht1.lines[0].get_xdata()) == [0, 1, 2, 3, 4]
        assert list(ax_cht1.lines[0].get_ydata()) == [1, 2, 5, 4, 5]
        draw()
        assert len(ax_cht1.lines) == 1, "반복 실행은 새 선을 겹치지 않아야 함"
        fields[0].value = "문자"
        draw()
        assert "숫자" in message.value and len(ax_cht1.lines) == 1
        fields[0].value = "1"
        clear()
        assert len(ax_cht1.lines) == 0
        draw()
        assert id(cht1.figure) == identity and ax_cht1 in cht1.figure.axes
        await asyncio.sleep(0)
        return {"x": [0, 1, 2, 3, 4], "y": [1, 2, 5, 4, 5],
                "reset": True, "redraw_reuses_figure": True,
                "invalid_input_preserves_previous_graph": True}

    return _case("ch14-practice-1", "입력값 꺾은선·초기화", control, exercise,
                 figure=fig_cht1)


def _scatter_case(page):
    fld1 = ft.TextField(label="fld1 · 키", value="170", width=160)
    fld2 = ft.TextField(label="fld2 · 몸무게", value="74", width=160)
    message = ft.Text()
    pairs = []
    fig_cht1, ax_cht1 = plt.subplots()
    cht1 = fch.MatplotlibChart(expand=True, figure=fig_cht1)
    cht1.height = 320
    identity = id(fig_cht1)

    def add(e=None):
        try:
            point = [_finite(fld1.value), _finite(fld2.value)]
        except ValueError:
            message.value = "키와 몸무게에 숫자를 입력하세요."
        else:
            pairs.append(point)
            # The data model accumulates; rebuilding artists avoids stale axes.
            ax_cht1.clear()
            ax_cht1.scatter(*zip(*pairs), c="blue")
            ax_cht1.set_xlabel("height")
            ax_cht1.set_ylabel("weight")
            fig_cht1.tight_layout()
            fig_cht1.canvas.draw_idle()
            message.value = f"{len(pairs)}개의 점을 누적했습니다."
        page.update()

    control = _layout(ft.Row([fld1, fld2]), ft.Button("시각화", on_click=add),
                      message, _chart_view(cht1))

    async def exercise():
        pairs.clear()
        for x, y in [(170, 74), (180, 82), (185, 89)]:
            fld1.value, fld2.value = str(x), str(y)
            add()
        actual = np.asarray(ax_cht1.collections[0].get_offsets())
        assert np.allclose(actual, [[170, 74], [180, 82], [185, 89]])
        fld1.value = ""
        add()
        assert len(pairs) == 3 and "숫자" in message.value
        fld1.value, fld2.value = "185", "89"
        page.update()
        assert id(cht1.figure) == identity
        await asyncio.sleep(0)
        return {"points": pairs.copy(), "accumulation": True,
                "invalid_input_does_not_append": True,
                "redraw_reuses_figure": True}

    return _case("ch14-practice-2", "키·몸무게 세 점 누적", control, exercise,
                 figure=fig_cht1)


def _bar_case(page):
    fld1 = ft.TextField(label="fld1 · 막대 높이", value="90", width=180)
    message = ft.Text()
    values = []
    fig_cht1, ax_cht1 = plt.subplots()
    cht1 = fch.MatplotlibChart(expand=True, figure=fig_cht1)
    cht1.height = 320
    identity = id(fig_cht1)

    def add(e=None):
        try:
            value = _finite(fld1.value)
        except ValueError:
            message.value = "막대 높이에 숫자를 입력하세요."
        else:
            values.append(value)
            ax_cht1.clear()
            ax_cht1.bar(range(len(values)), values)
            fig_cht1.tight_layout()
            fig_cht1.canvas.draw_idle()
            message.value = f"{len(values)}개의 막대를 누적했습니다."
        page.update()

    control = _layout(fld1, ft.Button("시각화", on_click=add), message, _chart_view(cht1))

    async def exercise():
        values.clear()
        for value in [90, 80, 70]:
            fld1.value = str(value)
            add()
        assert [patch.get_height() for patch in ax_cht1.patches] == [90, 80, 70]
        assert len(ax_cht1.patches) == 3
        fld1.value = "nan"
        add()
        assert len(values) == 3
        fld1.value = "70"
        page.update()
        assert id(cht1.figure) == identity
        await asyncio.sleep(0)
        return {"heights": values.copy(), "accumulation": True,
                "nonfinite_input_rejected": True, "redraw_reuses_figure": True}

    return _case("ch14-practice-3", "90·80·70 막대 누적", control, exercise,
                 figure=fig_cht1)


def _student_case(page, fixture):
    headers = ["id", "school", "grade", "gender", "height_cm", "weight_kg"]
    defaults = ["id", "height_cm", "weight_kg"]
    checks = [ft.Checkbox(label=key, value=key in defaults) for key in headers]
    dropdown_x = ft.Dropdown(label="X 열", value="height_cm", width=170,
                            options=[ft.DropdownOption(key=key, text=key)
                                     for key in ["height_cm", "weight_kg"]])
    dropdown_y = ft.Dropdown(label="Y 열", value="weight_kg", width=170,
                            options=[ft.DropdownOption(key=key, text=key)
                                     for key in ["height_cm", "weight_kg"]])
    table = ft.DataTable(columns=[ft.DataColumn(ft.Text("자료를 불러오세요"))], rows=[])
    table_holder = ft.Column([table], height=150, scroll=ft.ScrollMode.AUTO)
    message = ft.Text("제공된 학생 100명 CSV를 사용합니다.")
    fig_cht1, ax_cht1 = plt.subplots()
    cht1 = fch.MatplotlibChart(expand=True, figure=fig_cht1)
    cht1.height = 280

    def load(e=None):
        selected = [check.label for check in checks if check.value]
        if not selected:
            message.value = "표시할 열을 하나 이상 선택하세요."
            page.update()
            return
        table.columns = [ft.DataColumn(ft.Text(key)) for key in selected]
        table.rows = _text_rows([[row[key] for key in selected] for row in fixture])
        x_key, y_key = dropdown_x.value, dropdown_y.value
        ax_cht1.clear()
        ax_cht1.scatter([float(row[x_key]) for row in fixture],
                         [float(row[y_key]) for row in fixture], c="red", s=10)
        ax_cht1.set_xlabel(x_key)
        ax_cht1.set_ylabel(y_key)
        fig_cht1.tight_layout()
        fig_cht1.canvas.draw_idle()
        message.value = f"학생 {len(fixture)}명, X={x_key}, Y={y_key}"
        page.update()

    control = _layout(ft.Row(checks, wrap=True),
                      ft.Row([dropdown_x, dropdown_y,
                              ft.Button("자료 불러오기", on_click=load)]),
                      message, table_holder, _chart_view(cht1, 280))

    async def exercise():
        for check in checks:
            check.value = check.label in defaults
        dropdown_x.value, dropdown_y.value = "height_cm", "weight_kg"
        load()
        assert len(table.rows) == 100
        assert [column.label.value for column in table.columns] == defaults
        offsets = np.asarray(ax_cht1.collections[0].get_offsets())
        expected = [[float(row["height_cm"]), float(row["weight_kg"])] for row in fixture]
        assert np.allclose(offsets, expected)
        for check in checks:
            check.value = check.label in ["id", "gender", "height_cm", "weight_kg"]
        dropdown_x.value, dropdown_y.value = "weight_kg", "height_cm"
        load()
        reversed_offsets = np.asarray(ax_cht1.collections[0].get_offsets())
        assert np.allclose(reversed_offsets, np.asarray(expected)[:, ::-1])
        assert [column.label.value for column in table.columns] == ["id", "gender", "height_cm", "weight_kg"]
        dropdown_x.value, dropdown_y.value = "height_cm", "weight_kg"
        load()
        await asyncio.sleep(0)
        return {"rows": 100, "source": "provided student_body_100.csv",
                "visible_columns": ["id", "gender", "height_cm", "weight_kg"],
                "first_point": expected[0], "axis_swap_checked": True}

    return _case("ch15-practice-data", "학생 100명 자료·열 선택", control, exercise,
                 figure=fig_cht1)


def _school_case(page, fixture):
    message = ft.Text()
    fig_cht1, ax_cht1 = plt.subplots()
    cht1 = fch.MatplotlibChart(expand=True, figure=fig_cht1)
    cht1.height = 350
    counts = Counter()

    def draw(e=None):
        counts.clear()
        counts.update(row["school"] for row in fixture)
        labels = sorted(counts)
        ax_cht1.clear()
        ax_cht1.bar(labels, [counts[label] for label in labels])
        ax_cht1.set_ylabel("students")
        fig_cht1.tight_layout()
        fig_cht1.canvas.draw_idle()
        message.value = ", ".join(f"{label}: {counts[label]}명" for label in labels)
        page.update()

    control = _layout(ft.Text("학교 구분은 school 열을 사용합니다."),
                      ft.Button("학교별 개수 그리기", on_click=draw), message, _chart_view(cht1, 350))

    async def exercise():
        draw()
        expected = Counter(row["school"] for row in fixture)
        assert set(expected) == {"고등학교", "중학교"}
        assert sum(counts.values()) == 100 and counts == expected
        labels = [tick.get_text() for tick in ax_cht1.get_xticklabels()]
        heights = [patch.get_height() for patch in ax_cht1.patches]
        assert dict(zip(labels, heights)) == dict(expected)
        draw()
        assert len(ax_cht1.patches) == 2
        await asyncio.sleep(0)
        return {"column": "school", "counts": dict(counts),
                "total": sum(counts.values()), "redraw_does_not_duplicate": True}

    return _case("ch15-practice-school", "학교별 학생 수", control, exercise,
                 figure=fig_cht1)


def _persistence_case(page):
    fld1 = ft.TextField(label="fld1 · 걸음 수", value="10", width=180)
    fld2 = ft.TextField(label="fld2 · 이동거리", value="15", width=180)
    table_save = ft.Switch(label="표 저장", value=True)
    table = ft.DataTable(columns=[ft.DataColumn(ft.Text("걸음 수")),
                                 ft.DataColumn(ft.Text("이동거리"))], rows=[])
    table_holder = ft.Column([table], height=120, scroll=ft.ScrollMode.AUTO)
    message = ft.Text("로컬 JSON 프로젝트 저장 검증입니다. 웹 내 저장소와 구분합니다.")
    records = []
    fig_cht1, ax_cht1 = plt.subplots()
    cht1 = fch.MatplotlibChart(expand=True, figure=fig_cht1)
    cht1.height = 280
    path = ROOT / "tmp/flet-practices/walk-project.json"

    def render():
        table.rows = _text_rows(records)
        ax_cht1.clear()
        if records:
            ax_cht1.scatter(*zip(*records), c="blue")
        ax_cht1.set_xlabel("steps")
        ax_cht1.set_ylabel("distance")
        fig_cht1.tight_layout()
        fig_cht1.canvas.draw_idle()

    def add(e=None):
        try:
            row = [_finite(fld1.value), _finite(fld2.value)]
            if min(row) < 0:
                raise ValueError("음수는 사용할 수 없습니다.")
        except ValueError:
            message.value = "걸음 수와 이동거리에 0 이상의 숫자를 입력하세요."
        else:
            records.append(row)
            render()
            message.value = f"{len(records)}행을 추가했습니다."
        page.update()

    def clear(e=None):
        records.clear()
        render()
        message.value = "입력 기록을 초기화했습니다."
        page.update()

    def save(e=None):
        model = {"project_name": "데이터 저장", "schema": 1,
                 "table_columns": ["걸음 수", "이동거리"],
                 "table_save": bool(table_save.value),
                 "records": records if table_save.value else []}
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(model, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        message.value = "로컬 프로젝트 JSON을 저장했습니다."
        page.update()

    def load(e=None):
        if not path.is_file():
            message.value = "먼저 로컬 프로젝트를 저장하세요."
            page.update()
            return
        model = json.loads(path.read_text(encoding="utf-8"))
        if model.get("schema") != 1 or model.get("table_columns") != ["걸음 수", "이동거리"]:
            raise ValueError("지원하지 않는 저장 형식입니다.")
        restored = [[_finite(x), _finite(y)] for x, y in model["records"]]
        records[:] = restored
        table_save.value = model["table_save"]
        render()
        message.value = f"로컬 프로젝트에서 {len(records)}행을 불러왔습니다."
        page.update()

    control = _layout(ft.Row([fld1, fld2, table_save]),
                      ft.Row([ft.Button("데이터 추가", on_click=add),
                              ft.Button("초기화", on_click=clear),
                              ft.Button("로컬 저장", on_click=save),
                              ft.Button("로컬 불러오기", on_click=load)], wrap=True),
                      message, table_holder, _chart_view(cht1, 280))

    async def exercise():
        clear()
        table_save.value = True
        expected = [[10.0, 15.0], [20.0, 30.0], [30.0, 45.0]]
        for x, y in expected:
            fld1.value, fld2.value = str(x), str(y)
            add()
        assert len(table.rows) == 3
        save()
        saved_bytes = path.read_bytes()
        saved_sha = hashlib.sha256(saved_bytes).hexdigest()
        clear()
        assert len(table.rows) == 0 and len(ax_cht1.collections) == 0
        load()
        assert records == expected and len(table.rows) == 3
        assert np.allclose(ax_cht1.collections[0].get_offsets(), expected)
        assert hashlib.sha256(path.read_bytes()).hexdigest() == saved_sha
        # Turning persistence off must omit data, rather than silently save it.
        table_save.value = False
        save()
        assert json.loads(path.read_text(encoding="utf-8"))["records"] == []
        table_save.value = True
        save()
        await asyncio.sleep(0)
        return {"scope": "local JSON project model; Coala cloud not exercised",
                "records_restored": expected, "sha256_unchanged_on_load": True,
                "table_save_false_omits_records": True,
                "file": str(path), "figure_identity_preserved": cht1.figure is fig_cht1}

    return _case("ch15-practice-3", "걸음 수·거리 로컬 저장·불러오기", control,
                 exercise, figure=fig_cht1)


def _algorithm_case(page, case_id, title, labels, defaults, calculate, checks):
    fields = [ft.TextField(label=label, value=str(value), width=170)
              for label, value in zip(labels, defaults)]
    output = ft.Text(selectable=True)

    def run(e=None):
        try:
            output.value = str(calculate([field.value for field in fields]))
        except (ValueError, TypeError):
            output.value = "입력값을 확인하세요."
        page.update()

    control = _layout(ft.Text("순서도 규칙을 그대로 구현한 실행 확인 앱입니다."),
                      ft.Row(fields, wrap=True), ft.Button("계산·판정", on_click=run), output)

    async def exercise():
        evidence = []
        for values, expected in checks:
            for field, value in zip(fields, values):
                field.value = str(value)
            run()
            assert output.value == expected, (case_id, values, output.value, expected)
            evidence.append({"input": list(values), "output": expected})
        for field, value in zip(fields, defaults):
            field.value = str(value)
        run()
        await asyncio.sleep(0)
        return {"cases": evidence, "scope": "flowchart rules implemented in Flet"}

    return _case(case_id, title, control, exercise)


def build_cases(page):
    """Return six chart/data applications plus six executable algorithm checks."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    fixture = manifest["student_fixture"]["rows"]
    assert len(fixture) == 100
    cases = [_line_case(page), _scatter_case(page), _bar_case(page),
             _student_case(page, fixture), _school_case(page, fixture),
             _persistence_case(page)]

    def family(values):
        return str(sum(int(value) for value in values))

    def exercise_total(values):
        days = int(values[0])
        if days < 1:
            raise ValueError("날짜는 1 이상이어야 합니다.")
        total = 0
        time1 = 1
        while time1 <= days:
            total += time1
            time1 += 1
        return f"total={total}, time1={time1}"

    def caffeine(values):
        numbers = [_finite(part.strip()) for part in values[0].split(",")]
        if min(numbers) < 0:
            raise ValueError("음수 섭취량")
        total = 0
        for amount in numbers:
            total += amount
        return f"{total:g}mg"

    def sleep(values):
        hours = _finite(values[0])
        if hours < 0:
            raise ValueError("음수 시간")
        return "충분한 수면입니다" if hours >= 8 else ("적정 수면입니다" if hours >= 5 else "수면 부족입니다")

    def score(values):
        count = int(values[0])
        scores = [_finite(part.strip()) for part in values[1].split(",")]
        if count < 1 or count != len(scores) or any(value < 0 or value > 100 for value in scores):
            raise ValueError("학생 수·점수 범위")
        return ", ".join("PASS" if value >= 80 else "FAIL" for value in scores)

    def movie(values):
        ages = [int(part.strip()) for part in values[0].split(",")]
        if len(ages) != 4 or min(ages) < 0:
            raise ValueError("네 학생의 나이")
        return ", ".join("관람가능" if age >= 15 else "관람불가" for age in ages)

    cases.extend([
        _algorithm_case(page, "ch04-family-code", "가족 나이 합 103", ["엄마", "아빠", "나"], [43, 45, 15], family,
                        [([43, 45, 15], "103")]),
        _algorithm_case(page, "ch05-exercise-code", "10일 누적 운동 시간", ["마지막 날짜"], [10], exercise_total,
                        [([10], "total=55, time1=11"), ([1], "total=1, time1=2")]),
        _algorithm_case(page, "ch05-caffeine-code", "카페인 누적", ["섭취량을 쉼표로 입력"], ["50,80,20"], caffeine,
                        [(["50,80,20"], "150mg"), (["0,0"], "0mg")]),
        _algorithm_case(page, "ch06-sleep-code", "수면 조건 경계값", ["수면 시간"], [8], sleep,
                        [([8], "충분한 수면입니다"), ([7.9], "적정 수면입니다"), ([5], "적정 수면입니다"), ([4.9], "수면 부족입니다")]),
        _algorithm_case(page, "ch07-pass-code", "N명 점수 PASS 판정", ["학생 수 N", "점수 목록"], [3, "79,80,100"], score,
                        [([3, "79,80,100"], "FAIL, PASS, PASS"), ([2, "79,80,100"], "입력값을 확인하세요.")]),
        _algorithm_case(page, "ch07-movie-code", "네 학생 영화 관람 판정", ["네 학생의 나이"], ["14,15,16,10"], movie,
                        [(["14,15,16,10"], "관람불가, 관람가능, 관람가능, 관람불가"), (["14,15"], "입력값을 확인하세요.")]),
    ])
    return cases
