from __future__ import annotations

import hashlib
from math import sqrt

from backend.core.config import settings

try:
    from sentence_transformers import SentenceTransformer
except Exception:
    SentenceTransformer = None


_model = None


def _hash_embedding(text: str, dimensions: int) -> list[float]:
    values = [0.0] * dimensions
    tokens = text.lower().split()
    if not tokens:
        return values

    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        for index in range(dimensions):
            values[index] += (digest[index % len(digest)] / 255.0) - 0.5

    norm = sqrt(sum(v * v for v in values)) or 1.0
    return [v / norm for v in values]


def _get_model():
    global _model
    if _model is not None:
        return _model
    if SentenceTransformer is None:
        return None
    try:
        _model = SentenceTransformer(settings.hf_embedding_model)
    except Exception:
        _model = None
    return _model


def embed(text: str) -> list[float]:
    model = _get_model()
    if model is None:
        return _hash_embedding(text, settings.embedding_dimensions)

    try:
        vector = model.encode(text)
        return vector.tolist() if hasattr(vector, "tolist") else list(vector)
    except Exception:
        return _hash_embedding(text, settings.embedding_dimensions)


def embedding_provider() -> str:
    return f"huggingface:{settings.hf_embedding_model}" if _get_model() else "hash-fallback"


def cosine_similarity(a: list[float], b: list[float]) -> float:
    length = min(len(a), len(b))
    if length == 0:
        return 0.0
    dot = sum(a[i] * b[i] for i in range(length))
    norm_a = sqrt(sum(a[i] * a[i] for i in range(length))) or 1.0
    norm_b = sqrt(sum(b[i] * b[i] for i in range(length))) or 1.0
    return dot / (norm_a * norm_b)
