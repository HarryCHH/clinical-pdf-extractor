from __future__ import annotations

import re

# --- Common PDF unicode/whitespace artifacts ---
NBSP = "\u00a0"  # non-breaking space
ZERO_WIDTH = "\u200b"  # zero-width space
SOFT_HYPHEN = "\u00ad"  # soft hyphen


def normalize_unicode_whitespace(text: str) -> str:
    """
    Normalize invisible/odd whitespace characters often found in PDF extraction.

    Replacements:
      - NBSP (\\u00a0) -> normal space
      - ZERO_WIDTH (\\u200b) removed
      - SOFT_HYPHEN (\\u00ad) removed

    Parameters
    ----------
    text:
        Raw extracted text.

    Returns
    -------
    str
        Text with normalized unicode whitespace.
    """
    return text.replace(NBSP, " ").replace(ZERO_WIDTH, "").replace(SOFT_HYPHEN, "")


def fix_hyphenation_linebreaks(text: str) -> str:
    """
    Join words split across line breaks with hyphenation.

    Example
    -------
    'exac-\\n erbation' -> 'exacerbation'

    Notes
    -----
    This only joins letter-hyphen-newline-letter patterns. It avoids joining
    numeric ranges like '1-\\n2' or bullet separators.

    Parameters
    ----------
    text:
        Text possibly containing hyphenation line breaks.

    Returns
    -------
    str
        Text with hyphenation splits repaired.
    """
    return re.sub(r"([A-Za-z])-\n\s*([A-Za-z])", r"\1\2", text)


def normalize_newlines(text: str) -> str:
    """
    Normalize Windows/Mac newlines to '\\n'.

    Parameters
    ----------
    text:
        Input text.

    Returns
    -------
    str
        Text using only '\\n' for line breaks.
    """
    return text.replace("\r\n", "\n").replace("\r", "\n")


def collapse_inline_whitespace(text: str) -> str:
    """
    Collapse runs of spaces and tabs within lines (but keep newlines).

    Example
    -------
    'A   B\\t\\tC' -> 'A B C'

    Parameters
    ----------
    text:
        Input text.

    Returns
    -------
    str
        Text with consecutive spaces/tabs collapsed.
    """
    return re.sub(r"[ \t]+", " ", text)


def collapse_blank_lines(text: str, max_consecutive: int = 2) -> str:
    """
    Collapse excessive blank lines.

    Parameters
    ----------
    text:
        Input text.
    max_consecutive:
        Max number of consecutive '\\n' allowed.

    Returns
    -------
    str
        Text with large blank-line gaps reduced.

    Raises
    ------
    ValueError
        If max_consecutive < 1.
    """
    if max_consecutive < 1:
        raise ValueError("max_consecutive must be >= 1")

    pattern = r"\n{" + str(max_consecutive + 1) + r",}"
    return re.sub(pattern, "\n" * max_consecutive, text).strip()


def clean_extracted_text(text: str) -> str:
    """
    Apply a conservative cleaning pipeline for PDF extracted text.

    Pipeline
    --------
    1) normalize unicode whitespace
    2) normalize newlines
    3) fix hyphenation line breaks
    4) collapse inline whitespace
    5) collapse excessive blank lines

    Parameters
    ----------
    text:
        Raw extracted text.

    Returns
    -------
    str
        Cleaned text ready for downstream chunking/search.
    """
    text = normalize_unicode_whitespace(text)
    text = normalize_newlines(text)
    text = fix_hyphenation_linebreaks(text)
    text = collapse_inline_whitespace(text)
    text = collapse_blank_lines(text, max_consecutive=2)
    return text
