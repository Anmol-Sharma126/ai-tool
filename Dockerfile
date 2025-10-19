# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Copy project metadata first to leverage build cache
COPY pyproject.toml readme.md /app/

# Install project (prod)
RUN pip install --upgrade pip && pip install .

# Copy source
COPY src /app/src

# Expose API port
EXPOSE 8000

# Default command runs the API server
CMD ["uvicorn", "ai_bots.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
