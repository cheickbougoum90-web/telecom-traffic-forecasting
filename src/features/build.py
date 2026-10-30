"""Variables dérivées du temps pour les modèles de boosting."""
import pandas as pd


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["hour"] = out.index.hour
    out["dayofweek"] = out.index.dayofweek
    out["is_weekend"] = (out.index.dayofweek >= 5).astype(int)
    return out


def add_lags(df: pd.DataFrame, col: str = "internet", lags=(1, 24, 168)) -> pd.DataFrame:
    out = df.copy()
    for lag in lags:
        out[f"{col}_lag{lag}"] = out[col].shift(lag)
    return out
