import pandas as pd


def load_spreadsheet(path: str) -> pd.DataFrame:
    """Load an Excel spreadsheet into a DataFrame."""
    return pd.read_excel(path)