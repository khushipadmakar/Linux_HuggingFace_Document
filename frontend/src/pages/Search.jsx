import React, { useState } from "react";
import { searchDocuments } from "../services/api";

export default function Search() {
  const [query, setQuery] = useState("");
  const [matches, setMatches] = useState([]);

  const onSearch = async () => {
    if (!query.trim()) return;
    const result = await searchDocuments(query, 5);
    setMatches(Array.isArray(result?.matches) ? result.matches : []);
  };

  return (
    <section className="panel">
      <h2>Semantic Search</h2>
      <div className="row">
        <input
          type="text"
          placeholder="Ask about obligations, dates, entities..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={onSearch}>Search</button>
      </div>

      <ul className="result-list">
        {matches.map((match) => (
          <li key={match.chunk_id}>
            <header>
              <span>Document #{match.document_id ?? "N/A"}</span>
              <strong>Score: {Number(match.score ?? 0).toFixed(3)}</strong>
            </header>
            <p>{match.chunk_text ?? "No matching text returned."}</p>
          </li>
        ))}
      </ul>
    </section>
  );
}
