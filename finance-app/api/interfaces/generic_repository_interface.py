from datetime import date
from typing import Generic, Optional, TypeVar, List
from abc import ABC, abstractmethod

T = TypeVar("T")


class IGenericRepository(ABC, Generic[T]):
    @abstractmethod
    def get(
        self,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order_by: Optional[bool] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        clean: Optional[bool] = None,
    ) -> List[T]:
        pass
