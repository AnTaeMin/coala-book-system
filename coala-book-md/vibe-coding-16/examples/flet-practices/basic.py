"""8~11차시의 실제 Flet 0.86 위젯과 이벤트.

갤러리의 실제 Page에 control을 추가한 다음 await case['exercise']()로
실행한다. 검사는 화면에 연결된 위젯과 그 위젯의 실제 콜백을 사용한다.
이 모듈은 실행 창을 따로 시작하지 않으며 build_cases(page)를 제공한다.
"""
from __future__ import annotations

import inspect
import math
import struct
from pathlib import Path

import flet as ft

BOOK = Path(__file__).resolve().parents[2]


async def _invoke(control, event_name="on_click"):
    """Mounted control에 지정된 콜백을 실행한다. UI 클릭과 같은 함수다."""
    callback = getattr(control, event_name)
    assert callback is not None
    value = callback(None)
    if inspect.isawaitable(value):
        await value


def _case(page, case_id, title, controls, exercise, widgets):
    panel = ft.Container(
        content=ft.Column(controls, spacing=12), padding=12,
        data=f"practice-{case_id}",
    )

    async def mounted_exercise():
        assert panel.page is page, "Mount the case control on a real Page first."
        result = await exercise()
        page.update()
        return {"id": case_id, "status": "passed", **result}

    return {"id": case_id, "title": title, "control": panel,
            "exercise": mounted_exercise, "widgets": widgets}


def _colors(page):
    btn1 = ft.Button("버튼 색 바꾸기", bgcolor="grey200", color="black", data="btn1")

    def on_click(e):
        btn1.bgcolor, btn1.color = "blue", "white"
        page.update()

    btn1.on_click = on_click

    async def exercise():
        await _invoke(btn1)
        assert btn1.bgcolor == "blue" and btn1.color == "white"
        return {"bgcolor": btn1.bgcolor, "color": btn1.color}

    return _case(page, "008-1", "버튼 색 바꾸기", [btn1], exercise, {"btn1": btn1})


def _message(page):
    fld1 = ft.TextField(label="인사말", value="안녕하세요", data="fld1")
    btn1 = ft.Button("메시지 보기", data="btn1")
    txt1 = ft.Text("", data="txt1")
    state = {"dialog": None}

    def on_click(e):
        def close_dialog(e):
            page.pop_dialog()
        dialog = ft.AlertDialog(
            title=ft.Text("메시지"), content=ft.Text(fld1.value or ""),
            actions=[ft.Button("닫기", on_click=close_dialog)], modal=True,
        )
        state["dialog"] = dialog
        txt1.value = fld1.value or ""
        page.show_dialog(dialog)
        page.update()

    btn1.on_click = on_click

    async def exercise():
        fld1.value = "안녕하세요"
        await _invoke(btn1)
        dialog = state["dialog"]
        assert dialog.open and dialog.content.value == "안녕하세요"
        assert txt1.value == "안녕하세요"
        await _invoke(dialog.actions[0])
        assert not dialog.open
        return {"message": txt1.value, "dialog_opened_and_closed": True}

    return _case(page, "008-2", "입력 인사말 메시지 창", [fld1, btn1, txt1], exercise,
                 {"fld1": fld1, "btn1": btn1, "txt1": txt1, "state": state})


def _copy_delete(page):
    fld1 = ft.TextField(label="인사말 입력", data="fld1")
    fld2 = ft.TextField(label="결과", read_only=True, data="fld2")
    btn1, btn2 = ft.Button("추가", data="btn1"), ft.Button("삭제", data="btn2")

    def copy(e):
        fld2.value = fld1.value or ""
        page.update()

    def delete(e):
        fld1.value = fld2.value = ""
        page.update()

    btn1.on_click, btn2.on_click = copy, delete

    async def exercise():
        fld1.value = "안녕"
        await _invoke(btn1)
        assert fld2.value == "안녕"
        await _invoke(btn2)
        assert fld1.value == fld2.value == ""
        return {"copied": "안녕", "both_fields_cleared": True}

    return _case(page, "008-3", "Field 복사·삭제", [fld1, ft.Row([btn1, btn2]), fld2], exercise,
                 {"fld1": fld1, "fld2": fld2, "btn1": btn1, "btn2": btn2})


