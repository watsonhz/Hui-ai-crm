from datetime import datetime
from sqlalchemy import Integer, Column, BigInteger, String, SmallInteger, Text, DateTime
from app.core.database import Base

class DictType(Base):
    __tablename__ = "sys_dict_type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dict_name = Column(String(100), nullable=False)
    dict_type = Column(String(100), unique=True, nullable=False)
    status = Column(SmallInteger, default=1)
    remark = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class DictData(Base):
    __tablename__ = "sys_dict_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dict_type = Column(String(100), nullable=False, index=True)
    dict_label = Column(String(100), nullable=False)
    dict_value = Column(String(100), nullable=False)
    sort_order = Column(SmallInteger, default=0)
    status = Column(SmallInteger, default=1)
    remark = Column(String(500))
    css_class = Column(String(100))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
