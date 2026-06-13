from app.models.project import Project

class TestProjectModel:
    def test_create(self, db):
        p = Project(name="测试项目", stage=1)
        db.add(p)
        db.commit()
        assert p.id is not None

    def test_invalid_stage(self):
        p = Project(name="test")
        try:
            p.stage = 99
            assert False
        except ValueError:
            pass

    def test_stage_transition(self, db):
        p = Project(name="test", stage=1)
        db.add(p)
        db.commit()
        assert p.can_transition_to(2) is True
        assert p.can_transition_to(7) is False

class TestProjectsAPI:
    def test_create(self, client):
        resp = client.post("/api/v1/projects/", json={"name": "新项目", "stage": 1})
        assert resp.json()["data"]["name"] == "新项目"

    def test_list(self, client):
        client.post("/api/v1/projects/", json={"name": "项目A"})
        client.post("/api/v1/projects/", json={"name": "项目B"})
        assert client.get("/api/v1/projects/").json()["data"]["total"] == 2

    def test_get_by_id(self, client):
        r = client.post("/api/v1/projects/", json={"name": "详情"})
        pid = r.json()["data"]["id"]
        assert client.get(f"/api/v1/projects/{pid}").json()["data"]["name"] == "详情"

    def test_update(self, client):
        r = client.post("/api/v1/projects/", json={"name": "旧名称"})
        pid = r.json()["data"]["id"]
        resp = client.put(f"/api/v1/projects/{pid}", json={"name": "新名称"})
        assert resp.json()["data"]["name"] == "新名称"

    def test_update_stage_valid(self, client):
        r = client.post("/api/v1/projects/", json={"name": "阶段测试", "stage": 1})
        pid = r.json()["data"]["id"]
        resp = client.put(f"/api/v1/projects/{pid}/stage", json={"stage": 2})
        assert resp.json()["data"]["stage"] == 2

    def test_update_stage_invalid(self, client):
        r = client.post("/api/v1/projects/", json={"name": "跳阶段", "stage": 1})
        pid = r.json()["data"]["id"]
        resp = client.put(f"/api/v1/projects/{pid}/stage", json={"stage": 7})
        assert resp.status_code == 400

    def test_kanban(self, client):
        client.post("/api/v1/projects/", json={"name": "线索项目", "stage": 1})
        client.post("/api/v1/projects/", json={"name": "合同项目", "stage": 7})
        data = client.get("/api/v1/projects/board/kanban").json()["data"]
        assert len(data) == 12
        assert [d for d in data if d["stage"] == 1][0]["count"] == 1
        assert [d for d in data if d["stage"] == 7][0]["count"] == 1
