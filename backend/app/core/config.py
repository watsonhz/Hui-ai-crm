<<<<<<< HEAD
"""Application configuration via Pydantic Settings.

Reads from .env file automatically. Override with environment variables.
"""

import secrets
from typing import List
=======
"""Application configuration via Pydantic Settings + env fallback."""

import os
import secrets
from typing import List
from urllib.parse import quote_plus
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8

from pydantic_settings import BaseSettings, SettingsConfigDict


<<<<<<< HEAD
=======
def _build_database_url() -> str:
    """If DATABASE_URL not set, build from individual env vars."""
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASS", "")
    db = os.environ.get("DB_NAME", "ai_crm")
    return f"postgresql+psycopg2://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{db}"


>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
<<<<<<< HEAD
    DATABASE_URL: str = ""  # 强制从环境变量读取，无默认值即启动报错

    # Database pool
=======
    DATABASE_URL: str = _build_database_url()
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
<<<<<<< HEAD
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://192.168.0.169:3000", "http://192.168.0.168:3000"]

    # JWT
    SECRET_KEY: str = ""  # 强制从环境变量读取
=======
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://192.168.0.169:3000"]

    # JWT
    SECRET_KEY: str = ""
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 8

    # App
    APP_ENV: str = "development"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
<<<<<<< HEAD
        # 开发环境自动生成 SECRET_KEY
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
        if not self.SECRET_KEY:
            if self.APP_ENV == "development":
                self.SECRET_KEY = secrets.token_urlsafe(64)
            else:
                raise ValueError("生产环境必须设置 SECRET_KEY 环境变量")
<<<<<<< HEAD
        # 开发环境 DATABASE_URL 允许为空（使用 SQLite 内存库）
        if not self.DATABASE_URL:
            if self.APP_ENV == "development":
                self.DATABASE_URL = "sqlite:///./dev.db"
            else:
                raise ValueError("生产环境必须设置 DATABASE_URL 环境变量")


settings = Settings()
=======
        if not self.DATABASE_URL or "postgresql" in self.DATABASE_URL:
            # If it's a postgres URL and psycopg2 not installed, fall back
            try:
                import psycopg2  # noqa: F401
            except ImportError:
                if self.APP_ENV == "development":
                    self.DATABASE_URL = "sqlite:///./dev.db"


settings = Settings()
DEFAULT_DATABASE_URL = settings.DATABASE_URL
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
