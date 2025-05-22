from collections import defaultdict
from datetime import date
import datetime
from typing import Any, Dict, List, Optional
import logging

from adapters.repositories.transaction_repository import TransactionRepository
from domain.models.transaction import Transaction
from domain.utlis.clean_data import (
    categorize_expense,
    clean_data,
    get_investment_transactions,
    get_saving_transactions,
)

logger = logging.getLogger("uvicorn")


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self.repository = repository

    def _validate_dates(
        self, start_date: Optional[date], end_date: Optional[date]
    ) -> bool:
        """Validates date inputs and converts them if necessary."""
        try:
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if start_date and end_date and start_date > end_date:
                logger.warning(f"Invalid date range: {start_date} > {end_date}")
                return False
            return True
        except ValueError as e:
            logger.error(f"Invalid date format: {e}")
            return False

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
    ) -> List[Transaction]:
        """Fetches transactions with optional filtering and pagination."""
        try:
            return self.repository.get(
                query=query,
                limit=limit,
                offset=offset,
                order_by=order_by,
                sort_by=sort_by,
                start_date=start_date,
                end_date=end_date,
                clean=clean,
            )
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return []

    def get_saving(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Transaction]:
        try:
            transactions = self.repository.get(
                start_date=start_date, end_date=end_date, limit=-1
            )
            clean_transactions = get_saving_transactions(transactions)

            return clean_transactions
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return []

    def get_investment(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> List[Transaction]:
        try:
            transactions = self.repository.get(
                start_date=start_date, end_date=end_date, limit=-1
            )

            clean_transactions = get_investment_transactions(transactions)

            return clean_transactions
        except Exception as e:
            logger.error(f"Error fetching transactions: {e}")
            return []

    def income_expenditure_analysis(
        self, start_date: Optional[date], end_date: Optional[date]
    ) -> List[Dict]:
        """Analyzes income and expenditure for a given range of years and months."""
        if not self._validate_dates(start_date, end_date):
            return []

        try:
            transactions_filtered = self.repository.get(
                start_date=start_date, end_date=end_date
            )
            summary = defaultdict(lambda: {"income": 0.0, "expenditure": 0.0})

            for tx in transactions_filtered:
                key = (tx.transaction_date.year, tx.transaction_date.month)
                summary[key]["income"] += tx.credit
                summary[key]["expenditure"] += tx.debit

            return [
                {"year": year, "month": month, **data}
                for (year, month), data in sorted(summary.items())
            ]
        except Exception as e:
            logger.error(f"Error analyzing income and expenditure: {e}")
            return []

    def generate_overview_section(
        self, start_date: Optional[date], end_date: Optional[date]
    ) -> Dict[str, Any]:
        """Generates an overview of income, expense, and savings."""
        try:
            transactions = self.repository.get(start_date=start_date, end_date=end_date)
            saving_transactions = get_saving_transactions(transactions)
            investment_transactions = get_investment_transactions(transactions)
            saving_balance = sum(tx.balance for tx in saving_transactions)
            investment_balance = sum(tx.balance for tx in investment_transactions)

            clean_transactions = clean_data(transactions)
            total_income = (
                sum(tx.credit for tx in clean_transactions)
                + saving_balance
                + investment_balance
            )
            total_expense = sum(tx.debit for tx in clean_transactions)
            total_saving = saving_balance + investment_balance

            return {
                "income": total_income,
                "expense": total_expense,
                "saving": total_saving,
            }

        except Exception as e:
            logger.error(f"Error generating overview section: {e}")
            return []

    def generate_summary(
        self,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> Dict[str, Any]:
        """Generates a financial summary including total assets and transaction count."""
        try:
            transactions = self.repository.get(start_date=start_date, end_date=end_date)
            saving_transactions = get_saving_transactions(transactions)
            investment_transactions = get_investment_transactions(transactions)
            saving_balance = sum(tx.balance for tx in saving_transactions)
            investment_balance = sum(tx.balance for tx in investment_transactions)

            clean_transactions = clean_data(transactions)
            saving_balance = sum(tx.balance for tx in saving_transactions)
            investment_balance = sum(tx.balance for tx in investment_transactions)
            balance = clean_transactions[0].balance if clean_transactions else 0
            total_asset = balance + saving_balance + investment_balance
            transaction_count = len(clean_transactions)

            return {
                "total": total_asset,
                "balance": balance,
                "totalSaving": saving_balance,
                "invest": investment_balance,
                "transactions": transaction_count,
            }
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return {}

    def balance_trends(
        self,
        offset: int,
        start_date: Optional[date],
        end_date: Optional[date],
        limit: int = -1,
    ) -> List[Dict[str, Any]]:
        """Computes balance trends over time."""
        try:
            filtered_transactions = self.repository.get(
                start_date=start_date, end_date=end_date, limit=limit, offset=offset
            )
            filtered_transactions = filtered_transactions[offset : offset + limit]
            daily_balances = defaultdict(float)

            for tx in sorted(filtered_transactions, key=lambda t: t.transaction_date):
                day_key = tx.transaction_date.strftime("%Y-%m-%d")
                daily_balances[day_key] = tx.balance

            return [
                {"date": day, "balance": balance}
                for day, balance in daily_balances.items()
            ]
        except Exception as e:
            logger.error(f"Error computing balance trends: {e}")
            return []


    def expense_tree(
        self,
        offset: int,
        start_date: Optional[date],
        end_date: Optional[date],
        limit: int = -1,
    ) -> List[Dict[str, Any]]:
        try:
            # Fetch transactions from repository
            filtered_transactions = self.repository.get(
                start_date=start_date, end_date=end_date, limit=limit, offset=offset
            )

            # Slice the list if needed
            filtered_transactions = (
                filtered_transactions[offset : offset + limit]
                if limit != -1
                else filtered_transactions
            )

            # Prepare a category sum map
            category_totals = defaultdict(float)

            for tx in filtered_transactions:
                debit = tx.debit
                description = tx.counter_account
                category = tx.category

                if debit is None or not description:
                    continue

                expense_category = categorize_expense(description, category)
                category_totals[expense_category] += debit

            # Format for frontend Treemap
            result = [
                {"name": name, "size": amount}
                for name, amount in category_totals.items()
                if amount > 0
            ]

            return result

        except Exception as e:
            logger.error(f"Error computing expense tree: {e}")
            return []
