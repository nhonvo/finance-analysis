from dash import dcc, html

from application.highlight_service import highlight_service

import pandas as pd

from presentation.components.navbar import get_header, get_menu
from services.transaction_service import (
    get_transactions,
)
from utils.util_methods import get_current_day_and_month

def create_layout(app):
    # Define default API parameters for yearly data
    (month, year) = get_current_day_and_month()
    params = {"start_date": "2023-01-01", "end_date": f"{year}-12-31"}
    # Fetch data from APIs
    transactions = get_transactions(params, limit=-1)

    finance = highlight_service(pd.DataFrame(transactions))
    account_analysis_panel = finance.account_analysis()
    category_food_analysis_panel = finance.category_analysis("food")
    category_anchoi_team_analysis_panel = finance.category_analysis("team")
    category_muasam_analysis_panel = finance.category_analysis("shopping")
    highest_expense_chart_panel = finance.create_highest_expense_by_account_chart(4)
    expense_category_tree_map = finance.expense_category_tree_map()
    expense_category_column_shorter = finance.expense_category_column_shorter()

    return html.Div(
        [
            html.Div([get_header(), html.Br([]), get_menu()]),
            html.Div(
                [
                    # Section Title and Description
                    html.Div(
                        [
                            html.H4("Financial Overview", className="header-title"),
                            html.P(
                                "Explore a comprehensive breakdown of expenses across accounts, categories, "
                                "and highest spend areas to gain insights into spending patterns.",
                                className="description",
                            ),
                        ],
                        className="row",
                    ),
                    # Row 4: Highest Expense Chart
                    html.Div(
                        [
                            html.H6("Expense Tree Map", className="subtitle padded"),
                            html.P(
                                "Visualize the distribution of expenses across categories in a tree map.",
                                className="description",
                            ),
                            dcc.Graph(
                                id="expense-category-tree-map",
                                figure=expense_category_tree_map,
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="twelve columns",
                    ),
                    # Row 5: Expense Category Tree Map and Column Shorter
                    html.Div(
                        [
                            html.H6(
                                "Category Expense Comparison",
                                className="subtitle padded",
                            ),
                            html.P(
                                "Compare expenses across categories for a clear breakdown of spending habits.",
                                className="description",
                            ),
                            dcc.Graph(
                                id="expense-category-column-shorter",
                                figure=expense_category_column_shorter,
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="twelve columns",
                    ),
                    # Row 2: Category Food Analysis
                    html.Div(
                        [
                            html.H6(
                                "Food Category Analysis", className="subtitle padded"
                            ),
                            html.P(
                                "Examine spending trends in the 'ăn uống' category to track food-related expenses.",
                                className="description",
                            ),
                            dcc.Graph(
                                id="category-food-analysis-chart",
                                figure=category_food_analysis_panel,
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
                                        "Team Entertainment Analysis",
                                        className="subtitle padded",
                                    ),
                                    html.P(
                                        "Explore expenses in the 'ăn chơi team' category, showing team-related activities.",
                                        className="description",
                                    ),
                                    dcc.Graph(
                                        id="category-anchoi-team-chart",
                                        figure=category_anchoi_team_analysis_panel,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Shopping Analysis", className="subtitle padded"
                                    ),
                                    html.P(
                                        "Analyze 'mua sắm' category expenses to understand shopping trends.",
                                        className="description",
                                    ),
                                    dcc.Graph(
                                        id="category-muasam-chart",
                                        figure=category_muasam_analysis_panel,
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                    ),
                    # Top Expense Categories
                    html.Div(
                        [
                            html.H6(
                                "Top Expense Categories", className="subtitle padded"
                            ),
                            html.P(
                                "View the categories with the highest spending, helping prioritize budget adjustments.",
                                className="description",
                            ),
                            dcc.Graph(
                                id="highest-expense-chart",
                                figure=highest_expense_chart_panel,
                                config={"displayModeBar": False},
                            ),
                        ],
                        className="twelve columns",
                    ),
                    # Row 1: Account Analysis
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Account Analysis", className="subtitle padded"
                                    ),
                                    html.P(
                                        "Analyze expenses by account to see where spending is most concentrated.",
                                        className="description",
                                    ),
                                    dcc.Graph(
                                        id="account-analysis-chart",
                                        figure=account_analysis_panel,
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
