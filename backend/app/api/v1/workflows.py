from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.workflow import (
    WorkflowDefinition, WorkflowInstance, WorkflowTask,
    VALID_WORKFLOW_STATUSES, VALID_TASK_STATUSES,
)
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()


# ── Schemas ──────────────────────────────────────────────────────────────────

class WorkflowDefCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    definition_json: dict = Field(...)
    status: str = Field(default="active", pattern="^(draft|active)$")

class WorkflowDefResponse(BaseModel):
    id: int
    name: str
    status: str
    created_at: datetime
    model_config = {"from_attributes": True}

class InstanceCreate(BaseModel):
    definition_id: int
    title: str = Field(..., min_length=1, max_length=200)
    variables: dict = Field(default_factory=dict)

class InstanceResponse(BaseModel):
    id: int
    definition_id: int
    title: str
    current_stage: str
    status: str
    variables: Optional[dict] = None
    created_by: int
    created_at: datetime
    model_config = {"from_attributes": True}

class TaskResponse(BaseModel):
    id: int
    instance_id: int
    stage_name: str
    assignee_id: int
    status: str
    comment: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    model_config = {"from_attributes": True}

class TaskAction(BaseModel):
    comment: Optional[str] = Field(None, max_length=1000)


# ── Helpers ──────────────────────────────────────────────────────────────────

def _get_definition(db: Session, def_id: int) -> WorkflowDefinition:
    d = db.query(WorkflowDefinition).filter(WorkflowDefinition.id == def_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="工作流定义不存在")
    return d


def _get_instance(db: Session, inst_id: int) -> WorkflowInstance:
    inst = db.query(WorkflowInstance).filter(WorkflowInstance.id == inst_id).first()
    if not inst:
        raise HTTPException(status_code=404, detail="工作流实例不存在")
    return inst


def _current_task(db: Session, inst_id: int) -> Optional[WorkflowTask]:
    return (
        db.query(WorkflowTask)
        .filter(WorkflowTask.instance_id == inst_id, WorkflowTask.status == "pending")
        .first()
    )


def _transition(
    definition_json: dict, current_stage: str, action: str
) -> Optional[str]:
    transitions = definition_json.get("transitions", {})
    stage_trans = transitions.get(current_stage, {})
    return stage_trans.get(action)


def _find_stage_assignee_role(definition_json: dict, stage_name: str) -> Optional[str]:
    for s in definition_json.get("stages", []):
        if s["name"] == stage_name:
            return s.get("assignee_role")
    return None


# ── Workflow Definitions ─────────────────────────────────────────────────────

