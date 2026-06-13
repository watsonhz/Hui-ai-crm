"""Application configuration via Pydantic Settings.

Reads from .env file automatically. Override with environment variables.
"""

import secrets
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = ""  # 强制从环境变量读取，无默认值即启动报错

    # Database pool
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://192.168.0.169:3000", "http://192.168.0.168:3000"]

    # JWT
    SECRET_KEY: str = ""  # 强制从环境变量读取
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_HOURS: int = 8

    # App
    APP_ENV: str = "development"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 开发环境自动生成 SECRET_KEY
        if not self.SECRET_KEY:
            if self.APP_ENV == "development":
                self.SECRET_KEY = secrets.token_urlsafe(64)
            else:
                raise ValueError("生产环境必须设置 SECRET_KEY 环境变量")
        # 开发环境 DATABASE_URL 允许为空（使用 SQLite 内存库）
        if not self.DATABASE_URL:
            if self.APP_ENV == "development":
                self.DATABASE_URL = "sqlite:///./dev.db"
            else:
                raise ValueError("生产环境必须设置 DATABASE_URL 环境变量")


settings = Settings()
