from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    chunk_id: str
    chunk_index: int
    char_start: int
    char_end: int
    text: str


def chunk_text(
    text: str,
    *,
    doc_id: str,
    chunk_size: int = 1500,
    chunk_overlap: int = 200,
) -> list[Chunk]:
    """
    Chunk text by character length with overlap.

    This is simple and robust for PDF-extracted text.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be >= 0")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be < chunk_size")

    chunks: list[Chunk] = []
    i = 0
    start = 0
    n = len(text)

    while start < n:
        end = min(start + chunk_size, n)
        chunk_str = text[start:end].strip()
        if chunk_str:
            chunk_id = f"{doc_id}::{i:04d}"
            chunks.append(
                Chunk(
                    doc_id=doc_id,
                    chunk_id=chunk_id,
                    chunk_index=i,
                    char_start=start,
                    char_end=end,
                    text=chunk_str,
                )
            )
            i += 1
        if end == n:
            break
        start = end - chunk_overlap

    return chunks


def write_chunks_jsonl(path: Path, chunks: list[Chunk], *, backend: str) -> None:
    """
    Write chunks as JSONL for embedding/RAG pipelines.
    """
    with path.open("w", encoding="utf-8") as f:
        for c in chunks:
            rec = asdict(c)
            rec["source"] = {"backend": backend}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
