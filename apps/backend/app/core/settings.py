from pathlib import Path

from pydantic import BaseModel


class AppSettings(BaseModel):
    app_name: str = "Win11 C2 Dashboard Backend"
    app_version: str = "0.1.0"
    database_path: Path = Path("data/dashboard.sqlite3")
    cors_allowed_origins: list[str] = [
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ]


settings = AppSettings()
