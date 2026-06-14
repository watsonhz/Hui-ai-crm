"""Shared test fixtures: SQLite in-memory DB, authenticated client, seed users."""

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.security import create_access_token
from app.models.user import User

# Force SQLite for tests regardless of .env
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci")
os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    eng = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)
    eng.dispose()


@pytest.fixture
def db(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def _seed_user(db, user_id: int, username: str, role: str, password: str = "test123") -> User:
    from passlib.hash import bcrypt
    u = User(id=user_id, username=username, password_hash=bcrypt.hash(password), role=role, is_active=True)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@pytest.fixture
def admin_user(db) -> User:
    return _seed_user(db, 1, "admin", "admin")


@pytest.fixture
def normal_user(db) -> User:
    return _seed_user(db, 2, "user01", "user")


@pytest.fixture
def other_user(db) -> User:
    return _seed_user(db, 3, "user02", "user")


@pytest.fixture
def auth_header(admin_user) -> str:
    token = create_access_token(admin_user.id, admin_user.username, admin_user.role)
    return f"Bearer {token}"


@pytest.fixture
def normal_auth_header(normal_user) -> str:
    token = create_access_token(normal_user.id, normal_user.username, normal_user.role)
    return f"Bearer {token}"


@pytest.fixture
def other_auth_header(other_user) -> str:
    token = create_access_token(other_user.id, other_user.username, other_user.role)
    return f"Bearer {token}"


@pytest.fixture(autouse=True)
def _reset_rate_limiters():
    """Reset shared rate limiters before each test."""
    try:
        from app.core.rate_limit import login_limiter, brute_force
        login_limiter._buckets.clear()
        brute_force._failures.clear()
        brute_force._locked_until.clear()
    except ImportError:
        pass


@pytest.fixture
def client(db):
    from fastapi.testclient import TestClient
    from app.main import app
    from app.core.database import get_db

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