def _product(page):
    fld1 = ft.TextField(label="시작 정수", value="1", width=150, data="fld1")
    fld2 = ft.TextField(label="끝 정수", value="6", width=150, data="fld2")
    fld3 = ft.TextField(label="누적곱 결과", read_only=True, data="fld3")
    btn1 = ft.Button("누적", data="btn1")

    def calculate(e):
        try:
            start, end = int(fld1.value or ""), int(fld2.value or "")
            if start > end:
                raise ValueError("시작 값은 끝 값보다 클 수 없습니다.")
            total = 1  # 버튼을 다시 눌러도 이전 결과를 다시 곱하지 않는다.
            for value in range(start, end + 1):
                total *= value
            fld3.value = str(total)
        except ValueError:
            fld3.value = "시작·끝에 정수를 입력하고 시작 ≤ 끝으로 정하세요."
        page.update()

    btn1.on_click = calculate

    async def exercise():
        fld1.value, fld2.value = "1", "6"
        await _invoke(btn1)
        assert fld3.value == "720"
        await _invoke(btn1)
        assert fld3.value == "720"
        fld1.value, fld2.value = "2", "4"
        await _invoke(btn1)
        assert fld3.value == "24"
        for start, end in [("6", "1"), ("", "6"), ("abc", "6"), ("1.5", "6")]:
            fld1.value, fld2.value = start, end
            await _invoke(btn1)
            assert "정수" in fld3.value
        fld1.value, fld2.value = "1", "6"
        await _invoke(btn1)
        return {"one_to_six": fld3.value, "repeat_reset": True,
                "two_to_four": 24, "invalid_cases": 4}

    return _case(page, "009-1", "두 정수 사이의 누적곱", [ft.Row([fld1, btn1, fld2]), fld3], exercise,
                 {"fld1": fld1, "fld2": fld2, "fld3": fld3, "btn1": btn1})


def _calculator(page):
    fld1 = ft.TextField(label="첫째 수", value="100", width=150, data="fld1")
    fld2 = ft.TextField(label="둘째 수", value="5", width=150, data="fld2")
    fld3 = ft.TextField(label="계산 결과", read_only=True, data="fld3")
    btn1, btn2 = ft.Button("+", data="btn1"), ft.Button("=", data="btn2")
    operators = ["+", "-", "*", "/"]

    def change_operator(e):
        btn1.content = operators[(operators.index(btn1.content) + 1) % len(operators)]
        page.update()

    def calculate(e):
        try:
            first, second = float(fld1.value or ""), float(fld2.value or "")
            if not all(map(math.isfinite, (first, second))):
                raise ValueError
            operator = btn1.content
            if operator == "+":
                result = first + second
            elif operator == "-":
                result = first - second
            elif operator == "*":
                result = first * second
            else:
                result = first / second
            fld3.value = str(result)
        except ValueError:
            fld3.value = "두 칸에 유한한 숫자를 입력하세요."
        except ZeroDivisionError:
            fld3.value = "0으로 나눌 수 없습니다."
        page.update()

    btn1.on_click, btn2.on_click = change_operator, calculate

    async def exercise():
        fld1.value, fld2.value, btn1.content = "100", "5", "+"
        results = {}
        for operator, expected in [("+", "105.0"), ("-", "95.0"), ("*", "500.0"), ("/", "20.0")]:
            assert btn1.content == operator
            await _invoke(btn2)
            assert fld3.value == expected
            results[operator] = fld3.value
            await _invoke(btn1)
        assert btn1.content == "+"
        for invalid in ["", "문자", "nan", "inf"]:
            fld1.value = invalid
            await _invoke(btn2)
            assert "숫자" in fld3.value
        fld1.value, fld2.value, btn1.content = "100", "0", "/"
        await _invoke(btn2)
        assert fld3.value == "0으로 나눌 수 없습니다."
        fld2.value = "5"
        await _invoke(btn2)
        return {"operations": results, "invalid_cases": 4, "zero_division_handled": True}

    return _case(page, "009-2", "사칙연산 계산기", [ft.Row([fld1, btn1, fld2, btn2]), fld3], exercise,
                 {"fld1": fld1, "fld2": fld2, "fld3": fld3, "btn1": btn1, "btn2": btn2})


