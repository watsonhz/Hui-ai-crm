"""Application configuration via Pydantic Settings + env fallback."""

import os
import secrets
from typing import List
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings, SettingsConfigDict


def _build_database_url() -> str:
    """If DATABASE_URL not set, build from individual env vars."""
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASS", "")
    db = os.environ.get("DB_NAME", "ai_crm")
    return f"postgresql+psycopg2://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = _build_database_url()
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://192.168.0.169:3000"]

    # JWT
    SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 8

    # App
    APP_ENV: str = "development"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.SECRET_KEY:
            if self.APP_ENV == "development":
                self.SECRET_KEY = secrets.token_urlsafe(64)
            else:
                raise ValueError("生产环境必须设置 SECRET_KEY 环境变量")
        if not self.DATABASE_URL or "postgresql" in self.DATABASE_URL:
            # If it's a postgres URL and psycopg2 not installed, fall back
            try:
                import psycopg2  # noqa: F401
            except ImportError:
                if self.APP_ENV == "development":
                    self.DATABASE_URL = "sqlite:///./dev.db"


settings = Settings()
DEFAULT_DATABASE_URL = settings.DATABASE_URL
