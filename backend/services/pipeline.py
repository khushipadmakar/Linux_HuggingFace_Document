from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from backend.db.models import AISummary, DocumentChunk, DocumentMetadata, EmbeddingStore, PipelineLog, UploadedDocument
from backend.services.chunker import chunk_text
from backend.services.cleaner import clean_text
from backend.services.embeddings import embed, embedding_provider
from backend.services.extractor import extract_text
from backend.services.llm import llm_service
from backend.services.metadata import extract_metadata


class DocumentPipeline:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _log(self, stage: str, status: str, message: str, document_id: int | None = None) -> None:
        self.db.add(
            PipelineLog(document_id=document_id, stage=stage, status=status, message=message)
        )
        self.db.commit()

    def process_document(self, document_id: int) -> dict:
        document = self.db.get(UploadedDocument, document_id)
        if document is None:
            raise ValueError(f"Document {document_id} was not found.")

        self._log("ingestion", "running", f"Started processing {document.filename}", document_id)

        try:
            raw_text = extract_text(document.filepath)
            cleaned_text = clean_text(raw_text)
            chunks = chunk_text(cleaned_text)
            metadata = extract_metadata(cleaned_text)
            summary = llm_service.summarize(cleaned_text)
            provider = embedding_provider()

            self.db.query(DocumentChunk).filter(DocumentChunk.document_id == document_id).delete()
            self.db.query(EmbeddingStore).filter(EmbeddingStore.document_id == document_id).delete()
            self.db.query(DocumentMetadata).filter(DocumentMetadata.document_id == document_id).delete()
            self.db.query(AISummary).filter(AISummary.document_id == document_id).delete()
            self.db.commit()

            created_chunks = 0
            for idx, chunk in enumerate(chunks):
                chunk_row = DocumentChunk(
                    document_id=document_id,
                    chunk_index=idx,
                    chunk_text=chunk,
                    token_count=max(1, len(chunk.split())),
                )
                self.db.add(chunk_row)
                self.db.flush()

                self.db.add(
                    EmbeddingStore(
                        document_id=document_id,
                        chunk_id=chunk_row.id,
                        embedding=embed(chunk),
                        vector_provider=provider,
                    )
                )
                created_chunks += 1

            self.db.add(
                DocumentMetadata(
                    document_id=document_id,
                    document_type=metadata["document_type"],
                    language=metadata["language"],
                    word_count=metadata["word_count"],
                    key_entities=metadata["key_entities"],
                )
            )

            self.db.add(
                AISummary(
                    document_id=document_id,
                    summary_text=summary,
                    model_name=f"huggingface:{llm_service.summary_model}",
                )
            )

            document.status = "processed"
            document.processed_at = datetime.utcnow()
            self.db.commit()

            self._log("serving", "success", "Processing completed", document_id)
            return {
                "document_id": document_id,
                "status": "processed",
                "chunks": created_chunks,
                "message": "Document processed successfully.",
            }

        except Exception as exc:
            self.db.rollback()
            document.status = "failed"
            self.db.commit()
            self._log("processing", "failed", str(exc), document_id)
            raise

    def retry_failed(self) -> dict:
        failed_docs = self.db.query(UploadedDocument).filter(UploadedDocument.status == "failed").all()
        retried = 0

        for doc in failed_docs:
            try:
                self.process_document(doc.id)
                retried += 1
            except Exception:
                continue

        return {"retried": retried, "failed_count": len(failed_docs)}
