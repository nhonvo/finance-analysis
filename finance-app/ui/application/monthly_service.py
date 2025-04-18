import plotly.graph_objs as go
from utils.util_methods import (
    categorize_expense,
)
import pandas as pd

# from datetime import datetime

import plotly.express as px
import locale

from utils.cleanning import clean_data, get_investigate_df, get_saving_df


class monthly_service:
    def __init__(self, month_df, saving_df, investigate_df):
        self.month_df = month_df
        self.saving_df = saving_df
        self.investigate_df = investigate_df

    def generate_overview_section(self):
        # 1. get saving and investigate current balance and add in revenue
        saving_balance = self.saving_df["balance"].sum()
        investigate_balance = self.investigate_df["balance"].sum()

        # 2. remove saving and investigate data
        self.df = clean_data(self.df)

        # 3.sum get 4 infomations
        total_income = self.df["credit"].sum() + saving_balance + investigate_balance
        total_expense = self.df["debit"].sum()
        total_saving = saving_balance + investigate_balance

        return (
            locale.currency(total_income, grouping=True),
            locale.currency(total_expense, grouping=True),
            locale.currency(total_saving, grouping=True),
        )

    def generate_summary_df(self):
        # 1. get saving and investigate current balance and add in revenue
        saving_df = get_saving_df(self.df)
        saving_balance = saving_df["balance"].sum()

        investigate_df = get_investigate_df(self.df)
        investigate_balance = investigate_df["balance"].sum()
        # 2. remove saving and investigate data
        self.df = clean_data(self.df)
        # 3.sum get 4 infomations
        balance = self.df["balance"].iloc[0]
        total_asset = self.df["balance"].iloc[0] + saving_balance + investigate_balance
        transaction_count = self.df.shape[0]

        summary_data = {
            "Description": [
                "Tổng tài sản",
                "Số dư tài khoản",
                "Tiết kiệm",
                "Đầu tư",
                "Số lượng giao dịch",
            ],
            "Value": [
                locale.currency(balance, grouping=True),
                locale.currency(total_asset, grouping=True),
                locale.currency(saving_balance, grouping=True),
                locale.currency(investigate_balance, grouping=True),
                transaction_count,
            ],
        }
        return pd.DataFrame(summary_data)

    def n_latest_transaction(self, n):
        self.df = self.df.sort_values(by="transaction_date", ascending=True)
        # Extract the latest 4 transactions
        data = self.df.tail(n)

        # Format credit and debit values using locale.currency
        formatted_credit = [
            locale.currency(value, grouping=True) for value in data["credit"]
        ]
        formatted_debit = [
            locale.currency(value, grouping=True) for value in data["debit"]
        ]

        # Create a DataFrame with the required structure
        table_data = pd.DataFrame(
            {
                "Date": data["transaction_date"].dt.strftime("%Y-%m-%d").tolist(),
                "Credit": formatted_credit,
                "Debit": formatted_debit,
                "Category": data["category"].tolist(),
                "Account": data["counter_account"].tolist(),
            }
        )

        # Create a DataFrame from the table data
        latest_transactions_df = pd.DataFrame(table_data)

        return latest_transactions_df

    def top_n_highest_transaction(self, n):
        df = self.df[self.df["credit"].isna()]
        df = df.sort_values(by="debit", ascending=False)
        data = df.head(n)
        # Format credit and debit values using locale.currency

        formatted_debit = [
            locale.currency(value, grouping=True) for value in data["debit"]
        ]

        # Create a DataFrame with the required structure
        table_data = pd.DataFrame(
            {
                "Date": data["transaction_date"].dt.strftime("%Y-%m-%d").tolist(),
                "Debit": formatted_debit,
                "Category": data["category"].tolist(),
                "Account": data["counter_account"].tolist(),
                "Description": data["description"].tolist(),
            }
        )

        # Create a DataFrame from the table data
        latest_transactions_df = pd.DataFrame(table_data)

        return latest_transactions_df

    # the balance chart just for this month
    def balance_trends(self):
        sorted_df = self.df.sort_values(by="transaction_date", ascending=True)

        monthly_data = (
            sorted_df.groupby(sorted_df["transaction_date"].dt.to_period("D"))
            .agg({"balance": "last"})
            .reset_index()
        )
        # Convert the period back to datetime for the x-axis
        monthly_data["transaction_date"] = monthly_data[
            "transaction_date"
        ].dt.to_timestamp()

        # Extract dates and balances
        dates = monthly_data["transaction_date"]
        balances = monthly_data["balance"]

        # Define the data trace
        data = [
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
            font=dict(family="Raleway", size=10),
            height=200,
            hovermode="closest",
            legend=dict(x=-0.03, y=-0.15, orientation="h"),
            margin=dict(r=20, t=20, b=20, l=60),
            showlegend=True,
            xaxis=dict(
                autorange=True,
                linecolor="rgb(0, 0, 0)",
                linewidth=1,
                showgrid=True,
                gridcolor="LightGrey",
                title="Transaction Date",
                tickformat="%Y-%m-%d",  # Format x-axis labels as dates
                type="date",
            ),
            yaxis=dict(
                autorange=True,
                gridcolor="rgba(127, 127, 127, 0.2)",
                mirror=False,
                nticks=4,
                showgrid=True,
                showline=True,
                ticklen=10,
                ticks="outside",
                title="Balance (VND)",
                tickprefix="VND ",
                tickformat=",.0f",
                zeroline=False,
            ),
        )

        # Return the figure dictionary with "data" and "layout"
        fig = {"data": data, "layout": layout}
        return fig

    # column in and ex compare for current month
    def income_expenditure_analysis(self):
        # Group data by month and aggregate income and expenditure
        monthly_data = (
            self.month_df.groupby(self.month_df["transaction_date"].dt.to_period("M"))
            .agg(income=("credit", "sum"), expenditure=("debit", "sum"))
            .reset_index()
        )

        # Format the month for the x-axis labels
        monthly_data["transaction_date"] = monthly_data["transaction_date"].dt.strftime(
            "%m"
        )

        # Define data for income and expenditure bars
        data = [
            go.Bar(
                x=monthly_data["transaction_date"],
                y=monthly_data["income"],
                name="Income",
                marker=dict(
                    color="#97151c", line=dict(color="rgb(255, 255, 255)", width=2)
                ),
            ),
            go.Bar(
                x=monthly_data["transaction_date"],
                y=monthly_data["expenditure"],
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
            # title="Monthly Income and Expenditure",
            # width=330,
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

        # Return the figure as a dictionary with "data" and "layout"
        fig = {"data": data, "layout": layout}
        return fig

    # pie chart all main counter_account
    def transaction_distribution(self):
        # Group by "counter_account" and sum "debit" for each category
        df_grouped = self.month_df.groupby("counter_account", as_index=False)[
            "debit"
        ].sum()

        # Define data for the pie chart using go.Pie
        data = [
            go.Pie(
                labels=df_grouped["counter_account"],
                values=df_grouped["debit"],
                hole=0.0,  # No hole for a pie chart
                textinfo="percent+label",
                textposition="inside",
                marker=dict(
                    colors=px.colors.sequential.RdBu  # Use color sequence similar to px.colors.sequential.RdBu
                ),
                name="Transaction Distribution",
            )
        ]

        # Define layout for the pie chart
        layout = go.Layout(
            title="Phân bổ chi tiêu theo loại giao dịch",
            font=dict(family="Raleway", size=12),
            autosize=True,
            margin=dict(t=50, b=20, l=20, r=20),
            showlegend=True,
            legend=dict(
                x=0.8,
                y=0.5,
                font=dict(size=10),
                orientation="v",
            ),
        )

        # Return the figure dictionary with "data" and "layout"
        fig = {"data": data, "layout": layout}
        return fig

    # column chart about total ex and in
    def detailed_transaction_analysis(self):
        # Filter the DataFrame for entries with non-null "debit" values
        df = self.month_df[self.month_df["debit"].notna()]

        # Get unique categories
        categories = df["category"].unique()

        # Prepare a color scale to assign colors to each category
        color_map = {
            category: f"hsl({i * 30}, 60%, 60%)"
            for i, category in enumerate(categories)
        }

        # Define data for each category as a separate trace in the bar chart
        data = []
        for category in categories:
            filtered_df = df[df["category"] == category]
            data.append(
                go.Bar(
                    x=filtered_df["transaction_date"],
                    y=filtered_df["debit"],
                    name=category,
                    customdata=filtered_df["counter_account"],
                    marker=dict(
                        color=color_map[category],
                        line=dict(
                            width=0.5, color="rgba(0,0,0,0.5)"
                        ),  # Slight border around bars
                    ),
                    hovertemplate=f"<b>Category</b>: {category}<br>"
                    + "<b>Date</b>: %{x}<br>"
                    + "<b>Expense</b>: VND %{y:,.0f}<extra></extra>"
                    + "<b>Counter Account</b>: %{customdata}<extra></extra>",
                )
            )

        # Define layout for the grouped bar chart
        layout = go.Layout(
            title=dict(
                text="Detailed Transaction Analysis by Category",
                font=dict(family="Raleway", size=16, color="#4a4a4a"),
            ),
            font=dict(family="Raleway", size=12, color="#333333"),
            barmode="stack",  # Stack bars within each date
            plot_bgcolor="rgba(245, 245, 245, 1)",
            autosize=True,
            margin=dict(t=60, b=40, l=50, r=30),
            xaxis=dict(
                title="Transaction Date",
                tickangle=45,
                title_font=dict(size=12, color="#4a4a4a"),
                linecolor="#BBBBBB",
                linewidth=1.2,
                showgrid=True,
                gridcolor="rgba(200, 200, 200, 0.3)",
                ticks="outside",
                tickcolor="#AAAAAA",
                tickfont=dict(color="#4a4a4a"),
            ),
            yaxis=dict(
                title="Total Expenses (VND)",
                title_font=dict(size=12, color="#4a4a4a"),
                tickprefix="VND ",
                tickformat=",.0f",
                autorange=True,
                showline=True,
                linecolor="#BBBBBB",
                linewidth=1.2,
                showgrid=True,
                gridcolor="rgba(200, 200, 200, 0.3)",
                tickfont=dict(color="#4a4a4a"),
            ),
        )

        # Return the figure with "data" and "layout"
        fig = {"data": data, "layout": layout}

        return fig

    # table detail debit per category
    def detailed_debit_per_category(self, category_name):
        self.month_df["category"] = self.month_df["category"].fillna("null")
        category_df = self.month_df[
            self.month_df["category"].str.startswith(category_name)
        ]

        category_df = category_df.sort_values(by="debit", ascending=False)
        # Format credit and debit values using locale.currency

        formatted_debit = [
            locale.currency(value, grouping=True) for value in category_df["debit"]
        ]

        # Create a DataFrame with the required structure
        table_data = pd.DataFrame(
            {
                "Date": category_df["transaction_date"]
                .dt.strftime("%Y-%m-%d")
                .tolist(),
                "Debit": formatted_debit,
                "Category": category_df["category"].tolist(),
                "Account": category_df["counter_account"].tolist(),
                "Description": category_df["description"].tolist(),
            }
        )
        return table_data

    def expense_category_tree_map(self):
        # Clean the DataFrame by dropping NaN values
        month_df = self.month_df[self.month_df["debit"].notna()].copy()
        month_df = self.month_df[self.month_df["counter_account"].notna()].copy()
        month_df = self.month_df[self.month_df["category"].notna()].copy()

        month_df["Expense Category"] = month_df.apply(
            lambda row: categorize_expense(row["counter_account"], row["category"]),
            axis=1,
        )

        # Group by 'Expense Category' and sum the 'debit' amounts
        category_summary = (
            month_df.groupby("Expense Category")["debit"].sum().reset_index()
        )

        # Create the treemap
        fig = px.treemap(
            category_summary,
            path=["Expense Category"],
            values="debit",
            title="Phân bố chi phí theo nhóm",
        )

        return fig
