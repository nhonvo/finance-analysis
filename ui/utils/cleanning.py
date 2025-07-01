import pandas as pd
import locale

locale.setlocale(locale.LC_ALL, "vi_VN.utf8")

def hidden_data(df: pd.DataFrame, remove_column: str, name: str) -> pd.DataFrame:
    return df[~df[remove_column].str.contains(name, na=False)].copy()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Make a copy of the DataFrame to avoid modifying the original
    cleaned_df = df.copy()

    # Apply filters to remove unwanted rows
    cleaned_df = hidden_data(cleaned_df, "description", "TAT TOAN TAI KHOAN TIET KIEM")
    cleaned_df = hidden_data(cleaned_df, "description", "Tiết kiệm Điện tử")
    cleaned_df = hidden_data(
        cleaned_df, "counter_account", "TAT TOAN TAI KHOAN TIET KIEM"
    )
    cleaned_df = hidden_data(cleaned_df, "description", "TAT TOAN SO TIET KIEM")
    cleaned_df = hidden_data(cleaned_df, "description", "tiền nhận hộ cty")
    cleaned_df = hidden_data(cleaned_df, "category", "đầu tư")

    return cleaned_df

@staticmethod
def get_saving_df(df):
    saving_df = df[
        df["description"].str.startswith("TAT TOAN TAI KHOAN TIET KIEM")
        | df["description"].str.startswith("Tiết kiệm Điện tử")
        | df["description"].str.startswith("DONG TIET KIEM TK")
        | df["description"].str.startswith("TAT TOAN SO TIET KIEM")
        | df["category"].str.startswith("saving")
    ]
    saving_df = saving_df.fillna(0)
    saving_df["balance"] = saving_df["debit"] - saving_df["credit"]
    return saving_df


def get_investigate_df(df):
    df["category"] = df["category"].fillna("null").copy()
    investment_df = df[
        df["description"].str.startswith("đầu tư") 
        | df["category"].str.startswith("invest")
    ]
    investment_df = investment_df.fillna(0)
    investment_df["balance"] = investment_df["debit"] - investment_df["credit"]
    return investment_df
