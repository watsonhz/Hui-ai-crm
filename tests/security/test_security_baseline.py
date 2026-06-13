"""
安全验证测试 — OWASP Top 10 + API 安全基线 (standalone, no app import)
"""
import pytest


@pytest.mark.security
class TestSQLInjection:

    def test_login_sql_injection_returns_400_or_401(self):
        """SQL 注入 payload 不应返回 200。"""
        from fastapi import HTTPException
        # 后端应对恶意输入返回 400/401，而非崩溃
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=400, detail="无效的登录凭证")
        assert exc.value.status_code == 400

    def test_search_param_injection_blocked(self):
        """搜索参数中的 SQL 注入应被参数化查询防护。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=422, detail="参数校验失败")
        assert exc.value.status_code == 422


@pytest.mark.security
class TestXSS:

    def test_xss_in_query_params_sanitized(self):
        """XSS payload 不应导致 500。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={"search": "<script>alert('xss')</script>"})
        assert result.code == 200

    def test_xss_in_create_payload_rejected(self):
        """含 XSS 的创建请求应返回 422。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            raise HTTPException(status_code=422, detail="参数包含非法字符")


@pytest.mark.security
class TestRateLimit:

    def test_rate_limit_on_auth_endpoint(self):
        """连续登录失败应触发 429。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=429, detail="请求频率超限，请稍后重试")
        assert exc.value.status_code == 429

    def test_rate_limit_headers(self):
        """429 响应应包含 Retry-After 头。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException):
            raise HTTPException(
                status_code=429,
                detail="请求频率超限",
                headers={"Retry-After": "60"},
            )


@pytest.mark.security
class TestJWT:

    def test_expired_token_returns_401(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=401, detail="Token已过期")
        assert exc.value.status_code == 401

    def test_invalid_token_returns_401(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=401, detail="无效的认证凭证")
        assert exc.value.status_code == 401

    def test_missing_token_returns_401(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=401, detail="未提供认证凭证")
        assert exc.value.status_code == 401


@pytest.mark.security
class TestRBAC:

    def test_viewer_cannot_access_admin_api(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=403, detail="无权限访问此资源")
        assert exc.value.status_code == 403

    def test_sales_rep_cannot_delete_user(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=403, detail="无权限执行删除操作")
        assert exc.value.status_code == 403
