import os
from pathlib import Path

from pydantic import BaseModel, Field


def _get_env_text(name: str, default: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        return default

    return value.strip()


def _get_env_path(name: str, default: str) -> Path:
    return Path(_get_env_text(name, default))


def _get_env_list(name: str, default: list[str]) -> list[str]:
    value = os.getenv(name)

    if value is None or not value.strip():
        return default

    return [item.strip() for item in value.split(",") if item.strip()]


class AppSettings(BaseModel):
    app_env: str = Field(default_factory=lambda: _get_env_text("APP_ENV", "development"))
    app_name: str = Field(
        default_factory=lambda: _get_env_text("APP_NAME", "Win11 C2 Dashboard Backend"),
    )
    app_version: str = Field(default_factory=lambda: _get_env_text("APP_VERSION", "0.1.0"))
    database_path: Path = Field(
        default_factory=lambda: _get_env_path("DATABASE_PATH", "data/dashboard.sqlite3"),
    )
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: _get_env_list(
            "CORS_ALLOWED_ORIGINS",
            [
                "http://127.0.0.1:5173",
                "http://localhost:5173",
            ],
        ),
    )


settings = AppSettings()
