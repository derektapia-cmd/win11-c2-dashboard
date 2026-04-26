from fastapi import APIRouter, status

from app.models.note import NoteCreate, NoteResponse
from app.services.notes import create_note, list_notes

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteResponse])
async def get_notes() -> list[NoteResponse]:
    return list_notes()


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def post_note(note: NoteCreate) -> NoteResponse:
    return create_note(note)

