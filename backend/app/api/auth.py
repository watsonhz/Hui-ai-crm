"""Authentication endpoints — login, refresh."""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from app.core.auth import (
    create_access_token, create_refresh_token, decode_token,
    hash_password, verify_password, TokenPayload, get_current_user,
)

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

# Mock user DB (replace with real DB in production)
MOCK_USERS = {
    "admin": {"id": 1, "username": "admin", "password": hash_password("admin123"), "role": "admin"},
    "manager": {"id": 2, "username": "manager", "password": hash_password("mgr123"), "role": "manager"},
}

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login", summary="用户登录", operation_id="auth_login")
async def login(body: LoginRequest):
    user = MOCK_USERS.get(body.username)
    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    return {
        "code": 200, "message": "登录成功",
        "data": {
            "access_token": create_access_token(user["id"], user["username"], user["role"]),
            "refresh_token": create_refresh_token(user["id"], user["username"]),
            "token_type": "bearer",
            "expires_in": 3600,
        },
    }

@router.post("/refresh", summary="刷新Token", operation_id="auth_refresh")
async def refresh(body: RefreshRequest):
    try:
        payload = decode_token(body.refresh_token)
    except HTTPException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token无效")
    return {
        "code": 200, "message": "Token已刷新",
        "data": {
            "access_token": create_access_token(int(payload.sub), payload.username, payload.role),
            "expires_in": 3600,
        },
    }

@router.get("/me", summary="当前用户信息", operation_id="auth_me")
async def me(user: TokenPayload = Depends(get_current_user)):
    return {"code": 200, "message": "success", "data": {"id": user.sub, "username": user.username, "role": user.role}}
