import pickle
import pandas as pd
from django.core.cache import cache

SESSION_TTL = 6000  # 100 minutes


def cache_dataframe(session_id: str, df: pd.DataFrame):
    cache.set(session_id, pickle.dumps(df), timeout=SESSION_TTL)


def get_cached_dataframe(session_id: str) -> pd.DataFrame:
    pickled = cache.get(session_id)
    if pickled:
        return pickle.loads(pickled)
    return None


def update_cached_dataframe(session_id: str, df: pd.DataFrame):
    cache_dataframe(session_id, df)