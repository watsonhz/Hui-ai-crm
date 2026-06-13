"""组织架构 API 测试 —— CRUD + 树形结构 + 级联删除保护。"""

import pytest
from fastapi.testclient import TestClient


def _create_org(client: TestClient, **overrides) -> dict:
    """快捷创建组织节点，返回响应 data。"""
    payload = {
        "name": "测试组织",
        "level": 1,
        **overrides,
    }
    resp = client.post("/api/v1/organizations", json=payload)
    assert resp.status_code == 201, resp.text
    return resp.json()["data"]


class TestOrgCRUD:
    """CRUD 基础测试。"""

    def test_create_root(self, client: TestClient):
        data = _create_org(client, name="华东大区", level=1)
        assert data["name"] == "华东大区"
        assert data["level"] == 1
        assert data["parent_id"] is None
        assert data["is_active"] is True
        assert data["id"] is not None

    def test_create_child(self, client: TestClient):
        parent = _create_org(client, name="华东大区", level=1)
        child = _create_org(client, name="浙江省", level=2, parent_id=parent["id"])
        assert child["parent_id"] == parent["id"]
        assert child["level"] == 2

    def test_create_grandchild(self, client: TestClient):
        root = _create_org(client, name="华东大区", level=1)
        province = _create_org(client, name="浙江省", level=2, parent_id=root["id"])
        city = _create_org(client, name="杭州市", level=3, parent_id=province["id"])
        assert city["parent_id"] == province["id"]
        assert city["level"] == 3

    def test_create_child_wrong_level(self, client: TestClient):
        """父节点 level=1 时，子节点 level 应为 2。给定 3 应被拒绝。"""
        parent = _create_org(client, name="华东大区", level=1)
        resp = client.post("/api/v1/organizations", json={
            "name": "越级市", "level": 3, "parent_id": parent["id"],
        })
        assert resp.status_code == 400

    def test_create_nonexistent_parent(self, client: TestClient):
        resp = client.post("/api/v1/organizations", json={
            "name": "孤儿", "level": 2, "parent_id": 99999,
        })
        assert resp.status_code == 400

    def test_get_by_id(self, client: TestClient):
        data = _create_org(client, name="华北")
        resp = client.get(f"/api/v1/organizations/{data['id']}")
        assert resp.status_code == 200
        assert resp.json()["data"]["name"] == "华北"

    def test_get_not_found(self, client: TestClient):
        resp = client.get("/api/v1/organizations/99999")
        assert resp.status_code == 404

    def test_update(self, client: TestClient):
        data = _create_org(client, name="旧名称")
        resp = client.put(f"/api/v1/organizations/{data['id']}", json={
            "name": "新名称", "sort_order": 10,
        })
        assert resp.status_code == 200
        assert resp.json()["data"]["name"] == "新名称"
        assert resp.json()["data"]["sort_order"] == 10

    def test_delete_leaf_node(self, client: TestClient):
        data = _create_org(client)
        resp = client.delete(f"/api/v1/organizations/{data['id']}")
        assert resp.status_code == 200

    def test_delete_with_children_rejected(self, client: TestClient):
        """有子节点的组织不能被删除。"""
        parent = _create_org(client, name="华东大区", level=1)
        _create_org(client, name="浙江省", level=2, parent_id=parent["id"])

        resp = client.delete(f"/api/v1/organizations/{parent['id']}")
        assert resp.status_code == 400


class TestOrgTree:
    """组织树测试。"""

    def test_tree_empty(self, client: TestClient):
        resp = client.get("/api/v1/organizations/tree")
        assert resp.status_code == 200
        assert resp.json()["data"]["tree"] == []

    def test_tree_single_root(self, client: TestClient):
        _create_org(client, name="华东大区", level=1)
        resp = client.get("/api/v1/organizations/tree")
        tree = resp.json()["data"]["tree"]
        assert len(tree) == 1
        assert tree[0]["name"] == "华东大区"
        assert tree[0]["children"] == []

    def test_tree_nested(self, client: TestClient):
        root = _create_org(client, name="华东大区", level=1)
        province = _create_org(client, name="浙江省", level=2, parent_id=root["id"])
        _create_org(client, name="杭州市", level=3, parent_id=province["id"])

        resp = client.get("/api/v1/organizations/tree")
        tree = resp.json()["data"]["tree"]

        assert len(tree) == 1
        assert tree[0]["name"] == "华东大区"
        assert len(tree[0]["children"]) == 1
        assert tree[0]["children"][0]["name"] == "浙江省"
        assert len(tree[0]["children"][0]["children"]) == 1
        assert tree[0]["children"][0]["children"][0]["name"] == "杭州市"

    def test_tree_multiple_roots(self, client: TestClient):
        _create_org(client, name="华东", level=1)
        _create_org(client, name="华北", level=1)
        _create_org(client, name="华南", level=1)

        resp = client.get("/api/v1/organizations/tree")
        tree = resp.json()["data"]["tree"]
        assert len(tree) == 3
        names = {n["name"] for n in tree}
        assert names == {"华东", "华北", "华南"}

    def test_tree_sort_order(self, client: TestClient):
        _create_org(client, name="B大区", level=1, sort_order=2)
        _create_org(client, name="A大区", level=1, sort_order=1)

        resp = client.get("/api/v1/organizations/tree")
        tree = resp.json()["data"]["tree"]
        assert tree[0]["name"] == "A大区"
        assert tree[1]["name"] == "B大区"

    def test_get_node_has_children(self, client: TestClient):
        root = _create_org(client, name="华东大区", level=1)
        _create_org(client, name="浙江省", level=2, parent_id=root["id"])

        resp = client.get(f"/api/v1/organizations/{root['id']}")
        data = resp.json()["data"]
        assert len(data["children"]) == 1
        assert data["children"][0]["name"] == "浙江省"
