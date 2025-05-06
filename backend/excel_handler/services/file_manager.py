import pandas as pd
from io import BytesIO

def read_excel_file(file) -> pd.DataFrame:
    return pd.read_excel(file)


def write_excel_to_memory(df: pd.DataFrame) -> BytesIO:
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine='openpyxl')
    buffer.seek(0)
    return buffer
