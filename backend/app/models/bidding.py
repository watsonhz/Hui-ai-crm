from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Numeric, SmallInteger, Text, DateTime
from sqlalchemy.orm import validates
from app.core.database import Base

BID_STATUS_MAP = {1: "意向", 2: "招标中", 3: "投标中", 4: "评标中", 5: "中标", 6: "失标", 7: "废标", 8: "暂停", 9: "完成"}
VALID_BID_TRANSITIONS = {
    1: {2, 8}, 2: {3, 6, 7, 8}, 3: {4, 6, 7, 8}, 4: {5, 6, 7, 8},
    5: {9}, 6: {9}, 7: {9}, 8: {1, 2, 3, 5, 6, 7}, 9: set(),
}

class Bidding(Base):
    __tablename__ = "bidding"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    project_name = Column(String(200))
    bid_amount = Column(Numeric(15, 2))
    bid_status = Column(SmallInteger, nullable=False, default=1)
    bid_deadline = Column(DateTime(timezone=True))
    submit_deadline = Column(DateTime(timezone=True))
    client_company = Column(String(200))
    client_contact = Column(String(100))
    description = Column(Text)
    notes = Column(Text)
    owner_id = Column(BigInteger)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(timezone=True))
    @validates("bid_status")
    def validate_bid_status(self, key, value):
        if value not in BID_STATUS_MAP:
            raise ValueError(f"无效的投标状态: {value}")
        return value
    def can_transition_to(self, target_status: int) -> bool:
        return target_status in VALID_BID_TRANSITIONS.get(self.bid_status, set())
