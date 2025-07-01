import pandas as pd
import plotly.graph_objs as go
import locale


class housefee_service:
    def __init__(self, df):
        self.df = df

    def filter_transactions(self, account_name, category_keyword):
        """Filter transactions based on counter account and description keywords."""
        transactions = self.df[self.df["category"] == category_keyword]
        return transactions[
            transactions["counter_account"].str.contains(account_name, case=False)
        ]

    def group_monthly_totals(self, transactions, column_name):
        """Group transactions by month and sum specified column."""
        return (
            transactions.groupby(transactions["transaction_date"].dt.to_period("M"))
            .agg({"debit": "sum"})
            .rename(columns={"debit": column_name})
        )

    def format_currency(self, amount):
        """Format amount to VND currency."""
        return locale.currency(amount, grouping=True)

    def create_stacked_area_chart(
        self, x_data, y_data, title, y_axis_title, fill_color
    ):
        """Create a stacked area chart using Plotly go.Figure."""
        return go.Figure(
            data=go.Scatter(
                x=x_data,
                y=y_data,
                mode="lines",
                line=dict(color=fill_color),
                fill="tonexty",
                stackgroup="one",  # This enables stacking
                name=title,
            ),
            layout=go.Layout(
                title=title,
                yaxis=dict(title=y_axis_title, tickprefix="VND ", tickformat=",.0f"),
                xaxis=dict(title="Date"),
            ),
        )

    def create_stacked_column_chart(self, x_data, y_data_list, labels, title, y_axis_title, colors):
        """Create a stacked column chart using Plotly go.Figure."""
        traces = []
        for y_data, label, color in zip(y_data_list, labels, colors):
            traces.append(
                go.Bar(
                    x=x_data,
                    y=y_data,
                    name=label,
                    marker=dict(color=color)
                )
            )

        return go.Figure(
            data=traces,
            layout=go.Layout(
                title=title,
                barmode="stack",  # Enables stacking
                yaxis=dict(title=y_axis_title, tickprefix="VND ", tickformat=",.0f"),
                xaxis=dict(title="Date"),
            ),
        )


    def house_fee(self):
        """Main method to generate the house fee report, combining all steps."""
        # Filtered data for each category
        self.df["transaction_date"] = pd.to_datetime(
            self.df["transaction_date"], errors="coerce"
        )

        rent_payment = self.filter_transactions("tiền nhà", "rent")
        management_fee = self.filter_transactions("phí quản lý", "rent")
        utility_payment = self.filter_transactions("tiền điện nước", "rent")

        # Group data by month
        rent_payment_monthly = self.group_monthly_totals(rent_payment, "Rent Payment")
        management_fee_monthly = self.group_monthly_totals(
            management_fee, "Management Fee"
        )
        utility_payment_monthly = self.group_monthly_totals(
            utility_payment, "Utility Payment"
        )

        # Combine monthly totals into a DataFrame
        monthly_report = pd.concat(
            [rent_payment_monthly, management_fee_monthly, utility_payment_monthly],
            axis=1,
        ).fillna(0)
        monthly_report.index = monthly_report.index.to_timestamp()

        # Calculate raw sum before formatting
        monthly_report["Sum"] = (
            monthly_report["Rent Payment"]
            + monthly_report["Management Fee"]
            + monthly_report["Utility Payment"]
        )

        # Add formatted currency columns
        monthly_report["Formatted Rent Payment"] = monthly_report["Rent Payment"].apply(
            self.format_currency
        )
        monthly_report["Formatted Management Fee"] = monthly_report[
            "Management Fee"
        ].apply(self.format_currency)
        monthly_report["Formatted Utility Payment"] = monthly_report[
            "Utility Payment"
        ].apply(self.format_currency)

        monthly_report["Formatted Sum"] = monthly_report["Sum"].apply(
            self.format_currency
        )

        # Create charts
        fig_rent = self.create_stacked_area_chart(
            monthly_report.index,
            monthly_report["Rent Payment"],
            "Monthly Rent Payments",
            "Rent Payment (VND)",
            "#2ca02c",
        )
        fig_management = self.create_stacked_area_chart(
            monthly_report.index,
            monthly_report["Management Fee"],
            "Monthly Management Fees",
            "Management Fee (VND)",
            "#ff7f0e",
        )
        fig_utility = self.create_stacked_area_chart(
            monthly_report.index,
            monthly_report["Utility Payment"],
            "Monthly Utility Payments",
            "Utility Payment (VND)",
            "#1f77b4",
        )
        fig_sum = self.create_stacked_column_chart(
            x_data = monthly_report.index,
            y_data_list=[
                monthly_report["Rent Payment"],
                monthly_report["Management Fee"],
                monthly_report["Utility Payment"],
            ],
            labels=["Rent", "Management", "Utilities"],
            title="Monthly Expense Breakdown",
            y_axis_title="Amount (VND)",
            colors=["#1f77b4", "#2ca02c", "#ff7f0e"],
        )

        # Table for formatted data
        # Add Month-Year column to the report table
        monthly_report["Month-Year"] = monthly_report.index.strftime(
            "%B %Y"
        )  # Format month and year

        report_table = pd.DataFrame(
            {
                "Date": monthly_report["Month-Year"],
                "Rent Payment": monthly_report["Formatted Rent Payment"],
                "Management Fee": monthly_report["Formatted Management Fee"],
                "Utility Payment": monthly_report["Formatted Utility Payment"],
                "Sum": monthly_report["Formatted Sum"],
            }
        ).tail(10)

        return (fig_rent, fig_management, (report_table), fig_utility, fig_sum)
