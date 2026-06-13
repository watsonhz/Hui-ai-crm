"""BPM Workflow Engine models — JSON-defined workflows, no XML (XXE-safe)."""

from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, JSON
from sqlalchemy.orm import validates
from app.core.database import Base

VALID_WORKFLOW_STATUSES = {"draft", "active", "archived"}
VALID_TASK_STATUSES = {"pending", "approved", "rejected", "withdrawn"}


class WorkflowDefinition(Base):
    __tablename__ = "workflow_definitions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    definition_json = Column(JSON, nullable=False)
    """
    Example definition_json:
    {
      "stages": [
        {"name": "提交申请", "assignee_role": "user", "order": 1},
        {"name": "部门审批", "assignee_role": "dept_manager", "order": 2},
        {"name": "财务审批", "assignee_role": "finance", "order": 3},
        {"name": "总经理审批", "assignee_role": "admin", "order": 4}
      ],
      "transitions": {
        "提交申请":    {"approve": "部门审批", "reject": null},
        "部门审批":    {"approve": "财务审批", "reject": "提交申请"},
        "财务审批":    {"approve": "总经理审批", "reject": "部门审批"},
        "总经理审批":  {"approve": null, "reject": "财务审批"}
      }
    }
    """
    status = Column(String(20), nullable=False, default="draft")
    created_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    @validates("status")
    def validate_status(self, key, value):
        if value not in VALID_WORKFLOW_STATUSES:
            raise ValueError(f"Invalid status: {value}")
        return value

    @validates("definition_json")
    def validate_definition(self, key, value):
        """Ensure definition has required fields."""
        if not isinstance(value, dict):
            raise ValueError("definition_json must be a dict")
        if "stages" not in value or not isinstance(value["stages"], list):
            raise ValueError("definition_json must contain 'stages' list")
        if len(value["stages"]) < 2:
            raise ValueError("Workflow must have at least 2 stages")
        stage_names = {s["name"] for s in value["stages"] if "name" in s}
        transitions = value.get("transitions", {})
        for stage_name, trans in transitions.items():
            if stage_name not in stage_names:
                raise ValueError(f"Transition references unknown stage: {stage_name}")
            if "approve" in trans and trans["approve"] and trans["approve"] not in stage_names:
                raise ValueError(f"approve target not in stages: {trans['approve']}")
            if "reject" in trans and trans["reject"] and trans["reject"] not in stage_names:
                raise ValueError(f"reject target not in stages: {trans['reject']}")
        return value


class WorkflowInstance(Base):
    __tablename__ = "workflow_instances"

    id = Column(Integer, primary_key=True, autoincrement=True)
    definition_id = Column(BigInteger, nullable=False)
    title = Column(String(200), nullable=False)
    current_stage = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, default="active")  # active/approved/rejected
    variables = Column(JSON)
    """Process variables: {key: value} — scoped to this instance only."""
    tenant_id = Column(BigInteger, nullable=False)
    created_by = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    instance_id = Column(BigInteger, nullable=False)
    stage_name = Column(String(100), nullable=False)
    assignee_id = Column(BigInteger, nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime(timezone=True))
