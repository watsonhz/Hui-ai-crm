import time
import threading

_lock = threading.Lock()
_failures: dict[str, list[float]] = {}  # username → [fail_timestamps]

MAX_FAILURES = 10
LOCKOUT_WINDOW = 300  # 5分钟
LOCKOUT_DURATION = 600  # 锁定10分钟


def record_failure(username: str):
    with _lock:
        now = time.time()
        if username not in _failures:
            _failures[username] = []
        _failures[username] = [t for t in _failures[username] if t > now - LOCKOUT_WINDOW]
        _failures[username].append(now)


def is_locked(username: str) -> bool:
    with _lock:
        if username not in _failures:
            return False
        now = time.time()
        recent = [t for t in _failures[username] if t > now - LOCKOUT_WINDOW]
        _failures[username] = recent
        if len(recent) >= MAX_FAILURES:
            if now - recent[0] < LOCKOUT_DURATION:
                return True
        return False


def reset_failures(username: str):
    with _lock:
        _failures.pop(username, None)
