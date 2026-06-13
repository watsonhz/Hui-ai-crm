"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import bidding, customers, organizations, projects
from app.core.config import settings

app = FastAPI(
    title="AI-CRM API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware — allow frontend dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── 路由注册 ──
app.include_router(customers.router, prefix="/api/v1")
app.include_router(bidding.router)
app.include_router(projects.router)
app.include_router(organizations.router)


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {"code": 200, "message": "ok", "data": {"status": "healthy"}}
