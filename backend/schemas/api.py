from datetime import datetime

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    document_id: int
    filename: str
    status: str


class DocumentItem(BaseModel):
    id: int
    filename: str
    file_type: str
    status: str
    uploaded_at: datetime
    processed_at: datetime | None


class DocumentDetail(DocumentItem):
    summary: str | None
    metadata: dict | None
    chunk_count: int = 0


class ProcessResponse(BaseModel):
    document_id: int
    status: str
    chunks: int
    message: str


class SearchRequest(BaseModel):
    query: str = Field(min_length=2)
    top_k: int = Field(default=5, ge=1, le=20)
    document_id: int | None = None


class SearchMatch(BaseModel):
    document_id: int
    chunk_id: int
    score: float
    chunk_text: str


class SearchResponse(BaseModel):
    query: str
    matches: list[SearchMatch]


class AskRequest(BaseModel):
    question: str = Field(min_length=4)
    top_k: int = Field(default=4, ge=1, le=10)


class AskResponse(BaseModel):
    question: str
    answer: str
    references: list[SearchMatch]


class DashboardMetrics(BaseModel):
    total_documents: int
    processed_documents: int
    failed_documents: int
    total_chunks: int
    total_queries: int
    recent_activity: list[dict]
