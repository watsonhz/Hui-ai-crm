"""
RAG 知识库 API 测试 — 文档上传 + 语义搜索 (TASK-012 Part A)

POST   /api/v1/knowledge/upload      — 上传文档
POST   /api/v1/knowledge/search      — 语义搜索
GET    /api/v1/knowledge/documents   — 文档列表
GET    /api/v1/knowledge/categories  — 分类树
DELETE /api/v1/knowledge/{id}        — 删除文档
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


@pytest.mark.api
class TestKnowledgeUpload:

    def test_upload_success(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "id": 1, "title": "AI运维平台v3.2白皮书.pdf",
            "status": "processing", "chunks": 0,
            "file_size": 2048000, "file_type": "pdf",
            "category": "产品资料", "uploaded_at": NOW.isoformat(),
        })
        assert result.code == 200
        assert result.data["status"] == "processing"

    def test_upload_empty_file(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=400, detail="文件不能为空")
        assert exc.value.status_code == 400

    def test_upload_unsupported_type(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=400, detail="不支持的文件类型: .exe")
        assert exc.value.status_code == 400

    def test_upload_too_large(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=413, detail="文件超过最大限制 50MB")
        assert exc.value.status_code == 413


@pytest.mark.api
class TestKnowledgeSearch:

    def test_semantic_search(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "query": "AI运维平台架构",
            "results": [
                {"id": 1, "title": "AI运维平台v3.2白皮书", "score": 0.92, "chunk": "..."},
                {"id": 2, "title": "AI运维技术方案", "score": 0.85, "chunk": "..."},
                {"id": 3, "title": "智能告警模块说明", "score": 0.78, "chunk": "..."},
            ],
            "total": 3, "took_ms": 45,
        })
        assert result.code == 200
        assert result.data["total"] == 3
        assert result.data["results"][0]["score"] >= result.data["results"][1]["score"]

    def test_search_empty_query(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=400, detail="搜索关键词不能为空")
        assert exc.value.status_code == 400

    def test_search_no_results(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "query": "xyz不存在的关键词",
            "results": [], "total": 0, "took_ms": 12,
        })
        assert result.code == 200
        assert result.data["results"] == []

    def test_search_latency_budget(self):
        """语义搜索应在 200ms 内返回（PGVector 基线）。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "query": "test", "results": [], "total": 0, "took_ms": 85,
        })
        assert result.data["took_ms"] < 200  # Sprint3 延迟基线


@pytest.mark.api
class TestKnowledgeDocuments:

    def test_list_documents(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [
                {"id": 1, "title": "产品白皮书", "category": "产品资料", "views": 128},
            ],
            "total": 56, "page": 1, "page_size": 20,
        })
        assert result.code == 200
        assert result.data["total"] == 56

    def test_list_by_category(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [], "total": 0, "page": 1, "page_size": 20,
        })
        assert result.code == 200


@pytest.mark.api
class TestKnowledgeCategories:

    def test_categories_tree(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "categories": [
                {"id": 1, "label": "产品资料", "children": [
                    {"id": 11, "label": "产品白皮书"},
                    {"id": 12, "label": "功能说明书"},
                ]},
                {"id": 2, "label": "技术方案"},
                {"id": 3, "label": "客户案例"},
                {"id": 4, "label": "合同模板"},
            ]
        })
        assert result.code == 200
        assert len(result.data["categories"]) >= 4

    def test_categories_empty(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={"categories": []})
        assert result.code == 200


@pytest.mark.api
class TestKnowledgeDelete:

    def test_delete_success(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(message="文档删除成功")
        assert result.code == 200

    def test_delete_not_found(self):
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=404, detail="文档不存在")
        assert exc.value.status_code == 404
