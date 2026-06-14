<<<<<<< HEAD
"""Rate limiting & brute-force protection middleware.

In-memory store for development; Redis-backed in production.
"""
=======
"""Rate limiting & brute-force protection — thread-safe."""
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8

import time
import threading
from collections import defaultdict
<<<<<<< HEAD
from typing import Optional


class RateLimiter:
    """Simple sliding-window rate limiter. Thread-safe."""

=======


class RateLimiter:
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._buckets: dict[str, list[float]] = defaultdict(list)

<<<<<<< HEAD
    def _clean(self, key: str, now: float) -> None:
=======
    def _clean(self, key: str, now: float):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
        cutoff = now - self.window_seconds
        self._buckets[key] = [t for t in self._buckets[key] if t > cutoff]

    def is_allowed(self, key: str) -> bool:
<<<<<<< HEAD
        """Returns True if the request is within the rate limit."""
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
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


<<<<<<< HEAD
# Shared instances
api_limiter = RateLimiter(max_requests=100, window_seconds=60)   # 100 req/min per IP
login_limiter = RateLimiter(max_requests=5, window_seconds=60)   # 5 login attempts/min
sms_limiter = RateLimiter(max_requests=1, window_seconds=60)     # 1 SMS/min per phone


class BruteForceProtector:
    """Login brute-force protection: track failures, lock after threshold."""

=======
login_limiter = RateLimiter(max_requests=5, window_seconds=60)
sms_limiter = RateLimiter(max_requests=1, window_seconds=60)


class BruteForceProtector:
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    MAX_FAILURES = 5
    LOCK_MINUTES = 15

    def __init__(self):
        self._lock = threading.Lock()
        self._failures: dict[str, list[float]] = defaultdict(list)
        self._locked_until: dict[str, float] = {}

    def record_failure(self, username: str) -> int:
<<<<<<< HEAD
        """Record a failed login attempt. Returns remaining attempts (0 = locked)."""
        now = time.time()
        with self._lock:
            # Purge old failures (> 15 min)
=======
        now = time.time()
        with self._lock:
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
            cutoff = now - (self.LOCK_MINUTES * 60)
            self._failures[username] = [t for t in self._failures[username] if t > cutoff]
            self._failures[username].append(now)
            remaining = max(0, self.MAX_FAILURES - len(self._failures[username]))
<<<<<<< HEAD

            if remaining == 0:
                self._locked_until[username] = now + (self.LOCK_MINUTES * 60)

            return remaining

    def is_locked(self, username: str) -> bool:
        """Check if an account is locked."""
        until = self._locked_until.get(username, 0)
        if until > time.time():
            return True
        # Lock expired
=======
            if remaining == 0:
                self._locked_until[username] = now + (self.LOCK_MINUTES * 60)
            return remaining

    def is_locked(self, username: str) -> bool:
        until = self._locked_until.get(username, 0)
        if until > time.time():
            return True
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
        if until > 0:
            with self._lock:
                self._locked_until.pop(username, None)
                self._failures.pop(username, None)
        return False

<<<<<<< HEAD
    def reset(self, username: str) -> None:
        """Reset failures after successful login."""
=======
    def reset(self, username: str):
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
        with self._lock:
            self._failures.pop(username, None)
            self._locked_until.pop(username, None)

    def remaining_attempts(self, username: str) -> int:
<<<<<<< HEAD
        """How many attempts remain before lock."""
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
        if self.is_locked(username):
            return 0
        return max(0, self.MAX_FAILURES - len(self._failures[username]))


brute_force = BruteForceProtector()
<<<<<<< HEAD

# TODO(Sprint7): Redis backend - replace dict with Redis sorted sets for production
=======
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
