from datetime import datetime
from time import strptime
import plotly.graph_objects as go
from dash import dcc, html
from presentation.components.navbar import get_header, get_menu
from presentation.components.table_components import make_dash_table_dict, make_dash_table_list
from services.transaction_service import (
    get_income_expenditure,
    get_overview,
    get_summary,
    get_transactions,
    get_balance_trends
)
from utils.util_methods import get_current_day_and_month
from presentation.layout import (
    get_section,
)
import locale

locale.setlocale(locale.LC_ALL, "vi_VN.utf8")


def create_layout(app, year=None):
    """Main function to generate the layout."""
    if year is None:
        (month, year) = get_current_day_and_month()
    # Define default API parameters for yearly data
    params = {"start_date": f"{year}-01-01", "end_date": f"{year}-12-31"}
    # Fetch data from APIs

    overview = get_overview(params)
    summary = get_summary(params)

    income_expenditure_data = get_income_expenditure(params)
    income_expenditure_chart_data = (
        income_expenditure_chart(income_expenditure_data)
        if income_expenditure_data
        else None
    )

    top_n_highest_transaction = get_transactions(params, limit=10, sort_by="debit")

    balance_data = get_balance_trends(year)
    balance_trends_chart = balance_trends(balance_data) if balance_data else None

    return html.Div(
        [
            html.Div([get_header(), html.Br([]), get_menu()]),
            html.Div(
                [
                    # Row 1 - Overview
                    get_section(
                        "Overview",
                        "Overall report shows all highlighted transactions, saving money, and all funds.",
                    ),
                    overview_section(overview),
                    # Row 2 - Summary & Income/Expenditure Analysis
                    html.Div(
                        [
                            get_summary_table(summary),
                            get_income_expenditure_chart(income_expenditure_chart_data),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 3 - Balance Trends
                    html.Div(
                        [
                            get_balance_trends_chart(balance_trends_chart, year),
                        ],
                        className="row",
                    ),
                    # Row 4 - Top Transactions
                    html.Div(
                        [
                            get_top_n_transactions_table(top_n_highest_transaction),
                        ],
                        className="row",
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )


def get_income_expenditure_chart(figure):
    """Generate the income and expenditure analysis chart layout."""
    return html.Div(
        [
            html.H6(
                "Income and Expenditure Analysis",
                className="subtitle padded",
            ),
            dcc.Graph(
                id="graph-income-expenditure",
                figure=figure,
                config={"displayModeBar": False},
            ),
        ],
        className="six columns",
    )


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


def generate_income_expenditure_figure(data, year):
    """Generate a bar chart for income and expenditure analysis."""

    # Extracting data for the selected year
    filtered_data = [d for d in data if d["year"] == year]

    # Sorting by month to ensure correct order
    filtered_data.sort(key=lambda x: x["month"])

    # Extracting months, income, and expenditure
    months = [d["month"] for d in filtered_data]
    income = [d["income"] for d in filtered_data]
    expenditure = [d["expenditure"] for d in filtered_data]

    # Create figure using go.Figure()
    fig = go.Figure()

    # Add Income Bar
    fig.add_trace(go.Bar(x=months, y=income, name="Income", marker_color="green"))

    # Add Expenditure Bar
    fig.add_trace(
        go.Bar(x=months, y=expenditure, name="Expenditure", marker_color="red")
    )

    # Layout customization
    fig.update_layout(
        title=f"Income and Expenditure Analysis - {year}",
        xaxis=dict(title="Month"),
        yaxis=dict(title="Amount (VND)"),
        barmode="group",  # Grouped bars
        template="plotly_white",
    )

    return fig


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


def get_balance_trends_chart(figure, year):
    """Generate the account balance trends chart layout."""
    return html.Div(
        [
            html.H6(f"Account Balance in {year}", className="subtitle padded"),
            dcc.Graph(
                id="graph-balance-trends",
                figure=figure,
                config={"displayModeBar": False},
            ),
        ],
        className="six columns",
    )


def get_top_n_transactions_table(transactions):
    """Generate the top n highest transactions table layout."""
    return html.Div(
        [
            html.H6(
                f"Top {len(transactions)} Highest Transactions",
                className="subtitle padded",
            ),
            html.Table(make_dash_table_list(transactions)),
        ],
        className="twelve columns",
    )


def get_summary_table(summary):
    """Generate the summary table layout."""
    return html.Div(
        [
            html.H6(["Summary"], className="subtitle padded"),
            html.Table(make_dash_table_dict(summary)),
        ],
        className="six columns",
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
                                f"{locale.currency(value, grouping=True)}",
                                className="overview-value",
                            ),
                        ],
                    )
                    for label, value in data.items()
                ],
            ),
        ],
    )
