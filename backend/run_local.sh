#!/bin/bash
export $(grep -v '^#' ../.env.local | xargs)
echo "ENVIRONMENT: $ENVIRONMENT"
echo "POSTGRES_HOST: $POSTGRES_HOST"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
echo "CORS_ORIGINS: $CORS_ORIGINS"
echo "FRONT_END_BASE_URL: $FRONT_END_BASE_URL"
echo "JWT_SECRET_KEY: $JWT_SECRET_KEY"
echo "SMTP_HOST: $SMTP_HOST"
echo "SMTP_PORT: $SMTP_PORT"
echo "SMTP_USER: $SMTP_USER"
echo "SMTP_PASSWORD: $SMTP_PASSWORD"
echo "EMAILS_FROM_EMAIL: $EMAILS_FROM_EMAIL"
echo "EMAILS_FROM_NAME: $EMAILS_FROM_NAME"
echo "JWT_LIFETIME_SECONDS: $JWT_LIFETIME_SECONDS"
echo "API_V1_STR: $API_V1_STR"
echo "PROJECT_NAME: $PROJECT_NAME"
echo "PROJECT_VERSION: $PROJECT_VERSION"
echo "POSTGRES_URI: $POSTGRES_URI"

# uv python pin pypy@3.13.0
# uv venv --python 3.13.0 -- --managed 
uv venv
source .venv/bin/activate
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
#load environment variables
uv run --env-file ../.env.local -- echo "ENVIRONMENT: $ENVIRONMENT"
uv run alembic upgrade head 
#uv run python -m app.core.init_db
#uv run python app/scripts/initial_data.py
uv run python main.py
#uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
#uv run alembic revision --autogenerate -m "fix_relationships"

