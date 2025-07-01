from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger("uvicorn")

class GlobalExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            # Process the request
            response = await call_next(request)
            return response
        except Exception as exc:
            # Catch unexpected errors
            logger.error(f"Unexpected error occurred: {exc}, Path: {request.url.path}")
            return JSONResponse(
                {"detail": "Internal Server Error. Please try again later."},
                status_code=500
            )
