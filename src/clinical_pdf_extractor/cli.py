import argparse
from pathlib import Path

from clinical_pdf_extractor.cleaning import clean_extracted_text

from .chunking import chunk_text, write_chunks_jsonl
from .extract.tables_pdfplumber import extract_tables_pdfplumber
from .extract.text import extract_text
from .provenance import build_manifest, write_manifest


def main() -> int:
    p = argparse.ArgumentParser(prog="cpe", description="Clinical PDF extractor (mini project).")
    p.add_argument("pdf", type=Path, help="Path to a PDF")
    p.add_argument("--out", type=Path, default=Path("out"), help="Output folder")
    p.add_argument("--tables", action="store_true", help="Also extract tables via pdfplumber")
    p.add_argument(
        "--chunks",
        action="store_true",
        help="Write RAG-ready chunks.jsonl from cleaned text",
    )
    p.add_argument("--chunk-size", type=int, default=1500, help="Chunk size in characters")
    p.add_argument("--chunk-overlap", type=int, default=200, help="Chunk overlap in characters")
    args = p.parse_args()

    if not args.pdf.exists():
        p.error(f"PDF file not found: {args.pdf}")
    if args.pdf.is_dir():
        p.error(f"PDF path is a directory, not a file: {args.pdf}")
    if args.pdf.suffix.lower() != ".pdf":
        p.error(f"Expected a .pdf file, got: {args.pdf}")

    args.out.mkdir(parents=True, exist_ok=True)

    res = extract_text(args.pdf)

    text_raw = res.text
    text_clean = clean_extracted_text(text_raw)
    if args.chunks:
        doc_id = args.pdf.name
        chunks = chunk_text(
            text_clean,
            doc_id=doc_id,
            chunk_size=args.chunk_size,
            chunk_overlap=args.chunk_overlap,
        )
    write_chunks_jsonl(args.out / "chunks.jsonl", chunks, backend=res.backend)

    (args.out / "text_raw.txt").write_text(text_raw, encoding="utf-8")
    (args.out / "text.txt").write_text(text_clean, encoding="utf-8")
    (args.out / "backend.txt").write_text(res.backend, encoding="utf-8")

    if args.tables:
        tables = extract_tables_pdfplumber(args.pdf)
        for i, df in enumerate(tables, start=1):
            df.to_csv(args.out / f"table_{i:03d}.csv", index=False)

    print(f"Wrote outputs to: {args.out.resolve()}")

    manifest = build_manifest(
        input_pdf=args.pdf,
        output_dir=args.out,
        backend=res.backend,
        args={
            "pdf": str(args.pdf),
            "out": str(args.out),
            "tables": bool(args.tables),
            "chunks": bool(args.chunks),
            "chunk_size": int(args.chunk_size),
            "chunk_overlap": int(args.chunk_overlap),
        },
    )
    write_manifest(args.out / "manifest.json", manifest)
    return 0
