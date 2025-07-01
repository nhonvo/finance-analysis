from fastapi import FastAPI
from infrastructure.middleware.global_exception_middleware import (
    GlobalExceptionMiddleware,
)
from infrastructure.middleware.request_response_logging_middleware import (
    RequestResponseLoggingMiddleware,
)
from presentation.v1 import api_router
import logging
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger("uvicorn")

app = FastAPI(title="Finance API")

# Register the middleware
app.add_middleware(GlobalExceptionMiddleware)
app.add_middleware(RequestResponseLoggingMiddleware)

app.include_router(api_router.api_router, prefix="/api/v1")

# Allow all CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


if __name__ == "__main__":
    logger = logging.getLogger("uvicorn")
    logger.info("🚀 Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1")
