#!/bin/sh

echo "Waiting for Postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  >&2 echo "Postgres [$POSTGRES_HOST]:[$POSTGRES_PORT] is unavailable - sleeping"
  sleep 0.4
done
echo "PostgreSQL started"

echo "Starting backend"

python ./src/main.py