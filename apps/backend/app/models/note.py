from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class NoteCreate(BaseModel):
    title: str = Field(default="Untitled note", max_length=120)
    body: str = Field(min_length=1, max_length=5000)
    tags: list[str] = Field(default_factory=list, max_length=12)
    pinned: bool = False

    @field_validator("body")
    @classmethod
    def body_must_have_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Note body cannot be empty.")

        return value


class NoteResponse(BaseModel):
    id: str
    title: str
    body: str
    tags: list[str]
    pinned: bool
    created_at: datetime
    updated_at: datetime
