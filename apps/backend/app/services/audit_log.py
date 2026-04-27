import json
from datetime import datetime, timezone
from sqlite3 import Row
from uuid import uuid4

from app.models.audit_log import AuditLogCreate, AuditLogResponse
from app.models.audit_log import AuditRiskLevel, AuditStatus
from app.storage.database import get_connection


def list_audit_entries(limit: int = 50) -> list[AuditLogResponse]:
    safe_limit = min(max(limit, 1), 200)

    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, action, actor, target, risk_level, status, summary, metadata, created_at
            FROM audit_log
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (safe_limit,),
        ).fetchall()

    return [_row_to_audit_entry(row) for row in rows]


def create_audit_entry(entry: AuditLogCreate) -> AuditLogResponse:
    now = datetime.now(timezone.utc).isoformat()
    entry_id = str(uuid4())

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO audit_log (
                id, action, actor, target, risk_level, status, summary, metadata, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry_id,
                entry.action.strip(),
                entry.actor.strip(),
                entry.target.strip(),
                entry.risk_level,
                entry.status,
                entry.summary.strip(),
                json.dumps(entry.metadata),
                now,
            ),
        )
        connection.commit()

    return AuditLogResponse(
        id=entry_id,
        action=entry.action.strip(),
        actor=entry.actor.strip(),
        target=entry.target.strip(),
        risk_level=entry.risk_level,
        status=entry.status,
        summary=entry.summary.strip(),
        metadata=entry.metadata,
        created_at=now,
    )


def record_audit_event(
    *,
    action: str,
    summary: str,
    target: str = "dashboard",
    actor: str = "local-user",
    risk_level: AuditRiskLevel = "low",
    status: AuditStatus = "completed",
    metadata: dict[str, str | int | float | bool | None] | None = None,
) -> AuditLogResponse:
    return create_audit_entry(
        AuditLogCreate(
            action=action,
            actor=actor,
            target=target,
            risk_level=risk_level,
            status=status,
            summary=summary,
            metadata=metadata or {},
        ),
    )


def _row_to_audit_entry(row: Row) -> AuditLogResponse:
    return AuditLogResponse(
        id=row["id"],
        action=row["action"],
        actor=row["actor"],
        target=row["target"],
        risk_level=row["risk_level"],
        status=row["status"],
        summary=row["summary"],
        metadata=json.loads(row["metadata"]),
        created_at=row["created_at"],
    )
