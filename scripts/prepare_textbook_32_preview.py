"""Refresh only the 32-session edition's local ebook preview and its provenance.

The preview uses the actual cover and first contents page of the supplied PDF.
All user-supplied screenshots and the 16-session edition remain untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from pypdf import PdfReader

import prepare_coala_access_assets as prior

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coala-book-md/vibe-coding-32"
DEST = BOOK / "assets/coala-access-20261028"
PREVIEW_SRC = "assets/coala-access-20261028/ebook-preview.png"
PREVIEW_FILES = {"ebook-preview.png", "ebook-preview.pdf", "provenance.json"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path,
                        default=ROOT / "output/pdf/vibe-coding-32-coala-access-reviewed.pdf")
    args = parser.parse_args()
    source = args.pdf.resolve()
    reader = PdfReader(source)
    cover = "".join((reader.pages[0].extract_text() or "").split())
    if "32차시" not in cover:
        raise ValueError("The preview source must show the actual 32-session cover")
    if len(reader.pages) < 2 or "학습차례" not in "".join(
            (reader.pages[1].extract_text() or "").split()):
        raise ValueError("The preview source's second page must be its contents")

    provenance_path = DEST / "provenance.json"
    manifest_path = BOOK / "asset-manifest.json"
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = [item for item in manifest["items"] if item.get("src") == PREVIEW_SRC]
    if len(items) != 1:
        raise ValueError("Expected exactly one ebook preview item in the 32-session asset manifest")

    # Verify that this narrowly scoped operation does not touch other assets.
    unchanged_assets = {
        path: digest(path) for path in (BOOK / "assets").rglob("*")
        if path.is_file() and not (path.parent == DEST and path.name in PREVIEW_FILES)
    }
    original_root = ROOT / "coala-book-md/vibe-coding-16"
    original_files = {
        path: digest(path) for path in (
            original_root / "asset-manifest.json",
            original_root / "assets/coala-access-20261028/provenance.json",
            original_root / PREVIEW_SRC,
            original_root / "assets/coala-access-20261028/ebook-preview.pdf",
        ) if path.exists()
    }

    prior.BOOK = BOOK
    prior.DEST = DEST
    preview = prior.prepare_preview(source)
    preview["source_pdf_edition_sessions"] = 32
    preview["source_pdf_snapshot_note"] = (
        "Generated from the actual cover and first contents page of this local "
        "32-session PDF at the recorded source hash. Re-embedding the preview "
        "changes the whole PDF hash while retaining those source pages."
    )
    provenance["ebook_preview"] = preview
    provenance["ebook_preview_review_date"] = "2026-11-03"
    # Preserve placement and chapter fields while updating generated-asset data.
    items[0].update(preview)
    write_json(provenance_path, provenance)
    write_json(manifest_path, manifest)

    changed = [str(path.relative_to(BOOK)) for path, sha in unchanged_assets.items()
               if not path.exists() or digest(path) != sha]
    if changed:
        raise ValueError(f"Unexpected non-preview asset changes: {changed}")
    if any(not path.exists() or digest(path) != sha
           for path, sha in original_files.items()):
        raise ValueError("The 16-session edition must remain unchanged")
    print(json.dumps({
        "preview": PREVIEW_SRC,
        "sourcePdf": str(source),
        "sourcePages": preview["source_pdf_pages"],
        "sourceEditionSessions": 32,
        "preservedOtherAssets": len(unchanged_assets),
        "provenance": str(provenance_path.relative_to(ROOT)),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
