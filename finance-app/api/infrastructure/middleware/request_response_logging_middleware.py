from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging


logger = logging.getLogger("uvicorn")

class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        # logger.info(f"Request headers: {dict(request.headers)}")

        response: Response = await call_next(request)

        # Log the outgoing response
        logger.info(f"Response status: {response.status_code}")
        # logger.info(f"Response headers: {dict(response.headers)}")

        return response
