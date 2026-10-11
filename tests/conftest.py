import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

import database
import router
from main import app
from models import Base


@pytest.fixture
def client(tmp_path, monkeypatch):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)
    monkeypatch.setattr(router, "engine", engine)
    monkeypatch.setattr(database, "engine", engine)

    with TestClient(app) as test_client:
        yield test_client

    engine.dispose()
