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


def test_note_create_writes_audit_entry() -> None:
    client = TestClient(app)

    create_response = client.post(
        "/notes",
        json={
            "title": "Audit me",
            "body": "This note should create an audit entry.",
        },
    )
    audit_response = client.get("/audit-log")

    assert create_response.status_code == 201
    entries = audit_response.json()
    assert entries[0]["action"] == "note.create.completed"
    assert entries[0]["target"] == f"note:{create_response.json()['id']}"
    assert entries[0]["metadata"]["tile"] == "notes"
    assert entries[0]["metadata"]["title_length"] == len("Audit me")


def test_notes_can_be_updated() -> None:
    client = TestClient(app)
    create_response = client.post(
        "/notes",
        json={
            "title": "Draft",
            "body": "Original body",
            "tags": ["draft"],
        },
    )
    note_id = create_response.json()["id"]

    update_response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "Pinned note",
            "body": "Updated body",
            "tags": ["dashboard", "updated"],
            "pinned": True,
        },
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "Pinned note"
    assert updated["body"] == "Updated body"
    assert updated["tags"] == ["dashboard", "updated"]
    assert updated["pinned"] is True


def test_note_update_writes_audit_entry_without_body_content() -> None:
    client = TestClient(app)
    create_response = client.post(
        "/notes",
        json={
            "title": "Draft",
            "body": "Original body",
        },
    )
    note_id = create_response.json()["id"]

    update_response = client.patch(
        f"/notes/{note_id}",
        json={
            "body": "Updated body",
            "pinned": True,
        },
    )
    audit_response = client.get("/audit-log")

    assert update_response.status_code == 200
    entries = audit_response.json()
    assert entries[0]["action"] == "note.update.completed"
    assert entries[0]["target"] == f"note:{note_id}"
    assert entries[0]["metadata"]["changed_fields"] == "body,pinned"
    assert "Updated body" not in str(entries[0])


def test_notes_can_be_deleted() -> None:
    client = TestClient(app)
    create_response = client.post(
        "/notes",
        json={
            "title": "Temporary note",
            "body": "Delete this note.",
        },
    )
    note_id = create_response.json()["id"]

    delete_response = client.delete(f"/notes/{note_id}")
    list_response = client.get("/notes")

    assert delete_response.status_code == 204
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_note_delete_writes_medium_risk_audit_entry() -> None:
    client = TestClient(app)
    create_response = client.post(
        "/notes",
        json={
            "title": "Temporary note",
            "body": "Delete this note.",
            "pinned": True,
        },
    )
    note_id = create_response.json()["id"]

    delete_response = client.delete(f"/notes/{note_id}")
    audit_response = client.get("/audit-log")

    assert delete_response.status_code == 204
    entries = audit_response.json()
    assert entries[0]["action"] == "note.delete.completed"
    assert entries[0]["target"] == f"note:{note_id}"
    assert entries[0]["risk_level"] == "medium"
    assert entries[0]["metadata"]["pinned"] is True


def test_missing_note_update_returns_404() -> None:
    client = TestClient(app)

    response = client.patch(
        "/notes/missing-note",
        json={
            "pinned": True,
        },
    )

    assert response.status_code == 404


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
