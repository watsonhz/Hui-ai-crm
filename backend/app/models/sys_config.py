from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from app.core.database import Base


class SysConfig(Base):
    __tablename__ = "sys_config"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    config_key = Column(String(100), unique=True, nullable=False)
    config_value = Column(Text, nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
