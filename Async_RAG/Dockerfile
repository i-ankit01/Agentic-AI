FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY Async_RAG/requirements-docker.txt ./requirements-docker.txt
RUN pip install --no-cache-dir -r requirements-docker.txt

COPY Async_RAG ./Async_RAG

EXPOSE 8000