import time
import threading
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

# 速率限制规则
RATE_LIMITS = {
    r"/api/v1/auth/login": (5, 60),           # 5次/分钟
    r"/api/v1/auth/register": (3, 60),          # 3次/分钟
    r"/api/v1/ai/": (30, 60),                    # AI 30次/分钟
    r"/api/v1/ai/service/tickets": (30, 60),
    r"default": (120, 60),                        # CRUD 120次/分钟
}

_lock = threading.Lock()
_hits: dict[str, list[float]] = {}  # key → [timestamps]
MAX_ENTRIES = 10000


def _get_limits(path: str) -> tuple[int, int]:
    for prefix, limits in RATE_LIMITS.items():
        if prefix != "default" and path.startswith(prefix):
            return limits
    return RATE_LIMITS["default"]


def _cleanup():
    """清理过期条目"""
    now = time.time()
    stale = [k for k, ts in _hits.items() if not ts or ts[-1] < now - 300]
    for k in stale:
        del _hits[k]


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        max_hits, window = _get_limits(path)
        client_ip = request.client.host if request.client else "unknown"
        key = f"{client_ip}:{path}"

        with _lock:
            now = time.time()
            cutoff = now - window
            if key not in _hits:
                _hits[key] = []
            _hits[key] = [t for t in _hits[key] if t > cutoff]
            _hits[key].append(now)

            if len(_hits[key]) > max_hits:
                retry_after = int(window - (now - _hits[key][0]))
                raise HTTPException(status_code=429, detail="请求过于频繁，请稍后再试",
                                    headers={"Retry-After": str(retry_after)})

            if len(_hits) > MAX_ENTRIES:
                _cleanup()

        response = await call_next(request)
        return response
