from fastapi import APIRouter
from app.config import get_settings

settings = get_settings()

router = APIRouter()


@router.get("/")
def health_check():
    return {
        "app_name": settings.app_name,
        "env": settings.environment,
        "debug": settings.debug,
    }
