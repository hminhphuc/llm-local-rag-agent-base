"""
Customize reference.docx để pandoc dùng style chuyên nghiệp:
- Heading 1: 18pt, bold, màu xanh navy
- Heading 2: 15pt, bold, màu xanh navy nhạt hơn
- Heading 3: 13pt, bold, màu navy
- Body: Calibri 11pt
- Code: Consolas 9.5pt, background xám
- Table: viền nhẹ, header xám nhạt
"""
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor

REPO_ROOT = Path(__file__).resolve().parent.parent
REF_DOCX = REPO_ROOT / "docs" / "reference.docx"


def style_heading(style, size_pt: float, color: tuple[int, int, int], bold: bool = True):
    style.font.size = Pt(size_pt)
    style.font.bold = bold
    style.font.color.rgb = RGBColor(*color)
    style.font.name = "Calibri"


def main():
    doc = Document(REF_DOCX)

    # Body text
    if "Normal" in doc.styles:
        normal = doc.styles["Normal"]
        normal.font.name = "Calibri"
        normal.font.size = Pt(11)
        normal.font.color.rgb = RGBColor(0x21, 0x25, 0x29)

    # Heading 1
    if "Heading 1" in doc.styles:
        style_heading(doc.styles["Heading 1"], 18, (0x1E, 0x40, 0xAF))

    # Heading 2
    if "Heading 2" in doc.styles:
        style_heading(doc.styles["Heading 2"], 15, (0x1E, 0x40, 0xAF))

    # Heading 3
    if "Heading 3" in doc.styles:
        style_heading(doc.styles["Heading 3"], 13, (0x37, 0x37, 0x37))

    # Heading 4
    if "Heading 4" in doc.styles:
        style_heading(doc.styles["Heading 4"], 12, (0x4B, 0x55, 0x63))

    # Code (inline + block)
    if "Source Code" in doc.styles:
        sc = doc.styles["Source Code"]
        sc.font.name = "Consolas"
        sc.font.size = Pt(9.5)
        sc.font.color.rgb = RGBColor(0x21, 0x25, 0x29)

    # Verbatim Char
    for style_name in ["Verbatim Char", "Source Code"]:
        if style_name in doc.styles:
            s = doc.styles[style_name]
            s.font.name = "Consolas"
            s.font.size = Pt(9.5)

    # Title (cover)
    if "Title" in doc.styles:
        style_heading(doc.styles["Title"], 28, (0x1E, 0x40, 0xAF))

    # Subtitle
    if "Subtitle" in doc.styles:
        style_heading(doc.styles["Subtitle"], 16, (0x4B, 0x55, 0x63), bold=False)

    doc.save(REF_DOCX)
    print(f"Customized {REF_DOCX}")


if __name__ == "__main__":
    main()