@router.post("/definitions", response_model=APIResponse[WorkflowDefResponse])
def create_definition(
    body: WorkflowDefCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    wf = WorkflowDefinition(
        name=body.name,
        description=body.description,
        definition_json=body.definition_json,
        created_by=user.id,
        status=body.status,
    )
    db.add(wf)
    db.commit()
    db.refresh(wf)
    return APIResponse.success(data=WorkflowDefResponse.model_validate(wf))


@router.get("/definitions", response_model=APIResponse[PaginatedData[WorkflowDefResponse]])
def list_definitions(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    q = db.query(WorkflowDefinition)
    if status:
        q = q.filter(WorkflowDefinition.status == status)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data=PaginatedData(
        items=[WorkflowDefResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    ))


# ── Workflow Instances ───────────────────────────────────────────────────────

@router.post("/instances", response_model=APIResponse[InstanceResponse])
def start_instance(
    body: InstanceCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    definition = _get_definition(db, body.definition_id)
    if definition.status != "active":
        raise HTTPException(status_code=400, detail="工作流定义未激活")

    stages = definition.definition_json.get("stages", [])
    if not stages:
        raise HTTPException(status_code=400, detail="工作流定义无阶段")

    first_stage = stages[0]["name"]

    inst = WorkflowInstance(
        definition_id=body.definition_id,
        title=body.title,
        current_stage=first_stage,
        variables=body.variables,
        tenant_id=user.id,
        created_by=user.id,
    )
    db.add(inst)
    db.commit()
    db.refresh(inst)

    # Create first task — assigned to creator by default
    first_assignee_role = stages[0].get("assignee_role", "user")
    task = WorkflowTask(
        instance_id=inst.id,
        stage_name=first_stage,
        assignee_id=user.id,  # first stage assigned to initiator
    )
    db.add(task)
    db.commit()

    return APIResponse.success(data=InstanceResponse.model_validate(inst))


@router.get("/instances", response_model=APIResponse[PaginatedData[InstanceResponse]])
def list_instances(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    q = db.query(WorkflowInstance).filter(WorkflowInstance.tenant_id == user.id)
    if status:
        q = q.filter(WorkflowInstance.status == status)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data=PaginatedData(
        items=[InstanceResponse.model_validate(i) for i in items],
        total=total, page=page, page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    ))


@router.get("/instances/{instance_id}", response_model=APIResponse[InstanceResponse])
def get_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    inst = _get_instance(db, instance_id)
    if inst.tenant_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="无权查看此工作流实例")
    return APIResponse.success(data=InstanceResponse.model_validate(inst))


# ── Approval Actions ─────────────────────────────────────────────────────────

def _do_transition(
    db: Session,
    inst: WorkflowInstance,
    definition: WorkflowDefinition,
    task: WorkflowTask,
    action: str,
    comment: Optional[str],
    user: CurrentUser,
) -> WorkflowInstance:
    """Execute a workflow transition (approve/reject)."""
    # Authorization: only assignee or admin can act
    if task.assignee_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="无权执行此审批操作")

    # Execute transition
    next_stage = _transition(definition.definition_json, inst.current_stage, action)

    # Complete current task
    task.status = "approved" if action == "approve" else "rejected"
    task.comment = comment
    task.completed_at = datetime.now(timezone.utc)
    db.commit()

    if next_stage is None:
        # Terminal: approve → completed, reject → rejected
        inst.status = "approved" if action == "approve" else "rejected"
        inst.current_stage = inst.current_stage  # stays on final stage
        db.commit()
        db.refresh(inst)
        return inst

    # Move to next stage
    inst.current_stage = next_stage
    inst.status = "active"
    db.commit()

    # Create next task
    assignee_role = _find_stage_assignee_role(definition.definition_json, next_stage)
    # If assignee_role is "admin", assign to admin (id=1); otherwise assign to initiator
    next_assignee = 1 if assignee_role == "admin" else inst.created_by

    new_task = WorkflowTask(
        instance_id=inst.id,
        stage_name=next_stage,
        assignee_id=next_assignee,
    )
    db.add(new_task)
    db.commit()
    db.refresh(inst)

    return inst


@router.post("/instances/{instance_id}/approve", response_model=APIResponse[InstanceResponse])
def approve(
    instance_id: int,
    body: TaskAction = TaskAction(),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    inst = _get_instance(db, instance_id)
    if inst.status != "active":
        raise HTTPException(status_code=400, detail="工作流已结束")

    task = _current_task(db, instance_id)
    if not task:
        raise HTTPException(status_code=400, detail="无待处理任务")

    definition = _get_definition(db, inst.definition_id)
    inst = _do_transition(db, inst, definition, task, "approve", body.comment, user)
    return APIResponse.success(data=InstanceResponse.model_validate(inst))


@router.post("/instances/{instance_id}/reject", response_model=APIResponse[InstanceResponse])
def reject(
    instance_id: int,
    body: TaskAction = TaskAction(),
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    inst = _get_instance(db, instance_id)
    if inst.status != "active":
        raise HTTPException(status_code=400, detail="工作流已结束")

    task = _current_task(db, instance_id)
    if not task:
        raise HTTPException(status_code=400, detail="无待处理任务")

    definition = _get_definition(db, inst.definition_id)
    inst = _do_transition(db, inst, definition, task, "reject", body.comment, user)
    return APIResponse.success(data=InstanceResponse.model_validate(inst))


@router.get("/instances/{instance_id}/tasks", response_model=APIResponse[list[TaskResponse]])
def get_tasks(
    instance_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    inst = _get_instance(db, instance_id)
    if inst.tenant_id != user.id and user.role != "admin":
        raise HTTPException(status_code=403, detail="无权查看")
    tasks = (
        db.query(WorkflowTask)
        .filter(WorkflowTask.instance_id == instance_id)
        .order_by(WorkflowTask.created_at)
        .all()
    )
    return APIResponse.success(data=[TaskResponse.model_validate(t) for t in tasks])
