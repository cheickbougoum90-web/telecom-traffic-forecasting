"""Chargement et agrégation des données Telecom Italia (Milan, nov. à déc. 2013).

Format réel des fichiers journaliers (séparés par tabulation, sans en-tête) :
cell_id, timestamp (ms, UTC), country_code, sms_in, sms_out, call_in, call_out, internet.
Les lignes sont creuses : un champ vide ou absent signifie « aucune activité » pour cette mesure.
Il y a une ligne par cellule, par intervalle de 10 minutes et par code pays.
"""
from pathlib import Path
import pandas as pd

LOCAL_TZ = "Europe/Rome"  # les timestamps sont en UTC, mais les cycles d'activité suivent l'heure de Milan
COLUMNS = ["cell_id", "timestamp_ms", "country_code",
           "sms_in", "sms_out", "call_in", "call_out", "internet"]


def load_raw_file(path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", header=None, names=COLUMNS)
    df["timestamp"] = (pd.to_datetime(df["timestamp_ms"], unit="ms", utc=True)
                         .dt.tz_convert(LOCAL_TZ))
    return df.drop(columns="timestamp_ms")


def aggregate_traffic(df: pd.DataFrame, cell_id=None, freq: str = "1h") -> pd.DataFrame:
    """Série de trafic Internet (somme sur les codes pays), pour une cellule ou pour toute la zone.

    Un intervalle sans ligne pour une cellule est une absence d'activité : il est rempli par 0.
    """
    if cell_id is not None:
        df = df[df["cell_id"] == cell_id]
    ten_min = df.groupby("timestamp")["internet"].sum()
    full = pd.date_range(ten_min.index.min(), ten_min.index.max(), freq="10min")
    ten_min = ten_min.reindex(full, fill_value=0.0)
    out = ten_min.resample(freq).sum()
    return out.to_frame("internet")


def load_folder(folder, pattern: str = "sms-call-internet-mi-*.txt") -> pd.DataFrame:
    files = sorted(Path(folder).glob(pattern))
    if not files:
        raise FileNotFoundError(f"Aucun fichier {pattern} dans {folder}")
    return pd.concat([load_raw_file(f) for f in files], ignore_index=True)
