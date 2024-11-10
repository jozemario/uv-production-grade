from contextlib import asynccontextmanager
# from dotenv import load_dotenv

# load_dotenv()

import logging
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.core.config import get_config
from app.api import router 
from app.core.init_db import init_app
from app.core.config import get_config
from app.middleware.auth_debug import AuthDebugMiddleware
config = get_config()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_app()
    yield

app = FastAPI(title=config.PROJECT_NAME, version=config.PROJECT_VERSION, openapi_url=f'{config.API_V1_STR}/openapi.json', lifespan=lifespan)

# init_settings()

environment = os.getenv("ENVIRONMENT", "dev")  # Default to 'development' if not set


# if environment == "dev":
logger = logging.getLogger("uvicorn")
logger.warning(f"Running in development mode - allowing CORS for {config.CORS_ORIGINS.split(',')} origins")
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS.split(',') ,
    # allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
app.add_middleware(AuthDebugMiddleware)
# Redirect to documentation page when accessing base URL
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


app.include_router(router)


if __name__ == "__main__":
    app_host = os.getenv("APP_HOST", "0.0.0.0")
    app_port = int(os.getenv("APP_PORT", "8000"))
    reload = True if environment == "dev" else False

    uvicorn.run(app="main:app", host=app_host, port=app_port, reload=reload)