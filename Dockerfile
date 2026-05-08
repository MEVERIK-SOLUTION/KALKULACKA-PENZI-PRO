# Dockerfile pro KALKULAČKA PENZÍ PRO API
# Multi-stage: nejdřív závislosti, pak aplikace

FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /usr/local /usr/local

COPY api/ ./api/
COPY src/ ./src/
COPY config/ ./config/
COPY alembic.ini ./
COPY alembic/ ./alembic/
COPY run.py ./

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

CMD ["sh", "-c", "alembic upgrade head 2>&1; uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
