from typing import Optional, List
from abc import ABC, abstractmethod
from datetime import date
from typing import Any, Dict

from domain.models.transaction import Transaction


class ITransactionService(ABC):
    @abstractmethod
    def get_transactions(
        self,
        query: Optional[str],
        limit: int,
        offset: int,
        sort_by: str,
        order_by: bool,
        start_date: Optional[date],
        end_date: Optional[date],
        clean: bool,
    ) -> list[Transaction]:
        pass

    @abstractmethod
    def income_expenditure_analysis(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Dict]:
        """Analyzes income and expenditure for a given range of years and months."""
        pass

    @abstractmethod
    def get_saving(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Transaction]:
        pass

    @abstractmethod
    def get_investment(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Transaction]:
        pass

    @abstractmethod
    def generate_overview_section(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def generate_summary(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def balance_trends(
        self,
        limit: int,
        offset: int,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Dict[str, any]]:
        """Computes the last balance for each day within the date range and returns structured data."""
        pass
