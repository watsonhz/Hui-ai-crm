from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.core.database import get_db
from app.core.security import hash_password, get_current_user, CurrentUser
from app.models.user import User
from app.models.permission import Role, Permission, RolePermission
from app.models.audit_log import AuditLog
from app.models.organization import Organization
from app.schemas.response import APIResponse, PaginatedData

router = APIRouter()


class UserCreate(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=8)
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: str = Field(default="sales")
    department_id: Optional[int] = None
    org_id: Optional[int] = None


class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    department_id: Optional[int] = None
    org_id: Optional[int] = None


class DepartmentCreate(BaseModel):
    name: str = Field(..., max_length=200)
    parent_id: Optional[int] = None
    description: Optional[str] = None
    manager_id: Optional[int] = None
    sort_order: int = Field(default=0)


class TeamMemberAdd(BaseModel):
    org_id: int
    username: str
    password: str = Field(default="123456")
    full_name: Optional[str] = None
    role: str = Field(default="sales")


class RoleCreate(BaseModel):
    role_name: str = Field(..., max_length=50)
    role_code: str = Field(..., max_length=50)
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    role_name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: Optional[int] = None


class RoleAssignRequest(BaseModel):
    role_id: int
    permission_ids: list[int]


class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    sort_order: Optional[int] = None
    path: Optional[str] = None


def _log(db: Session, user_id: int, username: str, action: str, detail: str = "", resource: str = ""):
    db.add(AuditLog(user_id=user_id, username=username, action=action, resource=resource, detail=detail))
    db.commit()


# ── 用户管理 ──
@router.get("/users", response_model=APIResponse[dict])
def list_users(page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=100),
               search: Optional[str] = None, role: Optional[str] = None, db: Session = Depends(get_db),
               user: CurrentUser = Depends(get_current_user)):
    q = db.query(User).order_by(User.created_at.desc())
    if search: q = q.filter(User.username.ilike(f"%{search}%"))
    if role: q = q.filter(User.role == role)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data={"items": [{"id": u.id, "username": u.username, "email": u.email, "full_name": u.full_name, "role": u.role, "is_active": u.is_active, "created_at": u.created_at.isoformat()} for u in items], "total": total, "page": page, "page_size": page_size})


