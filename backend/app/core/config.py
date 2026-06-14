"""Application configuration via Pydantic Settings."""
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "sqlite:///./ai_crm.db"
    REDIS_URL: str = "redis://localhost:6379/0"
    CORS_ORIGINS: List[str] = []

    @property
    def cors_origins_list(self) -> List[str]:
        env_val = os.getenv("CORS_ORIGINS", "")
        if env_val:
            import json
            try: return json.loads(env_val)
            except json.JSONDecodeError: return [o.strip() for o in env_val.split(",")]
        return self.CORS_ORIGINS or ["http://localhost:5173"]

    SECRET_KEY: str = ""
    @property
    def secret_key(self) -> str:
        key = os.getenv("SECRET_KEY") or self.SECRET_KEY
        if not key:
            raise RuntimeError("SECRET_KEY 环境变量未设置！请在 .env 文件中配置。")
        return key

    APP_ENV: str = "development"
    DEBUG: bool = False

settings = Settings()
