from fastapi import Depends
from interfaces.transaction_service_interface import ITransactionService
from repository.transaction_repository import TransactionRepository
from services.transaction_service import TransactionService


def get_transaction_repository() -> TransactionRepository:
    return TransactionRepository()  # You can modify this to use a real database session

def get_transaction_service(
    repository: TransactionRepository = Depends(get_transaction_repository),
) -> ITransactionService:
    return TransactionService(repository)