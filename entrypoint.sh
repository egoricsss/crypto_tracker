#!/bin/bash
set -e

echo "Waiting for database to be ready..."
until pg_isready -h db -p 5432 -U "${POSTGRES_USER:-crypto_user}" -d "${POSTGRES_DB:-crypto_tracker}"; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is up - running migrations..."
alembic upgrade head

echo "Starting Celery with command: $@"
exec "$@"
