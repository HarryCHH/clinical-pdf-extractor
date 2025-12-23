from pathlib import Path

from clinical_pdf_extractor.extract.text_pypdf import extract_text_pypdf


def test_extract_text_shape(tmp_path: Path):
    # Placeholder “shape” test. Replace with a small real PDF fixture later.
    assert callable(extract_text_pypdf)
