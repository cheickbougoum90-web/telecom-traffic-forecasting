"""Modèles de référence à battre avant ARIMA, Prophet, XGBoost et LSTM."""
import pandas as pd


def naive_seasonal(series: pd.Series, horizon: int, season: int = 24) -> pd.Series:
    """Prévision naïve saisonnière : répète le dernier cycle observé."""
    last = series.iloc[-season:].to_numpy()
    reps = -(-horizon // season)
    values = list(last) * reps
    idx = pd.date_range(series.index[-1] + series.index.freq, periods=horizon, freq=series.index.freq)
    return pd.Series(values[:horizon], index=idx)


def mae(y_true, y_pred) -> float:
    return float((pd.Series(y_true).to_numpy() - pd.Series(y_pred).to_numpy()).__abs__().mean())