@router.post("/users", response_model=APIResponse[dict])
def create_user(body: UserCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(400, "用户名已存在")
    u = User(username=body.username, password_hash=hash_password(body.password), email=body.email, full_name=body.full_name, role=body.role)
    db.add(u); db.commit(); db.refresh(u)
    _log(db, user.id, user.username, "user.create", f"创建用户 {u.username}")
    return APIResponse.success(data={"id": u.id, "username": u.username, "role": u.role})


@router.put("/users/{user_id}", response_model=APIResponse[dict])
def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u: raise HTTPException(404, "用户不存在")
    for k, v in body.model_dump(exclude_unset=True).items(): setattr(u, k, v)
    db.commit()
    return APIResponse.success(data={"id": u.id, "username": u.username, "is_active": u.is_active})


@router.delete("/users/{user_id}", response_model=APIResponse[None])
def delete_user(user_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    u = db.query(User).filter(User.id == user_id).first()
    if not u: raise HTTPException(404)
    u.is_active = False; db.commit()
    return APIResponse.success(message="已禁用")


# ── 角色管理 ──
@router.get("/roles", response_model=APIResponse[list])
def list_roles(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    roles = db.query(Role).order_by(Role.created_at).all()
    return APIResponse.success(data=[{"id": r.id, "role_name": r.role_name, "role_code": r.role_code, "description": r.description, "status": r.status} for r in roles])


@router.post("/roles", response_model=APIResponse[dict])
def create_role(body: RoleCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    r = Role(**body.model_dump())
    db.add(r); db.commit(); db.refresh(r)
    return APIResponse.success(data={"id": r.id, "role_name": r.role_name})


@router.put("/roles/{role_id}", response_model=APIResponse[dict])
def update_role(role_id: int, body: RoleUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    r = db.query(Role).filter(Role.id == role_id).first()
    if not r: raise HTTPException(404, "角色不存在")
    for k, v in body.model_dump(exclude_unset=True).items(): setattr(r, k, v)
    db.commit()
    return APIResponse.success(data={"id": r.id, "role_name": r.role_name})


@router.delete("/roles/{role_id}", response_model=APIResponse[None])
def delete_role(role_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    r = db.query(Role).filter(Role.id == role_id).first()
    if not r: raise HTTPException(404)
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
    db.delete(r); db.commit()
    return APIResponse.success(message="已删除")


@router.put("/roles/{role_id}/permissions", response_model=APIResponse[dict])
def assign_permissions(role_id: int, body: RoleAssignRequest, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
    for pid in body.permission_ids: db.add(RolePermission(role_id=role_id, permission_id=pid))
    db.commit()
    return APIResponse.success(data={"role_id": role_id, "assigned_count": len(body.permission_ids)})


@router.get("/roles/{role_id}/permissions", response_model=APIResponse[list])
def get_role_permissions(role_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    rps = db.query(RolePermission).filter(RolePermission.role_id == role_id).all()
    perm_ids = [rp.permission_id for rp in rps]
    perms = db.query(Permission).filter(Permission.id.in_(perm_ids)).all() if perm_ids else []
    return APIResponse.success(data=[{"id": p.id, "name": p.name, "code": p.code} for p in perms])


# ── 权限管理 ──
@router.get("/permissions", response_model=APIResponse[list])
def list_permissions(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    perms = db.query(Permission).order_by(Permission.sort_order).all()
    return APIResponse.success(data=[{"id": p.id, "name": p.name, "code": p.code, "parent_id": p.parent_id, "perm_type": p.perm_type, "path": p.path, "icon": p.icon} for p in perms])


@router.put("/permissions/{perm_id}", response_model=APIResponse[dict])
def update_permission(perm_id: int, body: PermissionUpdate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    p = db.query(Permission).filter(Permission.id == perm_id).first()
    if not p: raise HTTPException(404)
    for k, v in body.model_dump(exclude_unset=True).items(): setattr(p, k, v)
    db.commit()
    return APIResponse.success(data={"id": p.id, "name": p.name})


# ── 操作日志 ──
@router.get("/audit-logs", response_model=APIResponse[dict])
def list_audit_logs(page: int = Query(default=1, ge=1), page_size: int = Query(default=20, ge=1, le=100),
                    user_id: Optional[int] = None, action: Optional[str] = None, db: Session = Depends(get_db),
                    user: CurrentUser = Depends(get_current_user)):
    q = db.query(AuditLog).order_by(AuditLog.created_at.desc())
    if user_id: q = q.filter(AuditLog.user_id == user_id)
    if action: q = q.filter(AuditLog.action == action)
    total = q.count()
    items = q.offset((page - 1) * page_size).limit(page_size).all()
    return APIResponse.success(data={"items": [{"id": a.id, "user_id": a.user_id, "username": a.username, "action": a.action, "resource": a.resource, "detail": a.detail, "created_at": a.created_at.isoformat()} for a in items], "total": total, "page": page, "page_size": page_size})


# ── 部门管理 ──
@router.get("/departments", response_model=APIResponse[list])
def list_departments(db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    depts = db.query(Organization).filter(Organization.org_type.in_(["dept", "team"]), Organization.deleted_at.is_(None)).order_by(Organization.sort_order).all()
    return APIResponse.success(data=[{"id": d.id, "name": d.name, "parent_id": d.parent_id, "org_type": d.org_type, "description": d.description, "manager_id": d.manager_id, "sort_order": d.sort_order} for d in depts])


@router.post("/departments", response_model=APIResponse[dict])
def create_department(body: DepartmentCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    if body.parent_id:
        parent = db.query(Organization).filter(Organization.id == body.parent_id, Organization.deleted_at.is_(None)).first()
        if not parent: raise HTTPException(400, "父级部门不存在")
    d = Organization(name=body.name, parent_id=body.parent_id, org_type="dept", description=body.description, manager_id=body.manager_id, sort_order=body.sort_order)
    db.add(d); db.commit(); db.refresh(d)
    return APIResponse.success(data={"id": d.id, "name": d.name, "org_type": d.org_type})


@router.put("/departments/{dept_id}", response_model=APIResponse[dict])
def update_department(dept_id: int, body: DepartmentCreate, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    d = db.query(Organization).filter(Organization.id == dept_id).first()
    if not d: raise HTTPException(404)
    for k, v in body.model_dump(exclude_unset=True).items(): setattr(d, k, v)
    db.commit()
    return APIResponse.success(data={"id": d.id, "name": d.name})


@router.delete("/departments/{dept_id}", response_model=APIResponse[None])
def delete_department(dept_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    d = db.query(Organization).filter(Organization.id == dept_id).first()
    if not d: raise HTTPException(404)
    d.deleted_at = datetime.now(timezone.utc); db.commit()
    return APIResponse.success(message="已删除")


# ── 团队成员管理 ──
@router.get("/teams/{team_id}/members", response_model=APIResponse[list])
def list_team_members(team_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    team = db.query(Organization).filter(Organization.id == team_id, Organization.deleted_at.is_(None)).first()
    if not team: raise HTTPException(404, "团队不存在")
    members = db.query(User).filter(User.org_id == team_id, User.is_active == True).all()
    return APIResponse.success(data=[{"id": m.id, "username": m.username, "full_name": m.full_name, "role": m.role, "email": m.email} for m in members])


@router.post("/teams/{team_id}/members", response_model=APIResponse[dict])
def add_team_member(team_id: int, body: TeamMemberAdd, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    team = db.query(Organization).filter(Organization.id == team_id, Organization.deleted_at.is_(None)).first()
    if not team: raise HTTPException(404, "团队不存在")
    if db.query(User).filter(User.username == body.username).first(): raise HTTPException(400, "用户名已存在")
    u = User(username=body.username, password_hash=hash_password(body.password), full_name=body.full_name or body.username, role=body.role, org_id=team_id, department_id=team.parent_id)
    db.add(u); db.commit(); db.refresh(u)
    _log(db, user.id, user.username, "team.member.add", f"团队{team.name}添加成员{body.username}")
    return APIResponse.success(data={"user_id": u.id, "username": u.username, "team": team.name, "message": "成员已同步到用户管理"})


@router.delete("/teams/{team_id}/members/{user_id}", response_model=APIResponse[None])
def remove_team_member(team_id: int, user_id: int, db: Session = Depends(get_db), user: CurrentUser = Depends(get_current_user)):
    u = db.query(User).filter(User.id == user_id, User.org_id == team_id).first()
    if not u: raise HTTPException(404)
    u.is_active = False; db.commit()
    return APIResponse.success(message="已从团队移除")
