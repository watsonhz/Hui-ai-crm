from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.response import APIResponse
from app.services.workflow_service import start_approval, get_process_instance, complete_task

router = APIRouter()


class StartRequest(BaseModel):
    process_key: str = Field(..., pattern="^(contract-approval|acceptance-approval|change-approval)$")
    business_key: str = Field(..., min_length=1)
    initiator: str = Field(default="system")
    variables: Optional[dict] = None


class CompleteRequest(BaseModel):
    task_name: str
    assignee: str = "system"
    comment: str = ""


@router.post("/start", response_model=APIResponse[dict])
def start(body: StartRequest):
    record = start_approval(body.process_key, body.business_key, body.initiator, body.variables)
    return APIResponse.success(data=record)


@router.get("/{instance_id}", response_model=APIResponse[dict])
def get_instance(instance_id: str):
    record = get_process_instance(instance_id)
    if not record:
        raise HTTPException(404, "流程实例不存在")
    return APIResponse.success(data=record)


@router.post("/{instance_id}/complete", response_model=APIResponse[dict])
def complete(instance_id: str, body: CompleteRequest):
    record = complete_task(instance_id, body.task_name, body.assignee, body.comment)
    if not record:
        raise HTTPException(404, "流程实例不存在")
    return APIResponse.success(data=record)
