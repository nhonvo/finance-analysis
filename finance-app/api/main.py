from fastapi import FastAPI, Request
from presentation.v1 import api_router
import logging
import uvicorn

logger = logging.getLogger("uvicorn")

app = FastAPI(title="Finance API")

app.include_router(api_router.api_router, prefix="/api/v1")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


if __name__ == "__main__":
    logger = logging.getLogger("uvicorn")
    logger.info("🚀 Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1")
