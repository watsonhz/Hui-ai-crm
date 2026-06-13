from datetime import datetime
from sqlalchemy import Column, BigInteger, String, SmallInteger, Boolean, Text, DateTime, ForeignKey
from app.core.database import Base

PRIORITY_MAP = {0: "P0紧急", 1: "P1重要", 2: "P2普通"}


class ActionItem(Base):
    __tablename__ = "action_items"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    priority = Column(SmallInteger, nullable=False, default=2)
    is_done = Column(Boolean, default=False)
    due_date = Column(DateTime(timezone=True))
    assignee_id = Column(BigInteger)
    project_id = Column(BigInteger, ForeignKey("projects.id"))
    customer_id = Column(BigInteger, ForeignKey("organizations.id"))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