def _append_text(page):
    fld1, txt1 = ft.TextField(label="추가할 문장", data="fld1"), ft.Text("", data="txt1")
    btn1 = ft.Button("추가", data="btn1")

    def append(e):
        value = (fld1.value or "").strip()
        if value:
            txt1.value = "\n".join(filter(None, [txt1.value, value]))
        page.update()

    btn1.on_click = append

    async def exercise():
        txt1.value = ""
        for sentence in ["안녕하세요 저는 코알라입니다", "저는 12살입니다"]:
            fld1.value = sentence
            await _invoke(btn1)
        expected = "안녕하세요 저는 코알라입니다\n저는 12살입니다"
        assert txt1.value == expected
        fld1.value = ""
        await _invoke(btn1)
        assert txt1.value == expected
        return {"text": txt1.value, "line_count": len(txt1.value.splitlines())}

    return _case(page, "009-3", "Text 내용 추가", [fld1, btn1, txt1], exercise,
                 {"fld1": fld1, "btn1": btn1, "txt1": txt1})


def _times_table(page):
    fld1 = ft.TextField(label="출력할 단", value="4", data="fld1")
    btn1, txt1 = ft.Button("구구단 출력", data="btn1"), ft.Text("", data="txt1")

    def calculate(e):
        try:
            number = int(fld1.value or "")
            txt1.value = "\n".join(f"{number} × {i} = {number * i}" for i in range(1, 10))
        except ValueError:
            txt1.value = "정수를 입력하세요."
        page.update()

    btn1.on_click = calculate

    async def exercise():
        fld1.value = "4"
        await _invoke(btn1)
        lines = txt1.value.splitlines()
        assert lines == [f"4 × {i} = {4 * i}" for i in range(1, 10)]
        fld1.value = "문자"
        await _invoke(btn1)
        assert txt1.value == "정수를 입력하세요."
        fld1.value = "4"
        await _invoke(btn1)
        return {"first": lines[0], "last": lines[-1], "line_count": len(lines)}

    return _case(page, "009-4", "4단 구구단 출력", [fld1, btn1, txt1], exercise,
                 {"fld1": fld1, "btn1": btn1, "txt1": txt1})


def _dropdown(page):
    fld1, txt1 = ft.TextField(label="새 항목", data="fld1"), ft.Text("", data="txt1")
    ddl1 = ft.Dropdown(label="색상", options=[], data="ddl1", width=240)
    btn1 = ft.Button("목록 추가", data="btn1")

    def add(e):
        name = (fld1.value or "").strip()
        if name and name not in [option.key for option in ddl1.options]:
            ddl1.options.append(ft.DropdownOption(key=name, text=name))
        page.update()

    def select(e):
        txt1.value = ddl1.value or ""
        page.update()

    btn1.on_click, ddl1.on_select = add, select

    async def exercise():
        ddl1.options = []
        for name in ["빨강", "파랑", "빨강", ""]:
            fld1.value = name
            await _invoke(btn1)
        assert [option.key for option in ddl1.options] == ["빨강", "파랑"]
        ddl1.value = "빨강"
        await _invoke(ddl1, "on_select")
        assert txt1.value == "빨강"
        return {"options": [option.key for option in ddl1.options], "selected": txt1.value}

    return _case(page, "010-1", "Dropdown 항목 추가·선택", [fld1, btn1, ddl1, txt1], exercise,
                 {"fld1": fld1, "btn1": btn1, "ddl1": ddl1, "txt1": txt1})


def _checkboxes(page):
    labels = ["물 충분히 마시기", "운동하기", "아침 식사하기", "7시간 이상 자기"]
    checks = [ft.Checkbox(label=name, value=False, data=f"chk{i + 1}") for i, name in enumerate(labels)]
    btn1, txt1 = ft.Button("결과 확인", data="btn1"), ft.Text("", data="txt1")

    def confirm(e):
        selected = [check.label for check in checks if check.value]
        txt1.value = f"선택한 습관: {', '.join(selected) if selected else '없음'}\n총 {len(selected)}개"
        page.update()

    btn1.on_click = confirm

    async def exercise():
        for check in checks:
            check.value = False
        await _invoke(btn1)
        assert "총 0개" in txt1.value
        checks[0].value = checks[2].value = True
        await _invoke(btn1)
        assert "물 충분히 마시기, 아침 식사하기" in txt1.value and "총 2개" in txt1.value
        checks[0].value = False
        await _invoke(btn1)
        assert "총 1개" in txt1.value and "물 충분히" not in txt1.value
        return {"selected": [c.label for c in checks if c.value], "count": 1, "empty_count": 0}

    return _case(page, "010-2", "건강습관 Checkbox", [*checks, btn1, txt1], exercise,
                 {**{f"chk{i + 1}": c for i, c in enumerate(checks)}, "btn1": btn1, "txt1": txt1})


