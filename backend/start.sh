#!/bin/bash

# Wait for the database to be ready
while ! nc -z db 5432; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is ready!"

echo "Running migrations..."
uv run alembic upgrade head

echo "Starting the application..."
uv run python main.py
# uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
