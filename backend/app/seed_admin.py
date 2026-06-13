"""Seed script: create initial admin user for development.

Usage:
    cd backend
    python -m app.seed_admin
"""

from passlib.hash import bcrypt
from app.core.database import SessionLocal, init_db
from app.models.user import User


def seed_admin():
    init_db()
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            print("[skip] admin user already exists")
            return

        admin = User(
            username="admin",
            password_hash=bcrypt.hash("Admin@123456"),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print(f"[OK] admin user created (id={admin.id}, username=admin, password=Admin@123456)")
        print("[WARN] 请在生产环境中立即修改默认密码!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_admin()
