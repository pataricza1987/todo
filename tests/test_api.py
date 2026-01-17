import os

import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.db import Base, engine

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"


@pytest.fixture(autouse=True)
def _create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_and_get_todo():
    client = TestClient(app)
    r = client.post("/todos", json={"title": "Teszt", "priority": 3})
    assert r.status_code == 201
    todo = r.json()
    r2 = client.get(f"/todos/{todo['id']}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Teszt"


def test_delete_todo():
    client = TestClient(app)
    r = client.post("/todos", json={"title": "Del", "priority": 2})
    todo_id = r.json()["id"]
    d = client.delete(f"/todos/{todo_id}")
    assert d.status_code == 204
    g = client.get(f"/todos/{todo_id}")
    assert g.status_code == 404
