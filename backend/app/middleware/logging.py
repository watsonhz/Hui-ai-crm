import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("aicrm.access")


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration_ms = round((time.time() - start) * 1000, 1)
        rid = getattr(request.state, "request_id", "-")
        logger.info(
            f"[{rid}] {request.method} {request.url.path} → {response.status_code} ({duration_ms}ms)"
        )
        return response
