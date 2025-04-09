import logging
from functools import wraps

logger = logging.getLogger("uvicorn")


# ✅ Middleware Decorator for Logging & Exception Handling
def global_exception_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"Finished {func.__name__} successfully")
            return result
        except ValueError as ve:
            logger.error(f"Validation error in {func.__name__}: {ve}")
            raise
        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}: {e}")
            raise

    return wrapper
