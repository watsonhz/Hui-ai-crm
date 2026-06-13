"""
Pytest 全局配置和共享 fixtures。

为所有测试模块提供：
- FastAPI TestClient
- 内存数据库会话
- 模拟认证 token
- 标准测试数据工厂
"""

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def anyio_backend():
    """指定异步后端（pytest-asyncio 兼容）。"""
    return "asyncio"


@pytest.fixture
def base_url():
    """API 基础 URL（测试环境）。"""
    return "http://testserver/api/v1"


@pytest.fixture
def auth_headers():
    """模拟认证请求头（JWT Bearer Token）。

    每个测试可以 override 此 fixture 来模拟不同角色。
    """
    return {
        "Authorization": "Bearer test-mock-token",
        "Content-Type": "application/json",
    }


@pytest.fixture
def admin_headers():
    """管理员角色的认证请求头。"""
    return {
        "Authorization": "Bearer admin-mock-token",
        "Content-Type": "application/json",
    }


# ============================================================
# Async HTTP 客户端 fixtures（用于 API 端点测试）
# ============================================================

@pytest.fixture
async def async_client():
    """异步 HTTP 客户端 — 用于测试 FastAPI 端点。

    使用方式:
        async def test_something(async_client):
            response = await async_client.get("/api/v1/health")
            assert response.status_code == 200
    """
    # 延迟导入，避免在主模块未就绪时加载
    from backend.app.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


# ============================================================
# 测试数据工厂 fixtures
# ============================================================

@pytest.fixture
def sample_customer_data():
    """标准客户测试数据。"""
    return {
        "name": "测试客户有限公司",
        "industry": "信息技术",
        "scale": "中型企业",
        "contact_person": "张三",
        "contact_phone": "13800138000",
        "contact_email": "test@example.com",
        "address": "北京市朝阳区测试路100号",
    }


@pytest.fixture
def sample_project_data():
    """标准项目测试数据。"""
    return {
        "name": "测试项目",
        "description": "用于自动化测试的示例项目",
        "status": "pending",
        "budget": 1000000.00,
        "start_date": "2026-01-01",
        "end_date": "2026-12-31",
    }


# ============================================================
# 数据库 fixtures
# ============================================================

@pytest.fixture
def db_session():
    """内存数据库会话（单元测试用）。

    每个测试函数获得独立的数据库事务，测试结束后自动回滚。
    """
    # TODO: 待 ORM 确定后实现（SQLAlchemy / GORM / MyBatis-Plus）
    # 当前为占位 fixture，实际实现取决于最终技术选型
    pytest.skip("数据库 fixture 待技术选型确定后实现")


# ============================================================
# Redis fixtures
# ============================================================

@pytest.fixture
def redis_mock(mocker):
    """Mock Redis 客户端（单元测试用）。"""
    # 使用 pytest-mock 的 mocker fixture
    mock_redis = mocker.MagicMock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    mock_redis.delete.return_value = 1
    return mock_redis
