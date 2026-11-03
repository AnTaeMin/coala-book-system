"""Record the textbook's typesetter as editable PowerPoint drawing primitives."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from reportlab.pdfbase import pdfmetrics

import finalize_textbook_pdf as book
import build_textbook_pdf as base

ROOT = Path(__file__).resolve().parents[1]


def color(value):
    return "#" + "".join(f"{round(getattr(value, c) * 255):02X}" for c in ("red", "green", "blue"))


class RecordingCanvas:
    instance = None

    def __init__(self, *args, **kwargs):
        self.pages = []
        self.page = []
        self.fill = "#000000"
        self.stroke = "#000000"
        self.line_width = 1
        self.font = "WantedMedium"
        self.font_size = 14
        RecordingCanvas.instance = self

    def setFillColor(self, value): self.fill = color(value)
    def setStrokeColor(self, value): self.stroke = color(value)
    def setLineWidth(self, value): self.line_width = value
    def setFont(self, name, size): self.font, self.font_size = name, size
    def setTitle(self, *args): pass
    def setAuthor(self, *args): pass
    def setSubject(self, *args): pass
    def bookmarkPage(self, *args): pass
    def addOutlineEntry(self, *args, **kwargs): pass
    def linkRect(self, *args, **kwargs): pass
    def save(self): pass

    def drawString(self, x, y, value):
        width = pdfmetrics.stringWidth(value, self.font, self.font_size)
        self.page.append({"kind": "text", "text": value, "left": x,
                          "top": book.H-y-self.font_size*.84,
                          "width": width, "size": self.font_size,
                          "font": self.font, "color": self.fill})

    def drawRightString(self, x, y, value):
        self.drawString(x-pdfmetrics.stringWidth(value, self.font, self.font_size), y, value)

    def rect(self, x, y, width, height, stroke=1, fill=0):
        self.page.append({"kind": "rect", "left": x, "top": book.H-y-height,
                          "width": width, "height": height,
                          "fill": self.fill if fill else "none",
                          "stroke": self.stroke if stroke else "none", "lineWidth": self.line_width})

    def roundRect(self, x, y, width, height, radius, stroke=1, fill=0):
        self.rect(x,y,width,height,stroke,fill)
        self.page[-1].update(kind="roundRect", radius=radius)

    def circle(self, x,y,radius,stroke=1,fill=0):
        self.rect(x-radius,y-radius,2*radius,2*radius,stroke,fill)
        self.page[-1]["kind"]="ellipse"

    def line(self,x1,y1,x2,y2):
        self.page.append({"kind":"line", "x1":x1,"y1":book.H-y1,"x2":x2,"y2":book.H-y2,
                          "stroke":self.stroke,"lineWidth":self.line_width})

    def drawImage(self, path,x,y,width,height,**kwargs):
        self.page.append({"kind":"image","path":str(path),"left":x,"top":book.H-y-height,
                          "width":width,"height":height})

    def showPage(self):
        self.pages.append(self.page)
        self.page=[]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=Path, default=ROOT/"output/pdf/vibe-coding-16-upstream.pdf")
    parser.add_argument("--dest", type=Path, default=ROOT/"tmp/pptx/textbook")
    args = parser.parse_args()
    dest = args.dest.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    book.fonts()
    spec=json.loads((ROOT/"tmp/pdfs/book-spec.json").read_text(encoding="utf-8"))
    production=book.FinalProduction(spec)
    production.plan()
    original_draw=book.draw_block

    def record_block(c,b):
        if b["kind"] == "table":
            c.page.append({"kind":"table","block":b})
        else:
            original_draw(c,b)

    book.draw_block=record_block
    book.canvas.Canvas=RecordingCanvas
    book.embed_source_diagrams=lambda *args: None
    book.render_final(production,dest/"unused.pdf")
    records=RecordingCanvas.instance.pages
    for index,page in enumerate(production.pages):
        for block in page["blocks"]:
            if block["kind"] not in ("flowchart","vector-image"):
                continue
            if block["kind"] == "flowchart":
                asset=production.flow_sources[page["id"]]
                src=asset["src"]
            else:
                src=block["src"]
            records[index].append({"kind":"image","path":str(base.BOOK/src),
                                   "left":block["x"],"top":block["y"],
                                   "width":block["printWidthPt"],
                                   "height":block.get("imageHeight",block["height"])})
    scene={"width":book.W,"height":book.H,"pages":records,
           "titles":[page["title"] for page in production.pages],
           "source":str(args.pdf.resolve())}
    (dest/"scene.json").write_text(json.dumps(scene,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"pages":len(records),"primitives":sum(map(len,records))}))


if __name__ == "__main__":
    main()
