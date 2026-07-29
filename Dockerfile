FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir poetry==1.8.3
WORKDIR /build
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true && poetry install --only main --no-root --no-interaction

FROM python:3.11-slim AS runtime
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev curl && rm -rf /var/lib/apt/lists/*
RUN addgroup --system --gid 1001 appuser && adduser --system --uid 1001 --gid appuser appuser
WORKDIR /app
COPY --from=builder /build/.venv .venv
COPY src/ src/
COPY configs/ configs/
RUN chown -R appuser:appuser /app
USER appuser
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=10s \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--log-level", "info"]
