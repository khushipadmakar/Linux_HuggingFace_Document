from pathlib import Path


def test_upload_and_list_documents(client, sample_text_file: Path):
    with sample_text_file.open("rb") as handle:
        response = client.post(
            "/api/documents/upload",
            files={"file": ("sample.txt", handle, "text/plain")},
        )

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "uploaded"

    docs = client.get("/api/documents")
    assert docs.status_code == 200
    assert len(docs.json()) == 1
