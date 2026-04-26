import json
from datetime import datetime, timezone
from sqlite3 import Row
from uuid import uuid4

from app.models.note import NoteCreate, NoteResponse
from app.storage.database import get_connection


def list_notes() -> list[NoteResponse]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, title, body, tags, pinned, created_at, updated_at
            FROM notes
            ORDER BY pinned DESC, updated_at DESC
            """
        ).fetchall()

    return [_row_to_note(row) for row in rows]


def create_note(note: NoteCreate) -> NoteResponse:
    now = datetime.now(timezone.utc).isoformat()
    note_id = str(uuid4())
    title = note.title.strip() or "Untitled note"
    tags = [tag.strip() for tag in note.tags if tag.strip()]

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO notes (id, title, body, tags, pinned, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                note_id,
                title,
                note.body.strip(),
                json.dumps(tags),
                1 if note.pinned else 0,
                now,
                now,
            ),
        )
        connection.commit()

    return NoteResponse(
        id=note_id,
        title=title,
        body=note.body.strip(),
        tags=tags,
        pinned=note.pinned,
        created_at=now,
        updated_at=now,
    )


def _row_to_note(row: Row) -> NoteResponse:
    return NoteResponse(
        id=row["id"],
        title=row["title"],
        body=row["body"],
        tags=json.loads(row["tags"]),
        pinned=bool(row["pinned"]),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )

