"""Shared test fixtures: SQLite in-memory DB, authenticated client, seed users."""

<<<<<<< HEAD
=======
import os
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base
from app.core.security import create_access_token
from app.models.user import User

<<<<<<< HEAD

@pytest.fixture(autouse=True)
def _reset_rate_limiters():
    """Reset shared rate limiters before each test to prevent cross-test interference."""
    from app.core.rate_limit import login_limiter, brute_force
    login_limiter._buckets.clear()
    brute_force._failures.clear()
    brute_force._locked_until.clear()

=======
# Force SQLite for tests regardless of .env
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-ci")
os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
<<<<<<< HEAD
    """Session-scoped in-memory SQLite engine."""
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
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


def _seed_user(db, user_id: int, username: str, role: str, password: str = "test123") -> User:
<<<<<<< HEAD
    """Create a test user in the DB. Returns the User ORM object."""
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
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
<<<<<<< HEAD
    """Bearer token for admin user (role=admin, id=1)."""
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    token = create_access_token(admin_user.id, admin_user.username, admin_user.role)
    return f"Bearer {token}"


@pytest.fixture
def normal_auth_header(normal_user) -> str:
<<<<<<< HEAD
    """Bearer token for normal user (role=user, id=2)."""
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    token = create_access_token(normal_user.id, normal_user.username, normal_user.role)
    return f"Bearer {token}"


@pytest.fixture
def other_auth_header(other_user) -> str:
<<<<<<< HEAD
    """Bearer token for another normal user (role=user, id=3)."""
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    token = create_access_token(other_user.id, other_user.username, other_user.role)
    return f"Bearer {token}"


<<<<<<< HEAD
=======
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


>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
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
