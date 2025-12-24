from __future__ import annotations

import json
from pathlib import Path

from clinical_pdf_extractor.provenance import build_manifest, write_manifest


def test_manifest_written(tmp_path: Path, basic_pdf: Path) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    # create a fake output file
    (out_dir / "text.txt").write_text("hello", encoding="utf-8")

    manifest = build_manifest(
        input_pdf=basic_pdf,
        output_dir=out_dir,
        backend="pypdf",
        args={"tables": False},
    )
    write_manifest(out_dir / "manifest.json", manifest)

    loaded = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    assert "input" in loaded and loaded["input"]["sha256"]
    assert any(o["path"].endswith("text.txt") for o in loaded["outputs"])
