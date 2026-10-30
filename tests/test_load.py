import pandas as pd
from src.data.load import aggregate_traffic


def test_aggregate_traffic_hourly_sum():
    ts = pd.date_range("2013-11-01", periods=6, freq="10min", tz="UTC")
    df = pd.DataFrame({"cell_id": 1, "timestamp": ts, "internet": [1, 2, 3, 4, 5, 6]})
    out = aggregate_traffic(df, freq="1h")
    assert out["internet"].iloc[0] == 21
