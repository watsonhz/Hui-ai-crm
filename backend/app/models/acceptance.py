from datetime import datetime, date
from sqlalchemy import Integer, Column, BigInteger, String, Date, SmallInteger, Text, DateTime, ForeignKey
from app.core.database import Base

class Acceptance(Base):
    __tablename__ = "acceptance"
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False)
    title = Column(String(200), nullable=False)
    acceptance_date = Column(Date)
    status = Column(SmallInteger, nullable=False, default=1)
    result = Column(Text)
    reviewer = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
