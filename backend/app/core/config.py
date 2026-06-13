import os
import secrets
from urllib.parse import quote_plus

# 安全密钥
SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(64)
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

# 数据库连接 — 优先用 DATABASE_URL，否则从独立变量拼接 (自动对 user/password 做 URL 编码)
def _build_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if url:
        return url
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    user = os.environ.get("DB_USER", "postgres")
    password = os.environ.get("DB_PASS", "Admin@90088*")
    db = os.environ.get("DB_NAME", "ai_crm")
    return f"postgresql+psycopg2://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{db}"

DATABASE_URL = _build_database_url()
