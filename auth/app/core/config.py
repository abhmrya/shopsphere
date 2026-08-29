from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):

    # =========================
    # APPLICATION
    # =========================

    app_name: str
    app_env: str
    debug: bool = False
    app_version: str

    # =========================
    # AUTH DATABASE
    # =========================

    auth_db_user: str
    auth_db_password: str
    auth_db_name: str
    auth_db_port: int

    auth_database_url: str

    # =========================
    # JWT                                                                                                                                                                    
    # =========================


    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


settings = Settings()