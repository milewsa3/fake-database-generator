FROM python:3.10 AS builder

ARG OPENAI_API_KEY
ARG NUMBER_OF_TABLES

WORKDIR /app

COPY ./scripts/ /app/
COPY ./schemas /app/schemas

RUN pip install --no-cache-dir -r requirements.txt
RUN python script.py

FROM postgres:latest

COPY --from=builder /app/created_schema.sql /docker-entrypoint-initdb.d/
COPY --from=builder /app/data.sql /docker-entrypoint-initdb.d/