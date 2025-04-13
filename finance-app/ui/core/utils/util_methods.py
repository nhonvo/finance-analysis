from datetime import datetime

import locale

locale.setlocale(locale.LC_ALL, "vi_VN.utf8")


def get_current_day_and_month():
    """Returns the current month and year."""
    now = datetime.now()
    return now.month, now.year


def get_monthly_range(month=None, year=None):
    """Calculate the range from 19th of the previous month to 18th of the current month."""
    # Ensure month and year have default values
    current_month, current_year = get_current_day_and_month()
    month = month or current_month
    year = year or current_year

    # Adjust for the case where month = 1 (previous month should be December of last year)
    start_month = 12 if month == 1 else month - 1
    start_year = year - 1 if month == 1 else year

    start_date = datetime(
        start_year, start_month, 19
    )  # Start from 19th of the previous month
    end_date = datetime(year, month, 18)  # End on 18th of the given month

    return start_date, end_date

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


def format_value(value):
    """Format numbers using Vietnamese locale with thousands separator."""
    if isinstance(value, (int, float)):
        formatted_value = locale.currency(value, grouping=True)  # Format as an integer with commas
        return formatted_value.replace(",00", "")  # Remove ",00" if present
    return value  # Return non-numeric values as they are
