from fastapi import APIRouter, Query, Depends
from datetime import date
from typing import List, Dict, Any, Optional
from domain.interfaces.transaction_service_interface import ITransactionService
from presentation.dependencies import get_transaction_service
from domain.models.transaction import Transaction

router = APIRouter()


@router.get("/", response_model=List[Transaction])
def list_transactions(
    search: Optional[str] = None,
    limit: int = Query(10, ge=-1),
    offset: int = Query(0, ge=0),
    order_by: bool = False,
    sort_by: str = "transaction_date",
    start_date: Optional[date] = "2023-01-01",
    end_date: Optional[date] = "2025-12-31",
    clean: bool = False,
    service: ITransactionService = Depends(get_transaction_service),
):
    """Retrieve transactions with optional filters and sorting.
    limit = -1 => all of transacitons
    """
    return service.get_transactions(
        query=search,
        limit=limit,
        offset=offset,
        order_by=order_by,
        sort_by=sort_by,
        start_date=start_date,
        end_date=end_date,
        clean=clean,
    )


@router.get("/income-expenditure", response_model=List[Dict[str, Any]])
def analyze_income_expenditure(
    start_date: Optional[date] = "2023-01-01",
    end_date: Optional[date] = "2025-12-31",
    service: ITransactionService = Depends(get_transaction_service),
):
    """Analyze and return income vs. expenditure statistics."""
    return service.income_expenditure_analysis(
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/overview", response_model=Dict[str, Any])
def get_transaction_overview(
    start_date: Optional[date] = "2023-01-01",
    end_date: Optional[date] = "2025-12-31",
    service: ITransactionService = Depends(get_transaction_service),
):
    """Generate an overview section for transactions."""
    return service.generate_overview_section(
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/investment", response_model=List[Transaction])
def get_investment(
    start_date: Optional[date] = "2023-01-01",
    end_date: Optional[date] = "2025-12-31",
    service: ITransactionService = Depends(get_transaction_service),
):
    """Generate an overview section for transactions."""
    return service.get_investment(
        start_date=start_date,
        end_date=end_date,
    )


@router.get("/saving", response_model=List[Transaction])
def get_saving(
    start_date: Optional[date] = "2023-01-01",
    end_date: Optional[date] = "2025-12-31",
    service: ITransactionService = Depends(get_transaction_service),
):
    """Generate an overview section for transactions."""
    return service.get_saving(
        start_date=start_date,
        end_date=end_date,
    )

@router.get("/summary", response_model=Dict[str, Any])
def get_transaction_summary(
    start_date: Optional[date] = "2023-01-01",
    end_date: Optional[date] = "2025-12-31",
    service: ITransactionService = Depends(get_transaction_service),
):
    """Generate a summary of transactions."""
    return service.generate_summary(
        start_date=start_date,
        end_date=end_date,
    )

@router.get("/balance-trends", response_model=List[Dict[str, Any]])
def get_balance_trends(
    limit: int = Query(10, ge=-1),
    offset: int = Query(0, ge=0),
    start_date: Optional[date] = "2023-01-01",
    end_date: Optional[date] = "2025-12-31",
    service: ITransactionService = Depends(get_transaction_service),
):
    """Retrieve balance trends over time."""
    return service.balance_trends(
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        offset=offset,
    )

