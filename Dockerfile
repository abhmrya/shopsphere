FROM python:3.13-slim

# =========================================================
# PYTHON ENVIRONMENT
# =========================================================

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1

# =========================================================
# WORKING DIRECTORY
# =========================================================

WORKDIR /app

# =========================================================
# SYSTEM DEPENDENCIES
# =========================================================

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# =========================================================
# PYTHON DEPENDENCIES
# =========================================================

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# =========================================================
# APPLICATION CODE
# =========================================================

COPY services ./services

# =========================================================
# NON-ROOT USER
# =========================================================

RUN useradd \
        --create-home \
        --shell /bin/bash \
        appuser \
    && chown -R appuser:appuser /app

USER appuser

# =========================================================
# DEFAULT COMMAND
# =========================================================

CMD ["uvicorn", "services.auth_service.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
