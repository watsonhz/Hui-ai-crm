from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

class TestSecurity:
    def test_hash_verify(self):
        pw = "test123"
        hashed = hash_password(pw)
        assert verify_password(pw, hashed) is True
        assert verify_password("wrong", hashed) is False

    def test_create_token(self):
        token = create_access_token({"sub": "1"})
        assert token is not None
        assert len(token) > 20

class TestAuthAPI:
    def test_register(self, client):
        resp = client.post("/api/v1/auth/register", json={"username": "newuser", "password": "pass123", "full_name": "New User"})
        assert resp.status_code == 200
        assert resp.json()["data"]["username"] == "newuser"

    def test_register_duplicate(self, client):
        client.post("/api/v1/auth/register", json={"username": "dup", "password": "pass123"})
        resp = client.post("/api/v1/auth/register", json={"username": "dup", "password": "pass123"})
        assert resp.status_code == 400

    def test_login_success(self, client):
        client.post("/api/v1/auth/register", json={"username": "loginuser", "password": "pass123"})
        resp = client.post("/api/v1/auth/login", json={"username": "loginuser", "password": "pass123"})
        assert resp.status_code == 200
        assert "access_token" in resp.json()["data"]

    def test_login_wrong_password(self, client):
        client.post("/api/v1/auth/register", json={"username": "pwuser", "password": "correct"})
        resp = client.post("/api/v1/auth/login", json={"username": "pwuser", "password": "wrong"})
        assert resp.status_code == 401

    def test_me_authorized(self, client):
        client.post("/api/v1/auth/register", json={"username": "meuser", "password": "pass123"})
        token = client.post("/api/v1/auth/login", json={"username": "meuser", "password": "pass123"}).json()["data"]["access_token"]
        resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert resp.json()["data"]["username"] == "meuser"

    def test_me_unauthorized(self, client):
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

class TestUserModel:
    def test_create_user(self, db):
        u = User(username="modeluser", password_hash=hash_password("pw"), role="admin")
        db.add(u)
        db.commit()
        assert u.id is not None
        assert u.role == "admin"
        assert u.is_active is True
