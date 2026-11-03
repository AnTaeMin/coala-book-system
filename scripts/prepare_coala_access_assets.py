"""Prepare evidence-preserving screen viewports and a local ebook preview.

The screenshots are retained byte-for-byte under sources/. Viewports are
native PDF page clips rendered to PNG, without redrawing any website UI.
The ebook preview is a document layout made from the current local PDF,
not a screenshot of a newly published website.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas

from build_textbook_pdf import BOOK, ROOT, fonts

DEST = BOOK / "assets/coala-access-20261028"
SOURCES = Path("C:/Users/use/Pictures/Screenshots")
CURRENT_PDF = ROOT / "output/pdf/vibe-coding-16-coala-access.pdf"
SOURCE_FILES = {
    "homepage": "스크린샷 2026-10-28 134809.png",
    "download": "스크린샷 2026-10-28 134835.png",
    "login": "스크린샷 2026-10-28 134907.png",
    "dashboard": "스크린샷 2026-10-28 134926.png",
    "old-ebook-reference": "스크린샷 2026-10-28 135122.png",
}

# Bounds are in the original screenshot's top-left pixel coordinate system.
VIEWPORTS = {
    "homepage": ("homepage", (240, 0, 1660, 735)),
    "download": ("download", (440, 455, 1125, 903)),
    "web-version": ("download", (450, 465, 785, 680)),
    "online-book": ("download", (790, 690, 1120, 903)),
    "login": ("login", (1185, 335, 1630, 585)),
    "login-context": ("login", (500, 0, 1630, 590)),
    "dashboard": ("dashboard", (600, 65, 1550, 335)),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_pdf(path: Path, output: Path) -> tuple[int, int]:
    doc = pdfium.PdfDocument(str(path))
    page = doc[0]
    bitmap = page.render(scale=1)
    image = bitmap.to_pil().convert("RGB")
    image.save(output)
    size = image.size
    bitmap.close()
    page.close()
    doc.close()
    return size


def screenshot_viewport(source: Path, bounds: tuple[int, int, int, int],
                        name: str) -> dict:
    with Image.open(source) as image:
        iw, ih = image.size
    x0, y0, x1, y1 = bounds
    assert 0 <= x0 < x1 <= iw and 0 <= y0 < y1 <= ih
    width, height = x1 - x0, y1 - y0
    pdf = DEST / f"{name}.pdf"
    png = DEST / f"{name}.png"
    c = canvas.Canvas(str(pdf), pagesize=(width, height), pageCompression=1)
    c.setTitle(f"COALA screen viewport: {name}")
    c.saveState()
    clip = c.beginPath()
    clip.rect(0, 0, width, height)
    c.clipPath(clip, stroke=0, fill=0)
    c.drawImage(str(source), -x0, y1 - ih, width=iw, height=ih)
    c.restoreState()
    c.showPage()
    c.save()
    pixels = render_pdf(pdf, png)
    return {
        "src": png.relative_to(BOOK).as_posix(),
        "document_viewport_pdf": pdf.relative_to(BOOK).as_posix(),
        "kind": "user-supplied-screenshot-viewport",
        "source": source.relative_to(BOOK).as_posix(),
        "source_sha256": digest(source),
        "crop_bounds_top_left_px": list(bounds),
        "source_dimensions_px": [iw, ih],
        "width": pixels[0], "height": pixels[1],
        "ratio": f"{pixels[0]}:{pixels[1]}",
        "sha256": digest(png),
        "ui_text_redrawn": False,
        "pixel_content_invented": False,
        "upscaled": False,
    }


def prepare_screenshots() -> tuple[list[dict], list[dict]]:
    originals = DEST / "sources"
    originals.mkdir(parents=True, exist_ok=True)
    sources = []
    for key, filename in SOURCE_FILES.items():
        source = SOURCES / filename
        copied = originals / f"{key}.png"
        shutil.copy2(source, copied)
        assert digest(source) == digest(copied)
        sources.append({
            "original_filename": filename,
            "src": copied.relative_to(BOOK).as_posix(),
            "sha256": digest(copied),
            "copied_intact": True,
            "used_in_student_guide": key != "old-ebook-reference",
            "note": ("Reference only: shows the superseded edition; never placed in the guide."
                     if key == "old-ebook-reference" else "User-provided screenshot"),
        })
    assets = [screenshot_viewport(originals / f"{source}.png", bounds, name)
              for name, (source, bounds) in VIEWPORTS.items()]
    return sources, assets


def prepare_preview(pdf_source: Path) -> dict:
    """Make a two-page reader-like layout using actual local PDF vectors."""
    fonts()
    width, height = 1600, 900
    header, margin, gap = 52, 24, 24
    base = DEST / "ebook-preview-frame.pdf"
    result = DEST / "ebook-preview.pdf"
    png = DEST / "ebook-preview.png"
    c = canvas.Canvas(str(base), pagesize=(width, height), pageCompression=1)
    c.setTitle("전자책 · 수정 교재 화면 예시")
    c.setAuthor("Coala")
    c.setFillColor(HexColor("#F4F5F7"))
    c.rect(0, 0, width, height, fill=1, stroke=0)
    c.setFillColor(white)
    c.rect(0, height-header, width, header, fill=1, stroke=0)
    c.setStrokeColor(HexColor("#DDE3EC"))
    c.line(0, height-header, width, height-header)
    c.setFillColor(HexColor("#151515"))
    c.setFont("WantedBold", 20)
    c.drawCentredString(width/2, height-33, "전자책")
    source = PdfReader(pdf_source)
    assert len(source.pages) >= 2
    scale = min((height-header-margin*2) / float(source.pages[0].mediabox.height),
                (width-margin*2-gap) / (2*float(source.pages[0].mediabox.width)))
    page_width = float(source.pages[0].mediabox.width) * scale
    page_height = float(source.pages[0].mediabox.height) * scale
    left = (width - page_width*2-gap) / 2
    bottom = margin + (height-header-margin*2-page_height)/2
    for index in range(2):
        c.setFillColor(white)
        c.rect(left+index*(page_width+gap), bottom, page_width, page_height,
               fill=1, stroke=0)
    c.showPage()
    c.save()
    writer = PdfWriter()
    writer.add_page(PdfReader(base).pages[0])
    for index in range(2):
        transform = Transformation().scale(scale).translate(
            left+index*(page_width+gap), bottom)
        writer.pages[0].merge_transformed_page(source.pages[index], transform)
    writer.write(result)
    pixels = render_pdf(result, png)
    base.unlink()
    return {
        "src": png.relative_to(BOOK).as_posix(),
        "vector_src": result.relative_to(BOOK).as_posix(),
        "kind": "generated-local-ebook-preview",
        "source_pdf": str(pdf_source.resolve()),
        "source_pdf_sha256": digest(pdf_source),
        "source_pdf_pages": [1, 2],
        "source_pdf_page_count": len(source.pages),
        "width": pixels[0], "height": pixels[1],
        "ratio": "16:9", "sha256": digest(png),
        "vector_sha256": digest(result),
        "caption": "수정 교재 화면 예시",
        "is_live_website_screenshot": False,
        "old_ebook_screenshot_used": False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-only", action="store_true")
    parser.add_argument("--screenshots-only", action="store_true")
    parser.add_argument("--pdf", type=Path, default=CURRENT_PDF)
    args = parser.parse_args()
    assert not (args.preview_only and args.screenshots_only)
    DEST.mkdir(parents=True, exist_ok=True)
    manifest = DEST / "provenance.json"
    record = (json.loads(manifest.read_text(encoding="utf-8"))
              if manifest.exists() else {"date": "2026-10-28"})
    if not args.preview_only:
        record["sources"], record["screenshots"] = prepare_screenshots()
    if not args.screenshots_only:
        record["ebook_preview"] = prepare_preview(args.pdf)
    manifest.write_text(json.dumps(record, ensure_ascii=False, indent=2)+"\n",
                        encoding="utf-8")
    print(json.dumps({"assets": [item["src"] for item in record.get("screenshots", [])],
                      "preview": record.get("ebook_preview", {}).get("src"),
                      "provenance": manifest.relative_to(ROOT).as_posix()},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
