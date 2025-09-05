FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir uv
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY src/uv.lock /app/uv.lock

RUN uv venv
RUN uv pip install -r uv.lock

COPY src /app/src
COPY data /app/data

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/src

# Expose port and run uvicorn
EXPOSE 8000
CMD ["gunicorn", "tasks.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8070", "--workers", "4"]
