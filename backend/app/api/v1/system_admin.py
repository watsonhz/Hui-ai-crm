from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.core.security import hash_password
from app.models.user import User
from app.models.permission import Role, Permission, RolePermission
from app.models.audit_log import AuditLog
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=4)
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str = Field(default="sales")


class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class RoleCreate(BaseModel):
    role_name: str = Field(..., max_length=50)
    role_code: str = Field(..., max_length=50)
    description: Optional[str] = None


class RoleAssignRequest(BaseModel):
    role_id: int
    permission_ids: list[int]


# ── 用户管理 ──
@router.get("/users", response_model=APIResponse[dict])
def list_users(page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=100),
               search: Optional[str] = None, role: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(User).order_by(User.created_at.desc())
    if search:
        q = q.filter(User.username.ilike(f"%{search}%"))
    if role:
        q = q.filter(User.role == role)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data={"items": [{"id": u.id, "username": u.username, "email": u.email, "full_name": u.full_name, "role": u.role, "is_active": u.is_active, "created_at": u.created_at.isoformat()} for u in items], "total": total, "page": page, "page_size": page_size})


@router.post("/users", response_model=APIResponse[dict])
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(400, "用户名已存在")
    u = User(username=body.username, password_hash=hash_password(body.password), email=body.email, full_name=body.full_name, role=body.role)
    db.add(u); db.commit(); db.refresh(u)
    _log(db, u.id, body.username, "user.create", f"创建用户 {u.username}")
    return APIResponse.success(data={"id": u.id, "username": u.username, "role": u.role})


@router.put("/users/{user_id}", response_model=APIResponse[dict])
def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(404, "用户不存在")
    for k, v in body.model_dump(exclude_unset=True).items():
        setattr(u, k, v)
    db.commit()
    return APIResponse.success(data={"id": u.id, "username": u.username, "is_active": u.is_active})


@router.delete("/users/{user_id}", response_model=APIResponse[None])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u:
        raise HTTPException(404)
    u.is_active = False; db.commit()
    return APIResponse.success(message="已禁用")


# ── 角色管理 ──
@router.get("/roles", response_model=APIResponse[list])
def list_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).order_by(Role.created_at).all()
    return APIResponse.success(data=[{"id": r.id, "role_name": r.role_name, "role_code": r.role_code, "description": r.description, "status": r.status} for r in roles])


@router.post("/roles", response_model=APIResponse[dict])
def create_role(body: RoleCreate, db: Session = Depends(get_db)):
    r = Role(**body.model_dump())
    db.add(r); db.commit(); db.refresh(r)
    return APIResponse.success(data={"id": r.id, "role_name": r.role_name})


@router.put("/roles/{role_id}/permissions", response_model=APIResponse[dict])
def assign_permissions(role_id: int, body: RoleAssignRequest, db: Session = Depends(get_db)):
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
    for pid in body.permission_ids:
        db.add(RolePermission(role_id=role_id, permission_id=pid))
    db.commit()
    return APIResponse.success(data={"role_id": role_id, "assigned_count": len(body.permission_ids)})


# ── 权限管理 ──
@router.get("/permissions", response_model=APIResponse[list])
def list_permissions(db: Session = Depends(get_db)):
    perms = db.query(Permission).order_by(Permission.sort_order).all()
    return APIResponse.success(data=[{"id": p.id, "name": p.name, "code": p.code, "parent_id": p.parent_id, "perm_type": p.perm_type, "path": p.path, "icon": p.icon} for p in perms])


# ── 操作日志 ──
@router.get("/audit-logs", response_model=APIResponse[dict])
def list_audit_logs(page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=100),
                    user_id: Optional[int] = None, action: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(AuditLog).order_by(AuditLog.created_at.desc())
    if user_id:
        q = q.filter(AuditLog.user_id == user_id)
    if action:
        q = q.filter(AuditLog.action == action)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data={"items": [{"id": a.id, "user_id": a.user_id, "username": a.username, "action": a.action, "resource": a.resource, "detail": a.detail, "created_at": a.created_at.isoformat()} for a in items], "total": total, "page": page, "page_size": page_size})


def _log(db: Session, user_id: int, username: str, action: str, detail: str = "", resource: str = ""):
    db.add(AuditLog(user_id=user_id, username=username, action=action, resource=resource, detail=detail))
    db.commit()
