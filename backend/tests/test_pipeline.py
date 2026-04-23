from pathlib import Path


def test_pipeline_process_document(client, sample_text_file: Path):
    with sample_text_file.open("rb") as handle:
        upload_resp = client.post(
            "/api/documents/upload",
            files={"file": ("agreement.txt", handle, "text/plain")},
        )

    document_id = upload_resp.json()["document_id"]

    process_resp = client.post(f"/api/process/{document_id}")
    assert process_resp.status_code == 200
    assert process_resp.json()["status"] == "processed"

    detail_resp = client.get(f"/api/documents/{document_id}")
    detail = detail_resp.json()
    assert detail["chunk_count"] > 0
    assert detail["summary"] is not None
    assert detail["metadata"]["document_type"] in {"contract", "business_document", "nda", "invoice"}
