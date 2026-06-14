<<<<<<< HEAD
"""User model for authentication and ownership."""

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, Integer
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")  # admin / user / readonly
=======
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100))
    full_name = Column(String(100))
    role = Column(String(20), nullable=False, default="sales")
    department_id = Column(BigInteger)
    org_id = Column(BigInteger)
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
