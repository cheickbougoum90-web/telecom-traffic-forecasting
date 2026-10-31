import pandas as pd
from src.data.load import load_raw_file, aggregate_traffic

# Lignes creuses, au format réel (tabulations, champs vides, lignes courtes)
SAMPLE = (
    "1\t1383260400000\t0\t0.08\n"
    "1\t1383260400000\t39\t0.14\t0.15\t0.16\t0.05\t11.0\n"
    "1\t1383261000000\t0\t0.13\t\t\t\t0.02\n"
    "2\t1383261000000\t39\t0.2\t0.1\t0.1\t0.1\t5.0\n"
)


def test_load_sparse_rows(tmp_path):
    p = tmp_path / "day.txt"
    p.write_text(SAMPLE)
    df = load_raw_file(p)
    assert len(df) == 4
    assert df["internet"].notna().sum() == 3
    # 1383260400000 ms = 2013-10-31 23:00 UTC = 2013-11-01 00:00 à Milan
    assert df["timestamp"].iloc[0].hour == 0


def test_aggregate_sums_and_fills_gaps(tmp_path):
    p = tmp_path / "day.txt"
    p.write_text(SAMPLE)
    df = load_raw_file(p)
    zone = aggregate_traffic(df, freq="10min")
    assert zone["internet"].iloc[0] == 11.0
    assert zone["internet"].iloc[1] == 5.02
    cell2 = aggregate_traffic(df, cell_id=2, freq="10min")
    assert len(cell2) == 1
