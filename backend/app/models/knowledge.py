from datetime import datetime
<<<<<<< HEAD
from sqlalchemy import Column, BigInteger, String, Text, DateTime
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class Knowledge(Base):
    __tablename__ = "knowledge"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
=======
from sqlalchemy import Integer, Column, BigInteger, String, Text, DateTime
from app.core.database import Base

try:
    from pgvector.sqlalchemy import Vector
    EmbeddingColumn = Vector(1536)
except ImportError:
    EmbeddingColumn = Text  # fallback: store embedding as JSON string

class Knowledge(Base):
    __tablename__ = "knowledge"
    id = Column(Integer, primary_key=True, autoincrement=True)
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(String(500))
    source = Column(String(200))
<<<<<<< HEAD
    embedding = Column(Vector(1536))
=======
    embedding = Column(EmbeddingColumn, nullable=True)
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
