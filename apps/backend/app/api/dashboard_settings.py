from fastapi import APIRouter

from app.models.dashboard_settings import DashboardSettingsResponse, DashboardSettingsUpdate
from app.services.dashboard_settings import get_dashboard_settings, update_dashboard_settings

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=DashboardSettingsResponse)
async def get_settings() -> DashboardSettingsResponse:
    return get_dashboard_settings()


@router.patch("", response_model=DashboardSettingsResponse)
async def patch_settings(
    settings_update: DashboardSettingsUpdate,
) -> DashboardSettingsResponse:
    return update_dashboard_settings(settings_update)

