"""Execute textbook drawing snippets using the real generated Flet chart context.

The common setup imports flet_charts before pyplot so its actual Matplotlib
backend is used. Each fixed-data snippet runs twice against the same chart.
Layout and canvas refresh are performed by this tool after the exact student
logic, so those execution details are absent from the printed examples.
No fake chart, replacement canvas, injected Agg backend or pyplot.show hook is
used. Control mounting and live Flet event dispatch are outside this checker.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.metadata
import io
import json
import re
import sys
import warnings
from datetime import date
from pathlib import Path

# flet_charts selects its Matplotlib backend before pyplot is imported.
import flet_charts as fch
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coala-book-md/vibe-coding-16"


def code_blocks(text: str) -> dict[str, str]:
    blocks = {}
    pattern = r':::page\{[^\n]*id="([^\"]+)"[^\n]*\}\n(.*?)(?=\n:::\s*(?:\n|$))'
    for page in re.finditer(pattern, text, re.S):
        code = re.search(r"```python\n(.*?)\n```", page[2], re.S)
        if code:
            assert page[1] not in blocks, f"Duplicate code page: {page[1]}"
            blocks[page[1]] = code[1]
    return blocks


def assert_chart_binding(namespace: dict, identities=None):
    figure = namespace["fig_cht1"]
    axes = namespace["ax_cht1"]
    chart = namespace["cht1"]
    assert isinstance(chart, fch.MatplotlibChart)
    assert chart.figure is figure
    assert len(figure.axes) == 1 and figure.axes[0] is axes
    assert np.allclose(figure.get_size_inches(), (6.4, 4.8))
    assert type(figure.canvas).__module__.startswith("flet_charts.")
    assert "flet_charts" in str(matplotlib.get_backend())
    current = tuple(id(namespace[name]) for name in ("fig_cht1", "ax_cht1", "cht1"))
    if identities is not None:
        assert current == identities, "Snippet replaced the chart, Figure or Axes"
    return current


def execute_setup(code: str):
    plt.rcdefaults()
    plt.close("all")
    namespace = {"__name__": "textbook_chart_setup"}
    capture = io.StringIO()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with contextlib.redirect_stdout(capture):
            exec(compile(code, "chart_setup.py", "exec"), namespace)
            assert_chart_binding(namespace)
            namespace["fig_cht1"].canvas.draw()
    messages = sorted({str(item.message) for item in caught})
    assert not messages, f"Warnings in chart setup: {messages}"
    return namespace, capture.getvalue().rstrip(), messages


def execute_plot(path: Path, image_path: Path, setup_code: str, page_id: str):
    namespace, setup_stdout, setup_messages = execute_setup(setup_code)
    identities = assert_chart_binding(namespace)
    code = path.read_text(encoding="utf-8").rstrip()
    assert "plt.subplots" not in code and "plt.show" not in code
    assert "ax_cht1.clear()" in code
    assert "fig_cht1.tight_layout()" not in code and "fig_cht1.canvas.draw_idle()" not in code
    capture = io.StringIO()
    repeated_semantics = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        with contextlib.redirect_stdout(capture):
            for _ in range(2):
                exec(compile(code, str(path), "exec"), namespace)
                assert_chart_binding(namespace, identities)
                figure, axes = namespace["fig_cht1"], namespace["ax_cht1"]
                # The execution tool owns layout/refresh; these calls are not
                # part of the student-visible drawing logic.
                figure.tight_layout()
                figure.canvas.draw_idle()
                figure.canvas.draw()
                semantics = check_semantics(page_id, axes, namespace)
                if page_id.startswith("ch12-"):
                    assert len(axes.lines) == 1 and not axes.collections and not axes.patches
                elif page_id == "ch13-scatter":
                    assert len(axes.collections) == 1 and not axes.lines and not axes.patches
                repeated_semantics.append(semantics)
            assert repeated_semantics[0] == repeated_semantics[1]
            figure.savefig(image_path, dpi=240, facecolor="white")
            assert_chart_binding(namespace, identities)
    messages = sorted({str(item.message) for item in caught})
    assert not messages, f"Warnings in {path.name}: {messages}"
    with Image.open(image_path) as image:
        assert image.size == (1536, 1152)
    return namespace["ax_cht1"], namespace, capture.getvalue().rstrip(), messages, repeated_semantics[-1]


def check_semantics(page_id: str, ax, namespace: dict) -> dict:
    if page_id == "ch12-one-array":
        line = ax.lines[0]
        assert list(line.get_xdata()) == list(range(5))
        assert list(line.get_ydata()) == [1, 2, 3, 4, 5]
        return {"x": list(map(float, line.get_xdata())),
                "y": list(map(float, line.get_ydata()))}

    if page_id == "ch12-two-arrays":
        line = ax.lines[0]
        assert list(line.get_xdata()) == [15, 25, 35, 45, 55]
        assert list(line.get_ydata()) == [5, 10, 15, 20, 25]
        return {"x": list(map(float, line.get_xdata())),
                "y": list(map(float, line.get_ydata()))}

    if page_id == "ch12-range":
        line = ax.lines[0]
        assert list(line.get_xdata()) == [1, 2, 3, 4, 5]
        assert list(line.get_ydata()) == [5, 10, 15, 20, 25]
        assert line.get_marker() == "+"
        assert line.get_color() == "b"
        assert tuple(ax.get_xlim()) == (0, 10)
        assert tuple(ax.get_ylim()) == (0, 25)
        return {"marker": line.get_marker(), "color": line.get_color(),
                "xlim": list(ax.get_xlim()), "ylim": list(ax.get_ylim())}

    if page_id == "ch12-markers":
        line = ax.lines[0]
        assert line.get_marker() == "o"
        assert line.get_color() == "r"
        assert line.get_linestyle() == "None"
        assert ax.get_xlabel() == "x"
        assert ax.get_ylabel() == "y"
        assert ax.get_title() == "hello"
        assert any(t.get_text() == "12/19" and t.get_position() == (3, 5)
                   for t in ax.texts)
        return {"marker": line.get_marker(), "color": line.get_color(),
                "linestyle": line.get_linestyle(),
                "annotation": "12/19 at (3, 5)"}

    if page_id == "ch13-bars":
        heights = [bar.get_height() for bar in ax.patches]
        assert heights == [1, 2, 4, 8, 16, 32, 64, 128]
        assert len(ax.patches) == 8
        return {"heights": heights}

    if page_id == "ch13-grouped":
        assert len(ax.patches) == 10
        heights = [bar.get_height() for bar in ax.patches]
        assert heights == [35, 80, 84, 83, 50, 73, 80, 77, 40, 86]
        centers = [bar.get_x() + bar.get_width() / 2 for bar in ax.patches]
        assert np.allclose(centers[:5], [.8, 2.8, 4.8, 6.8, 8.8])
        assert np.allclose(centers[5:], [1.6, 3.6, 5.6, 7.6, 9.6])
        assert np.allclose(ax.get_xticks(), [1.2, 3.2, 5.2, 7.2, 9.2])
        assert [tick.get_text() for tick in ax.get_xticklabels()] == [
            "one", "two", "three", "four", "five",
        ]
        return {"heights": heights, "centers": centers,
                "ticks": list(ax.get_xticks())}

    if page_id == "ch13-scatter":
        offsets = np.asarray(ax.collections[0].get_offsets())
        x, y = offsets[:, 0], offsets[:, 1]
        assert len(x) == 20
        assert np.allclose(x, np.arange(1.1, 100.0, 5.0))
        assert np.all(y >= x * 1.5)
        assert np.all(y < x * 1.5 + 50)
        np.random.seed(20211206)
        assert np.allclose(y, x * 1.5 + np.random.rand(20) * 50)
        assert ax.get_xlabel() == "X axis"
        assert ax.get_ylabel() == "Y axis"
        assert ax.get_title() == "random"
        assert [t.get_text() for t in ax.get_legend().get_texts()] == ["random"]
        return {"points": len(x), "first_point": offsets[0].tolist(),
                "last_point": offsets[-1].tolist(), "seed_repeatability": True,
                "labels": [ax.get_xlabel(), ax.get_ylabel()]}

    raise AssertionError(f"No semantic check defined for {page_id}")


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2,
                               default=lambda value: value.item()) + "\n",
                    encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path("tmp/pdfs/flet-code-review"))
    parser.add_argument("--review-date", type=date.fromisoformat, default=date(2026, 10, 27))
    args = parser.parse_args()
    output = args.dest if args.dest.is_absolute() else ROOT / args.dest
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    specs = json.loads((BOOK / "code-specs.json").read_text(encoding="utf-8"))
    results_path = BOOK / "code-results.json"
    previous = json.loads(results_path.read_text(encoding="utf-8"))
    historical = {record["page_id"]: record for record in previous["records"]}
    full_blocks = code_blocks((BOOK / "book.md").read_text(encoding="utf-8"))
    chapter_blocks = code_blocks("\n".join(
        (BOOK / f"ch{chapter:02d}.md").read_text(encoding="utf-8")
        for chapter in sorted({spec["chapter"] for spec in specs})
    ))
    expected_ids = {spec["page_id"] for spec in specs}
    assert set(chapter_blocks) == set(full_blocks) == expected_ids
    assert len(expected_ids) == 8
    assert {path.name for path in (BOOK / "examples/source-based").glob("*.py")} == {
        spec["file"] for spec in specs
    }
    for spec in specs:
        path = BOOK / "examples/source-based" / spec["file"]
        code = path.read_text(encoding="utf-8").rstrip()
        assert code == chapter_blocks[spec["page_id"]], f"Chapter mismatch: {path.name}"
        assert code == full_blocks[spec["page_id"]], f"book.md mismatch: {path.name}"
        assert code == spec["code"], f"Code specification mismatch: {path.name}"
    setup_specs = [spec for spec in specs if spec["role"] == "generated-chart-setup"]
    practice_specs = [spec for spec in specs if spec["role"] == "drawing-event-body"]
    assert len(setup_specs) == 1 and len(practice_specs) == 7
    setup_spec = setup_specs[0]
    setup_code = setup_spec["code"]
    namespace, stdout, messages = execute_setup(setup_code)
    records = [{"page_id": setup_spec["page_id"], "status": "passed",
                "role": setup_spec["role"], "file": setup_spec["file"],
                "source_pdf_pages": None, "stdout": stdout,
                "code_sha256": hashlib.sha256(setup_code.encode("utf-8")).hexdigest(),
                "result_asset": None, "warnings": messages,
                "semantics": {"figure_inches": [6.4, 4.8],
                              "chart_binding": True, "real_flet_control": True},
                "chart_binding": True}]
    plt.close("all")
    for spec in practice_specs:
        page_id = spec["page_id"]
        path = BOOK / "examples/source-based" / spec["file"]
        ax, namespace, stdout, messages, semantics = execute_plot(
            path, output / (spec["result"] + ".png"), setup_code, page_id,
        )
        metadata = historical.get(page_id, {})
        records.append({
            "page_id": page_id, "status": "passed", "role": spec["role"],
            "file": spec["file"],
            "source_pdf_pages": spec.get("source_pdf_pages", metadata.get("source_pdf_pages")),
            "stdout": stdout,
            "code_sha256": hashlib.sha256(spec["code"].encode("utf-8")).hexdigest(),
            "result_asset": spec["result"], "semantics": semantics, "warnings": messages,
            "chart_binding": True, "repeated_updates": True, "draw_count": 2,
            "automatic_refresh_outside_logic": True,
        })
        plt.close("all")
    report = {
        "reviewed_date": args.review_date.isoformat(),
        "edition": "flet-chart-context-16-sessions",
        "python": sys.version.split()[0], "runtime": sys.executable,
        "flet": importlib.metadata.version("flet"),
        "flet_charts": importlib.metadata.version("flet-charts"),
        "matplotlib": matplotlib.__version__, "numpy": np.__version__,
        "matplotlib_backend": str(matplotlib.get_backend()),
        "executed_blocks": len(records), "passed": len(records),
        "practice_blocks": len(practice_specs), "setup_blocks": len(setup_specs),
        "practice_runs": len(practice_specs) * 2,
        "records": records, "chapter_blocks_match_files": True,
        "book_blocks_match_files": True, "code_specs_match_files": True,
        "plot_pixels": [1536, 1152], "plot_dpi": 240,
        "chart_binding": True, "repeated_updates": True,
        "automatic_refresh_outside_logic": True,
        "execution_scope": "Real Flet MatplotlibChart construction and backend rendering; each of 7 drawing bodies executed twice on its original Figure/Axes/control. Controls were not mounted in a live Flet session by this checker.",
    }
    write_json(output / "execution-results.json", report)
    write_json(results_path, report)
    print(json.dumps({"executed_blocks": len(records), "passed": len(records),
                      "practice_blocks": len(practice_specs), "practice_runs": 14,
                      "warnings": sum(len(item["warnings"]) for item in records),
                      "chart_binding": True, "repeated_updates": True,
                      "backend": report["matplotlib_backend"],
                      "output": str(output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
