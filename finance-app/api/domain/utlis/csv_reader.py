import pandas as pd
import logging
from typing import List

from domain.models.transaction import Transaction

logger = logging.getLogger("uvicorn")

_CACHED_TRANSACTIONS: List[Transaction] = []
_FILE_PATH = "D://1.Project//1.project//tool//tool-finance-analysis-py//data.xlsx"


def read_data_excel(path: str):
    df = pd.read_excel(path)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"], format="%d/%m/%Y")
    df["effective_date"] = pd.to_datetime(df["effective_date"], format="%d/%m/%Y")

    # Convert numeric columns safely
    df["debit"] = pd.to_numeric(df["debit"], errors="coerce").fillna(0)
    df["credit"] = pd.to_numeric(df["credit"], errors="coerce").fillna(0)
    df["balance"] = pd.to_numeric(df["balance"], errors="coerce").fillna(0)

    # Convert NaN in string fields to empty string
    df["counter_account"] = df["counter_account"].fillna("").astype(str)
    df["category"] = df["category"].fillna("").astype(str)
    df["transaction_code"] = df["transaction_code"].fillna("").astype(str)

    # Identify the index of rows to drop
    # index_to_drop = df[df['description'] == 'knvqs'].index

    # Drop the rows
    # df.drop(index=index_to_drop, inplace=True)
    return df


def read_transactions_from_csv(
    file_path: str = _FILE_PATH, reload: bool = False
) -> List[Transaction]:
    """Reads transactions from CSV and caches them. If reload=True, refresh the cache."""
    global _CACHED_TRANSACTIONS

    if reload:
        logger.info("🔄 Reloading transactions from CSV: %s", file_path)
        _CACHED_TRANSACTIONS.clear()

    if not _CACHED_TRANSACTIONS:
        logger.info(
            "📂 Loading transactions from CSV for the first time: %s", file_path
        )
        df = read_data_excel(file_path)
        # _CACHED_TRANSACTIONS = [Transaction(**row) for _, row in df.iterrows()]
        for _, row in df.iterrows():
            try:
                transaction = Transaction(**row.to_dict())
                _CACHED_TRANSACTIONS.append(transaction)
            except Exception as e:
                logger.error(f"🚨 Error processing row: {row.to_dict()}")
                logger.error(f"❌ Validation Error: {e}")
    else:
        logger.info(
            "⚡ Using cached transactions (%d items)", len(_CACHED_TRANSACTIONS)
        )

    return _CACHED_TRANSACTIONS
