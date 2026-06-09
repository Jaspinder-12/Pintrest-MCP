# Dockerfile
#
# Purpose:
# Run the minimal Pinterest MCP Server in a lightweight Python container.
#
# Dependencies:
# python:3.12-slim base image
#
# Usage:
# Build: docker build -t pinterest-mcp .
# Run: docker run -i pinterest-mcp
#
# Future Notes:
# - Add health check scripts for SSE transport modes

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose ports if running as SSE, though default is STDIO
EXPOSE 8000

CMD ["python", "src/server.py"]

# ============================================
# FUTURE IMPROVEMENTS
# ============================================
#
# 1. Image size optimization using distroless containers
# 2. Automated non-root user execution setup
#
# ============================================
