# Use Python 3.11 slim image as builder
FROM python:3.11-slim AS builder

# Set work directory for builder
WORKDIR /app

# Set build environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        postgresql-client \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Set runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=gda.settings \
    PATH="/home/app/.local/bin:$PATH"

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user and required directories
RUN useradd --create-home --shell /bin/bash app && \
    mkdir -p /wheels /app/static /app/media && \
    chown -R app:app /app /wheels /home/app

# Copy wheels and requirements from builder
COPY --from=builder --chown=app:app /app/wheels /wheels/
COPY --from=builder --chown=app:app /app/requirements.txt .

# Copy project files
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Install Python packages and clean wheels
RUN pip install --no-cache-dir --user --no-index --find-links=/wheels -r requirements.txt && \
    find /wheels -type f -delete

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/admin/ || exit 1

# Run the application
CMD ["gunicorn", "gda.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2", "--timeout", "120"]