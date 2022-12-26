#!/bin/sh

echo "Waiting for Postgres..."

while ! nc -z $BILLING_POSTGRES_HOST $POSTGRES_PORT; do
  >&2 echo "Postgres [$BILLING_POSTGRES_HOST]:[$POSTGRES_PORT] is unavailable - sleeping"
  sleep 0.4
done
echo "PostgreSQL started"

echo "Starting backend"

gunicorn src.main:app -w 9 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001
