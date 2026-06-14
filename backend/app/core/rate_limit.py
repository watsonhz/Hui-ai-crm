"""Rate limiting & brute-force protection middleware.

In-memory store for development; Redis-backed in production.
"""

import time
import threading
from collections import defaultdict
from typing import Optional


class RateLimiter:
    """Simple sliding-window rate limiter. Thread-safe."""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._buckets: dict[str, list[float]] = defaultdict(list)

    def _clean(self, key: str, now: float) -> None:
        cutoff = now - self.window_seconds
        self._buckets[key] = [t for t in self._buckets[key] if t > cutoff]

    def is_allowed(self, key: str) -> bool:
        """Returns True if the request is within the rate limit."""
        now = time.time()
        with self._lock:
            self._clean(key, now)
            if len(self._buckets[key]) >= self.max_requests:
                return False
            self._buckets[key].append(now)
            return True

    def remaining(self, key: str) -> int:
        now = time.time()
        with self._lock:
            self._clean(key, now)
            return max(0, self.max_requests - len(self._buckets[key]))


# Shared instances
api_limiter = RateLimiter(max_requests=100, window_seconds=60)   # 100 req/min per IP
login_limiter = RateLimiter(max_requests=5, window_seconds=60)   # 5 login attempts/min
sms_limiter = RateLimiter(max_requests=1, window_seconds=60)     # 1 SMS/min per phone


class BruteForceProtector:
    """Login brute-force protection: track failures, lock after threshold."""

    MAX_FAILURES = 5
    LOCK_MINUTES = 15

    def __init__(self):
        self._lock = threading.Lock()
        self._failures: dict[str, list[float]] = defaultdict(list)
        self._locked_until: dict[str, float] = {}

    def record_failure(self, username: str) -> int:
        """Record a failed login attempt. Returns remaining attempts (0 = locked)."""
        now = time.time()
        with self._lock:
            # Purge old failures (> 15 min)
            cutoff = now - (self.LOCK_MINUTES * 60)
            self._failures[username] = [t for t in self._failures[username] if t > cutoff]
            self._failures[username].append(now)
            remaining = max(0, self.MAX_FAILURES - len(self._failures[username]))

            if remaining == 0:
                self._locked_until[username] = now + (self.LOCK_MINUTES * 60)

            return remaining

    def is_locked(self, username: str) -> bool:
        """Check if an account is locked."""
        until = self._locked_until.get(username, 0)
        if until > time.time():
            return True
        # Lock expired
        if until > 0:
            with self._lock:
                self._locked_until.pop(username, None)
                self._failures.pop(username, None)
        return False

    def reset(self, username: str) -> None:
        """Reset failures after successful login."""
        with self._lock:
            self._failures.pop(username, None)
            self._locked_until.pop(username, None)

    def remaining_attempts(self, username: str) -> int:
        """How many attempts remain before lock."""
        if self.is_locked(username):
            return 0
        return max(0, self.MAX_FAILURES - len(self._failures[username]))


brute_force = BruteForceProtector()

# TODO(Sprint7): Redis backend - replace dict with Redis sorted sets for production
