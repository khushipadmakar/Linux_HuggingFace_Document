from pathlib import Path
import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

ROOT = Path(__file__).resolve().parents[2]
os.environ.setdefault("AIDOC_DATABASE_URL", f"sqlite:///{(ROOT / 'storage' / 'test_bootstrap.db').as_posix()}")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.db.models import Base  # noqa: E402
from backend.db.session import get_db  # noqa: E402
from backend.main import create_app  # noqa: E402


@pytest.fixture()
def client(tmp_path: Path) -> TestClient:
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    app = create_app()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def sample_text_file(tmp_path: Path) -> Path:
    file_path = tmp_path / "sample.txt"
    file_path.write_text(
        "Service Agreement\nEffective date 12/01/2025\nThe parties agree to payment of $1,500.00 every month.",
        encoding="utf-8",
    )
    return file_path
