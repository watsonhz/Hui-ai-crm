from datetime import datetime
<<<<<<< HEAD
from sqlalchemy import Column, BigInteger, String, SmallInteger, DateTime
=======
from sqlalchemy import Integer, Column, BigInteger, String, SmallInteger, DateTime
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from app.core.database import Base

class Role(Base):
    __tablename__ = "sys_role"
<<<<<<< HEAD
    id = Column(BigInteger, primary_key=True, autoincrement=True)
=======
    id = Column(Integer, primary_key=True, autoincrement=True)
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    role_name = Column(String(50), nullable=False, unique=True)
    role_code = Column(String(50), nullable=False, unique=True)
    description = Column(String(200))
    status = Column(SmallInteger, default=1)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class Permission(Base):
    __tablename__ = "sys_permission"
<<<<<<< HEAD
    id = Column(BigInteger, primary_key=True, autoincrement=True)
=======
    id = Column(Integer, primary_key=True, autoincrement=True)
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
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
<<<<<<< HEAD
    id = Column(BigInteger, primary_key=True, autoincrement=True)
=======
    id = Column(Integer, primary_key=True, autoincrement=True)
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    role_id = Column(BigInteger, nullable=False)
    permission_id = Column(BigInteger, nullable=False)
