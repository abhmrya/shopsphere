from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@router.get("/version")
def version_check():
    return {
        "version": settings.app_version,
        "service": settings.app_name,
        "environment": settings.app_env
    }