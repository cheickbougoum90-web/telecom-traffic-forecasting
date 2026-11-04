"""SARIMA avec variables exogènes calendaires (week-end, jour férié)."""
import numpy as np
import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

from src.models.validation import calendar_exog


def fit_sarima(train: pd.Series, order=(2, 0, 0), seasonal_order=(1, 1, 1, 24), log: bool = True):
    y = np.log(train) if log else train
    model = SARIMAX(y, exog=calendar_exog(train.index), order=order, seasonal_order=seasonal_order,
                    enforce_stationarity=False, enforce_invertibility=False)
    return model.fit(disp=False, maxiter=200)


def sarima_forecast(train: pd.Series, index: pd.DatetimeIndex, order=(2, 0, 0),
                    seasonal_order=(1, 1, 1, 24), log: bool = True) -> pd.Series:
    res = fit_sarima(train, order, seasonal_order, log)
    pred = res.get_forecast(steps=len(index), exog=calendar_exog(index)).predicted_mean
    pred.index = index
    return np.exp(pred) if log else pred
