from pathlib import Path


def test_semantic_search_and_qa(client, sample_text_file: Path):
    with sample_text_file.open("rb") as handle:
        upload_resp = client.post(
            "/api/documents/upload",
            files={"file": ("legal.txt", handle, "text/plain")},
        )

    document_id = upload_resp.json()["document_id"]
    client.post(f"/api/process/{document_id}")

    search_resp = client.post(
        "/api/search",
        json={"query": "payment terms", "top_k": 3},
    )
    assert search_resp.status_code == 200
    assert len(search_resp.json()["matches"]) >= 1

    qa_resp = client.post(
        "/api/ask",
        json={"question": "What does the contract say about payment?", "top_k": 2},
    )
    assert qa_resp.status_code == 200
    assert len(qa_resp.json()["answer"]) > 0
