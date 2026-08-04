FROM python:3.12.8-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -r -g 1001 eventnexus && \
    useradd -r -u 1001 -g eventnexus -s /bin/sh eventnexus

FROM base AS deps
COPY pyproject.toml ./
COPY app ./app
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir . && \
    rm -rf /root/.cache

FROM base AS runtime
COPY --from=deps /opt/venv /opt/venv
COPY app ./app

RUN chown -R eventnexus:eventnexus /app
USER eventnexus

ENV PATH="/opt/venv/bin:$PATH"
ENV VIRTUAL_ENV="/opt/venv"

EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8001/health', timeout=5).status==200 else 1)" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
