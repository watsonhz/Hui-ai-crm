from datetime import datetime
<<<<<<< HEAD
from sqlalchemy import Column, BigInteger, String, Text, DateTime
=======
from sqlalchemy import Integer, Column, BigInteger, String, Text, DateTime
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"
<<<<<<< HEAD
    id = Column(BigInteger, primary_key=True, autoincrement=True)
=======
    id = Column(Integer, primary_key=True, autoincrement=True)
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    user_id = Column(BigInteger)
    username = Column(String(50))
    action = Column(String(50), nullable=False)
    resource = Column(String(100))
    detail = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
