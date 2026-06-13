from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

if not settings.DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL 未配置。请设置环境变量 DATABASE_URL 或在 .env 文件中配置。\n"
        "开发环境示例: DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/ai_crm"
    )

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
