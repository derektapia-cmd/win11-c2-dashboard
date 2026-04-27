import pytest
from fastapi.testclient import TestClient

from app.core.settings import settings
from app.main import app
from app.models.dashboard_settings import DEFAULT_VISIBLE_TILE_IDS
from app.storage.database import init_database


@pytest.fixture(autouse=True)
def isolated_settings_database(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "database_path", tmp_path / "test-dashboard.sqlite3")
    init_database()


def test_settings_default_privacy_mode_is_off() -> None:
    client = TestClient(app)

    response = client.get("/settings")

    assert response.status_code == 200
    assert response.json() == {
        "privacy_mode": False,
        "compact_mode": False,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
    }


def test_settings_privacy_mode_can_be_updated_and_loaded() -> None:
    client = TestClient(app)

    update_response = client.patch("/settings", json={"privacy_mode": True})
    load_response = client.get("/settings")

    assert update_response.status_code == 200
    assert update_response.json() == {
        "privacy_mode": True,
        "compact_mode": False,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
    }
    assert load_response.status_code == 200
    assert load_response.json() == {
        "privacy_mode": True,
        "compact_mode": False,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
    }


def test_settings_update_writes_audit_entry() -> None:
    client = TestClient(app)

    update_response = client.patch(
        "/settings",
        json={
            "privacy_mode": True,
            "compact_mode": True,
        },
    )
    audit_response = client.get("/audit-log")

    assert update_response.status_code == 200
    entries = audit_response.json()
    assert entries[0]["action"] == "settings.update.completed"
    assert entries[0]["target"] == "settings:dashboard"
    assert entries[0]["metadata"] == {
        "tile": "settings",
        "privacy_mode": True,
        "compact_mode": True,
    }


def test_settings_compact_mode_can_be_updated_and_loaded() -> None:
    client = TestClient(app)

    update_response = client.patch("/settings", json={"compact_mode": True})
    load_response = client.get("/settings")

    assert update_response.status_code == 200
    assert update_response.json() == {
        "privacy_mode": False,
        "compact_mode": True,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
    }
    assert load_response.status_code == 200
    assert load_response.json() == {
        "privacy_mode": False,
        "compact_mode": True,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
    }


def test_settings_visible_tile_ids_can_be_updated_and_loaded() -> None:
    client = TestClient(app)

    update_response = client.patch(
        "/settings",
        json={
            "visible_tile_ids": ["notes", "terminal"],
        },
    )
    load_response = client.get("/settings")

    assert update_response.status_code == 200
    assert update_response.json() == {
        "privacy_mode": False,
        "compact_mode": False,
        "visible_tile_ids": ["notes", "terminal"],
    }
    assert load_response.status_code == 200
    assert load_response.json() == {
        "privacy_mode": False,
        "compact_mode": False,
        "visible_tile_ids": ["notes", "terminal"],
    }


def test_settings_visible_tile_update_writes_compact_audit_metadata() -> None:
    client = TestClient(app)

    update_response = client.patch(
        "/settings",
        json={
            "visible_tile_ids": ["notes", "terminal"],
        },
    )
    audit_response = client.get("/audit-log")

    assert update_response.status_code == 200
    entries = audit_response.json()
    assert entries[0]["action"] == "settings.update.completed"
    assert entries[0]["metadata"] == {
        "tile": "settings",
        "visible_tile_count": 2,
        "visible_tile_ids": "notes,terminal",
    }


def test_settings_patch_allows_local_renderer_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/settings",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "PATCH",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"
