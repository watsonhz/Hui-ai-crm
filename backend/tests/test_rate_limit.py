"""Tests for rate limiting and brute-force protection."""
from app.core.rate_limit import RateLimiter, BruteForceProtector

class TestRateLimiter:
    def test_allows_within_limit(self):
        rl = RateLimiter(max_requests=5)
        for _ in range(5): assert rl.is_allowed("k1")
    def test_blocks_over_limit(self):
        rl = RateLimiter(max_requests=2)
        rl.is_allowed("k2"); rl.is_allowed("k2")
        assert rl.is_allowed("k2") is False
    def test_remaining(self):
        rl = RateLimiter(max_requests=5)
        assert rl.remaining("k3") == 5; rl.is_allowed("k3")
        assert rl.remaining("k3") == 4

class TestBruteForce:
    def test_lock_after_max(self):
        bf = BruteForceProtector(); bf.MAX_FAILURES = 3
        bf.record_failure("u1"); bf.record_failure("u1")
        assert bf.record_failure("u1") == 0
        assert bf.is_locked("u1")
    def test_reset(self):
        bf = BruteForceProtector(); bf.MAX_FAILURES = 3
        bf.record_failure("u2"); bf.reset("u2")
        assert not bf.is_locked("u2")

class TestLoginRateLimit:
    def test_failure_401(self, client):
        r = client.post("/api/v1/auth/login", json={"username":"x","password":"x"})
        assert r.status_code == 401
    def test_success(self, client, admin_user):
        r = client.post("/api/v1/auth/login", json={"username":admin_user.username,"password":"test123"})
        assert r.status_code == 200
        assert "access_token" in r.json()["data"]
