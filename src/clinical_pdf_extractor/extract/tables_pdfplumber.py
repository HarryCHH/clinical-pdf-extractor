from __future__ import annotations

from pathlib import Path

import pandas as pd  # type: ignore[import-untyped]
import pdfplumber


def extract_tables_pdfplumber(pdf_path: Path) -> list[pd.DataFrame]:
    """
    Extract tables page-by-page. Works best for machine-generated PDFs.
    Returns list of DataFrames in reading order.
    """
    out: list[pd.DataFrame] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for page in pdf.pages:
            for table in page.extract_tables() or []:
                if not table or len(table) < 2:
                    continue
                header = [h or "" for h in table[0]]
                rows = [[c or "" for c in r] for r in table[1:]]
                out.append(pd.DataFrame(rows, columns=header))
    return out
