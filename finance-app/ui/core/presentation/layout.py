from dash import html


def get_section(name: str, summary: str):
    """Generate the section layout."""
    return html.Div(
        [
            html.H5(name),
            html.Br([]),
            html.P(
                summary,
                style={"color": "#ffffff"},
                className="row",
            ),
        ],
        className="product",
    )
