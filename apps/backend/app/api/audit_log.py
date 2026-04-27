from fastapi import APIRouter, Query, status

from app.models.audit_log import AuditLogCreate, AuditLogResponse
from app.services.audit_log import create_audit_entry, list_audit_entries

router = APIRouter(prefix="/audit-log", tags=["audit-log"])


@router.get("", response_model=list[AuditLogResponse])
async def get_audit_log(limit: int = Query(default=50, ge=1, le=200)) -> list[AuditLogResponse]:
    return list_audit_entries(limit=limit)


@router.post("", response_model=AuditLogResponse, status_code=status.HTTP_201_CREATED)
async def post_audit_entry(entry: AuditLogCreate) -> AuditLogResponse:
    return create_audit_entry(entry)
