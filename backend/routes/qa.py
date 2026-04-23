from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.models import QueryHistory
from backend.db.session import get_db
from backend.schemas.api import AskRequest, AskResponse
from backend.services.llm import llm_service
from backend.services.search import semantic_search

router = APIRouter(prefix="/api", tags=["qa"])


@router.post("/ask", response_model=AskResponse)
def ask_question(payload: AskRequest, db: Session = Depends(get_db)) -> AskResponse:
    references = semantic_search(db, payload.question, payload.top_k)
    context = "\n\n".join(item["chunk_text"] for item in references)
    answer = llm_service.answer(payload.question, context)

    db.add(
        QueryHistory(
            query_type="qa",
            query_text=payload.question,
            response_text=answer,
            top_k=payload.top_k,
        )
    )
    db.commit()

    return AskResponse(question=payload.question, answer=answer, references=references)
