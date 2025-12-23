from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def basic_pdf(fixtures_dir: Path) -> Path:
    pdf = fixtures_dir / "basic.pdf"
    if not pdf.exists():
        raise FileNotFoundError(f"Fixture not found: {pdf}")
    return pdf
