from services.api_client import APIClient


def get_overview(params):
    """Fetch financial overview."""
    return APIClient.fetch_data("overview", params)


def get_summary(params):
    """Fetch summary data."""
    return APIClient.fetch_data("summary", params)


def get_income_expenditure(params):
    """Fetch income-expenditure data."""
    return APIClient.fetch_data("income-expenditure", params)


def get_transactions(
    params,
    limit=10,
    offset=0,
    sort_by="transaction_date",
    order_by=True,
    clean=True,
    search="",
):
    """Fetch the transactions."""
    transaction_params = {
        **params,
        "search": search,
        "limit": limit,
        "offset": offset,
        "sort_by": sort_by,
        "order_by": order_by,
        "clean": clean,
    }
    return APIClient.fetch_data("", transaction_params)


def get_saving_transactions(
    params,
):
    transaction_params = {
        **params,
    }
    return APIClient.fetch_data("saving", transaction_params)


def get_invest_transactions(
    params,
):
    transaction_params = {
        **params,
    }
    return APIClient.fetch_data("investment", transaction_params)


def get_balance_trends(year):
    """Fetches balance trends for a given year."""
    params = {
        "start_date": "2023-01-01",
        "end_date": f"{year}-12-31",
        "limit": -1,
        "offset": 0,
    }
    return APIClient.fetch_data("balance-trends", params)


def get_balance_trends_month(year, month, previos_month):
    """Fetches balance trends for a given year."""
    params = {
        "start_date": f"{year}-{previos_month}-19",
        "end_date": f"{year}-{month}-19",
        "limit": -1,
        "offset": 0,
    }
    return APIClient.fetch_data("balance-trends", params)

