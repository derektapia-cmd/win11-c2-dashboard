import pytest
from fastapi.testclient import TestClient

from app.core.settings import settings
from app.main import app
from app.storage.database import init_database


@pytest.fixture(autouse=True)
def isolated_notes_database(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "database_path", tmp_path / "test-dashboard.sqlite3")
    init_database()


def test_notes_list_starts_empty() -> None:
    client = TestClient(app)

    response = client.get("/notes")

    assert response.status_code == 200
    assert response.json() == []


def test_notes_can_be_saved_and_loaded() -> None:
    client = TestClient(app)

    create_response = client.post(
        "/notes",
        json={
            "title": "First cockpit note",
            "body": "Local notes are wired to SQLite.",
            "tags": ["dashboard", "local"],
            "pinned": True,
        },
    )

    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "First cockpit note"
    assert created["body"] == "Local notes are wired to SQLite."
    assert created["tags"] == ["dashboard", "local"]
    assert created["pinned"] is True

    list_response = client.get("/notes")

    assert list_response.status_code == 200
    notes = list_response.json()
    assert len(notes) == 1
    assert notes[0]["id"] == created["id"]


def test_blank_note_body_is_rejected() -> None:
    client = TestClient(app)

    response = client.post(
        "/notes",
        json={
            "title": "Empty",
            "body": "   ",
        },
    )

    assert response.status_code == 422

