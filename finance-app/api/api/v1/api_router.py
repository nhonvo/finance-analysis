from fastapi import APIRouter

from api.v1.endpoints import transactions

api_router = APIRouter()

# Include each router from endpoint modules with a prefix and tags
api_router.include_router(
    transactions.router, prefix="/transactions", tags=["Transactions"]
)