def _radio(page):
    descriptions = {"코딩": "프로그램과 앱을 만드는 동아리입니다.",
                    "방송": "방송과 영상 콘텐츠를 만드는 동아리입니다.",
                    "미술": "그림과 디자인 활동을 하는 동아리입니다.",
                    "과학": "과학 실험과 탐구 활동을 하는 동아리입니다."}
    radios = [ft.Radio(value=name, label=f"{name} 동아리", data=f"rad{i + 1}")
              for i, name in enumerate(descriptions)]
    group = ft.RadioGroup(content=ft.Column(radios), data="radio_group")
    btn1, txt1 = ft.Button("확인", data="btn1"), ft.Text("", data="txt1")

    def confirm(e):
        name = group.value
        txt1.value = f"{name} 동아리: {descriptions[name]}" if name in descriptions else "동아리를 선택하세요."
        page.update()

    btn1.on_click = confirm

    async def exercise():
        group.value = None
        await _invoke(btn1)
        assert txt1.value == "동아리를 선택하세요."
        for name, description in descriptions.items():
            group.value = name
            await _invoke(btn1)
            assert txt1.value == f"{name} 동아리: {description}"
        assert group.value == "과학"
        return {"tested_choices": list(descriptions), "selected": group.value,
                "description": txt1.value, "single_group": True}

    return _case(page, "010-3", "동아리 RadioGroup", [group, btn1, txt1], exercise,
                 {**{f"rad{i + 1}": c for i, c in enumerate(radios)}, "group": group, "btn1": btn1, "txt1": txt1})


def _progress(page):
    prg1, txt1 = ft.ProgressBar(value=0.0, data="prg1"), ft.Text("0.0", data="txt1")
    btn1, btn2 = ft.Button("증가", data="btn1"), ft.Button("감소", data="btn2")

    def change(delta):
        prg1.value = min(1.0, max(0.0, round((prg1.value or 0.0) + delta, 1)))
        txt1.value = f"{prg1.value:.1f}"
        page.update()

    btn1.on_click, btn2.on_click = lambda e: change(0.1), lambda e: change(-0.1)

    async def exercise():
        prg1.value = 0.0
        await _invoke(btn2)
        assert prg1.value == 0.0
        for i in range(1, 11):
            await _invoke(btn1)
            assert prg1.value == round(i / 10, 1)
        await _invoke(btn1)
        assert prg1.value == 1.0
        for i in range(9, -1, -1):
            await _invoke(btn2)
            assert prg1.value == round(i / 10, 1)
        await _invoke(btn2)
        assert prg1.value == 0.0
        for _ in range(5):
            await _invoke(btn1)
        return {"min": 0.0, "max": 1.0, "step": 0.1, "display": txt1.value, "boundary_checks": 2}

    return _case(page, "010-4", "진행 막대 증가·감소", [prg1, ft.Row([btn1, btn2]), txt1], exercise,
                 {"prg1": prg1, "btn1": btn1, "btn2": btn2, "txt1": txt1})


def _images(page):
    # 배포된 책에 포함된 실제 PNG 두 개를 사용하므로 네트워크가 필요 없다.
    files = [BOOK / "assets/ch01/ai-human-summary.png", BOOK / "assets/source-20261006/plot-one.png"]
    sources = [path.read_bytes() for path in files]
    img1 = ft.Image(src=sources[0], width=320, height=120, fit=ft.BoxFit.CONTAIN, data="img1")
    img2 = ft.Image(src=sources[1], width=240, height=150, fit=ft.BoxFit.CONTAIN, data="img2")

    async def exercise():
        sizes = []
        for image, source, expected in zip([img1, img2], sources, [(320, 120), (240, 150)]):
            assert image.page is page and isinstance(image.src, bytes)
            assert source.startswith(b"\x89PNG\r\n\x1a\n")
            width, height = struct.unpack(">II", source[16:24])
            assert width > 0 and height > 0
            assert (image.width, image.height) == expected
            sizes.append({"source_pixels": [width, height], "display_size": list(expected)})
        return {"images": sizes, "vertical_order": ["img1", "img2"],
                "source_files": [p.relative_to(BOOK).as_posix() for p in files]}

    return _case(page, "010-5", "두 Image 세로 배치", [img1, img2], exercise, {"img1": img1, "img2": img2})


