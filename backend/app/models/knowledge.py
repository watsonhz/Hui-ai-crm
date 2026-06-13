from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class Knowledge(Base):
    __tablename__ = "knowledge"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(String(500))
    source = Column(String(200))
    embedding = Column(Vector(1536))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
