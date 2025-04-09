from application.monthly_service import monthly_service
from presentation.components.navbar import get_header, get_menu

from presentation.components.table_components import (
    make_dash_table_dict,
    make_dash_table_list,
)
from services.transaction_service import (
    get_income_expenditure,
    get_invest_transactions,
    get_overview,
    get_saving_transactions,
    get_summary,
    get_balance_trends_month,
)
import pandas as pd
from utils.util_methods import format_value, get_current_day_and_month
from datetime import datetime
from time import strptime
import plotly.graph_objects as go
from dash import dcc, html
from services.transaction_service import (
    get_transactions,
)
from presentation.layout import (
    get_section,
)
import locale

locale.setlocale(locale.LC_ALL, "vi_VN.utf8")


def create_layout(app, month=None, year=None):
    if year is None or month is None:
        (month, year) = get_current_day_and_month()
        previos_month = month - 1
        # month = month + 1
        if previos_month == 1:
            month = 12
        # month = month + 1
        month = f"{month:02X}"
        previos_month = f"{previos_month:02X}"
    # Generate data for each component

    params = {
        "start_date": f"{year}-{previos_month}-19",
        "end_date": f"{year}-{month}-19",
    }

    monthly_transaction = get_transactions(params, limit=-1)
    saving_transactions = get_saving_transactions(params)
    invest_transactions = get_invest_transactions(params)

    monthlyDashboard = monthly_service(
        month_df=pd.DataFrame(monthly_transaction),
        saving_df=pd.DataFrame(saving_transactions),
        investigate_df=pd.DataFrame(invest_transactions),
    )
    # Logic in API
    overview = get_overview(params)
    summary = get_summary(params)
    latest_transaction = get_transactions(params, limit=4, sort_by="transaction_date")
    balance_data = get_balance_trends_month(
        year=year, month=month, previos_month=previos_month
    )
    balance_trends_chart = balance_trends(balance_data) if balance_data else None

    top_4_highest_transaction = get_transactions(params, limit=4, sort_by="debit")
    detailed_debit_per_category_chiphi = get_transactions(
        params, limit=4, sort_by="debit", search="chi phí"
    )
    detailed_debit_per_category_utilities = get_transactions(
        params, limit=4, sort_by="debit", search="food"
    )
    detailed_debit_per_category_shopping = get_transactions(
        params, limit=4, sort_by="debit", search="shopping"
    )

    income_expenditure_data = get_income_expenditure(params)
    income_expenditure_chart_data = (
        income_expenditure_chart(income_expenditure_data)
        if income_expenditure_data
        else None
    )
    # Logic in UI
    transaction_distribution = monthlyDashboard.transaction_distribution()
    detailed_transaction_analysis = monthlyDashboard.detailed_transaction_analysis()
    expense_category_tree_map = monthlyDashboard.expense_category_tree_map()

    # Build layout
    return html.Div(
        [
            html.Div([get_header(), html.Br([]), get_menu()]),
            # Summary and Historical Transaction
            html.Div(
                [
                    # Header
                    get_section(
                        "Monthly",
                        f"The personal finance report start day 19th each month ({month})",
                    ),
                    overview_section(overview),
                    # Historical Transaction
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Summary", className="subtitle padded"),
                                    html.Table(make_dash_table_dict(summary)),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Historical Transaction",
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table_list(latest_transaction)
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Balance Trend
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Balance Trend", className="subtitle padded"
                                    ),
                                    dcc.Graph(
                                        id="graph-4",
                                        figure=balance_trends_chart,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Top 4 Highest Transactions
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Top 4 Highest Transactions",
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table_list(top_4_highest_transaction),
                                        className="tiny-header",
                                    ),
                                ],
                                style={"overflow-x": "auto"},
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Income and Expenditure Analysis
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Monthly Income and Expenditure Analysis",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="income-expenditure-analysis",
                                        figure=income_expenditure_chart_data,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                style={"overflow-x": "auto"},
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Transaction Distribution
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Transaction Distribution",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="transaction-distribution",
                                        figure=transaction_distribution,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                style={"overflow-x": "auto"},
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Detailed Transaction Analysis
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Daily Spending Overview: Detailed Breakdown of Expenses",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="detailed-transaction-analysis",
                                        figure=detailed_transaction_analysis,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                style={"overflow-x": "auto"},
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Expense Tree Map
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Expense Tree Map",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        figure=expense_category_tree_map,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row ",
                    ),
                    # Table detail debit per category
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Shopping expense",
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table_list(
                                            detailed_debit_per_category_shopping
                                        ),
                                        className="tiny-header",
                                    ),
                                ],
                                style={"overflow-x": "auto"},
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Utilities expense",
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table_list(
                                            detailed_debit_per_category_utilities
                                        ),
                                        className="tiny-header",
                                    ),
                                ],
                                style={"overflow-x": "auto"},
                                className="six columns",
                            ),
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Chi phi expense",
                                        className="subtitle padded",
                                    ),
                                    html.Table(
                                        make_dash_table_list(
                                            detailed_debit_per_category_chiphi
                                        ),
                                        className="tiny-header",
                                    ),
                                ],
                                style={"overflow-x": "auto"},
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )


