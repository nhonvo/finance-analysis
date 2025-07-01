from dash import dcc, html
import locale
from application.saving_service import saving_service
from application.investment_service import investment_service
from presentation.components.navbar import get_header, get_menu
from presentation.components.table_components import make_dash_table
from presentation.layout import get_section
from services.transaction_service import (
    get_invest_transactions,
    get_saving_transactions,
)
from utils.util_methods import get_current_day_and_month
import pandas as pd


def create_layout(app):
    (month, year) = get_current_day_and_month()
    params = {"start_date": "2023-01-01", "end_date": f"{year}-12-31"}
    # Fetch data from APIs
    saving_transactions = get_saving_transactions(params)
    saving_transactions_df = pd.DataFrame(saving_transactions)

    savingDashBoard = saving_service(saving_transactions_df)
    summarySaving = savingDashBoard.table_saving_report()
    total_saving = savingDashBoard.total_saving()
    saving_bar_chart = savingDashBoard.saving_bar_chart()
    saving_line_chart = savingDashBoard.saving_line_chart()

    invest_transactions = get_invest_transactions(params)
    invest_transactions_df = pd.DataFrame(invest_transactions)

    investmentDashBoard = investment_service(invest_transactions_df)
    summaryInvestment = investmentDashBoard.table_investment_report()
    total_investment = investmentDashBoard.total_investment()
    investment_bar_chart = investmentDashBoard.investment_bar_chart()
    investment_line_chart = investmentDashBoard.investment_line_chart()

    total = total_saving + total_investment

    total_saving = locale.currency(total_saving, grouping=True)
    total_investment = locale.currency(total_investment, grouping=True)
    total = locale.currency(total, grouping=True)
    return html.Div(
        [
            html.Div([get_header(), html.Br([]), get_menu()]),
            # Page Container
            html.Div(
                [
                    # Title Row
                    get_section(
                        "Savings & Investment Dashboard",
                        "An overview of your monthly and cumulative savings and investment, including insights on balance trends.",
                    ),
                    # Summary and Current Saving Row
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Current Balance", className="subtitle padded"
                                    ),
                                    # Display total savings, investment, and combined total
                                    html.Div(
                                        [
                                            html.P(
                                                f"Total Savings: {total_saving}",
                                                style={
                                                    "font-weight": "bold",
                                                },
                                            ),
                                            html.P(
                                                f"Total Investment: {total_investment}",
                                                style={
                                                    "font-weight": "bold",
                                                },
                                            ),
                                            html.P(
                                                f"Overall Balance: {total}",
                                                style={
                                                    "font-weight": "bold",
                                                    "margin-bottom": "15px",
                                                },
                                            ),
                                        ],
                                    ),
                                    # Display investment goal
                                    html.P(
                                        "Goal: Reach the first 100M milestone",
                                        style={
                                            "font-size": "16px",
                                            "color": "#7D3C98",
                                            "font-style": "italic",
                                            "margin-top": "10px",
                                            "margin-bottom": "20px",
                                        },
                                    ),
                                    html.H6(
                                        "Investment Summary",
                                        className="subtitle padded",
                                    ),
                                    # Display investment summary table
                                    html.Div(
                                        html.Table(make_dash_table(summaryInvestment)),
                                        style={
                                            "overflow-x": "auto",
                                            "margin-top": "10px",
                                        },
                                    ),
                                ],
                                className="six columns",
                                style={"padding": "20px"},
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Savings Summary", className="subtitle padded"
                                    ),
                                    html.Table(
                                        make_dash_table(summarySaving),
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Monthly Balance Bar Chart Row
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(
                                        "Saving Monthly Balance Changes",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-5",
                                        figure=saving_bar_chart,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H5(
                                        "Saving Cumulative Balance Over Time",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-15",
                                        figure=investment_line_chart,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Cumulative Balance Line Chart Row
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(
                                        "Investment Cumulative Balance Over Time",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-15",
                                        figure=saving_line_chart,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H5(
                                        "Investment Monthly Balance Changes",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-5",
                                        figure=investment_bar_chart,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
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
