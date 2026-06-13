"""Flowable BPM 工作流服务 — 审批流 / 拜访阶段流转"""
from datetime import datetime, timezone
from typing import Optional

WORKFLOW_STORE: dict[str, dict] = {}  # 内存存储，生产环境应替换为 Flowable REST API 调用


def start_approval(process_key: str, business_key: str, initiator: str, variables: dict = None) -> dict:
    instance_id = f"{process_key}-{business_key}-{datetime.now(timezone.utc).timestamp():.0f}"
    record = {
        "instance_id": instance_id,
        "process_key": process_key,
        "business_key": business_key,
        "status": "running",
        "initiator": initiator,
        "variables": variables or {},
        "tasks": _get_initial_tasks(process_key),
        "started_at": datetime.now(timezone.utc).isoformat(),
    }
    WORKFLOW_STORE[instance_id] = record
    return record


def get_process_instance(instance_id: str) -> Optional[dict]:
    return WORKFLOW_STORE.get(instance_id)


def complete_task(instance_id: str, task_name: str, assignee: str, comment: str = "") -> Optional[dict]:
    record = WORKFLOW_STORE.get(instance_id)
    if not record:
        return None
    remaining = [t for t in record.get("tasks", []) if t["name"] != task_name or t.get("status") != "pending"]
    if len(remaining) == 0:
        record["status"] = "completed"
        record["completed_at"] = datetime.now(timezone.utc).isoformat()
    record["tasks"] = remaining
    return record


def _get_initial_tasks(process_key: str) -> list[dict]:
    templates = {
        "contract-approval": [
            {"name": "sales_submit", "label": "销售提交", "assignee": "sales"},
            {"name": "manager_review", "label": "经理审核", "assignee": "manager"},
            {"name": "finance_approve", "label": "财务审批", "assignee": "finance"},
            {"name": "ceo_approve", "label": "CEO终审", "assignee": "admin"},
        ],
        "acceptance-approval": [
            {"name": "pm_submit", "label": "项目经理提交", "assignee": "pm"},
            {"name": "customer_confirm", "label": "客户确认", "assignee": "customer"},
            {"name": "qa_verify", "label": "QA验证", "assignee": "qa"},
        ],
        "change-approval": [
            {"name": "change_request", "label": "变更申请", "assignee": "requester"},
            {"name": "impact_assess", "label": "影响评估", "assignee": "pm"},
            {"name": "approve", "label": "审批", "assignee": "manager"},
        ],
    }
    return templates.get(process_key, [{"name": "approve", "label": "审批", "assignee": "manager"}])
