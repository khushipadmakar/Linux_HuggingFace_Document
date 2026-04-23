import re
from collections import Counter


def detect_document_type(text: str) -> str:
    lowered = text.lower()
    if any(token in lowered for token in ["agreement", "party", "clause", "effective date"]):
        return "contract"
    if any(token in lowered for token in ["invoice", "po number", "tax"]):
        return "invoice"
    if any(token in lowered for token in ["nda", "confidential", "non-disclosure"]):
        return "nda"
    return "business_document"


def extract_metadata(text: str) -> dict:
    words = re.findall(r"[A-Za-z0-9$%.-]+", text)
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    amounts = re.findall(r"\$\s?\d+(?:,\d{3})*(?:\.\d{2})?", text)

    most_common_terms = [term for term, _ in Counter(w.lower() for w in words if len(w) > 4).most_common(8)]

    return {
        "document_type": detect_document_type(text),
        "language": "en",
        "word_count": len(words),
        "key_entities": {
            "emails": sorted(set(emails))[:10],
            "dates": sorted(set(dates))[:10],
            "amounts": sorted(set(amounts))[:10],
            "keywords": most_common_terms,
        },
    }
