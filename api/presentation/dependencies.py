from fastapi import Depends
from adapters.repositories.transaction_repository import TransactionRepository
from domain.interfaces.transaction_service_interface import ITransactionService
from domain.services.transaction_service import TransactionService

def get_transaction_repository() -> TransactionRepository:
    return TransactionRepository()  

def get_transaction_service(
    repository: TransactionRepository = Depends(get_transaction_repository),
) -> ITransactionService:
    return TransactionService(repository)