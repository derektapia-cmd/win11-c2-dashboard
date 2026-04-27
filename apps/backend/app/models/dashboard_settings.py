from pydantic import BaseModel, Field

DEFAULT_VISIBLE_TILE_IDS = [
    "notes",
    "gmail",
    "weather",
    "news",
    "terminal",
    "wallets",
    "ai-tools",
    "calendar",
    "markets",
]


class DashboardSettingsResponse(BaseModel):
    privacy_mode: bool = False
    compact_mode: bool = False
    visible_tile_ids: list[str] = Field(default_factory=lambda: DEFAULT_VISIBLE_TILE_IDS.copy())


class DashboardSettingsUpdate(BaseModel):
    privacy_mode: bool | None = None
    compact_mode: bool | None = None
    visible_tile_ids: list[str] | None = None
