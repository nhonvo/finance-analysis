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

    def create_line_chart(self, x_data, y_data, title, y_axis_title, line_color):
        """Create a line chart using Plotly go.Figure."""
        return go.Figure(
            data=go.Scatter(
                x=x_data,
                y=y_data,
                mode="lines+markers",
                line=dict(color=line_color),
                name=title,
            ),
            layout=go.Layout(
                title=title,
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

        # Create charts
        fig_rent = self.create_line_chart(
            monthly_report.index,
            monthly_report["Rent Payment"],
            "Monthly Rent Payments",
            "Rent Payment (VND)",
            "blue",
        )
        fig_management = self.create_line_chart(
            monthly_report.index,
            monthly_report["Management Fee"],
            "Monthly Management Fees",
            "Management Fee (VND)",
            "green",
        )
        fig_utility = self.create_line_chart(
            monthly_report.index,
            monthly_report["Utility Payment"],
            "Monthly Utility Payments",
            "Utility Payment (VND)",
            "purple",
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
            }
        )

        return (fig_rent, fig_management, (report_table), fig_utility)
