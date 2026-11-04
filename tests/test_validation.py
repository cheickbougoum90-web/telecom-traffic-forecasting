import numpy as np
import pandas as pd
from src.models.validation import make_window, WINDOWS, calendar_exog, TZ
from src.models.baseline import naive_seasonal


def _series():
    idx = pd.date_range("2013-11-01", "2014-01-01 23:00", freq="1h", tz=TZ)
    return pd.Series(np.arange(len(idx), dtype=float), idx)


def test_windows_no_leakage():
    s = _series()
    for start, end in WINDOWS.values():
        train, test = make_window(s, start, end)
        assert train.index.max() < test.index.min()
        assert len(test) == 168


def test_calendar_exog_flags_holiday():
    idx = pd.date_range("2013-12-25", periods=24, freq="1h", tz=TZ)
    assert calendar_exog(idx)["is_holiday"].all()


def test_naive_seasonal_repeats_last_cycle():
    s = _series()
    train, test = make_window(s, *WINDOWS["test_1 (9 au 15 déc.)"])
    pred = naive_seasonal(train, test.index, season=168)
    assert np.allclose(pred.to_numpy(), train.iloc[-168:].to_numpy())
