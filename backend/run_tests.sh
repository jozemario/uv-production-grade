#!/bin/bash
set -e

# Load test environment variables
export $(cat .env.test | xargs)

# Run tests
uv run pytest tests/ -v --asyncio-mode=auto 