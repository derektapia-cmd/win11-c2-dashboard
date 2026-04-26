import json
from datetime import datetime, timezone
from sqlite3 import Row
from uuid import uuid4

from app.models.note import NoteCreate, NoteResponse, NoteUpdate
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


def update_note(note_id: str, note: NoteUpdate) -> NoteResponse | None:
    existing = get_note(note_id)

    if existing is None:
        return None

    now = datetime.now(timezone.utc).isoformat()
    title = existing.title
    body = existing.body
    tags = existing.tags
    pinned = existing.pinned

    if note.title is not None:
        title = note.title.strip() or "Untitled note"

    if note.body is not None:
        body = note.body.strip()

    if note.tags is not None:
        tags = [tag.strip() for tag in note.tags if tag.strip()]

    if note.pinned is not None:
        pinned = note.pinned

    with get_connection() as connection:
        connection.execute(
            """
            UPDATE notes
            SET title = ?, body = ?, tags = ?, pinned = ?, updated_at = ?
            WHERE id = ?
            """,
            (
                title,
                body,
                json.dumps(tags),
                1 if pinned else 0,
                now,
                note_id,
            ),
        )
        connection.commit()

    return get_note(note_id)


def delete_note(note_id: str) -> bool:
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        connection.commit()

    return cursor.rowcount > 0


def get_note(note_id: str) -> NoteResponse | None:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT id, title, body, tags, pinned, created_at, updated_at
            FROM notes
            WHERE id = ?
            """,
            (note_id,),
        ).fetchone()

    if row is None:
        return None

    return _row_to_note(row)


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
