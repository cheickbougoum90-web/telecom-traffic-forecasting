"""Protocole de validation commun à tous les modèles (même découpage, mêmes métriques)."""
from typing import Callable
import numpy as np
import pandas as pd

from src.models.metrics import mae, rmse, mape, peak_mask

TZ = "Europe/Rome"

# Jours qui se comportent comme des dimanches malgré un jour de semaine
HOLIDAYS = [pd.Timestamp(d).date() for d in
            ("2013-11-01", "2013-12-25", "2013-12-26", "2014-01-01")]

# Entraînement jusqu'au 8 décembre 23 h ; deux fenêtres de test de 7 jours ; test de résistance à part
WINDOWS = {
    "test_1 (9 au 15 déc.)": ("2013-12-09", "2013-12-15"),
    "test_2 (16 au 22 déc.)": ("2013-12-16", "2013-12-22"),
}
STRESS = {"résistance (23 déc. au 1er janv.)": ("2013-12-23", "2014-01-01")}


def calendar_exog(index: pd.DatetimeIndex) -> pd.DataFrame:
    """Variables exogènes : week-end et jour férié."""
    is_holiday = pd.Index(index.date).isin(HOLIDAYS)
    return pd.DataFrame({"is_weekend": (index.day_of_week >= 5).astype(float),
                         "is_holiday": is_holiday.astype(float)}, index=index)


def make_window(series: pd.Series, start: str, end: str):
    """Renvoie (train, test) : train = tout ce qui précède start, test = de start à end inclus."""
    t0 = pd.Timestamp(start, tz=TZ)
    t1 = pd.Timestamp(end, tz=TZ) + pd.Timedelta(hours=23)
    return series[series.index < t0], series[(series.index >= t0) & (series.index <= t1)]


def evaluate(forecast_fn: Callable[[pd.Series, pd.DatetimeIndex], pd.Series],
             series: pd.Series, windows: dict, model_name: str) -> pd.DataFrame:
    """Applique forecast_fn(train, index_test) sur chaque fenêtre et calcule les métriques.

    Le train de chaque fenêtre contient tout l'historique précédent (origine glissante).
    """
    rows = []
    for name, (start, end) in windows.items():
        train, test = make_window(series, start, end)
        pred = forecast_fn(train, test.index)
        mask = peak_mask(test.index, HOLIDAYS)
        rows.append({
            "modèle": model_name, "fenêtre": name, "n_heures": len(test),
            "MAE": mae(test, pred), "RMSE": rmse(test, pred), "MAPE_%": mape(test, pred),
            "MAE_pointe": mae(test[mask], pred[mask]) if mask.any() else np.nan,
        })
    return pd.DataFrame(rows)
