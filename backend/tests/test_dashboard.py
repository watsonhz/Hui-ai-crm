class TestDashboard:
    def test_stats(self, client):
        resp = client.get("/api/v1/dashboard/stats")
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "customers" in data
        assert "projects" in data
        assert "bidding" in data
        assert "visits" in data
        assert "actions" in data
        assert "reports" in data
        assert "pipeline" in data

    def test_stats_structure(self, client):
        resp = client.get("/api/v1/dashboard/stats")
        data = resp.json()["data"]
        assert isinstance(data["customers"]["total"], int)
        assert isinstance(data["actions"]["pending"], int)
        assert isinstance(data["pipeline"], list)
