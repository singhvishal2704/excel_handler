import pandas as pd


def add_column(df: pd.DataFrame, new_column: str, expression: str) -> pd.DataFrame:
    try:
        df[new_column] = df.eval(expression)
        return df
    except Exception as e:
        raise ValueError(f"Failed to add column: {e}")


def filter_rows(df: pd.DataFrame, condition: str) -> pd.DataFrame:
    try:
        return df.query(condition)
    except Exception as e:
        raise ValueError(f"Failed to filter rows: {e}")


def combine_columns(df: pd.DataFrame, columns: list, new_column: str, separator: str = " ") -> pd.DataFrame:
    try:
        df[new_column] = df[columns].astype(str).agg(separator.join, axis=1)
        return df
    except Exception as e:
        raise ValueError(f"Failed to combine columns: {e}")