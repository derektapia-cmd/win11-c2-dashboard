from fastapi import APIRouter, HTTPException, Response, status

from app.models.note import NoteCreate, NoteResponse, NoteUpdate
from app.services.notes import create_note, delete_note, list_notes, update_note

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteResponse])
async def get_notes() -> list[NoteResponse]:
    return list_notes()


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def post_note(note: NoteCreate) -> NoteResponse:
    return create_note(note)


@router.patch("/{note_id}", response_model=NoteResponse)
async def patch_note(note_id: str, note: NoteUpdate) -> NoteResponse:
    updated_note = update_note(note_id, note)

    if updated_note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")

    return updated_note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_note(note_id: str) -> Response:
    was_deleted = delete_note(note_id)

    if not was_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
