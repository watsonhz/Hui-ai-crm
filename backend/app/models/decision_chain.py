from datetime import datetime
<<<<<<< HEAD
from sqlalchemy import Column, BigInteger, String, SmallInteger, Text, DateTime, ForeignKey
=======
from sqlalchemy import Integer, Column, BigInteger, String, SmallInteger, Text, DateTime, ForeignKey
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from app.core.database import Base

class DecisionChain(Base):
    __tablename__ = "decision_chain"
<<<<<<< HEAD
    id = Column(BigInteger, primary_key=True, autoincrement=True)
=======
    id = Column(Integer, primary_key=True, autoincrement=True)
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False)
    name = Column(String(100), nullable=False)
    role_type = Column(String(50), nullable=False)
    department = Column(String(100))
    weight = Column(SmallInteger, nullable=False, default=5)
    support_level = Column(SmallInteger, nullable=False, default=0)
    contact_frequency = Column(SmallInteger, default=7)
    org_unit = Column(String(100))
    contact_info = Column(String(200))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
