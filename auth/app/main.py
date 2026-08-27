from fastapi import FastAPI

from .core.config import settings
from .api.v1.router import router as api_router

from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-style e-commerce backend",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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