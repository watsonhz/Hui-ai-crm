"""投标管理（Bidding）SQLAlchemy 模型 —— 9 阶段状态机 + 软删除。"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

# 九阶段状态常量
BIDDING_STATUSES: tuple[str, ...] = (
    "线索",      # 1: 初始线索
    "商机确认",  # 2: 商机经过确认
    "方案设计",  # 3: 制作投标方案
    "投标中",    # 4: 正在投标/评标中
    "商务谈判",  # 5: 中标后商务谈判
    "中标",      # 6: 成功中标
    "丢标",      # 7: 未能中标
    "项目交付",  # 8: 进入项目交付阶段
    "维保",      # 9: 进入维保服务阶段
)

# 合法的状态转换（当前状态 -> 可到达的状态集合）
ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "线索":     {"商机确认"},
    "商机确认": {"方案设计"},
    "方案设计": {"投标中"},
    "投标中":   {"商务谈判","丢标"},
    "商务谈判": {"中标", "丢标"},
    "中标":     {"项目交付"},
    "丢标":     set(),            # 终态，不可再转换
    "项目交付": {"维保"},
    "维保":     set(),            # 终态，不可再转换
}


class Bidding(Base):
    """投标项目模型 —— 记录从线索到维保全流程的 9 阶段状态机。"""

    __tablename__ = "bidding_projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    project_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="项目名称")
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="客户名称")
    amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0.00, comment="项目金额"
    )
    bid_deadline: Mapped[date] = mapped_column(Date, nullable=False, comment="投标截止日期")
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="线索", comment="当前阶段"
    )
    probability: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="中标概率 0-100")
    competitor_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="竞争对手信息")
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="备注")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, comment="软删除时间"
    )

    __table_args__ = (
        CheckConstraint("probability >= 0 AND probability <= 100", name="ck_bidding_probability_range"),
        CheckConstraint(
            f"status IN ({', '.join(repr(s) for s in BIDDING_STATUSES)})",
            name="ck_bidding_status_valid",
        ),
    )
