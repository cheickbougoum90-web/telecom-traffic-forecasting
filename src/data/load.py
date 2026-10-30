"""Chargement et agrégation des données Telecom Italia (Milan, nov. à déc. 2013)."""
from pathlib import Path
import pandas as pd

# Format supposé des fichiers journaliers (séparés par tabulation) : à vérifier sur les fichiers réels
COLUMNS = ["cell_id", "timestamp_ms", "country_code",
           "sms_in", "sms_out", "call_in", "call_out", "internet"]


def load_raw_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", names=COLUMNS)
    df["timestamp"] = pd.to_datetime(df["timestamp_ms"], unit="ms", utc=True)
    return df.drop(columns="timestamp_ms")


def aggregate_traffic(df: pd.DataFrame, cell_id=None, freq: str = "1h") -> pd.DataFrame:
    """Série temporelle de trafic Internet, pour une cellule ou pour toute la zone."""
    if cell_id is not None:
        df = df[df["cell_id"] == cell_id]
    series = (df.set_index("timestamp")["internet"]
                .groupby(pd.Grouper(freq=freq)).sum(min_count=1))
    return series.to_frame("internet")
