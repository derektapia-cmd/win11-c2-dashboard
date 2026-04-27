import pytest
from fastapi.testclient import TestClient

from app.core.settings import settings
from app.main import app
from app.models.dashboard_settings import DEFAULT_TILE_ORDER_IDS, DEFAULT_VISIBLE_TILE_IDS
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
        "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
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
        "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
    }
    assert load_response.status_code == 200
    assert load_response.json() == {
        "privacy_mode": True,
        "compact_mode": False,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
        "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
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
        "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
    }
    assert load_response.status_code == 200
    assert load_response.json() == {
        "privacy_mode": False,
        "compact_mode": True,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
        "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
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
        "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
    }
    assert load_response.status_code == 200
    assert load_response.json() == {
        "privacy_mode": False,
        "compact_mode": False,
        "visible_tile_ids": ["notes", "terminal"],
        "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
    }


def test_settings_tile_order_ids_can_be_updated_and_loaded() -> None:
    client = TestClient(app)

    update_response = client.patch(
        "/settings",
        json={
            "tile_order_ids": ["terminal", "notes", "gmail"],
        },
    )
    load_response = client.get("/settings")

    assert update_response.status_code == 200
    assert update_response.json() == {
        "privacy_mode": False,
        "compact_mode": False,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
        "tile_order_ids": ["terminal", "notes", "gmail"],
    }
    assert load_response.status_code == 200
    assert load_response.json() == {
        "privacy_mode": False,
        "compact_mode": False,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
        "tile_order_ids": ["terminal", "notes", "gmail"],
    }


def test_settings_layout_can_be_reset_after_custom_visibility_and_order() -> None:
    client = TestClient(app)

    client.patch(
        "/settings",
        json={
            "visible_tile_ids": ["terminal", "notes"],
            "tile_order_ids": ["terminal", "notes", "gmail"],
        },
    )
    reset_response = client.patch(
        "/settings",
        json={
            "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
            "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
        },
    )
    load_response = client.get("/settings")
    audit_response = client.get("/audit-log")

    expected_settings = {
        "privacy_mode": False,
        "compact_mode": False,
        "visible_tile_ids": DEFAULT_VISIBLE_TILE_IDS,
        "tile_order_ids": DEFAULT_TILE_ORDER_IDS,
    }

    assert reset_response.status_code == 200
    assert reset_response.json() == expected_settings
    assert load_response.status_code == 200
    assert load_response.json() == expected_settings
    entries = audit_response.json()
    assert entries[0]["action"] == "settings.update.completed"
    assert entries[0]["metadata"] == {
        "tile": "settings",
        "visible_tile_count": len(DEFAULT_VISIBLE_TILE_IDS),
        "visible_tile_ids": ",".join(DEFAULT_VISIBLE_TILE_IDS),
        "tile_order_count": len(DEFAULT_TILE_ORDER_IDS),
        "tile_order_ids": ",".join(DEFAULT_TILE_ORDER_IDS),
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


def test_settings_tile_order_update_writes_compact_audit_metadata() -> None:
    client = TestClient(app)

    update_response = client.patch(
        "/settings",
        json={
            "tile_order_ids": ["terminal", "notes", "gmail"],
        },
    )
    audit_response = client.get("/audit-log")

    assert update_response.status_code == 200
    entries = audit_response.json()
    assert entries[0]["action"] == "settings.update.completed"
    assert entries[0]["metadata"] == {
        "tile": "settings",
        "tile_order_count": 3,
        "tile_order_ids": "terminal,notes,gmail",
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
