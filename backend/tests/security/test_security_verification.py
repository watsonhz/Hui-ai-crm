"""Security verification tests — confirm P0/P1 fixes are effective."""

import pytest


class TestP0Fixes:
    """Verify P0 blocking issues are resolved."""

    def test_secret_key_not_hardcoded(self):
        """P0-001: SECRET_KEY must not have a hardcoded default."""
        from app.core.config import Settings
        s = Settings(_env_file=None, APP_ENV="development", SECRET_KEY="", DATABASE_URL="sqlite://")
        assert s.SECRET_KEY != "change-me-to-a-random-string"
        assert s.SECRET_KEY != ""
        assert len(s.SECRET_KEY) >= 64

    def test_secret_key_production_must_fail(self):
        """P0-001: Production must reject empty SECRET_KEY."""
        from app.core.config import Settings
        with pytest.raises(ValueError, match="SECRET_KEY"):
            Settings(_env_file=None, APP_ENV="production", SECRET_KEY="", DATABASE_URL="sqlite://")

    def test_database_url_not_hardcoded(self):
        """P0-001: DATABASE_URL must come from env, not hardcoded."""
        import app.core.database as db_module
        source = open(db_module.__file__, encoding="utf-8").read()
        assert "Admin%4090088%2A" not in source
        assert "postgres:Admin" not in source


class TestP1Fixes:
    """Verify P1 serious issues are resolved."""

    def test_auth_required_all_bidding_endpoints(self, client):
        endpoints = [
            ("POST", "/api/v1/bidding/"),
            ("GET", "/api/v1/bidding/"),
            ("GET", "/api/v1/bidding/1"),
            ("PUT", "/api/v1/bidding/1"),
            ("GET", "/api/v1/bidding/calendar/upcoming"),
        ]
        for method, path in endpoints:
            r = client.request(method, path)
            assert r.status_code == 401, f"{method} {path} got {r.status_code}"

    def test_auth_required_all_project_endpoints(self, client):
        endpoints = [
            ("POST", "/api/v1/projects/"),
            ("GET", "/api/v1/projects/"),
            ("GET", "/api/v1/projects/1"),
            ("PUT", "/api/v1/projects/1"),
            ("PUT", "/api/v1/projects/1/stage"),
            ("GET", "/api/v1/projects/board/kanban"),
        ]
        for method, path in endpoints:
            r = client.request(method, path)
            assert r.status_code == 401, f"{method} {path} got {r.status_code}"

    def test_auth_required_all_org_endpoints(self, client):
        endpoints = [
            ("POST", "/api/v1/organizations/"),
            ("GET", "/api/v1/organizations/tree"),
            ("PUT", "/api/v1/organizations/1"),
            ("DELETE", "/api/v1/organizations/1"),
        ]
        for method, path in endpoints:
            r = client.request(method, path)
            assert r.status_code == 401, f"{method} {path} got {r.status_code}"

    def test_owner_forced_on_create(self, client, normal_auth_header, normal_user):
        """P1-001: create must force owner_id to current user."""
        r = client.post("/api/v1/bidding/", json={
            "title": "owner test", "bid_status": 1, "owner_id": 999
        }, headers={"Authorization": normal_auth_header})
        assert r.status_code == 200
        assert r.json()["data"]["owner_id"] == normal_user.id

    def test_cross_user_update_blocked(self, client, normal_auth_header, other_auth_header):
        """P1-001: User B cannot modify User A's bidding."""
        r = client.post("/api/v1/bidding/", json={"title": "A's", "bid_status": 1},
                        headers={"Authorization": normal_auth_header})
        bid_id = r.json()["data"]["id"]
        r = client.put(f"/api/v1/bidding/{bid_id}", json={"title": "hijacked"},
                       headers={"Authorization": other_auth_header})
        assert r.status_code == 403


class TestLikeInjection:
    """Verify LIKE injection fix (P1-004)."""

    def test_percent_wildcard_escaped(self, client, auth_header):
        client.post("/api/v1/bidding/", json={"title": "normal"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/?search=%%",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 0

    def test_underscore_wildcard_escaped(self, client, auth_header):
        client.post("/api/v1/bidding/", json={"title": "abc"},
                    headers={"Authorization": auth_header})
        r = client.get("/api/v1/bidding/?search=_",
                       headers={"Authorization": auth_header})
        assert r.json()["data"]["total"] == 0
