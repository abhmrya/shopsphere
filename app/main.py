from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.router import router as api_router

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-style e-commerce backend",
)


@app.get("/")
def root():
    return {
        "message": "ShopSphere API"
    }

app.include_router(
    api_router,
    prefix="/api/v1",
)