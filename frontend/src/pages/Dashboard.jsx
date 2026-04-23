import React, { useEffect, useState } from "react";
import { getDashboardMetrics } from "../services/api";

function MetricCard({ title, value }) {
  return (
    <article className="metric-card">
      <span>{title}</span>
      <h3>{value}</h3>
    </article>
  );
}

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getDashboardMetrics()
      .then((data) =>
        setMetrics({
          total_documents: data?.total_documents ?? 0,
          processed_documents: data?.processed_documents ?? 0,
          failed_documents: data?.failed_documents ?? 0,
          total_chunks: data?.total_chunks ?? 0,
          total_queries: data?.total_queries ?? 0,
          recent_activity: Array.isArray(data?.recent_activity) ? data.recent_activity : [],
        })
      )
      .catch(() => setError("Unable to load dashboard metrics."));
  }, []);

  if (error) return <p className="error">{error}</p>;
  if (!metrics) return <p className="hint">Loading dashboard...</p>;

  return (
    <section className="panel">
      <h2>Platform Metrics</h2>

      <div className="metric-grid">
        <MetricCard title="Total Documents" value={metrics.total_documents} />
        <MetricCard title="Processed" value={metrics.processed_documents} />
        <MetricCard title="Failed" value={metrics.failed_documents} />
        <MetricCard title="Chunks" value={metrics.total_chunks} />
        <MetricCard title="Queries" value={metrics.total_queries} />
      </div>

      <h3>Recent Pipeline Activity</h3>
      <ul className="activity-list">
        {metrics.recent_activity.length === 0 ? (
          <li>No recent activity yet.</li>
        ) : (
          metrics.recent_activity.map((item, idx) => (
            <li key={`${item?.created_at ?? "log"}-${idx}`}>
              <strong>{item?.stage ?? "unknown"}</strong> [{item?.status ?? "unknown"}] -{" "}
              {item?.message ?? "No message"}
            </li>
          ))
        )}
      </ul>
    </section>
  );
}
