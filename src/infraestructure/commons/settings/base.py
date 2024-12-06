from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Restaurant API"
    APP_VERSION: str = "0.1.0"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings: Settings = Settings()
