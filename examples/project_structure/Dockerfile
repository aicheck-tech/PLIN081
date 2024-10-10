FROM public.ecr.aws/docker/library/python:3.12.3-slim-bullseye AS project

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

ARG USER=app

RUN adduser --system --no-create-home "$USER"

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY our_app /app

EXPOSE 8080

USER $USER

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", ":8080"]