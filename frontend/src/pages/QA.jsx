import React, { useState } from "react";
import { askQuestion } from "../services/api";

export default function QA() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [refs, setRefs] = useState([]);

  const onAsk = async () => {
    if (!question.trim()) return;
    const data = await askQuestion(question, 4);
    setAnswer(data?.answer ?? "No answer returned.");
    setRefs(Array.isArray(data?.references) ? data.references : []);
  };

  return (
    <section className="panel">
      <h2>Document Q&A</h2>

      <textarea
        rows="4"
        placeholder="What is the renewal term in the agreement?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={onAsk}>Ask</button>

      {answer && (
        <article className="detail-card">
          <h3>Answer</h3>
          <p>{answer}</p>

          <h4>References</h4>
          <ul className="activity-list">
            {refs.map((ref) => (
              <li key={ref.chunk_id}>
                [Doc {ref.document_id ?? "N/A"}] {ref.chunk_text ?? "Reference unavailable."}
              </li>
            ))}
          </ul>
        </article>
      )}
    </section>
  );
}
