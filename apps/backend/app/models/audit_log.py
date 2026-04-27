from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator

AuditRiskLevel = Literal["low", "medium", "high", "critical"]
AuditStatus = Literal["requested", "approved", "completed", "blocked", "failed"]


class AuditLogCreate(BaseModel):
    action: str = Field(min_length=1, max_length=120)
    actor: str = Field(default="local-user", max_length=80)
    target: str = Field(default="dashboard", max_length=160)
    risk_level: AuditRiskLevel = "low"
    status: AuditStatus = "completed"
    summary: str = Field(min_length=1, max_length=500)
    metadata: dict[str, str | int | float | bool | None] = Field(default_factory=dict)

    @field_validator("action", "actor", "target", "summary")
    @classmethod
    def text_fields_must_have_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Audit log text fields cannot be empty.")

        return value.strip()


class AuditLogResponse(BaseModel):
    id: str
    action: str
    actor: str
    target: str
    risk_level: AuditRiskLevel
    status: AuditStatus
    summary: str
    metadata: dict[str, str | int | float | bool | None]
    created_at: datetime
