from __future__ import annotations

from sqlalchemy.orm import Session

from backend.db.models import DocumentChunk, EmbeddingStore
from backend.services.embeddings import cosine_similarity, embed


def semantic_search(db: Session, query: str, top_k: int = 5, document_id: int | None = None) -> list[dict]:
    query_embedding = embed(query)

    query_builder = db.query(EmbeddingStore, DocumentChunk).join(
        DocumentChunk, EmbeddingStore.chunk_id == DocumentChunk.id
    )

    if document_id is not None:
        query_builder = query_builder.filter(EmbeddingStore.document_id == document_id)

    scored_results: list[dict] = []
    for embedding_row, chunk in query_builder.all():
        candidate = embedding_row.embedding or []
        score = cosine_similarity(query_embedding, list(candidate))
        scored_results.append(
            {
                "document_id": embedding_row.document_id,
                "chunk_id": chunk.id,
                "score": round(float(score), 6),
                "chunk_text": chunk.chunk_text,
            }
        )

    scored_results.sort(key=lambda item: item["score"], reverse=True)
    return scored_results[:top_k]
