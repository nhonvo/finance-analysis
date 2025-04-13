import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Importing dashboards
from presentation.dashboards import (
    highlight,
    house_fee,
    monthly,
    notes,
    saving_and_invest,
    overview,
)

# Initialize Dash app
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=["./assets/base2.css"],
    suppress_callback_exceptions=True,
)
app.title = "Financial Report"
server = app.server

# Define the base layout with a location component for URL routing
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

# Centralized Layout Creation Function
def get_page_layout(pathname):
    """Helper function to return the correct layout based on pathname."""
    # Page-specific layouts
    page_layouts = {
        "/dash-financial-report/monthly": monthly.create_layout(app),
        "/dash-financial-report/savingInvest": saving_and_invest.create_layout(app),
        "/dash-financial-report/highlight": highlight.create_layout(app),
        "/dash-financial-report/houseFee": house_fee.create_layout(app),
        "/dash-financial-report/notes": notes.create_layout(app),
        "/dash-financial-report/full-view": html.Div(
            [
                overview.create_layout(app),
                monthly.create_layout(app),
                saving_and_invest.create_layout(app),
                highlight.create_layout(app),
                house_fee.create_layout(app),
                notes.create_layout(app),
            ]
        ),
        # "/dash-financial-report/monthly-view": html.Div(
        #     [monthly.create_layout(month) for month in range(1, 13)]
        # ),
        # "/dash-financial-report/yearly-view": html.Div(
        #     [overview.create_layout(year) for year in range(2023, 2025)]
        # ),
    }

    # Return the corresponding layout, or a default layout
    return page_layouts.get(pathname, overview.create_layout(app))


# Update the page content based on the URL pathname
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    return get_page_layout(pathname)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
