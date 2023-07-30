from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    APP_ENVIRONMENT: str
    DEBUG: bool
    LOG_LEVEL: str
    SECRET_KEY: str

    DB_URL: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    JWT_ALGORITHMS: List[str] = ["HS256"]

    class Config:
        env_file = ".env"


settings: Settings = Settings()
