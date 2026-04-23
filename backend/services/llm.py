from __future__ import annotations

from backend.core.config import settings

try:
    from transformers import pipeline
except Exception:
    pipeline = None


class LLMService:
    def __init__(self) -> None:
        self.summary_model = settings.hf_summary_model
        self.qa_model = settings.hf_qa_model
        self._summarizer = None
        self._qa_pipeline = None

    def _get_summarizer(self):
        if self._summarizer is not None:
            return self._summarizer
        if pipeline is None:
            return None
        try:
            self._summarizer = pipeline("summarization", model=self.summary_model)
        except Exception:
            self._summarizer = None
        return self._summarizer

    def _get_qa(self):
        if self._qa_pipeline is not None:
            return self._qa_pipeline
        if pipeline is None:
            return None
        try:
            self._qa_pipeline = pipeline("question-answering", model=self.qa_model)
        except Exception:
            self._qa_pipeline = None
        return self._qa_pipeline

    @staticmethod
    def _fallback_summary(text: str) -> str:
        cleaned = " ".join(text.split())
        return cleaned[:600] + ("..." if len(cleaned) > 600 else "")

    def summarize(self, text: str) -> str:
        payload = text.strip()
        if not payload:
            return "No content found in the document."

        summarizer = self._get_summarizer()
        if summarizer is None:
            return self._fallback_summary(payload)

        try:
            chunk = payload[:3000]
            result = summarizer(chunk, max_length=180, min_length=40, do_sample=False)
            return (result[0].get("summary_text") or "").strip() or self._fallback_summary(payload)
        except Exception:
            return self._fallback_summary(payload)

    def answer(self, question: str, context: str) -> str:
        question = question.strip()
        context = context.strip()
        if not context:
            return "I could not find enough context in the uploaded documents to answer this question."

        qa_model = self._get_qa()
        if qa_model is None:
            return context[:400] + ("..." if len(context) > 400 else "")

        try:
            result = qa_model(question=question, context=context[:5000])
            answer = (result.get("answer") or "").strip()
            return answer or "I could not determine a reliable answer from the context."
        except Exception:
            return context[:400] + ("..." if len(context) > 400 else "")


llm_service = LLMService()
