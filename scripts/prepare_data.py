"""Construit la série horaire de trafic Internet et l'enregistre dans data/processed/.

Les fichiers sont traités un par un (faible consommation de mémoire).
Usage : python scripts/prepare_data.py [--cell 5161]
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.load import load_raw_file, aggregate_traffic  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--cell", type=int, default=None, help="identifiant de cellule (sinon zone entière)")
args = parser.parse_args()

root = Path(__file__).resolve().parents[1]
files = sorted((root / "data" / "raw").glob("sms-call-internet-mi-*.txt"))
if not files:
    sys.exit("Aucun fichier sms-call-internet-mi-*.txt dans data/raw/")

parts = []
for f in files:
    df = load_raw_file(f)
    parts.append(aggregate_traffic(df, cell_id=args.cell, freq="10min")["internet"])
    print(f"  {f.name} : {len(df)} lignes")

ten_min = pd.concat(parts).groupby(level=0).sum()
# Une heure sans aucun intervalle de 10 min (jour de fichier absent) reste NaN, et non 0
series = ten_min.resample("1h").sum(min_count=1).to_frame("internet")

name = f"traffic_cell_{args.cell}_1h.csv" if args.cell else "traffic_zone_1h.csv"
out = root / "data" / "processed" / name
series.to_csv(out)
print(f"{len(series)} points horaires, du {series.index.min()} au {series.index.max()}")
print(f"Heures manquantes : {int(series['internet'].isna().sum())}")
print(f"Enregistré : {out}")
