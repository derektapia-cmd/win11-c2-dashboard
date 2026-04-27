import json
from datetime import datetime, timezone

from app.models.dashboard_settings import DashboardSettingsResponse, DashboardSettingsUpdate
from app.services.audit_log import record_audit_event
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
        compact_mode=bool(stored.get("compact_mode", DEFAULT_SETTINGS.compact_mode)),
        visible_tile_ids=list(
            stored.get("visible_tile_ids", DEFAULT_SETTINGS.visible_tile_ids),
        ),
        tile_order_ids=list(
            stored.get("tile_order_ids", DEFAULT_SETTINGS.tile_order_ids),
        ),
    )


def update_dashboard_settings(
    settings_update: DashboardSettingsUpdate,
) -> DashboardSettingsResponse:
    current = get_dashboard_settings()
    requested_updates = settings_update.model_dump(exclude_none=True)
    updated = current.model_copy(
        update=requested_updates,
    )
    changed_settings = {
        key: value
        for key, value in requested_updates.items()
        if getattr(current, key) != value
    }
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

    if changed_settings:
        audit_metadata: dict[str, str | int | float | bool | None] = {"tile": "settings"}

        for key, value in changed_settings.items():
            if key == "visible_tile_ids":
                audit_metadata["visible_tile_count"] = len(value)
                audit_metadata["visible_tile_ids"] = ",".join(value)
            elif key == "tile_order_ids":
                audit_metadata["tile_order_count"] = len(value)
                audit_metadata["tile_order_ids"] = ",".join(value)
            else:
                audit_metadata[key] = value

        record_audit_event(
            action="settings.update.completed",
            target="settings:dashboard",
            summary="Dashboard settings were updated.",
            metadata=audit_metadata,
        )

    return updated
