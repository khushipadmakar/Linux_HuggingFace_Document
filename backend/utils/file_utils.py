from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def save_upload_file(upload_file: UploadFile, destination_dir: Path) -> tuple[str, Path, int]:
    suffix = Path(upload_file.filename or "").suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type. Allowed: PDF, DOCX, TXT")

    ensure_directory(destination_dir)
    safe_name = f"{uuid4().hex}_{Path(upload_file.filename).name}"
    destination = destination_dir / safe_name

    data = upload_file.file.read()
    destination.write_bytes(data)
    return safe_name, destination, len(data)
