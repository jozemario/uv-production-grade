#!/bin/bash

# Wait for the database to be ready
while ! nc -z db 5432; do
  echo "Waiting for database to be ready..."
  sleep 2
done

echo "Database is ready!"

# Create a virtual environment
uv venv
source .venv/bin/activate
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
# load environment variables
uv run --env-file ../.env -- echo "ENVIRONMENT: $ENVIRONMENT"
# Apply database migrations
uv run alembic upgrade head 

# Load initial data
# python3 todos/scripts/initial_data.py

# Start the FastAPI server
uv run python main.py 
# exec uvicorn app.main:app --host 0.0.0.0 --port 8000
