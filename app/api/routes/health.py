# app/api/routes/health.py
from fastapi import APIRouter
from app.schemas.chat import HealthResponse
from app.db.database import check_db_connection
from app.core.config import get_settings

router = APIRouter(tags=["Health"])
settings = get_settings()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    Confirms the app and database are running correctly.
    """
    db_connected = check_db_connection()

    return HealthResponse(
        status="ok" if db_connected else "degraded",
        app=settings.app_name,
        env=settings.app_env,
        database="connected" if db_connected else "disconnected",
    )