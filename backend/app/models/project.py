"""项目管理（Project）SQLAlchemy 模型 —— 12 阶段 + 软删除。"""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, DateTime, Integer, Numeric, String, Text, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base

# 十二阶段常量（按流程顺序）
PROJECT_STAGES: tuple[str, ...] = (
    "初步接洽",
    "需求分析",
    "方案演示",
    "报价",
    "商务谈判",
    "合同签订",
    "项目启动",
    "设计开发",
    "测试验收",
    "上线部署",
    "项目交付",
    "维保服务",
)

# 阶段序号映射，用于验证前进方向
STAGE_INDEX: dict[str, int] = {stage: i for i, stage in enumerate(PROJECT_STAGES)}


class Project(Base):
    """项目模型 —— 追踪从初步接洽到维保服务的 12 阶段全流程。"""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    project_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="项目名称")
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="客户名称")
    pm_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="项目经理")
    stage: Mapped[str] = mapped_column(
        String(20), nullable=False, default="初步接洽", comment="当前阶段"
    )
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="整体进度 0-100")
    start_date: Mapped[date] = mapped_column(Date, nullable=False, comment="开始日期")
    expected_end_date: Mapped[date] = mapped_column(Date, nullable=False, comment="预计结束日期")
    actual_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment="实际结束日期")
    amount: Mapped[Decimal] = mapped_column(
        Numeric(15, 2), nullable=False, default=0.00, comment="项目金额"
    )
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
        CheckConstraint("progress >= 0 AND progress <= 100", name="ck_project_progress_range"),
        CheckConstraint(
            f"stage IN ({', '.join(repr(s) for s in PROJECT_STAGES)})",
            name="ck_project_stage_valid",
        ),
    )
