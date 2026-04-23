from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.schemas.api import ProcessResponse
from backend.services.pipeline import DocumentPipeline

router = APIRouter(prefix="/api/process", tags=["process"])


@router.post("/{document_id}", response_model=ProcessResponse)
def process_document(document_id: int, db: Session = Depends(get_db)) -> ProcessResponse:
    pipeline = DocumentPipeline(db)
    try:
        result = pipeline.process_document(document_id)
    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Processing failed: {exc}") from exc

    return ProcessResponse(**result)


@router.post("/retry-failed")
def retry_failed_documents(db: Session = Depends(get_db)) -> dict:
    return DocumentPipeline(db).retry_failed()
