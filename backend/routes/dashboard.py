from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.models import DocumentChunk, PipelineLog, QueryHistory, UploadedDocument
from backend.db.session import get_db
from backend.schemas.api import DashboardMetrics

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/metrics", response_model=DashboardMetrics)
def dashboard_metrics(db: Session = Depends(get_db)) -> DashboardMetrics:
    total_documents = db.query(func.count(UploadedDocument.id)).scalar() or 0
    processed_documents = (
        db.query(func.count(UploadedDocument.id)).filter(UploadedDocument.status == "processed").scalar() or 0
    )
    failed_documents = (
        db.query(func.count(UploadedDocument.id)).filter(UploadedDocument.status == "failed").scalar() or 0
    )
    total_chunks = db.query(func.count(DocumentChunk.id)).scalar() or 0
    total_queries = db.query(func.count(QueryHistory.id)).scalar() or 0

    recent_logs = (
        db.query(PipelineLog)
        .order_by(PipelineLog.created_at.desc())
        .limit(10)
        .all()
    )

    recent_activity = [
        {
            "stage": log.stage,
            "status": log.status,
            "message": log.message,
            "document_id": log.document_id,
            "created_at": log.created_at.isoformat(),
        }
        for log in recent_logs
    ]

    return DashboardMetrics(
        total_documents=total_documents,
        processed_documents=processed_documents,
        failed_documents=failed_documents,
        total_chunks=total_chunks,
        total_queries=total_queries,
        recent_activity=recent_activity,
    )
