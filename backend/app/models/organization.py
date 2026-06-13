from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates
from app.core.database import Base

ORG_TYPES = {"company", "dept", "team"}

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    parent_id = Column(BigInteger, ForeignKey("organizations.id"))
    org_type = Column(String(20), nullable=False, default="dept")
    description = Column(Text)
    manager_id = Column(BigInteger)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(timezone=True))
    parent = relationship("Organization", remote_side="Organization.id", backref="children")
    @validates("org_type")
    def validate_org_type(self, key, value):
        if value not in ORG_TYPES:
            raise ValueError(f"无效的组织类型: {value}")
        return value
