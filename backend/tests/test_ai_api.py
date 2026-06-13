"""Tests for AI report + knowledge API endpoints."""


class TestAIReportsAPI:
    def test_generate_no_auth(self, client):
        r = client.post("/api/v1/ai/reports/generate", json={
            "report_type": "visit_summary", "context": {}
        })
        assert r.status_code == 401

    def test_generate_visit_summary(self, client, auth_header):
        r = client.post("/api/v1/ai/reports/generate", json={
            "report_type": "visit_summary",
            "context": {"customer": "华为", "date": "2026-06-15"}
        }, headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert "content" in r.json()["data"]

    def test_generate_invalid_type(self, client, auth_header):
        r = client.post("/api/v1/ai/reports/generate", json={
            "report_type": "hack_report", "context": {}
        }, headers={"Authorization": auth_header})
        assert r.status_code == 422

    def test_generate_with_rag(self, client, auth_header):
        r = client.post("/api/v1/ai/reports/generate", json={
            "report_type": "customer_analysis",
            "context": {"query": "云业务"},
            "use_rag": True,
        }, headers={"Authorization": auth_header})
        assert r.status_code == 200

    def test_generate_oversized_context(self, client, auth_header):
        r = client.post("/api/v1/ai/reports/generate", json={
            "report_type": "visit_summary",
            "context": {"data": "x" * 200000},  # > 100k limit
        }, headers={"Authorization": auth_header})
        assert r.status_code == 400


class TestKnowledgeAPI:
    def test_create_no_auth(self, client):
        r = client.post("/api/v1/knowledge/", json={"title": "doc", "content": "text"})
        assert r.status_code == 401

    def test_create(self, client, auth_header):
        r = client.post("/api/v1/knowledge/", json={
            "title": "技术文档", "content": "AI-CRM使用手册..."
        }, headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["title"] == "技术文档"

    def test_create_empty_title(self, client, auth_header):
        r = client.post("/api/v1/knowledge/", json={"title": "", "content": "x"},
                        headers={"Authorization": auth_header})
        assert r.status_code == 422

    def test_list_no_auth(self, client):
        r = client.get("/api/v1/knowledge/")
        assert r.status_code == 401

    def test_list(self, client, auth_header):
        r = client.get("/api/v1/knowledge/", headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert "items" in r.json()["data"]

    def test_search(self, client, auth_header):
        r = client.post("/api/v1/knowledge/search?query=CRM&top_k=3",
                        headers={"Authorization": auth_header})
        assert r.status_code == 200
        assert isinstance(r.json()["data"], list)

    def test_search_no_auth(self, client):
        r = client.post("/api/v1/knowledge/search?query=test")
        assert r.status_code == 401

    def test_get_not_found(self, client, auth_header):
        r = client.get("/api/v1/knowledge/99999", headers={"Authorization": auth_header})
        assert r.status_code == 404

    def test_delete_not_found(self, client, auth_header):
        r = client.delete("/api/v1/knowledge/99999", headers={"Authorization": auth_header})
        assert r.status_code == 200  # placeholder: delete is idempotent
