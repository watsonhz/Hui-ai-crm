from datetime import datetime
from sqlalchemy import Column, BigInteger, String, SmallInteger, Text, DateTime, ForeignKey
from app.core.database import Base

VISIT_TYPES = {1: "电话", 2: "拜访", 3: "会议", 4: "邮件", 5: "微信"}
OUTCOME_LEVELS = {0: "无产出", 1: "P1产出", 2: "P0产出"}


class CrmRelationship(Base):
    __tablename__ = "crm_relationship"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    customer_id = Column(BigInteger, ForeignKey("organizations.id"), nullable=False)
    contact_id = Column(BigInteger)
    project_id = Column(BigInteger, ForeignKey("projects.id"))
    visit_type = Column(SmallInteger, nullable=False, default=1)
    visit_date = Column(DateTime(timezone=True), nullable=False)
    content = Column(Text)
    outcome_level = Column(SmallInteger, default=0)
    warmth_change = Column(SmallInteger, default=0)  # -2 to +2
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
