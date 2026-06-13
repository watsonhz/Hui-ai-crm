from datetime import datetime
from sqlalchemy import Column, BigInteger, String, SmallInteger, DateTime
from app.core.database import Base

class Role(Base):
    __tablename__ = "sys_role"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)
    role_code = Column(String(50), nullable=False, unique=True)
    description = Column(String(200))
    status = Column(SmallInteger, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Permission(Base):
    __tablename__ = "sys_permission"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    code = Column(String(100), nullable=False, unique=True)
    parent_id = Column(BigInteger, default=0)
    perm_type = Column(String(20), default="button")  # menu/button/api
    path = Column(String(200))
    icon = Column(String(100))
    sort_order = Column(SmallInteger, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

class RolePermission(Base):
    __tablename__ = "sys_role_permission"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(BigInteger, nullable=False)
    permission_id = Column(BigInteger, nullable=False)
