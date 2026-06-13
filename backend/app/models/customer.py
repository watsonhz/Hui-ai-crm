"""Customer model for CRM core entity."""

from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from sqlalchemy.orm import validates
from app.core.database import Base

VALID_LEVELS = {"A", "B", "C", "D"}
VALID_STATUSES = {"潜在", "意向", "谈判", "成交", "流失"}


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    company = Column(String(200))
    industry = Column(String(50))
    phone = Column(String(20))
    email = Column(String(100))
    source = Column(String(50))
    level = Column(String(10), default="C")
    status = Column(String(20), default="潜在")
    owner_id = Column(BigInteger)
    deleted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @validates("level")
    def validate_level(self, key, value):
        if value and value not in VALID_LEVELS:
            raise ValueError(f"无效的客户等级: {value}，有效值: {VALID_LEVELS}")
        return value

    @validates("status")
    def validate_status(self, key, value):
        if value and value not in VALID_STATUSES:
            raise ValueError(f"无效的客户状态: {value}，有效值: {VALID_STATUSES}")
        return value
