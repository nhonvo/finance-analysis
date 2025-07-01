import pandas as pd
import plotly.graph_objs as go

from utils.util_methods import categorize_expense
import plotly.express as px


class highlight_service:
    def __init__(self, df):
        df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
        self.df = df

    def expense_category_tree_map(self):
        # Clean the DataFrame by dropping NaN values
        df = self.df[self.df["debit"].notna()].copy()
        df = self.df[self.df["counter_account"].notna()].copy()
        df = self.df[self.df["category"].notna()].copy()

        # Identify the index of rows to drop
        index_to_drop = df[df["category"] == "saving"].index

        # Drop the rows
        df.drop(index=index_to_drop, inplace=True)

        df["Expense Category"] = df.apply(
            lambda row: categorize_expense(row["counter_account"], row["category"]),
            axis=1,
        )

        # Group by 'Expense Category' and sum the 'debit' amounts
        category_summary = df.groupby("Expense Category")["debit"].sum().reset_index()

        # Create the treemap
        fig = px.treemap(
            category_summary,
            path=["Expense Category"],
            values="debit",
            title="Phân bố chi phí theo nhóm",
        )

        return fig

    def expense_category_column_shorter(self):
        # Clean the DataFrame by dropping NaN values
        df = self.df[self.df["debit"].notna()].copy()
        df = self.df[self.df["counter_account"].notna()].copy()
        df = self.df[self.df["category"].notna()].copy()

        df["Expense Category"] = df.apply(
            lambda row: categorize_expense(row["counter_account"], row["category"]),
            axis=1,
        )

        # Group by 'Expense Category' and sum the 'debit' amounts
        category_summary = df.groupby("Expense Category")["debit"].sum().reset_index()

        # Create the figure
        fig = go.Figure()

        # Add a bar trace for total expenses by category
        fig.add_trace(
            go.Bar(
                x=category_summary["Expense Category"],
                y=category_summary["debit"],
                hoverinfo="y+name",
                name="Total Expenses",
            )
        )

        # Update layout for better visualization
        fig.update_layout(
            title="Tổng chi phí theo nhóm",
            xaxis_title="Nhóm chi phí",
            yaxis_title="Tổng chi phí (VND)",
            xaxis_tickangle=45,
        )

        # Update y-axes to display amounts in VND
        fig.update_yaxes(tickprefix="VND ", tickformat=",.0f")

        return fig

    def account_analysis(self):
        account_data = (
            self.df.groupby("counter_account")
            .agg(total_income=("credit", "sum"), total_expenditure=("debit", "sum"))
            .reset_index()
        )
        fig = px.bar(
            account_data,
            x="counter_account",
            y=["total_income", "total_expenditure"],
            barmode="group",
            labels={"value": "Amount (VND)", "variable": "Type"},
            title="Transactions per Account",
        )
        fig.update_yaxes(tickprefix="VND ", tickformat=",.0f")
        return fig

    def category_analysis(self, name):
        data = self.df[self.df["category"].str.startswith(name)]

        grouped_data = (
            data.groupby("category")
            .agg(total_expenditure=("debit", "sum"))
            .reset_index()
        )

        grouped_data = grouped_data.sort_values(
            by="total_expenditure", ascending=False
        ).head(6)

        fig = px.bar(
            grouped_data,
            x="category",
            y="total_expenditure",
            barmode="group",
            labels={
                "total_expenditure": "Amount (VND)",
                "category": "Account Name",
            },
            title="Transactions per Account",
        )
        fig.update_yaxes(tickprefix="VND ", tickformat=",.0f")
        return fig

    def create_highest_expense_by_account_chart(self, number):
        grouped_expenses_by_account = (
            self.df.groupby("counter_account")
            .agg(total_ghi_no=("debit", "sum"))
            .reset_index()
        )
        grouped_expenses_by_account = grouped_expenses_by_account.sort_values(
            by="total_ghi_no", ascending=False
        ).head(number)

        fig = px.bar(
            grouped_expenses_by_account,
            x="counter_account",
            y="total_ghi_no",
            title="Total debit by Account",
            labels={
                "total_ghi_no": "Total debit (VND)",
                "counter_account": "Account Name",
            },
            color="counter_account",
            template="plotly",
        )
        fig.update_yaxes(tickprefix="VND ", tickformat=",.0f")
        return fig
