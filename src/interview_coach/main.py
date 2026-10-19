from fastapi import FastAPI

from interview_coach.api.routes.health import router as health_router
from interview_coach.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.include_router(health_router)
    return app

app = create_app()