import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
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
    description="企业级AI CRM 政企大B客户管理系统 API",
    version="4.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173,http://192.168.0.169:3000,http://192.168.0.168:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(v1_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI-CRM Enterprise API v4.0"}
