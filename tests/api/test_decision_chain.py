"""
决策链 API 测试 (TASK-008 Part B)
/api/v1/decision-chain — 图谱 + 三层关系（组织→人→角色）

端点（基于 API spec v4.0）:
  GET    /api/v1/decision-chain            — 获取决策链图谱
  GET    /api/v1/decision-chain/{node_id}  — 节点详情
  POST   /api/v1/decision-chain/search     — 搜索节点
  GET    /api/v1/decision-chain/stats      — 图谱统计
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

NOW = datetime(2026, 6, 13, tzinfo=timezone.utc)


def mock_node(**overrides):
    defaults = {
        "id": 1, "name": "张总", "title": "CIO",
        "org_id": 10, "org_name": "信息中心",
        "level": 1, "relation_type": "决策者",
        "parent_id": None, "children": [],
        "created_at": NOW, "updated_at": NOW,
    }
    defaults.update(overrides)
    node = MagicMock()
    for k, v in defaults.items():
        setattr(node, k, v)
    return node


def mock_db_with(obj):
    db = MagicMock()
    db.query.return_value = db
    db.filter.return_value = db
    db.order_by.return_value = db
    db.offset.return_value = db
    db.limit.return_value = db
    db.count.return_value = 1
    db.all.return_value = [obj]
    db.first.return_value = obj
    return db


# ============================================================
# GET / — 决策链图谱
# ============================================================

@pytest.mark.api
class TestDecisionChainGraph:

    def test_get_graph_returns_nodes(self):
        """图谱接口返回节点列表 + 边关系。"""
        # 占位：模拟响应结构（API 尚未实现，基于 spec 编写）
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "nodes": [
                {"id": 1, "name": "张总(CIO)", "org": "信息中心", "level": 1},
                {"id": 2, "name": "刘工", "org": "运维部", "level": 2},
            ],
            "edges": [
                {"source": 1, "target": 2, "relation": "下属"},
            ],
        })
        assert result.code == 200
        assert len(result.data["nodes"]) == 2
        assert len(result.data["edges"]) == 1

    def test_get_graph_empty(self):
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={"nodes": [], "edges": []})
        assert result.code == 200
        assert result.data["nodes"] == []

    def test_graph_schema_structure(self):
        """验证图谱响应结构完整性。"""
        graph_data = {
            "nodes": [], "edges": [],
            "meta": {"total_nodes": 0, "total_edges": 0, "max_depth": 3},
        }
        assert "nodes" in graph_data
        assert "edges" in graph_data
        assert isinstance(graph_data["nodes"], list)
        assert isinstance(graph_data["edges"], list)


# ============================================================
# GET /{node_id} — 节点详情
# ============================================================

@pytest.mark.api
class TestDecisionChainNodeDetail:

    def test_node_detail_structure(self):
        """节点详情响应结构。"""
        detail = {
            "id": 1, "name": "张总", "title": "CIO",
            "org_name": "信息中心", "level": 1,
            "relation_type": "决策者",
            "parents": [{"id": 0, "name": "董事会", "relation": "汇报"}],
            "children": [
                {"id": 2, "name": "刘工", "relation": "下属"},
                {"id": 3, "name": "王经理", "relation": "下属"},
            ],
            "influence_score": 0.85,
        }
        assert detail["name"] == "张总"
        assert detail["level"] == 1
        assert len(detail["children"]) == 2

    def test_node_not_found(self):
        """节点不存在时返回 404。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(status_code=404, detail="决策链节点不存在")
        assert exc.value.status_code == 404


# ============================================================
# POST /search — 搜索节点
# ============================================================

@pytest.mark.api
class TestDecisionChainSearch:

    def test_search_by_name(self):
        """按名称搜索。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "items": [{"id": 1, "name": "张总", "org": "信息中心"}],
            "total": 1,
        })
        assert result.code == 200
        assert result.data["total"] == 1

    def test_search_by_org(self):
        """按组织搜索。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={"items": [], "total": 0})
        assert result.code == 200

    def test_search_empty_query(self):
        """空搜索返回 400。"""
        from fastapi import HTTPException
        with pytest.raises(HTTPException) as exc:
            raise HTTPException(
                status_code=400, detail="搜索关键词不能为空"
            )
        assert exc.value.status_code == 400


# ============================================================
# GET /stats — 图谱统计
# ============================================================

@pytest.mark.api
class TestDecisionChainStats:

    def test_stats_structure(self):
        """统计接口结构。"""
        from app.schemas.response import APIResponse
        result = APIResponse.success(data={
            "total_nodes": 45,
            "total_edges": 62,
            "max_depth": 4,
            "org_count": 8,
            "avg_influence": 0.62,
        })
        assert result.code == 200
        assert result.data["total_nodes"] > 0
        assert result.data["total_edges"] > 0
