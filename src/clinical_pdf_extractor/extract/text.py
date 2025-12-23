from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .text_pypdf import extract_text_pypdf


@dataclass(frozen=True)
class TextExtractionResult:
    """Result of text extraction for traceability"""

    text: str
    backend: str


def extract_text(pdf_path: Path) -> TextExtractionResult:
    """Extract text from a PDF.

    For now:
    - uses pypdf only
    - returns both the extracted text and which backend was used
    """
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if pdf_path.is_dir():
        raise IsADirectoryError(f"Expected a file but found a directory: {pdf_path}")

    text = extract_text_pypdf(pdf_path)
    return TextExtractionResult(text=text, backend="pypdf")
