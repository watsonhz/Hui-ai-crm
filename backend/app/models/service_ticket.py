from datetime import datetime, timedelta
from sqlalchemy import Column, BigInteger, String, SmallInteger, Text, DateTime, ForeignKey, Boolean
from app.core.database import Base

class ServiceTicket(Base):
    __tablename__ = "service_tickets"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    customer_id = Column(BigInteger, ForeignKey("organizations.id"))
    status = Column(SmallInteger, nullable=False, default=1)  # 1=待处理 2=处理中 3=已解决 4=已关闭
    priority = Column(SmallInteger, default=2)  # 0=紧急 1=高 2=中 3=低
    assignee_id = Column(BigInteger)
    customer_level = Column(String(20), default="normal")  # vip/key/normal
    sla_response_hours = Column(SmallInteger, default=8)
    sla_resolve_hours = Column(SmallInteger, default=72)
    response_deadline = Column(DateTime(timezone=True))
    resolve_deadline = Column(DateTime(timezone=True))
    is_overdue = Column(Boolean, default=False)
    resolution = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
