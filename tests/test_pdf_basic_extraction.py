from __future__ import annotations

from pathlib import Path

import pytest

from clinical_pdf_extractor.extract.text import extract_text


def test_extract_text_basic(basic_pdf: Path):
    res = extract_text(basic_pdf)
    assert isinstance(res.text, str)
    assert len(res.text) > 0
    assert res.backend == "pypdf"


def test_extract_text_missing_file_raises() -> None:
    missing = Path("tests/fixtures/DOES_NOT_EXIST.pdf")
    with pytest.raises(FileNotFoundError):
        extract_text(missing)
