from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.core.settings import settings

router = APIRouter(tags=["system"])


class HealthResponse(BaseModel):
    status: str = Field(default="ok")
    service: str
    version: str
    timestamp_utc: datetime


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(
        service=settings.app_name,
        version=settings.app_version,
        timestamp_utc=datetime.now(timezone.utc),
    )

