import React, { useEffect, useState } from "react";
import { getDocument, getDocuments, processDocument, uploadDocument } from "../services/api";

export default function Documents() {
  const [file, setFile] = useState(null);
  const [documents, setDocuments] = useState([]);
  const [selected, setSelected] = useState(null);
  const [message, setMessage] = useState("");

  const refresh = async () => {
    const data = await getDocuments();
    setDocuments(Array.isArray(data) ? data : []);
  };

  useEffect(() => {
    refresh();
  }, []);

  const onUpload = async () => {
    if (!file) return;
    const result = await uploadDocument(file);
    setMessage(`Uploaded document #${result.document_id}`);
    setFile(null);
    await refresh();
  };

  const onProcess = async (documentId) => {
    const result = await processDocument(documentId);
    setMessage(result.message);
    await refresh();
  };

  const onView = async (documentId) => {
    const detail = await getDocument(documentId);
    setSelected(detail ?? null);
  };

  return (
    <section className="panel">
      <h2>Document Ingestion</h2>

      <div className="row">
        <input type="file" accept=".pdf,.docx,.txt" onChange={(e) => setFile(e.target.files?.[0])} />
        <button onClick={onUpload}>Upload</button>
      </div>

      {message && <p className="hint">{message}</p>}

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Filename</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {documents.map((doc) => (
              <tr key={doc.id}>
                <td>{doc.id}</td>
                <td>{doc.filename ?? "Unnamed file"}</td>
                <td>{doc.status ?? "unknown"}</td>
                <td>
                  <button onClick={() => onProcess(doc.id)}>Process</button>
                  <button className="ghost" onClick={() => onView(doc.id)}>
                    Details
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selected && (
        <article className="detail-card">
          <h3>Document #{selected.id}</h3>
          <p>
            <strong>Chunks:</strong> {selected.chunk_count}
          </p>
          <p>
            <strong>Summary:</strong> {selected.summary || "Not generated yet."}
          </p>
          <p>
            <strong>Metadata:</strong> {selected.metadata ? JSON.stringify(selected.metadata) : "Not available."}
          </p>
        </article>
      )}
    </section>
  );
}
