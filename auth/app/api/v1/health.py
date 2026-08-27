from fastapi import APIRouter,Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from ...core.dependencies import get_db
from ...core.config import settings

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

@router.get("/health/db")
def database_health_check(db:Session = Depends(get_db),):

    result = db.execute(text("select 1"))

    return {
        "database"  : "connected",
        "result": result.scalar(),
    }