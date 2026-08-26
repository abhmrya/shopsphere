from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str
    app_env: str
    debug: bool = False
    app_version: str

    class Config:
        env_file = ".env"


settings = Settings()