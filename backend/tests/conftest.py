"""Shared test fixtures: SQLite in-memory DB, authenticated client, seed users."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.security import create_access_token
from app.models.user import User


TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    """Session-scoped in-memory SQLite engine."""
    eng = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)
    eng.dispose()


@pytest.fixture
def db(engine):
    """Per-test DB session with automatic rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close()


def _seed_user(db, user_id: int, username: str, role: str) -> User:
    """Create a test user in the DB. Returns the User ORM object."""
    u = User(id=user_id, username=username, password_hash="hashed", role=role, is_active=True)
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
    """Bearer token for admin user (role=admin, id=1)."""
    token = create_access_token(admin_user.id, admin_user.username, admin_user.role)
    return f"Bearer {token}"


@pytest.fixture
def normal_auth_header(normal_user) -> str:
    """Bearer token for normal user (role=user, id=2)."""
    token = create_access_token(normal_user.id, normal_user.username, normal_user.role)
    return f"Bearer {token}"


@pytest.fixture
def other_auth_header(other_user) -> str:
    """Bearer token for another normal user (role=user, id=3)."""
    token = create_access_token(other_user.id, other_user.username, other_user.role)
    return f"Bearer {token}"


@pytest.fixture
def client(db):
    """FastAPI TestClient with DB override (no auth override — real JWT flows)."""
    from fastapi.testclient import TestClient
    from app.main import app
    from app.core.database import get_db

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
