FROM python:3.10 AS builder

ARG OPENAI_API_KEY

WORKDIR /app

COPY ./script.py /app/
COPY ./logger.conf /app/
COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN python script.py

FROM postgres:latest

COPY --from=builder /app/schema.sql /docker-entrypoint-initdb.d/
COPY --from=builder /app/data.sql /docker-entrypoint-initdb.d/
