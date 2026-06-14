from datetime import datetime
from sqlalchemy import Integer, Column, BigInteger, String, Text, DateTime
from app.core.database import Base

REPORT_TYPES = {"daily": "日报", "weekly": "周报", "monthly": "月报"}


class AiWorkSummary(Base):
    __tablename__ = "ai_work_summary"
    id = Column(Integer, primary_key=True, autoincrement=True)
    report_type = Column(String(20), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    is_edited = Column(Text, default="0")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
