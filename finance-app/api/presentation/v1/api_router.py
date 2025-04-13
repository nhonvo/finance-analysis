from fastapi import APIRouter

from api.v1.endpoints import transactions, health


api_router = APIRouter()

api_router.include_router(
    transactions.router, prefix="/transactions", tags=["Transactions"]
)
api_router.include_router(health.router, prefix="/health", tags=["health-check"])
