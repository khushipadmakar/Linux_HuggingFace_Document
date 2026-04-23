# AI Document Intelligence Platform

Backend-heavy platform for document ingestion, AI enrichment, semantic retrieval, and API serving.

## Stack
- Backend: FastAPI
- Frontend: React (UI only)
- Database: PostgreSQL (`document_intelligence_db`)
- Vector storage: `embedding_store` (pgvector-compatible column with SQLite JSON fallback for tests)
- AI/LLM: Ollama API for summarization and Q&A (fallback mode if unavailable)
- Tests: pytest
- CI/CD: GitHub Actions (`.github/workflows/ci.yml`)

## End-to-End Data Flow
1. Ingestion: upload PDF/DOCX/TXT (`POST /api/documents/upload`)
2. Processing: extract and clean text, chunk it (`POST /api/process/{document_id}`)
3. Enrichment: metadata, summary, embeddings persisted in DB
4. Serving: semantic search (`POST /api/search`), Q&A (`POST /api/ask`), dashboard metrics (`GET /api/dashboard/metrics`)

## Required Tables
- `uploaded_documents`
- `document_chunks`
- `document_metadata`
- `ai_summaries`
- `embedding_store`
- `query_history`
- `pipeline_logs`

## Local Development
### Backend
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Summary
- `POST /api/documents/upload`
- `GET /api/documents`
- `GET /api/documents/{document_id}`
- `GET /api/documents/{document_id}/insights`
- `POST /api/process/{document_id}`
- `POST /api/process/retry-failed`
- `POST /api/search`
- `POST /api/ask`
- `GET /api/dashboard/metrics`

## Linux Deployment Runbook
### Directory Structure
```bash
/opt/app/
  backend/
  frontend/
  uploads/
  logs/
  backups/
  linux/
```

### Environment
Create `/opt/app/.env`:
```bash
AIDOC_DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/document_intelligence_db
AIDOC_UPLOAD_ROOT=/opt/app/uploads
AIDOC_LOG_ROOT=/opt/app/logs
AIDOC_OLLAMA_URL=http://localhost:11434/api/generate
AIDOC_OLLAMA_MODEL=llama3
```

### systemd Service
- Service file: `linux/systemd/app.service`
```bash
sudo cp linux/systemd/app.service /etc/systemd/system/app.service
sudo systemctl daemon-reload
sudo systemctl enable app.service
sudo systemctl start app.service
```

### Nginx Reverse Proxy
- Site config: `linux/nginx/ai-doc-platform.conf`
```bash
sudo cp linux/nginx/ai-doc-platform.conf /etc/nginx/sites-available/ai-doc-platform
sudo ln -sf /etc/nginx/sites-available/ai-doc-platform /etc/nginx/sites-enabled/ai-doc-platform
sudo nginx -t
sudo systemctl restart nginx
```

### Cron Scheduler
- Cron file: `linux/cron/cleanup.cron`
```bash
sudo cp linux/cron/cleanup.cron /etc/cron.d/ai-doc-platform
sudo chmod 644 /etc/cron.d/ai-doc-platform
```

### Log Rotation
- Logrotate file: `linux/logrotate/ai-doc-platform`
```bash
sudo cp linux/logrotate/ai-doc-platform /etc/logrotate.d/ai-doc-platform
sudo logrotate -f /etc/logrotate.d/ai-doc-platform
```

### Linux Scripts
Make executable:
```bash
chmod +x linux/scripts/*.sh
```

Scripts included:
- `linux/scripts/start.sh` (startup + service restart)
- `linux/scripts/setup_env.sh` (venv + dependency setup)
- `linux/scripts/deploy.sh` (pull/build/restart)
- `linux/scripts/cleanup_cron.sh` (cleanup + retry pipeline)
- `linux/scripts/backup.sh` (DB and uploads backup/export)
- `linux/scripts/rotate_logs.sh` (trigger log rotation)
- `linux/scripts/permissions.sh` (permissions for upload/log directories)
- `linux/scripts/monitor.sh` (service and log checks)

## Testing
```bash
pytest backend/tests -q
```
