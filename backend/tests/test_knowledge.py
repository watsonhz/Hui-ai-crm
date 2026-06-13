from app.models.knowledge import Knowledge

class TestKnowledgeModel:
    def test_create(self, db):
        k = Knowledge(title="测试知识", content="内容", category="产品")
        db.add(k)
        db.commit()
        assert k.id is not None

class TestKnowledgeAPI:
    def test_create(self, client):
        resp = client.post("/api/v1/knowledge/", json={"title": "FAQ", "content": "常见问题", "category": "产品"})
        assert resp.status_code == 200
        assert resp.json()["data"]["title"] == "FAQ"

    def test_list(self, client):
        client.post("/api/v1/knowledge/", json={"title": "K1", "content": "c1", "category": "产品"})
        client.post("/api/v1/knowledge/", json={"title": "K2", "content": "c2", "category": "技术"})
        resp = client.get("/api/v1/knowledge/")
        data = resp.json()["data"]
        assert "items" in data
        assert "total" in data

    def test_list_filter(self, client):
        client.post("/api/v1/knowledge/", json={"title": "FK", "content": "c", "category": "财务"})
        resp = client.get("/api/v1/knowledge/?category=财务")
        assert "items" in resp.json()["data"]

    def test_get_by_id(self, client):
        r = client.post("/api/v1/knowledge/", json={"title": "详情", "content": "详细内容", "category": "产品"})
        kid = r.json()["data"]["id"]
        resp = client.get(f"/api/v1/knowledge/{kid}")
        assert resp.json()["data"]["title"] == "详情"

    def test_update(self, client):
        r = client.post("/api/v1/knowledge/", json={"title": "旧标题", "content": "c", "category": "产品"})
        kid = r.json()["data"]["id"]
        resp = client.put(f"/api/v1/knowledge/{kid}", json={"title": "新标题"})
        assert resp.json()["data"]["title"] == "新标题"

    def test_delete(self, client):
        r = client.post("/api/v1/knowledge/", json={"title": "待删除", "content": "c", "category": "产品"})
        kid = r.json()["data"]["id"]
        resp = client.delete(f"/api/v1/knowledge/{kid}")
        assert resp.json()["message"] == "删除成功"

    def test_not_found(self, client):
        resp = client.get("/api/v1/knowledge/99999")
        assert resp.status_code == 404
