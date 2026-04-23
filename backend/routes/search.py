from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.models import QueryHistory
from backend.db.session import get_db
from backend.schemas.api import SearchRequest, SearchResponse
from backend.services.search import semantic_search

router = APIRouter(prefix="/api", tags=["search"])


@router.post("/search", response_model=SearchResponse)
def search_documents(payload: SearchRequest, db: Session = Depends(get_db)) -> SearchResponse:
    matches = semantic_search(db, payload.query, payload.top_k, payload.document_id)

    db.add(
        QueryHistory(
            query_type="semantic_search",
            query_text=payload.query,
            response_text=f"Returned {len(matches)} matches",
            top_k=payload.top_k,
        )
    )
    db.commit()

    return SearchResponse(query=payload.query, matches=matches)
