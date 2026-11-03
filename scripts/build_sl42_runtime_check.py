"""Build a single pasteable sl42 program from the actual textbook Flet suite.

The resulting program reconstructs the same source files and fixture assets in
the browser Python filesystem, then runs the existing gallery against its real
Flet Page. This builder only packages and compiles source; it never runs Flet.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
from pathlib import Path
import textwrap
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BOOK_REL = Path("coala-book-md/vibe-coding-16")
SUITE_REL = BOOK_REL / "examples/flet-practices"


def gallery_for_sl42(source: str) -> str:
    """Add final bounded console evidence to an embedded copy of gallery.py."""
    marker = "    return report\n"
    assert source.count(marker) == 1
    summary = '''    if len(records) == 32:
        summary = {key: report[key] for key in (
            "reviewed_date", "python", "flet", "flet_charts", "tested", "passed", "failed",
            "cloud_project_save_tested",
        )}
        summary["execution"] = "sl42 real browser-connected Flet Page; actual control callbacks"
        summary["cases"] = [
            {key: record[key] for key in ("id", "status", "error") if key in record}
            for record in records
        ]
        print("SL42_CHECK_RESULTS=" + json.dumps(summary, ensure_ascii=False), flush=True)
    return report
'''
    return source.replace(marker, summary)


def package_files():
    files = [
        SUITE_REL / name for name in (
            "gallery.py", "basic.py", "data.py", "plots.py",
            "basic-cases.json", "data-cases.json",
        )
    ]
    files += [Path("scripts/check_practice_code.py"), BOOK_REL / "code-specs.json"]
    specs = json.loads((ROOT / BOOK_REL / "code-specs.json").read_text(encoding="utf-8"))
    assert len(specs) == 8
    files += [BOOK_REL / "examples/source-based" / item["file"] for item in specs]
    files += [BOOK_REL / "assets/ch01/ai-human-summary.png",
              BOOK_REL / "assets/source-20261006/plot-one.png"]
    assert len(files) == len(set(files)) == 18
    manifest = []
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in files:
            path = ROOT / relative
            original = path.read_bytes()
            data = (gallery_for_sl42(original.decode("utf-8")).encode("utf-8")
                    if relative == SUITE_REL / "gallery.py" else original)
            if path.suffix == ".py":
                compile(data.decode("utf-8"), relative.as_posix(), "exec")
            info = zipfile.ZipInfo(relative.as_posix(), (2026, 10, 27, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, data)
            manifest.append({
                "path": relative.as_posix(), "bytes": len(data),
                "source_sha256": hashlib.sha256(original).hexdigest(),
                "embedded_sha256": hashlib.sha256(data).hexdigest(),
            })
    return buffer.getvalue(), manifest


def make_program(payload: bytes, manifest: list[dict]) -> str:
    encoded = base64.b64encode(payload).decode("ascii")
    chunks = "\n".join("    " + repr(chunk) for chunk in textwrap.wrap(encoded, width=100))
    manifest_literal = repr(json.dumps(manifest, ensure_ascii=False, separators=(",", ":")))
    return '''"""실제 sl42 브라우저 Flet 런타임에서 교재 실습 32개를 점검합니다.

현재 교재와 같은 원본 실습·코드·학생 표본·이미지를 포함합니다.
가상 Page나 가짜 차트를 만들지 않습니다. 실제 페이지 연결 후 콜백을 실행합니다.
클라우드 프로젝트 제출·저장·업로드는 하지 않습니다.
"""
# These explicit imports are also consumed by sl42's real package detector.
import flet as ft
import flet_charts as fch
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import base64
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import runpy
import sys
import zipfile

_COALA_MANIFEST = json.loads(''' + manifest_literal + ''')
_COALA_BUNDLE = (
''' + chunks + '''
)
_COALA_ROOT = Path("/tmp/coala-check")
_COALA_ROOT.mkdir(parents=True, exist_ok=True)
_COALA_EXPECTED = {item["path"]: item for item in _COALA_MANIFEST}
with zipfile.ZipFile(io.BytesIO(base64.b64decode(_COALA_BUNDLE))) as _archive:
    assert set(_archive.namelist()) == set(_COALA_EXPECTED)
    for _name in _archive.namelist():
        _relative = PurePosixPath(_name)
        assert not _relative.is_absolute() and ".." not in _relative.parts
        _data = _archive.read(_name)
        assert hashlib.sha256(_data).hexdigest() == _COALA_EXPECTED[_name]["embedded_sha256"]
        _path = _COALA_ROOT.joinpath(*_relative.parts)
        _path.parent.mkdir(parents=True, exist_ok=True)
        _path.write_bytes(_data)

_gallery = _COALA_ROOT / "coala-book-md/vibe-coding-16/examples/flet-practices/gallery.py"
sys.path.insert(0, str(_COALA_ROOT / "scripts"))
sys.argv = [str(_gallery), "--auto-check"]
print("SL42_RUNTIME_CHECK_START=" + json.dumps({
    "embedded_files": len(_COALA_MANIFEST), "expected_cases": 32,
    "page": "actual sl42 Flet runtime", "cloud_project_save": False,
}, ensure_ascii=False), flush=True)
runpy.run_path(str(_gallery), run_name="__main__")
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "tmp/pdfs/sl42-runtime-check.py")
    parser.add_argument("--delivery-output", type=Path,
                        default=ROOT / SUITE_REL / "sl42-runtime-check.py")
    args = parser.parse_args()
    output = args.output.resolve()
    delivery_output = args.delivery_output.resolve()
    assert all(path.is_relative_to(ROOT.resolve()) for path in (output, delivery_output)), \
        "Outputs must stay in the task workspace"
    payload, manifest = package_files()
    program = make_program(payload, manifest)
    compile(program, str(output), "exec")
    for destination in {output, delivery_output}:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(program, encoding="utf-8", newline="\n")
    assert output.stat().st_size < 500_000
    assert output.read_bytes() == delivery_output.read_bytes()
    print(json.dumps({"output": str(output), "delivery_output": str(delivery_output),
          "files": len(manifest),
          "zip_bytes": len(payload), "program_bytes": output.stat().st_size,
          "program_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
          "compiled": True, "host_flet_execution": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
