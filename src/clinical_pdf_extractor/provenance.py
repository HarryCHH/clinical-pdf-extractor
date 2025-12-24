from __future__ import annotations

import hashlib
import json
import platform
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass(frozen=True)
class FileRecord:
    path: str
    sha256: str
    bytes: int


def file_record(path: Path) -> FileRecord:
    return FileRecord(
        path=str(path),
        sha256=sha256_file(path),
        bytes=path.stat().st_size,
    )


def build_manifest(
    *,
    input_pdf: Path,
    output_dir: Path,
    backend: str,
    args: dict[str, Any],
    extra_outputs: list[Path] | None = None,
) -> dict[str, Any]:
    """Build a provenance manifest with hashes and environment info."""
    extra_outputs = extra_outputs or []
    outputs: list[Path] = sorted([p for p in output_dir.rglob("*") if p.is_file()] + extra_outputs)

    # Try to read package versions without hard dependencies
    versions: dict[str, str] = {}
    try:
        from importlib.metadata import version  # py3.11

        for pkg in ["clinical-pdf-extractor", "pypdf", "pdfplumber", "pandas"]:
            try:
                versions[pkg] = version(pkg)
            except Exception:
                pass
    except Exception:
        pass

    manifest: dict[str, Any] = {
        "created_utc": datetime.now(UTC).isoformat(),
        "input": asdict(file_record(input_pdf)),
        "output_dir": str(output_dir),
        "backend": backend,
        "args": args,
        "outputs": [asdict(file_record(p)) for p in outputs if p.exists()],
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "packages": versions,
        },
    }
    return manifest


def write_manifest(path: Path, manifest: dict[str, Any]) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
