from pydantic import BaseModel


class AppSettings(BaseModel):
    app_name: str = "Win11 C2 Dashboard Backend"
    app_version: str = "0.1.0"


settings = AppSettings()

