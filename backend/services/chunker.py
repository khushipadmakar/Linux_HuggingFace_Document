from backend.core.config import settings


def chunk_text(text: str, chunk_size: int | None = None, overlap: int | None = None) -> list[str]:
    if not text:
        return []

    target = chunk_size or settings.chunk_size
    overlap_size = overlap or settings.chunk_overlap
    step = max(1, target - overlap_size)

    chunks: list[str] = []
    cursor = 0
    text_len = len(text)

    while cursor < text_len:
        chunk = text[cursor : cursor + target].strip()
        if chunk:
            chunks.append(chunk)
        cursor += step

    return chunks
