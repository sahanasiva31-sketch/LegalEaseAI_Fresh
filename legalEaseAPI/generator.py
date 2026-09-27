import html
import re
from io import BytesIO
from pathlib import Path
from typing import List

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt
from fpdf import FPDF

BASE_DIR = Path(__file__).resolve().parent.parent
LOGO_PATH = BASE_DIR / "image" / "logo.png"


def sanitize_text(text: str) -> str:
    """Normalize text so it is safe for the document exporters."""
    if not text:
        return ""

    replacements = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def _split_sections(text: str):
    lines = [line.strip() for line in sanitize_text(text).split("\n")]
    return [line for line in lines if line]


def _is_heading(line: str) -> bool:
    if len(line) > 100:
        return False
    if re.match(r"^\d+[\.\)]\s+", line):
        return True
    if line.upper() == line and any(c.isalpha() for c in line):
        return True
    return line.startswith("#")


def _clean_heading(line: str) -> str:
    return re.sub(r"^#+\s*", "", line).strip()


def terms_to_list(terms: str) -> List[str]:
    return [item.strip() for item in terms.split(";") if item.strip()]


def format_html_preview(text: str) -> str:
    """Create a safe HTML preview from generated plain text."""
    lines = _split_sections(text)
    output = []

    for line in lines:
        escaped = html.escape(line)
        if _is_heading(line):
            output.append(f"<h3>{html.escape(_clean_heading(line))}</h3>")
        elif line.startswith(("-", "*", "•")):
            output.append(f"<li>{html.escape(line[1:].strip())}</li>")
        else:
            output.append(f"<p>{escaped}</p>")

    # Wrap consecutive list items into one list.
    html_text = "\n".join(output)
    html_text = re.sub(r"((?:<li>.*?</li>\n?)+)", r"<ul>\1</ul>", html_text)
    return html_text


def format_docx(text: str, doc_type: str) -> bytes:
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Inches(0.7)
    section.bottom_margin = Inches(0.7)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

    # Header logo.
    header = section.header.paragraphs[0]
    header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if LOGO_PATH.exists():
        run = header.add_run()
        run.add_picture(str(LOGO_PATH), width=Inches(1.6))

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(doc_type.strip() or "Legal Document")
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    for line in _split_sections(text):
        if _is_heading(line):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(3)
            r = p.add_run(_clean_heading(line))
            r.bold = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(5)
            r = p.add_run(line.lstrip("-*• ").strip())
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)

    # Footer.
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = footer.add_run("LegalEase - AI-generated draft. Review with a qualified legal professional.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(8)

    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


class LegalEasePDF(FPDF):
    def __init__(self, doc_type: str):
        super().__init__()
        self.doc_type = doc_type

    def header(self):
        if LOGO_PATH.exists():
            try:
                self.image(str(LOGO_PATH), x=85, y=8, w=40)
                self.set_y(25)
            except Exception:
                self.set_y(12)
        else:
            self.set_y(12)

        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, self.doc_type[:90], align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=7)
        self.cell(
            0,
            8,
            "LegalEase - AI-generated draft. Review with a qualified legal professional.",
            align="C",
        )


def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = LegalEasePDF(doc_type or "Legal Document")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 35, 18)
    pdf.add_page()

    for line in _split_sections(text):
        if _is_heading(line):
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, _clean_heading(line))
            pdf.ln(2)
        else:
            pdf.set_font("Helvetica", size=10)
            content = line.lstrip("-*• ").strip()
            pdf.multi_cell(0, 5, content)
            pdf.ln(1)

    return bytes(pdf.output())


def format_txt(text: str) -> bytes:
    return sanitize_text(text).encode("utf-8")
