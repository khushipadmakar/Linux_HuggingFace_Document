from __future__ import annotations

from pathlib import Path

try:
    import docx
except Exception:
    docx = None

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def extract_text(path: str | Path) -> str:
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")

    if suffix == ".txt":
        return file_path.read_text(encoding="utf-8", errors="ignore")

    if suffix == ".docx":
        if docx is None:
            raise RuntimeError("python-docx is required for DOCX extraction")
        document = docx.Document(str(file_path))
        return "\n".join(p.text for p in document.paragraphs)

    if PdfReader is None:
        raise RuntimeError("pypdf is required for PDF extraction")
    reader = PdfReader(str(file_path))
    return "\n".join((page.extract_text() or "") for page in reader.pages)
