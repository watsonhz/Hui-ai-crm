"""Redis cache helper — get/set/delete with JSON serialization."""
import json
from typing import Optional, Any
import redis
from app.core.config import settings

_r: Optional[redis.Redis] = None

def _get_redis() -> redis.Redis:
    global _r
    if _r is None:
        try:
            _r = redis.from_url(settings.REDIS_URL, decode_responses=True, socket_connect_timeout=2)
            _r.ping()
        except (redis.ConnectionError, redis.TimeoutError):
            _r = None
    return _r

def cache_get(key: str) -> Optional[Any]:
    r = _get_redis()
    if r is None: return None
    try:
        val = r.get(key)
        return json.loads(val) if val else None
    except Exception: return None

def cache_set(key: str, value: Any, ttl: int = 300) -> bool:
    r = _get_redis()
    if r is None: return False
    try:
        r.setex(key, ttl, json.dumps(value, ensure_ascii=False))
        return True
    except Exception: return False

def cache_delete(key: str) -> None:
    r = _get_redis()
    if r is None: return
    try: r.delete(key)
    except Exception: pass
