from typing import List
from datetime import date

from domain.models.transaction import Transaction


@staticmethod
def hidden_data(
    transactions: List[Transaction], column: str, value: str
) -> List[Transaction]:
    """Filters out transactions where the specified column contains the given value (case-insensitive)."""
    value_lower = value.lower()

    filtered_transactions = [
        tx
        for tx in transactions
        if value_lower not in str(getattr(tx, column, "")).lower()
    ]

    return filtered_transactions


@staticmethod
def clean_data(transactions: List[Transaction]) -> List[Transaction]:
    """Cleans transaction data by removing entries based on specific filtering rules."""
    filters = [
        ("description", "TAT TOAN TAI KHOAN TIET KIEM"),
        ("description", "CONG TY TNHH PHAN MEM FPT "),
        ("description", "TRA LAI TIEN GUI TK"),
        ("description", "Tiết kiệm Điện tử"),
        ("counter_account", "TAT TOAN TAI KHOAN TIET KIEM"),
        ("description", "tiền nhận hộ cty"),
        ("description", "đầu tư"),
        ("category", "saving"),
        ("category", "invest"),
    ]

    for column, value in filters:
        transactions = hidden_data(transactions, column, value)

    return transactions


@staticmethod
def get_saving_transactions(transactions: List[Transaction]) -> List[Transaction]:
    """Filter transactions related to savings."""
    saving_keywords = [
        "TAT TOAN TAI KHOAN TIET KIEM",
        "Tiết kiệm Điện tử",
        "DONG TIET KIEM TK",
        "TAT TOAN SO TIET KIEM",
    ]

    saving_transactions = [
        tx
        for tx in transactions
        if any(tx.description.startswith(keyword) for keyword in saving_keywords)
        or tx.category.startswith("saving")
    ]

    for tx in saving_transactions:
        tx.category = tx.category or "saving"  # Ensure category is not None
        tx.balance = tx.debit - tx.credit  # Calculate balance

    return saving_transactions


@staticmethod
def get_investment_transactions(transactions: List[Transaction]) -> List[Transaction]:
    """Filter transactions related to investments."""
    investment_transactions = [
        tx
        for tx in transactions
        if tx.description.startswith("đầu tư") or tx.category.startswith("invest")
    ]

    for tx in investment_transactions:
        tx.category = tx.category or "invest"  # Ensure category is not None
        tx.balance = tx.debit - tx.credit  # Calculate balance

    return investment_transactions


@staticmethod
def filter_transactions_by_date_range(
    _data: List[Transaction], start_date: date, end_date: date
) -> List[Transaction]:
    """Filters transactions within the given start_date and end_date range."""

    return [tx for tx in _data if start_date <= tx.transaction_date <= end_date]


# @staticmethod
# def filter_transactions_by_date_range(
#     _data:List[Transaction],
#     start_year: int,
#     start_month: int,
#     end_year: int,
#     end_month: int,
#     start_day: Optional[int] = 1,
#     end_day: Optional[int] = None,
# ) -> List:
#     """Filters transactions within the given year, month, and optional day range."""

#     # Determine the last day of the end month if end_day is not provided
#     if end_day is None:
#         first_day_next_month = date(end_year, end_month, 1) + timedelta(days=31)
#         last_day = first_day_next_month.replace(day=1) - timedelta(days=1)
#         end_day = last_day.day  # Get actual last day of the month

#     start_date = date(start_year, start_month, start_day)
#     end_date = date(end_year, end_month, end_day)

#     return [
#         tx for tx in _data if start_date <= tx.transaction_date <= end_date
#     ]
