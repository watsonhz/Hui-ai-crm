from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger)
    username = Column(String(50))
    action = Column(String(50), nullable=False)
    resource = Column(String(100))
    detail = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
