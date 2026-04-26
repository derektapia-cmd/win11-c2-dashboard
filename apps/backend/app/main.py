from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard_settings import router as settings_router
from app.api.health import router as health_router
from app.api.notes import router as notes_router
from app.core.settings import settings
from app.storage.database import init_database


def create_app() -> FastAPI:
    init_database()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=["*"],
    )
    app.include_router(health_router)
    app.include_router(notes_router)
    app.include_router(settings_router)
    return app


app = create_app()
