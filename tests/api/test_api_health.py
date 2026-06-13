"""
API 健康检查测试 — 验证 FastAPI 应用可正常启动和响应。
"""

import pytest


@pytest.mark.api
class TestAPIHealth:
    """API 端点基本可用性测试。"""

    @pytest.mark.asyncio
    async def test_health_endpoint(self, async_client):
        """验证健康检查端点返回 200。

        TODO: 待 backend/app/main.py 添加 /api/v1/health 端点后启用。
        """
        pytest.skip("健康检查端点待实现")

    @pytest.mark.asyncio
    async def test_api_docs_accessible(self, async_client):
        """验证 Swagger 文档页面可访问。"""
        response = await async_client.get("/docs")
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_openapi_schema(self, async_client):
        """验证 OpenAPI schema 可获取。"""
        response = await async_client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "paths" in schema
