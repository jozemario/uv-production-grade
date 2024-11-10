from fastapi import Request
import logging
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
logger = logging.getLogger(__name__)

class AuthDebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # Log request details
        logger.info(f"Request path: {request.url.path}")
        logger.info(f"Request method: {request.method}")
        logger.info("Request headers:")
        for name, value in request.headers.items():
            if name.lower() == "authorization":
                logger.info(f"  {name}: Bearer <token>")  # Don't log the actual token
            else:
                logger.info(f"  {name}: {value}")

        # Process the request
        response = await call_next(request)
        
        # Log response status
        logger.info(f"Response status: {response.status_code}")
        
        return response