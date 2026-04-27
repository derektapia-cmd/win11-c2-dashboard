from fastapi.testclient import TestClient

from app.core.settings import AppSettings
from app.main import app


def test_health_check_returns_ok() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "Win11 C2 Dashboard Backend"
    assert payload["version"] == "0.1.0"
    assert "timestamp_utc" in payload


def test_health_check_allows_local_renderer_origin() -> None:
    client = TestClient(app)

    response = client.get(
        "/health",
        headers={"Origin": "http://127.0.0.1:5173"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


def test_notes_post_allows_local_renderer_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/notes",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


def test_notes_patch_allows_local_renderer_origin() -> None:
    client = TestClient(app)

    response = client.options(
        "/notes/example-id",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "PATCH",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


def test_app_settings_can_load_local_environment(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_NAME", "Custom Dashboard Backend")
    monkeypatch.setenv("APP_VERSION", "9.9.9")
    monkeypatch.setenv("DATABASE_PATH", "./tmp/custom.sqlite3")
    monkeypatch.setenv(
        "CORS_ALLOWED_ORIGINS",
        "http://127.0.0.1:5173, http://localhost:5173",
    )

    loaded_settings = AppSettings()

    assert loaded_settings.app_env == "test"
    assert loaded_settings.app_name == "Custom Dashboard Backend"
    assert loaded_settings.app_version == "9.9.9"
    assert loaded_settings.database_path.as_posix() == "tmp/custom.sqlite3"
    assert loaded_settings.cors_allowed_origins == [
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ]
