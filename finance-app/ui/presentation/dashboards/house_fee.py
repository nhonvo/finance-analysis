from presentation.components.navbar import get_header, get_menu
from dash import dcc, html
from application.housefee_service import housefee_service
from presentation.components.table_components import make_dash_table
from presentation.layout import get_section
from services.transaction_service import get_transactions
from utils.util_methods import get_current_day_and_month

import pandas as pd


def create_layout(app):
    # Define default API parameters for yearly data
    (month, year) = get_current_day_and_month()
    params = {"start_date": "2023-01-01", "end_date": f"{year}-12-31"}
    # Fetch data from APIs
    transactions = get_transactions(params, limit=-1)
    house_fee = housefee_service(pd.DataFrame(transactions))
    fig_rent, fig_management, report_table, fig_utility = house_fee.house_fee()

    return html.Div(
        [
            html.Div([get_header(), html.Br([]), get_menu()]),
            html.Div(
                [
                    # Section Title and Description
                    get_section(
                        "Household Expense Summary",
                        "This section provides a comprehensive overview of your household expenses, "
                        "including monthly rent, management fees, and utility payments. The insights below "
                        "offer a breakdown of each category to help track and manage monthly costs.",
                    ),
                    # Row 4: Highest Expense Chart
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Monthly Expense Distribution",
                                        className="subtitle padded",
                                    ),
                                    html.Table(make_dash_table(report_table)),
                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Row 5: Expense Category Tree Map and Column Shorter
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Rent Payment Trends",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="rent_graph",
                                        figure=fig_rent,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="twelve columns",
                            ),
                        ],
                        className="twelve columns",
                    ),
                    # Row 2: Category Food Analysis
                    html.Div(
                        [
                            html.H6(
                                "Management Fee Trends", className="subtitle padded"
                            ),
                            dcc.Graph(
                                id="management_graph",
                                figure=fig_management,
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="twelve columns",
                    ),
                    # Row 3: Team Entertainment and Shopping Analysis
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Utility Payment Trends",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="utility_graph",
                                        figure=fig_utility,
                                        config={"displayModeBar": False},
                                    ),
                                ],
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
