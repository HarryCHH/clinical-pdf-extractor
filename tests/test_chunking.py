from __future__ import annotations

import json
from pathlib import Path

import pytest

from clinical_pdf_extractor.chunking import chunk_text, write_chunks_jsonl


def test_chunk_text_basic() -> None:
    text = "A" * 1000 + "B" * 1000
    chunks = chunk_text(text, doc_id="doc.pdf", chunk_size=900, chunk_overlap=100)
    assert len(chunks) >= 2
    assert chunks[0].doc_id == "doc.pdf"
    assert chunks[0].chunk_id.startswith("doc.pdf::")


def test_chunk_text_validates_args() -> None:
    with pytest.raises(ValueError):
        chunk_text("hi", doc_id="x", chunk_size=100, chunk_overlap=100)


def test_write_chunks_jsonl(tmp_path: Path) -> None:
    chunks = chunk_text("hello world", doc_id="x", chunk_size=5, chunk_overlap=0)
    out = tmp_path / "chunks.jsonl"
    write_chunks_jsonl(out, chunks, backend="pypdf")

    lines = out.read_text(encoding="utf-8").splitlines()
    rec = json.loads(lines[0])
    assert "text" in rec and "source" in rec
