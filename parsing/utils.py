import re
from io import StringIO
from typing import Iterator
from docx import Document

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTPage, LAParams

__all__ = "parse_pdf", "parse_pdf_to_file"

def parse_pdf(path: str) -> str:

    pages: Iterator[LTPage] = extract_pages(
        pdf_file = path,
        laparams = LAParams(
            char_margin = 10.0,
            boxes_flow = None
        )
    )

    output = StringIO()

    for page in pages:
        for element in page:
            if isinstance(element, LTTextContainer):
                output.write(re.sub(r"  +", " ", f"{element.get_text().strip()}\n"))

    return re.sub(r"\n\s+", "\n\n", output.getvalue())

def parse_docx(path: str) -> str:
    document = Document(path)

    output = StringIO()

    for paragraph in document.paragraphs:
        output.write(paragraph.text)

    return output.getvalue()

def parse_pdf_to_file(pdf_path: str, output_path: str, encoding: str = "utf-8") -> None:
    with open(output_path, "w+", encoding = encoding) as file:
        file.write(parse_pdf(pdf_path))

def parse_docx_to_file(docx_path: str, output_path: str, encoding: str = "utf-8") -> None:
    with open(output_path, "w+", encoding = encoding) as file:
        file.write(parse_docx(docx_path))

