from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user, require_auth
from app.core.login_guard import record_failure, is_locked, reset_failures
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.response import APIResponse

router = APIRouter()


@router.post("/login", response_model=APIResponse[TokenResponse])
def login(body: LoginRequest, db: Session = Depends(get_db)):
    if is_locked(body.username):
        raise HTTPException(status_code=429, detail="登录尝试过多，账户已锁定10分钟，请稍后再试")
    user = db.query(User).filter(User.username == body.username, User.is_active == True).first()
    if not user or not verify_password(body.password, user.password_hash):
        record_failure(body.username)
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    reset_failures(body.username)
    token = create_access_token(data={"sub": user.id})
    return APIResponse.success(data=TokenResponse(
        access_token=token,
        user={"id": user.id, "username": user.username, "role": user.role, "full_name": user.full_name},
    ).model_dump())


@router.post("/register", response_model=APIResponse[dict])
def register(body: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == body.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    user = User(username=body.username, password_hash=hash_password(body.password),
                email=body.email, full_name=body.full_name, role="sales")
    db.add(user); db.commit(); db.refresh(user)
    return APIResponse.success(data={"id": user.id, "username": user.username, "message": "注册成功"})


@router.post("/refresh", response_model=APIResponse[TokenResponse])
def refresh_token(current_user: User = Depends(require_auth)):
    token = create_access_token(data={"sub": current_user.id})
    return APIResponse.success(data=TokenResponse(
        access_token=token,
        user={"id": current_user.id, "username": current_user.username, "role": current_user.role, "full_name": current_user.full_name},
    ).model_dump())


@router.get("/me", response_model=APIResponse[dict])
def me(current_user: User = Depends(require_auth)):
    return APIResponse.success(data={"id": current_user.id, "username": current_user.username,
        "email": current_user.email, "full_name": current_user.full_name, "role": current_user.role})
