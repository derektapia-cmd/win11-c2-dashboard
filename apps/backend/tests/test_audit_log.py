import pytest
from fastapi.testclient import TestClient

from app.core.settings import settings
from app.main import app
from app.storage.database import init_database


@pytest.fixture(autouse=True)
def isolated_audit_database(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "database_path", tmp_path / "test-dashboard.sqlite3")
    init_database()


def test_audit_log_starts_empty() -> None:
    client = TestClient(app)

    response = client.get("/audit-log")

    assert response.status_code == 200
    assert response.json() == []


def test_audit_entry_can_be_saved_and_loaded() -> None:
    client = TestClient(app)

    create_response = client.post(
        "/audit-log",
        json={
            "action": "note.delete.requested",
            "actor": "local-user",
            "target": "note:example",
            "risk_level": "medium",
            "status": "approved",
            "summary": "User approved deleting a local note.",
            "metadata": {"tile": "notes", "requires_confirmation": True},
        },
    )
    list_response = client.get("/audit-log")

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["action"] == "note.delete.requested"
    assert created["risk_level"] == "medium"
    assert created["status"] == "approved"
    assert created["metadata"] == {"tile": "notes", "requires_confirmation": True}
    assert "created_at" in created

    assert list_response.status_code == 200
    entries = list_response.json()
    assert len(entries) == 1
    assert entries[0]["id"] == created["id"]


def test_audit_log_limit_is_applied() -> None:
    client = TestClient(app)

    for index in range(3):
        client.post(
            "/audit-log",
            json={
                "action": f"test.action.{index}",
                "summary": f"Test audit entry {index}",
            },
        )

    response = client.get("/audit-log?limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_blank_audit_summary_is_rejected() -> None:
    client = TestClient(app)

    response = client.post(
        "/audit-log",
        json={
            "action": "terminal.command.requested",
            "summary": "   ",
        },
    )

    assert response.status_code == 422


def test_audit_log_post_allows_local_renderer_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/audit-log",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"
