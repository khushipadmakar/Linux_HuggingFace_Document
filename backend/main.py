from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.db.session import init_db
from backend.routes import dashboard, process, qa, search, upload
from backend.utils.logger import configure_logger


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version=settings.app_version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(upload.router)
    app.include_router(process.router)
    app.include_router(search.router)
    app.include_router(qa.router)
    app.include_router(dashboard.router)

    @app.on_event("startup")
    def startup_event() -> None:
        Path(settings.upload_root).mkdir(parents=True, exist_ok=True)
        Path(settings.log_root).mkdir(parents=True, exist_ok=True)
        Path(settings.backup_root).mkdir(parents=True, exist_ok=True)
        configure_logger()
        init_db()

    @app.get("/")
    def root() -> dict:
        return {
            "name": settings.app_name,
            "status": "running",
            "version": settings.app_version,
            "database": "document_intelligence_db",
        }

    return app


app = create_app()
