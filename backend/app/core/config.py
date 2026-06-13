"""Application configuration via Pydantic Settings.

Reads from .env file automatically. Override with environment variables.
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database (default: SQLite for dev; override DATABASE_URL for MySQL/PostgreSQL)
    DATABASE_URL: str = "sqlite:///./ai_crm.db"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://192.168.0.169:3000", "http://192.168.0.168:3000"]

    # App
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me-to-a-random-string"


settings = Settings()
