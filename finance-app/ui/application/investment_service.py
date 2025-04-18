import plotly.graph_objs as go
import pandas as pd
import locale


class investment_service:
    def __init__(self, df):
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
        self.df = df
        self.investment_df = df

    def total_investment(self):
        # Calculate the total balance number
        return self.investment_df["balance"].sum()

    def calculate_Investment_balance(self):
        # Group by year and month
        self.investment_df["YearMonth"] = self.investment_df[
            "transaction_date"
        ].dt.to_period("M")

        monthly_balance = (
            self.investment_df.groupby("YearMonth")["balance"].sum().reset_index()
        )

        monthly_balance["Cumulative Balance"] = monthly_balance["balance"].cumsum()
        monthly_balance["FormattedBalance"] = monthly_balance["balance"].apply(
            lambda x: locale.currency(x, grouping=True)
        )
        monthly_balance["FormattedCumulativeBalance"] = monthly_balance[
            "Cumulative Balance"
        ].apply(lambda x: locale.currency(x, grouping=True))

        # Convert Period to Timestamp for plotting
        monthly_balance["YearMonth"] = monthly_balance["YearMonth"].dt.to_timestamp()
        return monthly_balance

    def table_investment_report(self):
        monthly_balance = self.calculate_Investment_balance()
        # Generate table for the report
        result_table = monthly_balance[
            ["YearMonth", "FormattedBalance", "FormattedCumulativeBalance"]
        ]

        result_table = pd.DataFrame(
            {
                "Date": monthly_balance["YearMonth"].tolist(),
                "Credit": monthly_balance["FormattedBalance"].tolist(),
                "balance": monthly_balance["FormattedCumulativeBalance"].tolist(),
            }
        )

        return pd.DataFrame(result_table)

    def investment_bar_chart(self):
        monthly_balance = self.calculate_Investment_balance()

        # Extract data for the bar chart
        dates = monthly_balance["YearMonth"]
        balances = monthly_balance["balance"]

        # Define the data trace
        data = [
            go.Bar(
                x=dates,
                y=balances,
                marker=dict(color="rgba(150, 20, 20, 0.7)"),  # Custom color for bars
                hoverinfo="y+text",  # Show balance on hover
                name="Monthly Balance",
            )
        ]

        # Define the layout
        layout = go.Layout(
            title="Monthly Balance Changes",
            xaxis=dict(
                title="Date", tickformat="%Y-%m", linecolor="black", showgrid=False
            ),
            yaxis=dict(
                title="Balance (VND)",
                tickprefix="VND ",
                tickformat=",.0f",
                showgrid=True,
                gridcolor="LightGrey",
            ),
            height=400,
            margin=dict(l=60, r=20, t=40, b=60),
            font=dict(family="Raleway", size=12),
            template="plotly_white",
        )

        # Create and return the figure
        fig = go.Figure(data=data, layout=layout)
        return fig

    def investment_line_chart(self):
        monthly_balance = self.calculate_Investment_balance()

        # Extract data for the line chart
        dates = monthly_balance["YearMonth"]
        cumulative_balances = monthly_balance["Cumulative Balance"]

        # Define the data trace
        data = [
            go.Scatter(
                x=dates,
                y=cumulative_balances,
                mode="lines+markers",
                line=dict(color="rgba(0, 123, 255, 0.8)", width=2),
                marker=dict(size=6, color="rgba(0, 123, 255, 0.8)"),
                name="Cumulative Balance",
                hoverinfo="y+text",
            )
        ]

        # Define the layout
        layout = go.Layout(
            title="Cumulative Balance Over Time",
            xaxis=dict(
                title="Date", tickformat="%Y-%m", linecolor="black", showgrid=False
            ),
            yaxis=dict(
                title="Balance (VND)",
                tickprefix="VND ",
                tickformat=",.0f",
                showgrid=True,
                gridcolor="LightGrey",
            ),
            height=400,
            margin=dict(l=60, r=20, t=40, b=60),
            font=dict(family="Raleway", size=12),
            template="plotly_white",
        )

        # Create and return the figure
        fig = go.Figure(data=data, layout=layout)
        return fig