def overview_section(data):
    return html.Div(
        className="section overview-section",
        children=[
            html.Div(
                className="overview-summary",
                children=[
                    html.Div(
                        className="overview-item",
                        children=[
                            html.H4(label),
                            html.P(
                                f"{format_value(value)}",
                                className="overview-value",
                            ),
                        ],
                    )
                    for label, value in data.items()
                ],
            ),
        ],
    )


def balance_trends(data):
    """Generate a balance trend chart from a list of balance records without using pandas."""
    # Convert date strings to datetime objects and sort data by date
    sorted_data = sorted(data, key=lambda x: strptime(x["date"], "%Y-%m-%d"))

    # Extract dates and balances for plotting
    dates = [datetime.strptime(entry["date"], "%Y-%m-%d") for entry in sorted_data]
    balances = [entry["balance"] for entry in sorted_data]

    # Define the data trace
    data_trace = [
        go.Scatter(
            x=dates,
            y=balances,
            mode="lines",
            line=dict(color="#97151c"),
            name="Account Balance",
        )
    ]

    # Define the layout
    layout = go.Layout(
        autosize=True,
        width=700,
        height=200,
        font=dict(family="Raleway", size=10),
        margin=dict(r=30, t=30, b=30, l=30),
        showlegend=True,
        xaxis=dict(
            autorange=True,
            showline=True,
            type="date",
            zeroline=False,
            rangeselector=dict(
                buttons=[
                    dict(count=7, label="1W", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(label="All", step="all"),
                ]
            ),
        ),
        yaxis=dict(
            autorange=True,
            showline=True,
            type="linear",
            zeroline=False,
            tickprefix="VND ",
            tickformat=",.0f",
        ),
    )

    # Return the figure
    fig = go.Figure(data=data_trace, layout=layout)
    return fig


def income_expenditure_chart(data):
    # Convert month to string for the x-axis
    months = [str(entry["month"]) for entry in data]
    income = [entry["income"] for entry in data]
    expenditure = [entry["expenditure"] for entry in data]

    # Define data for income and expenditure bars
    chart_data = [
        go.Bar(
            x=months,
            y=income,
            name="Income",
            marker=dict(
                color="#97151c", line=dict(color="rgb(255, 255, 255)", width=2)
            ),
        ),
        go.Bar(
            x=months,
            y=expenditure,
            name="Expenditure",
            marker=dict(
                color="#dddddd", line=dict(color="rgb(255, 255, 255)", width=2)
            ),
        ),
    ]

    # Define layout
    layout = go.Layout(
        autosize=False,
        bargap=0.35,
        font={"family": "Raleway", "size": 10},
        height=200,
        hovermode="closest",
        legend=dict(x=-0.02, y=-0.18, orientation="h", yanchor="top"),
        margin=dict(r=0, t=20, b=10, l=50),
        showlegend=True,
        width=330,
        xaxis=dict(autorange=True, showline=True, title="Month", type="category"),
        yaxis=dict(
            autorange=True,
            showgrid=True,
            showline=True,
            title="Amount (VND)",
            type="linear",
            zeroline=False,
            tickprefix="VND ",
            tickformat=",.0f",
        ),
    )

    return {"data": chart_data, "layout": layout}
