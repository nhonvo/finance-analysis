from typing import List, Optional
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
def filter_transactions(
    transactions: List[Transaction],
    description_keywords: List[str],
    category_prefix: Optional[str] = None,
    default_category: Optional[str] = None,
) -> List[Transaction]:
    """
    Filter transactions based on description keywords or category prefix,
    and calculate the balance for each filtered transaction.

    Args:
        transactions (List[Transaction]): List of transactions to filter.
        description_keywords (List[str]): List of description start keywords.
        category_prefix (Optional[str]): Category prefix filter (e.g., 'saving').
        default_category (Optional[str]): Default category to assign if missing.

    Returns:
        List[Transaction]: Filtered transactions with balance and category set.
    """
    filtered = [
        tx for tx in transactions
        if any(tx.description.startswith(keyword) for keyword in description_keywords)
        or (category_prefix and tx.category and tx.category.startswith(category_prefix))
    ]

    for tx in filtered:
        if not tx.category and default_category:
            tx.category = default_category
        tx.balance = tx.debit - tx.credit

    return filtered

@staticmethod
def filter_transactions_by_date_range(
    _data: List[Transaction], start_date: date, end_date: date
) -> List[Transaction]:
    """Filters transactions within the given start_date and end_date range."""

    return [tx for tx in _data if start_date <= tx.transaction_date <= end_date]


@staticmethod
def categorize_expense(description, category=None):
    # Dictionary mapping keywords to categories
    category_map = {
        # Existing mappings
        "xăng": "Fuel",
        "nước": "Utilities",
        "điện": "Utilities",
        "TRAN MINH DAT": "Rent",
        "nhà": "Rent",
        "quản lý": "Management Fees",
        "internet": "Internet",
        "wifi": "Internet",
        "thuốc": "Health",
        "sức khỏe": "Health",
        "đo mắt": "Health",
        "khám tai": "Health",
        # New mappings
        "AN CHOI": "Entertainment",
        "BAO HIEM": "Insurance",
        "BENH VIEN DA KHOA": "Healthcare",
        "Long Châu": "Pharmacy",
        "RUT TIEN BANG QRC": "Cash Withdrawal",
        "VO THUONG TRUONG NHON": "Personal",
        "VPS": "Investment",
        "VPS-VO THUONG TRUONG NHON": "Investment",
        "Xe Hoàng Đạt": "Transportation",
        "Xe Phương Trang": "Transportation",
        "bbgym2": "Gym",
        "bhc cinema": "Entertainment",
        "fpt telecom": "Internet",
        "hutech": "Education",
        "ngày 8/3": "Gifts",
        "nha khoa": "Healthcare",
        "vinaphone": "Telecommunications",
        "hiệp gà barber": "Barber",
        "đông tây barber": "Barber",
        "cinestar": "Entertainment",
        "tk tgtt cn cong hoa": "Bank Transfer",
        "truong dai hoc cong nghe tphcm": "Education",
        "cty cp dich vu di dong truc tuyen": "Online Services",
        "coopmart": "Supermarket",
        "emart": "Supermarket",
        "siêu thị": "Supermarket",
        "winmart": "Supermarket",
        "nguyen le tan binh": "Personal Transfer",
        "pham minh thu": "Personal Transfer",
        "nhớt": "Vehicle Maintenance",
        "sửa xe": "Vehicle Maintenance",
        "honda head": "Vehicle Maintenance",
        "rửa xe": "Vehicle Maintenance",
        "NGUYEN THI MY NHAN": "Team",
        "HA THI MY TRAM": "Team",
        "circleK": "Convenience Store",
        "familymart": "Convenience Store",
        "gs25": "Convenience Store",
        "7eleven": "Convenience Store",
        "sendo": "Food",
        "bhx": "Food",
        "phong ký 2": "Food",
        "mì tôm": "Food",
        "cuốn thịt nướng": "Food",
        "canh chua": "Food",
        "canh cá lóc": "Food",
        "xiên bẩn": "Food",
        "xôi": "Food",
        "UTOP": "Food",
        "quán gỏi cá lăn": "Restaurant",
        "hương biển": "Restaurant",
        "chè": "Beverage",
        "mixue": "Beverage",
        "suncha": "Beverage",
        "tàu hủ": "Beverage",
        "cafe máy": "Beverage",
        "café": "Beverage",
        "nước dừa": "Beverage",
        "rau má": "Beverage",
        "sinh tố": "Beverage",
        "sữa hạt": "Beverage",
        "trà": "Beverage",
        "cây đồ uống": "Beverages",
        "coca": "Beverages",
        "tiktok": "Shopping",
        "Click buy": "Shopping",
        "mazo": "Shopping",
        "shopee": "Shopping",
        "simime shop": "Shopping",
        "chạm lá": "Shopping",
        "cellphoneS": "Shopping",
        "TPBANK": "Banking",
        "VISA": "Banking",
        "tpbank": "Banking",
        "phở gia truyền": "Food",
        "HO NGUYEN DUY": "Rent",
        "CN CTY CP VIEN THONG FPT": "Internet",
        "Quy Nhon Trip": "Quy Nhon Trip",
    }

    category_map = {
        keyword.lower(): category for keyword, category in category_map.items()
    }

    if category == "saving":
        return "saving"
    elif category == "team":
        return "team"
    elif category == "invest":
        return "Investment"
    elif category == "foodOffice":
        return "Food in office"
    elif category == "food":
        return "Food"
    elif category == "rent":
        return "rent"
    # elif category == "chi phí":
    #     return "expense"
    elif category == "cash":
        return "cash"
    elif category == "health":
        return "health"
    elif category == "Education":
        return "Education"
    elif category == "shopping":
        return "shopping"
    elif category == "income":
        return "income"

    # Add any other specific mappings as needed

    description = str(description).lower()

    # Find the first matching category based on keywords
    return next(
        (
            category
            for keyword, category in category_map.items()
            if keyword in description
        ),
        "Others",  # Default category if no match found
    )


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
