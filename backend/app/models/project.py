from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Numeric, SmallInteger, Date, Text, DateTime
from sqlalchemy.orm import validates
from app.core.database import Base

STAGE_MAP = {
    1: "线索", 2: "商机", 3: "需求", 4: "方案", 5: "报价", 6: "谈判",
    7: "合同", 8: "交付", 9: "验收", 10: "回款", 11: "运维", 12: "结项",
}
VALID_STAGE_TRANSITIONS = {
    1: {2, 12}, 2: {3, 12}, 3: {4, 12}, 4: {5, 12}, 5: {6, 12},
    6: {7, 12}, 7: {8}, 8: {9}, 9: {10}, 10: {11}, 11: {12}, 12: set(),
}

class Project(Base):
    __tablename__ = "projects"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    stage = Column(SmallInteger, nullable=False, default=1)
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Numeric(15, 2))
    actual_cost = Column(Numeric(15, 2))
    manager_id = Column(BigInteger)
    org_id = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(timezone=True))
    @validates("stage")
    def validate_stage(self, key, value):
        if value not in STAGE_MAP:
            raise ValueError(f"无效的项目阶段: {value}")
        return value
    def can_transition_to(self, target_stage: int) -> bool:
        return target_stage in VALID_STAGE_TRANSITIONS.get(self.stage, set())
