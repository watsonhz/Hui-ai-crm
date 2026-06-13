"""pytest 共享夹具 —— 内存 SQLite + TestClient。

关键：使用 StaticPool 确保 :memory: 数据库的所有连接共享同一实例。
"""

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session, sessionmaker

# 必须导入所有模型，确保 Base.metadata 中注册了所有表
import app.models.bidding  # noqa: F401
import app.models.organization  # noqa: F401
import app.models.project  # noqa: F401
import app.models.customer  # noqa: F401

from app.db.session import Base, get_db
from app.main import app

# 内存 SQLite 引擎（StaticPool 保证连接复用，避免 :memory: 多实例问题）
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """每个测试函数获得一个独立的数据库会话（所有表已创建）。"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """FastAPI TestClient，注入测试数据库会话。"""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
