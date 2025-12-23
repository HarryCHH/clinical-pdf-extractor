import argparse
from pathlib import Path

from clinical_pdf_extractor.cleaning import clean_extracted_text

from .extract.tables_pdfplumber import extract_tables_pdfplumber
from .extract.text import extract_text


def main() -> int:
    p = argparse.ArgumentParser(prog="cpe", description="Clinical PDF extractor (mini project).")
    p.add_argument("pdf", type=Path, help="Path to a PDF")
    p.add_argument("--out", type=Path, default=Path("out"), help="Output folder")
    p.add_argument("--tables", action="store_true", help="Also extract tables via pdfplumber")
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
    (args.out / "text_raw.txt").write_text(text_raw, encoding="utf-8")
    (args.out / "text.txt").write_text(text_clean, encoding="utf-8")
    (args.out / "backend.txt").write_text(res.backend, encoding="utf-8")

    if args.tables:
        tables = extract_tables_pdfplumber(args.pdf)
        for i, df in enumerate(tables, start=1):
            df.to_csv(args.out / f"table_{i:03d}.csv", index=False)

    print(f"Wrote outputs to: {args.out.resolve()}")
    return 0
