from __future__ import annotations

import os

import pytest
from fastapi.testclient import TestClient

from ai_bots.api.server import app


@pytest.fixture(scope="module")
def client():
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("requires OPENAI_API_KEY")
    return TestClient(app)


def test_health(client: TestClient):
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_ask(client: TestClient):
    r = client.post("/ask", json={"query": "What is the return window?"})
    assert r.status_code == 200
    assert "answer" in r.json()
    assert isinstance(r.json()["answer"], str)
