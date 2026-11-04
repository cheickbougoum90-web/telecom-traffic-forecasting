"""Modèles de référence à battre avant SARIMA, Prophet, XGBoost et LSTM."""
import numpy as np
import pandas as pd


def naive_seasonal(train: pd.Series, index: pd.DatetimeIndex, season: int = 168) -> pd.Series:
    """Répète le dernier cycle observé : 24 pour la veille, 168 pour la semaine précédente."""
    last = train.iloc[-season:].to_numpy()
    values = np.resize(last, len(index))
    return pd.Series(values, index=index, name="prediction")
