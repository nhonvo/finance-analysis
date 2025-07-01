from dash import dcc, html


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Overview",
                href="/dash-financial-report/overview",
                className="tab first",
            ),
            dcc.Link(
                "Monthly",
                href="/dash-financial-report/monthly",
                className="tab",
            ),
            dcc.Link(
                "Saving & Investment",
                href="/dash-financial-report/savingInvest",
                className="tab",
            ),
            dcc.Link(
                "House fee",
                href="/dash-financial-report/houseFee",
                className="tab",
            ),
            dcc.Link(
                "Highlight",
                href="/dash-financial-report/highlight",
                className="tab",
            ),
            dcc.Link(
                "Notes",
                href="/dash-financial-report/notes",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def get_header():
    header = html.Div(
        [
            html.Div(
                [
                    # Main title section
                    html.Div(
                        [html.H5("Personal Finance")],
                        className="seven columns main-title",
                    ),
                    # Link sections
                    html.Div(
                        [
                            # List of links dynamically created
                            dcc.Link(
                                text,
                                href=f"/dash-financial-report/{view}",
                                className="full-view-link",
                            )
                            for text, view in [
                                ("Month View", "monthly-view"),
                                ("Yearly View", "yearly-view"),
                                ("Full View", "full-view"),
                            ]
                        ],
                        className="five columns",
                    ),
                ],
                className="twelve columns",
                style={"padding-left": "0"},
            )
        ],
        className="row",
    )
    return header
