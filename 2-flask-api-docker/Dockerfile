# ============================================================
# Multi-stage Dockerfile — Flask API
# Stage 1: Build dependencies
# Stage 2: Production image (minimal, no dev tools)
# Author: Gaurav Kumar
# ============================================================

# ── Stage 1: Build ──────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build tools (only needed for compiling packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install to a local directory (copied to final stage)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Production ─────────────────────────────────────
FROM python:3.12-slim AS production

# Security: run as non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Runtime dependencies only (no gcc, no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root
USER appuser

# Gunicorn config
ENV FLASK_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE 8000

# Health check — ALB uses this
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/health || exit 1

# Gunicorn: 4 workers, bind to 0.0.0.0
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "wsgi:app"]
