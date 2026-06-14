"""Tests for rate limiting and brute-force protection."""
<<<<<<< HEAD

import time
import pytest
from app.core.rate_limit import RateLimiter, BruteForceProtector


class TestRateLimiter:
    def test_allows_within_limit(self):
        rl = RateLimiter(max_requests=5, window_seconds=60)
        for _ in range(5):
            assert rl.is_allowed("key1") is True

    def test_blocks_over_limit(self):
        rl = RateLimiter(max_requests=2, window_seconds=60)
        assert rl.is_allowed("key2") is True
        assert rl.is_allowed("key2") is True
        assert rl.is_allowed("key2") is False

    def test_remaining_count(self):
        rl = RateLimiter(max_requests=5, window_seconds=60)
        assert rl.remaining("key3") == 5
        rl.is_allowed("key3")
        assert rl.remaining("key3") == 4

    def test_different_keys_independent(self):
        rl = RateLimiter(max_requests=2, window_seconds=60)
        rl.is_allowed("a")
        rl.is_allowed("a")
        assert rl.is_allowed("a") is False
        assert rl.is_allowed("b") is True

    def test_expired_window(self):
        rl = RateLimiter(max_requests=2, window_seconds=0.01)
        rl.is_allowed("e1")
        rl.is_allowed("e1")
        assert rl.is_allowed("e1") is False
        time.sleep(0.02)
        assert rl.is_allowed("e1") is True


class TestBruteForceProtector:
    def test_allows_up_to_max_failures(self):
        bf = BruteForceProtector()
        bf.MAX_FAILURES = 3
        assert bf.record_failure("user1") == 2  # 1 used, 2 remaining
        assert bf.record_failure("user1") == 1
        remaining = bf.record_failure("user1")
        assert remaining == 0  # locked
        assert bf.is_locked("user1") is True

    def test_not_locked_initially(self):
        bf = BruteForceProtector()
        assert bf.is_locked("newuser") is False

    def test_reset_after_success(self):
        bf = BruteForceProtector()
        bf.MAX_FAILURES = 3
        bf.record_failure("user2")
        bf.record_failure("user2")
        bf.reset("user2")
        assert bf.is_locked("user2") is False
        assert bf.remaining_attempts("user2") == bf.MAX_FAILURES

    def test_remaining_attempts(self):
        bf = BruteForceProtector()
        bf.MAX_FAILURES = 5
        assert bf.remaining_attempts("user3") == 5
        bf.record_failure("user3")
        assert bf.remaining_attempts("user3") == 4

    def test_lock_expires(self):
        bf = BruteForceProtector()
        bf.MAX_FAILURES = 1
        bf.LOCK_MINUTES = 0.001  # 60ms
        bf.record_failure("user4")
        assert bf.is_locked("user4") is True
        time.sleep(0.1)
        assert bf.is_locked("user4") is False


class TestLoginRateLimit:
    def test_login_failure_returns_401(self, client):
        r = client.post("/api/v1/auth/login", json={
            "username": "nobody", "password": "wrong",
        })
        assert r.status_code == 401

    def test_login_success(self, client, admin_user):
        """Successful login with correct password returns token."""
        r = client.post("/api/v1/auth/login", json={
            "username": admin_user.username,
            "password": "test123",
        })
=======
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
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
        assert r.status_code == 200
        assert "access_token" in r.json()["data"]
