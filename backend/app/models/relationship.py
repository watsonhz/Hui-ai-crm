from datetime import datetime
from sqlalchemy import Column, BigInteger, String, SmallInteger, Text, DateTime, ForeignKey
from app.core.database import Base

class Relationship(Base):
    __tablename__ = "relationships"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(BigInteger, ForeignKey("organizations.id"), nullable=False)
    contact_name = Column(String(100), nullable=False)
    contact_role = Column(String(50))
    relationship_level = Column(SmallInteger, nullable=False, default=3)
    warmth = Column(SmallInteger, default=0)
    last_contact_date = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
