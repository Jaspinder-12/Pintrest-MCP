# Dockerfile
#
# Purpose:
# Containerizes the FastAPI Visual Core API.
#
# Dependencies:
# Python 3.12-slim base image
#
# Usage:
# Run: docker build -t pinterest-mcp/core-api -f services/core-api/Dockerfile .
#
# Notes:
# Implements multi-stage compilation for performance.
#
# Future Improvements:
# - Add GPU-acceleration base images for local model runs
# - Integrate dynamic secrets vault pulling

# ============================================
# BUILD STAGE
# ============================================
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip install --no-cache-dir --user -r requirements.txt

# ============================================
# RUNTIME STAGE
# ============================================
FROM python:3.12-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
COPY --from=builder /build/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY services/core-api/app/ ./app/

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Multi-arch build pipeline support
# 2. Alpine-based runner transition if packages allow
#
# ============================================
