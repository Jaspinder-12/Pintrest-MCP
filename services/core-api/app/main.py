"""
Module: main.py

Purpose:
Application entry point and core router registry.

Dependencies:
- fastapi
- uvicorn

Usage:
Started using uvicorn: uvicorn app.main:app --reload

Notes:
Sets up CORS, routers, logging and core hooks.

Future Improvements:
- Add automatic route documentation versioning
- Implement request correlation ID injection middlewares
"""

from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

from app.core.config import get_settings, Settings
from app.core.logging import configure_logging
from app.api.v1.search import router as search_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.boards import router as boards_router
from app.api.v1.pins import router as pins_router

# ============================================
# PURPOSE
# ============================================
# This is the primary module of the Core FastAPI service. It aggregates
# the configuration, initial logging, and global routing systems.

settings = get_settings()
configure_logging(settings.LOG_LEVEL)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Aesthetic RAG and Visual intelligence backend for Pinterest MCP Server",
    version="1.0.0"
)

app.include_router(search_router)
app.include_router(analysis_router)
app.include_router(boards_router)
app.include_router(pins_router)

# Enable Cross Origin Requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================
# BUSINESS LOGIC
# ============================================
@app.get("/health", status_code=status.HTTP_200_OK, response_model=Dict[str, Any])
def health_check() -> Dict[str, Any]:
    """
    Performs system health check checks.

    Parameters:
        None.

    Returns:
        Dict[str, Any]: Contains service status details.

    Notes:
        Used by docker orchestrators to check container viability.
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENV,
        "debug_mode": settings.DEBUG
    }

@app.get("/", status_code=status.HTTP_200_OK)
def root_endpoint(cfg: Settings = Depends(get_settings)) -> Dict[str, str]:
    """
    Entry root index route.

    Parameters:
        cfg (Settings): Loaded application configuration class.

    Returns:
        Dict[str, str]: Welcome info message.

    Notes:
        Verify settings are injected correctly.
    """
    return {
        "message": f"Welcome to the {cfg.PROJECT_NAME} API. Access /docs for swagger specifications."
    }

# ============================================
# AGENT INTERACTION
# ============================================
# IDE agent runners fetch /health to ensure local microservices are listening on target ports
# before issuing REST search calls.

# ============================================
# SECURITY NOTES
# ============================================
# CORS middleware is configured to allow "*" for development ease. Production
# deployments must lock allowed origins to authorized client domain patterns.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Integrate rate limiting middleware interfaces using Redis pools.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Multi-user workspace routing
# 2. Automated API load-shedding middlewares
# 3. OpenTelemetry tracing middleware integration
# 4. Gzip compression middleware setups
#
# ============================================
