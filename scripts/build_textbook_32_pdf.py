"""Typeset the 32-session edition while preserving the 16-session pipeline.

The source manuscript and split map live in vibe-coding-32.  Existing artwork,
code and vector flowcharts use the same production rules as the prior edition.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import HexColor

import build_textbook_pdf as base
import finalize_textbook_pdf as prior

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "coala-book-md/vibe-coding-32"
CONTENTS_GROUPS = [
    [("AI", list(range(1, 5))), ("알고리즘", list(range(5, 9)))],
    [("알고리즘 · 계속", list(range(9, 15)))],
    [("GUI · 앱 제작", list(range(15, 24)))],
    [("GUI · 앱 제작 · 계속", list(range(24, 33)))],
]


class Production32(prior.FinalProduction):
    def plan(self):
        self.pages = [{
            "id": "cover", "type": "cover", "chapter": 0,
            "title": self.spec["title"], "blocks": [],
        }]
        self.pages.extend({
            "id": f"toc-{index + 1}", "type": "contents", "chapter": 0,
            "title": "학습 차례", "part": index, "blocks": [],
        } for index in range(len(CONTENTS_GROUPS)))
        for source in self.spec["pages"]:
            kind = source["type"]
            if kind == "chapter-opening":
                self.chapter_opening(source)
            elif kind == "practice-opening":
                self.practice_opening(source)
            elif kind == "flowchart":
                self.diagram(source)
            else:
                self.compact_regular(source)
        self.chapter_pages = {
            page["chapter"]: index
            for index, page in enumerate(self.pages, 1)
            if page["type"] == "chapter-opening"
        }
        if sorted(self.chapter_pages) != list(range(1, 33)):
            raise ValueError("The manuscript must contain exactly 32 session openings")


def draw_cover(c, spec):
    prior.draw_text(c, "32차시 학생용 교재", prior.LEFT, 78,
                    "WantedBold", 15, prior.INDIGO)
    c.setStrokeColor(HexColor(prior.INDIGO))
    c.setLineWidth(2)
    c.line(prior.LEFT, prior.H - 122, prior.W - prior.RIGHT, prior.H - 122)
    for index, line in enumerate(["AI와 함께하는", "바이브 코딩"]):
        prior.draw_text(c, line, prior.LEFT, 185 + index * 83,
                        "WantedBold", 42, prior.INK)
    for index, line in enumerate([
        "개념을 익히고 실습으로 배우는",
        "Python · GUI · 앱 제작 · 데이터 · 프로젝트",
    ]):
        prior.draw_text(c, line, prior.LEFT, 472 + index * 38,
                        "WantedMedium", 20)
    prior.draw_text(c, "2026 · 32차시 실습 교재", prior.LEFT, 755,
                    "WantedMedium", 11, prior.GRAY)


def draw_contents(c, production, part):
    prior.draw_text(c, "학습 차례", prior.LEFT, 67,
                    "WantedBold", 25, prior.INDIGO)
    y = 136
    for label, chapters in CONTENTS_GROUPS[part]:
        prior.draw_text(c, label, prior.LEFT, y, "WantedBold", 15, prior.INDIGO)
        y += 46
        for chapter in chapters:
            title = prior.SHORT_TITLES[chapter - 1]
            if prior.text_width(title, "WantedMedium", 15) > prior.WIDTH - 104:
                raise ValueError(f"Contents title is too wide: {title}")
            prior.draw_text(c, f"{chapter:02d}", prior.LEFT, y,
                            "WantedBold", 17, prior.INDIGO)
            prior.draw_text(c, title, prior.LEFT + 53, y, "WantedMedium", 15)
            c.setFont("WantedMedium", 14)
            c.setFillColor(HexColor(prior.GRAY))
            c.drawRightString(prior.W - prior.RIGHT, prior.H - y - 12,
                              str(production.chapter_pages[chapter]))
            c.linkRect("", f"ch{chapter:02d}",
                       (prior.LEFT, prior.H - y - 32,
                        prior.W - prior.RIGHT, prior.H - y + 12),
                       relative=0, thickness=0)
            c.setStrokeColor(HexColor("#DDE3EC"))
            c.setLineWidth(.65)
            c.line(prior.LEFT, prior.H - y - 32,
                   prior.W - prior.RIGHT, prior.H - y - 32)
            y += 55
        y += 15
    if y > 740:
        raise ValueError(f"Contents page {part + 1} exceeds its text frame")
    prior.draw_text(c, "쪽수는 표지부터 계산합니다.", prior.LEFT, 760,
                    "WantedMedium", 10, prior.GRAY)


def configure(split):
    sessions = split["sessions"]
    if [session["number"] for session in sessions] != list(range(1, 33)):
        raise ValueError("The split map must list sessions 1 through 32 in order")
    base.BOOK = BOOK
    prior.BOOK = BOOK
    prior.SHORT_TITLES = [session["shortTitle"] for session in sessions]
    prior.draw_cover = draw_cover
    prior.draw_contents = draw_contents


def render(production, output):
    prior.render_final(production, output)
    # The shared renderer's drawing rules remain unchanged. Update its fixed
    # 16-session PDF subject after it has embedded the original vector artwork.
    reader = PdfReader(output)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    metadata = dict(reader.metadata or {})
    metadata["/Subject"] = "32차시 바이브 코딩 실습 교재"
    writer.add_metadata(metadata)
    staged = output.with_name(output.stem + "-metadata.pdf")
    writer.write(staged)
    staged.replace(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path,
                        default=ROOT / "tmp/pdfs/book-spec-32.json")
    parser.add_argument("--output", type=Path,
                        default=ROOT / "output/pdf/vibe-coding-32-coala-access-reviewed.pdf")
    parser.add_argument("--review-date", default="2026-11-03")
    args = parser.parse_args()
    output = args.output.resolve()
    if output == (ROOT / "output/pdf/vibe-coding-16-coala-access.pdf").resolve():
        raise ValueError("Choose a new output filename for the 32-session edition")
    split = json.loads((BOOK / "session-split.json").read_text(encoding="utf-8"))
    configure(split)
    prior.fonts()
    for title in prior.SHORT_TITLES:
        if prior.text_width(title, "WantedBold", 25) > prior.WIDTH - 85:
            raise ValueError(f"Session opening title is too wide: {title}")
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    production = Production32(spec)
    production.plan()
    render(production, output)
    source_reference = json.loads((BOOK / "asset-manifest.json").read_text(encoding="utf-8"))
    report = {
        "mode": "standalone-32-session-print-edition",
        "date": args.review_date,
        "pages": len(production.pages),
        "manuscriptSha256": hashlib.sha256((BOOK / "book.md").read_bytes()).hexdigest(),
        "pdfSha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "specPath": str(args.spec.resolve()),
        "splitMap": str((BOOK / "session-split.json").resolve()),
        "sessions": split["sessions"],
        "pageTypes": dict(Counter(page["type"] for page in production.pages)),
        "chapterPages": production.chapter_pages,
        "images": production.images,
        "merges": production.merges,
        "limitations": [
            "Canva 원본 틀과 정확히 일치하지 않는 독립 PDF 배치",
            "순서도는 제공 교재에서 추출한 PDF 벡터 도형·글꼴을 그대로 사용",
            "원본 캡처의 해상도는 보존하며 화질 복원 또는 재촬영을 주장하지 않음",
        ],
        "sourcePdf": source_reference["source_pdf"],
        "sourcePdfSha256": source_reference["source_sha256"],
        "layout": production.pages,
    }
    output.with_suffix(".json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output), "pages": report["pages"],
                      "pageTypes": report["pageTypes"],
                      "chapterPages": report["chapterPages"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
