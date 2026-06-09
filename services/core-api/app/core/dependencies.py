"""
Module: dependencies.py

Purpose:
Dependency injection utilities for FastAPI request handlers.

Dependencies:
- qdrant-client
- redis
- sqlalchemy

Usage:
Injected in route parameters: Depends(get_db_session).

Notes:
Yields client resources and handles release operations.

Future Improvements:
- Connection pool optimization configs
- Distributed request tracing injections
"""

from typing import Generator
from qdrant_client import QdrantClient
import redis
from app.core.config import get_settings

settings = get_settings()

# ============================================
# PURPOSE
# ============================================
# This module maps the Dependency injection interfaces for database connections, 
# redis caches, and vector DB clients, ensuring proper connection creation 
# and teardown lifecycles.

# ============================================
# BUSINESS LOGIC
# ============================================
def get_redis_client() -> Generator[redis.Redis, None, None]:
    """
    Yields a connection client instance for Redis caching operations.

    Parameters:
        None.

    Returns:
        Generator[redis.Redis, None, None]: Redis connection client.

    Notes:
        Closes connections automatically after lifecycle completion.
    """
    client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
    try:
        yield client
    finally:
        client.close()

def get_qdrant_client() -> Generator[QdrantClient, None, None]:
    """
    Yields Qdrant vector client instances.

    Parameters:
        None.

    Returns:
        Generator[QdrantClient, None, None]: Qdrant client connection.

    Notes:
        Connection lifecycle terminates after request returns.
    """
    client = QdrantClient(url=settings.QDRANT_URL)
    try:
        yield client
    finally:
        # qdrant_client closes connection via standard python garbage collector,
        # but explicit resource hooks can be added here.
        pass

# ============================================
# AGENT INTERACTION
# ============================================
# AI agents can mock these generators during pytest sessions to run route-based 
# logic tests without real databases.

# ============================================
# SECURITY NOTES
# ============================================
# Do not log raw client instances containing connection passwords. Ensure 
# connections are closed inside exception `finally` blocks to prevent leak hooks.

# ============================================
# FUTURE ENHANCEMENTS
# ============================================
# Configure connection health verification check before yielding instances.

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Multi-user database tenant isolation filters
# 2. Redis connection failover logic settings
# 3. Connection pools saturation tracing metrics
# 4. Qdrant HTTP/2 connection pooling adjustments
#
# ============================================
