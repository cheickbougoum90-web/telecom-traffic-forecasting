"""Métriques de prévision. La MAE est la métrique principale, plus robuste aux pics isolés."""
import numpy as np
import pandas as pd


def mae(y_true, y_pred) -> float:
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def rmse(y_true, y_pred) -> float:
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


def mape(y_true, y_pred) -> float:
    y_true = np.asarray(y_true)
    return float(np.mean(np.abs((y_true - np.asarray(y_pred)) / y_true)) * 100)


def peak_mask(index: pd.DatetimeIndex, holidays) -> np.ndarray:
    """Heures chargées : jours ouvrés non fériés, de 12 h à 18 h (heure de Milan)."""
    is_holiday = pd.Index(index.date).isin(list(holidays))
    return (index.day_of_week < 5) & (~is_holiday) & (index.hour >= 12) & (index.hour < 18)
