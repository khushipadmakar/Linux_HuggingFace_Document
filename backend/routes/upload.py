from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.db.models import AISummary, DocumentChunk, DocumentMetadata, UploadedDocument
from backend.db.session import get_db
from backend.schemas.api import DocumentDetail, DocumentItem, UploadResponse
from backend.utils.file_utils import save_upload_file
from backend.utils.logger import log_info

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)) -> UploadResponse:
    try:
        filename, filepath, size_bytes = save_upload_file(file, Path(settings.upload_root))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    row = UploadedDocument(
        filename=filename,
        filepath=str(filepath),
        file_type=Path(filename).suffix.lower().lstrip("."),
        size_bytes=size_bytes,
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    log_info(f"Uploaded document id={row.id} name={filename}")
    return UploadResponse(document_id=row.id, filename=row.filename, status=row.status)


@router.get("", response_model=list[DocumentItem])
def list_documents(db: Session = Depends(get_db)) -> list[DocumentItem]:
    rows = db.query(UploadedDocument).order_by(UploadedDocument.uploaded_at.desc()).all()
    return [
        DocumentItem(
            id=row.id,
            filename=row.filename,
            file_type=row.file_type,
            status=row.status,
            uploaded_at=row.uploaded_at,
            processed_at=row.processed_at,
        )
        for row in rows
    ]


@router.get("/{document_id}", response_model=DocumentDetail)
def get_document(document_id: int, db: Session = Depends(get_db)) -> DocumentDetail:
    row = db.get(UploadedDocument, document_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Document not found")

    summary = db.query(AISummary).filter(AISummary.document_id == document_id).first()
    metadata = db.query(DocumentMetadata).filter(DocumentMetadata.document_id == document_id).first()
    chunk_count = db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).count()

    return DocumentDetail(
        id=row.id,
        filename=row.filename,
        file_type=row.file_type,
        status=row.status,
        uploaded_at=row.uploaded_at,
        processed_at=row.processed_at,
        summary=summary.summary_text if summary else None,
        metadata={
            "document_type": metadata.document_type,
            "language": metadata.language,
            "word_count": metadata.word_count,
            "key_entities": metadata.key_entities,
        }
        if metadata
        else None,
        chunk_count=chunk_count,
    )


@router.get("/{document_id}/insights")
def get_summary_and_metadata(document_id: int, db: Session = Depends(get_db)) -> dict:
    summary = db.query(AISummary).filter(AISummary.document_id == document_id).first()
    metadata = db.query(DocumentMetadata).filter(DocumentMetadata.document_id == document_id).first()

    if summary is None and metadata is None:
        raise HTTPException(status_code=404, detail="No insights found for this document")

    return {
        "document_id": document_id,
        "summary": summary.summary_text if summary else None,
        "metadata": {
            "document_type": metadata.document_type,
            "language": metadata.language,
            "word_count": metadata.word_count,
            "key_entities": metadata.key_entities,
        }
        if metadata
        else None,
    }