def _student_table(page):
    titles = ["이름", "국어", "수학", "영어"]
    fields = [ft.TextField(label=title, width=125, data=f"fld{i + 1}") for i, title in enumerate(titles)]
    tbl1 = ft.DataTable(columns=[ft.DataColumn(ft.Text(title)) for title in titles], rows=[], data="tbl1")
    btn1, txt1 = ft.Button("추가하기", data="btn1"), ft.Text("", data="txt1")
    row_field = ft.TextField(label="행 번호(1부터)", value="1", width=135, data="edit_row")
    col_field = ft.TextField(label="열 번호(1부터)", value="1", width=135, data="edit_column")
    value_field = ft.TextField(label="변경할 값", width=140, data="edit_value")
    btn2 = ft.Button("셀 변경", data="btn2")

    def score(text):
        value = float(text)
        if not math.isfinite(value) or not 0 <= value <= 100:
            raise ValueError
        return f"{value:g}"

    def append(e):
        try:
            name = (fields[0].value or "").strip()
            if not name:
                raise ValueError
            values = [name] + [score(field.value or "") for field in fields[1:]]
            tbl1.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(value)) for value in values]))
            txt1.value = f"{len(tbl1.rows)}행 기록"
        except ValueError:
            txt1.value = "이름과 0~100 사이의 점수를 입력하세요."
        page.update()

    def edit(e):
        try:
            row, column = int(row_field.value or ""), int(col_field.value or "")
            if not 1 <= row <= len(tbl1.rows) or not 1 <= column <= len(titles):
                raise IndexError
            value = (value_field.value or "").strip()
            if not value:
                raise ValueError
            if column > 1:
                value = score(value)
            tbl1.rows[row - 1].cells[column - 1].content.value = value
            txt1.value = f"{row}행 {column}열 변경"
        except (ValueError, IndexError):
            txt1.value = "행·열 범위와 입력값을 확인하세요."
        page.update()

    btn1.on_click, btn2.on_click = append, edit

    def values():
        return [[cell.content.value for cell in row.cells] for row in tbl1.rows]

    async def exercise():
        tbl1.rows = []
        for record in [["학생1", "100", "90", "80"], ["학생2", "70", "60", "50"]]:
            for field, value in zip(fields, record):
                field.value = value
            await _invoke(btn1)
        assert values() == [["학생1", "100", "90", "80"], ["학생2", "70", "60", "50"]]
        row_field.value, col_field.value, value_field.value = "2", "3", "95"
        await _invoke(btn2)
        assert values()[1] == ["학생2", "70", "95", "50"]
        saved = values()
        for row, column in [("0", "1"), ("-1", "1"), ("3", "1"), ("1", "0"), ("1", "5"), ("x", "1")]:
            row_field.value, col_field.value = row, column
            await _invoke(btn2)
            assert values() == saved and "범위" in txt1.value
        fields[2].value = "101"
        await _invoke(btn1)
        assert values() == saved
        row_field.value, col_field.value, value_field.value = "1", "2", "100"
        await _invoke(btn2)
        return {"columns": titles, "rows": values(), "edited_cell": [2, 3, "95"],
                "invalid_index_cases": 6, "invalid_score_rejected": True}

    controls = [ft.Row(fields, wrap=True), btn1, tbl1,
                ft.Row([row_field, col_field, value_field, btn2], wrap=True), txt1]
    widgets = {**{f"fld{i + 1}": field for i, field in enumerate(fields)},
               "tbl1": tbl1, "btn1": btn1, "btn2": btn2, "txt1": txt1,
               "edit_row": row_field, "edit_column": col_field, "edit_value": value_field}
    return _case(page, "011-1", "학생 성적 DataTable 추가·셀 변경", controls, exercise, widgets)


def build_cases(page: ft.Page) -> list[dict]:
    """실제 Page에 장착할 13개 독립 실습과 실행 검증 함수를 만든다."""
    return [factory(page) for factory in [
        _colors, _message, _copy_delete, _product, _calculator, _append_text,
        _times_table, _dropdown, _checkboxes, _radio, _progress, _images, _student_table,
    ]]
