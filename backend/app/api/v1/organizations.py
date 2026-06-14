from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, CurrentUser
from app.models.organization import Organization
from app.schemas.organization import (
    OrganizationCreate, OrganizationUpdate,
    OrganizationResponse, OrganizationTreeNode,
)
from app.schemas.response import APIResponse

router = APIRouter()


def _check_circular_ref(db: Session, org_id: int, target_parent_id: int) -> bool:
    """Check if setting parent to target_parent_id would create a cycle."""
    if org_id == target_parent_id:
        return True
    visited = {org_id}
    current_id = target_parent_id
    while current_id is not None:
        if current_id in visited:
            return True
        visited.add(current_id)
        org = db.query(Organization).filter(
            Organization.id == current_id, Organization.deleted_at.is_(None)
        ).first()
        current_id = org.parent_id if org else None
    return False


@router.post("/", response_model=APIResponse[OrganizationResponse])
<<<<<<< HEAD
def create(body: OrganizationCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
=======
def create_org(body: OrganizationCreate, db: Session = Depends(get_db)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    if body.parent_id is not None:
        parent = db.query(Organization).filter(
            Organization.id == body.parent_id, Organization.deleted_at.is_(None)
        ).first()
        if not parent:
            raise HTTPException(status_code=400, detail="父级组织不存在")
    org = Organization(**body.model_dump())
    db.add(org)
    db.commit()
    db.refresh(org)
    return APIResponse.success(data=OrganizationResponse.model_validate(org))


<<<<<<< HEAD
@router.get("/tree", response_model=APIResponse)
def tree(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
=======
@router.get("/tree", response_model=APIResponse[list[OrganizationTreeNode]])
def get_tree(db: Session = Depends(get_db)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    orgs = (
        db.query(Organization)
        .filter(Organization.deleted_at.is_(None))
        .order_by(Organization.sort_order)
        .all()
    )
    org_map: dict[int, OrganizationTreeNode] = {}
    roots: list[OrganizationTreeNode] = []
    for o in orgs:
        node = OrganizationTreeNode(
            id=o.id, name=o.name, org_type=o.org_type,
            parent_id=o.parent_id, sort_order=o.sort_order,
        )
        org_map[o.id] = node
    for o in orgs:
        node = org_map[o.id]
        if o.parent_id is not None and o.parent_id in org_map:
            org_map[o.parent_id].children.append(node)
        else:
            roots.append(node)
    return APIResponse.success(data=roots)


@router.put("/{org_id}", response_model=APIResponse[OrganizationResponse])
<<<<<<< HEAD
def update(org_id: int, body: OrganizationUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
=======
def update_org(org_id: int, body: OrganizationUpdate, db: Session = Depends(get_db)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    org = db.query(Organization).filter(
        Organization.id == org_id, Organization.deleted_at.is_(None)
    ).first()
    if not org:
        raise HTTPException(status_code=404, detail="组织不存在")
    if body.parent_id is not None:
        if body.parent_id == org_id:
            raise HTTPException(status_code=400, detail="不能将自身设为父级")
        parent = db.query(Organization).filter(
            Organization.id == body.parent_id, Organization.deleted_at.is_(None)
        ).first()
        if not parent:
            raise HTTPException(status_code=400, detail="父级组织不存在")
        if _check_circular_ref(db, org_id, body.parent_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="不能设为此父级组织，会形成循环引用",
            )
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(org, k, v)
    org.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(org)
    return APIResponse.success(data=OrganizationResponse.model_validate(org))


@router.delete("/{org_id}", response_model=APIResponse[None])
<<<<<<< HEAD
def delete(org_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
=======
def delete_org(org_id: int, db: Session = Depends(get_db)):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    org = db.query(Organization).filter(
        Organization.id == org_id, Organization.deleted_at.is_(None)
    ).first()
    if not org:
        raise HTTPException(status_code=404, detail="组织不存在")
    children = db.query(Organization).filter(
        Organization.parent_id == org_id, Organization.deleted_at.is_(None)
    ).count()
    if children > 0:
        raise HTTPException(status_code=400, detail="存在子组织，无法删除")
    org.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return APIResponse.success(message="删除成功")
