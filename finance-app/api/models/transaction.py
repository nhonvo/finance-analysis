from pydantic import BaseModel
from datetime import date


class Transaction(BaseModel):
    transaction_date: date
    description: str
    effective_date: date
    debit: float
    credit: float
    balance: float
    counter_account: str
    category: str
    transaction_code: str
