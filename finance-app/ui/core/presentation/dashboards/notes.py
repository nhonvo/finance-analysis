from dash import dcc, html, dash_table, Input, Output, State, callback

import base64
import datetime
import io

import pandas as pd

from presentation.components.navbar import get_header, get_menu

# from dash import html, dcc


def create_layout(app):
    return html.Div(
        [
            html.Div([get_header(), html.Br([]), get_menu()]),
            # Report Notes Section
            html.Div(
                [
                    # Row 1 - Overview
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Report Summary", className="subtitle padded"
                                    ),
                                    html.Div(
                                        [
                                            dcc.Upload(
                                                id="upload-data",
                                                children=html.Div(
                                                    [
                                                        "Drag and Drop or ",
                                                        html.A("Select Files"),
                                                    ]
                                                ),
                                                # Allow multiple files to be uploaded
                                                multiple=True,
                                            ),
                                            html.Div(id="output-data-upload"),
                                        ]
                                    ),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P("Date: 11/03/2024"),
                                            html.P(
                                                "Prepared for: Financial Dashboard Project"
                                            ),
                                            html.P(
                                                "This report provides an analysis of monthly expenses and income trends, "
                                                "categorized by transaction types and accounts. Key visualizations offer insights "
                                                "into spending patterns, category-wise breakdowns, and high-level financial health indicators."
                                            ),
                                        ],
                                        style={"color": "#4a4a4a"},
                                    ),
                                ],
                                className="row",
                            ),
                            # Row 2 - Key Highlights
                            html.Div(
                                [
                                    html.H6(
                                        "Key Highlights", className="subtitle padded"
                                    ),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Li(
                                                "Significant expense categories: Daily expenses on food and team entertainment."
                                            ),
                                            html.Li(
                                                "High expenditure trends identified in specific categories with monthly fluctuations."
                                            ),
                                            html.Li(
                                                "Customizable filters available to isolate specific periods or categories for deeper insights."
                                            ),
                                        ],
                                        id="highlights-bullet-pts",
                                    ),
                                    html.Div(
                                        [
                                            html.P(
                                                "Note: This report is part of an ongoing analysis to optimize budget planning "
                                                "and highlight any unusual spending patterns."
                                            ),
                                            html.Br([]),
                                            html.P(
                                                "Please refer to the interactive dashboard for real-time updates and a detailed breakdown by date and category."
                                            ),
                                            html.Br([]),
                                            html.P(
                                                "All data is aggregated monthly. To adjust for seasonal variations, refer to the category trend analysis."
                                            ),
                                        ],
                                        style={"color": "#4a4a4a"},
                                    ),
                                ],
                                className="row",
                            ),
                        ],
                        className="row",
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        if "csv" in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
        elif "xls" in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return html.Div(
        [
            html.H5(filename),
            html.H6(datetime.datetime.fromtimestamp(date)),
            dash_table.DataTable(
                df.to_dict("records"), [{"name": i, "id": i} for i in df.columns]
            ),
            html.Hr(),  # horizontal line
            # For debugging, display the raw contents provided by the web browser
            html.Div("Raw Content"),
            html.Pre(
                contents[0:200] + "...",
                style={"whiteSpace": "pre-wrap", "wordBreak": "break-all"},
            ),
        ]
    )


@callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename"),
    State("upload-data", "last_modified"),
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d)
            for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children
