<<<<<<< HEAD
import os
=======
"""FastAPI application entry point — global error handling, no stack leaks."""

>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
=======
from fastapi.responses import JSONResponse

from app.core.config import settings
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
from app.core.database import init_db
from app.core.exceptions import validation_exception_handler, http_exception_handler, global_exception_handler
from app.middleware.request_id import RequestIDMiddleware
from app.api.v1 import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="AI-CRM Enterprise API",
    description="企业级AI CRM 政企大B客户管理系统 API v4.0",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

<<<<<<< HEAD
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://192.168.0.169:3000,http://192.168.0.168:3000").split(","),
=======
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
)

<<<<<<< HEAD
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)
=======

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import logging
    logging.getLogger("ai-crm").error(f"{type(exc).__name__}: {exc}")
    return JSONResponse(status_code=500, content={"code": 500, "message": "服务器内部错误", "data": None})

>>>>>>> 662f12488696422c660a7b9ff57a0f880cf8e5a8

app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI-CRM Enterprise API v4.0"}
