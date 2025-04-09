from datetime import date
from typing import List, Optional

from helper.csv_reader import read_transactions_from_csv
from helper.utils import clean_data, filter_transactions_by_date_range
from interfaces.generic_repository_interface import T, IGenericRepository


class GenericRepository(IGenericRepository[T]):
    def __init__(self):
        self._data = read_transactions_from_csv()

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
        if clean:
            self._data = clean_data(self._data)
        filtered_data = self._data
        filtered_data = filter_transactions_by_date_range(
            _data=self._data,
            start_date=start_date,
            end_date=end_date,
        )

        # Apply search filtering (query)
        if query:
            query = query.lower()
            filtered_data = [
                item
                for item in filtered_data
                if any(
                    hasattr(item, field)
                    and getattr(item, field, "").lower().find(query) != -1
                    for field in [
                        "description",
                        "category",
                        "transaction_code",
                        "counter_account",
                    ]
                )
            ]

        # Apply sorting
        if sort_by and hasattr(filtered_data[0], sort_by):
            filtered_data.sort(key=lambda x: getattr(x, sort_by), reverse=order_by)

        # Apply pagination
        if limit == -1:
            limit = None
        if offset is not None and limit is not None:
            return filtered_data[offset : offset + limit]
        return filtered_data
