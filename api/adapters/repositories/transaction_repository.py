from datetime import datetime
from typing import List

from adapters.repositories.generic_repository import GenericRepository
from domain.models.transaction import Transaction


class TransactionRepository(GenericRepository[Transaction]):
    def filter_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Transaction]:
        return self.filter(lambda tx: start_date <= tx.transaction_date <= end_date)
