from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.decision_chain import DecisionChain
from app.schemas.decision_chain import DecisionChainCreate, DecisionChainUpdate, DecisionChainResponse
from app.schemas.response import APIResponse

router = APIRouter()

@router.post("/", response_model=APIResponse[DecisionChainResponse])
def create_decision_chain(body: DecisionChainCreate, db: Session = Depends(get_db)):
    dc = DecisionChain(**body.model_dump())
    db.add(dc)
    db.commit()
    db.refresh(dc)
    return APIResponse.success(data=DecisionChainResponse.model_validate(dc))

@router.get("/project/{project_id}", response_model=APIResponse[list[DecisionChainResponse]])
def list_by_project(project_id: int, db: Session = Depends(get_db)):
    items = db.query(DecisionChain).filter(DecisionChain.project_id == project_id).order_by(DecisionChain.weight.desc()).all()
    return APIResponse.success(data=[DecisionChainResponse.model_validate(i) for i in items])

@router.put("/{dc_id}", response_model=APIResponse[DecisionChainResponse])
def update_decision_chain(dc_id: int, body: DecisionChainUpdate, db: Session = Depends(get_db)):
    dc = db.query(DecisionChain).filter(DecisionChain.id == dc_id).first()
    if not dc:
        raise HTTPException(status_code=404, detail="记录不存在")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(dc, k, v)
    dc.updated_at = __import__('datetime').datetime.now(__import__('datetime').timezone.utc)
    db.commit()
    db.refresh(dc)
    return APIResponse.success(data=DecisionChainResponse.model_validate(dc))

@router.get("/project/{project_id}/graph", response_model=APIResponse[dict])
def get_decision_graph(project_id: int, db: Session = Depends(get_db)):
    nodes = db.query(DecisionChain).filter(DecisionChain.project_id == project_id).order_by(DecisionChain.weight.desc()).all()
    n = [{"id": dc.id, "name": dc.name, "role": dc.role_type, "weight": dc.weight, "support": dc.support_level, "dept": dc.department, "org_unit": dc.org_unit} for dc in nodes]
    edges = []
    for i, a in enumerate(n):
        for j, b in enumerate(n):
            if i < j and a.get("org_unit") and b.get("org_unit") and a["org_unit"] == b["org_unit"]:
                edges.append({"source": a["id"], "target": b["id"], "label": a["org_unit"]})
    return APIResponse.success(data={"nodes": n, "edges": edges})


@router.get("/project/{project_id}/gap", response_model=APIResponse[dict])
def detect_decision_gap(project_id: int, db: Session = Depends(get_db)):
    nodes = db.query(DecisionChain).filter(DecisionChain.project_id == project_id).all()
    existing_roles = {n.role_type for n in nodes}
    required_roles = {"经济决策者", "技术决策者", "使用者", "影响者", "守门人", "教练", "审批者", "执行者"}
    missing = list(required_roles - existing_roles)
    total_weight = sum(n.weight for n in nodes)
    avg_support = sum(n.support_level for n in nodes) / len(nodes) if nodes else 0
    return APIResponse.success(data={
        "project_id": project_id,
        "total_nodes": len(nodes),
        "total_weight": total_weight,
        "avg_support": round(avg_support, 1),
        "existing_roles": list(existing_roles),
        "missing_roles": missing,
        "has_gap": len(missing) > 0,
        "weak_links": [{"id": n.id, "name": n.name, "weight": n.weight} for n in nodes if n.weight < 3],
    })


@router.delete("/{dc_id}", response_model=APIResponse[None])
def delete_decision_chain(dc_id: int, db: Session = Depends(get_db)):
    dc = db.query(DecisionChain).filter(DecisionChain.id == dc_id).first()
    if not dc:
        raise HTTPException(status_code=404)
    db.delete(dc)
    db.commit()
    return APIResponse.success(message="删除成功")
