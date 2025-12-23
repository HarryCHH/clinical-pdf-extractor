import pytest

from clinical_pdf_extractor.cleaning import (
    clean_extracted_text,
    collapse_blank_lines,
    fix_hyphenation_linebreaks,
    normalize_unicode_whitespace,
)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("A\u00a0B", "A B"),  # non-breaking space NBSP
        ("A\u200bB", "AB"),  # zero-width space
        ("A\u00adB", "AB"),  # soft hyphen
    ],
)
def test_normalize_unicode_whitespace(raw: str, expected: str) -> None:
    assert normalize_unicode_whitespace(raw) == expected


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("exac-\n erbation", "exacerbation"),
        ("non-\nsmoker", "nonsmoker"),
        ("well-\nknown", "wellknown"),
    ],
)
def test_fix_hyphenation_linebreaks(raw: str, expected: str) -> None:
    assert fix_hyphenation_linebreaks(raw) == expected


def test_collapse_blank_lines() -> None:
    assert collapse_blank_lines("a\n\n\n\nb") == "a\n\nb"


def test_clean_extracted_text_pipeline() -> None:
    raw = "exac-\n erbation\u00a0rate\n\n\n\nEnd"
    out = clean_extracted_text(raw)
    assert "exacerbation rate" in out
    assert "\n\n\n" not in out
