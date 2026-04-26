from pydantic import BaseModel


class DashboardSettingsResponse(BaseModel):
    privacy_mode: bool = False


class DashboardSettingsUpdate(BaseModel):
    privacy_mode: bool | None = None

