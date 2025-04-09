from dash import html

from utils.util_methods import format_value


def make_dash_table_dict(data: dict):
    """Generate a Dash HTML table from a dictionary with formatted numbers."""
    # Create table rows
    table_rows = [
        html.Tr([html.Th(key), html.Td(format_value(value))])
        for key, value in data.items()
    ]

    return html.Table([html.Tbody(table_rows)], className="dash-table")


def make_dash_table(df):
    """Return a dash definition of an HTML table for a Pandas dataframe"""
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row.iloc[i]]))
        table.append(html.Tr(html_row))
    return table


def make_dash_table_list(transactions: list):
    """Generate a Dash HTML table from a list of transaction dictionaries, selecting specific columns."""

    if not transactions:
        return html.P("No transactions available.", className="no-data")

    # Define the columns to keep
    selected_columns = [
        "transaction_date",
        "description",
        "debit",
        "counter_account",
        "category",
    ]

    # Create table header row
    table_header = html.Tr([html.Th(col) for col in selected_columns])

    # Create table rows from transaction data
    table_rows = [
        html.Tr([html.Td(format_value(tx[col])) for col in selected_columns])
        for tx in transactions
    ]

    return html.Table(
        [html.Thead(table_header), html.Tbody(table_rows)], className="dash-table"
    )
