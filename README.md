# clinical-pdf-extractor

A small, practical mini-project to extract **text** and **tables** from PDFs (e.g. clinical documents) with traceable outputs.

- Text extraction: 'pypdf' (and optionally other backends later)
- Table extraction: 'pdfplumber'
- Cleaning pipeline: unicode/whitespace normalization + hyphenation fixes
- Tests: pytest + fixtures
- Quality gates: black, ruff, mypy, CI (GitHub Actions)


## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e ".[dev]"
pytest
cpe path/to/file.pdf --out out --tables
```
