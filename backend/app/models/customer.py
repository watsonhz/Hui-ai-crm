from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime, Boolean
from app.core.database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True)
    industry = Column(String(50))
    source = Column(String(50))
    level = Column(String(20), default="normal")
    owner_id = Column(BigInteger)
    contact_name = Column(String(100))
    contact_phone = Column(String(30))
    contact_email = Column(String(100))
    address = Column(String(300))
    remark = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
