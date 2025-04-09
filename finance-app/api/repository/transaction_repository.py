from datetime import datetime
from typing import List

from models.transaction import Transaction
from repository.generic_repository import GenericRepository

class TransactionRepository(GenericRepository[Transaction]):
    def filter_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Transaction]:
        return self.filter(lambda tx: start_date <= tx.transaction_date <= end_date)
