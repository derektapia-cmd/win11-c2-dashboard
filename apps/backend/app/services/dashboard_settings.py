import json
from datetime import datetime, timezone

from app.models.dashboard_settings import DashboardSettingsResponse, DashboardSettingsUpdate
from app.storage.database import get_connection

DEFAULT_SETTINGS = DashboardSettingsResponse()


def get_dashboard_settings() -> DashboardSettingsResponse:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT key, value
            FROM user_settings
            """
        ).fetchall()

    stored = {row["key"]: json.loads(row["value"]) for row in rows}

    return DashboardSettingsResponse(
        privacy_mode=bool(stored.get("privacy_mode", DEFAULT_SETTINGS.privacy_mode)),
    )


def update_dashboard_settings(
    settings_update: DashboardSettingsUpdate,
) -> DashboardSettingsResponse:
    current = get_dashboard_settings()
    updated = current.model_copy(
        update=settings_update.model_dump(exclude_none=True),
    )
    now = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        for key, value in updated.model_dump().items():
            connection.execute(
                """
                INSERT INTO user_settings (key, value, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = excluded.updated_at
                """,
                (key, json.dumps(value), now),
            )
        connection.commit()

    return updated

