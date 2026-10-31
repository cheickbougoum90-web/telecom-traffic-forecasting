"""Construit la série horaire de trafic Internet et l'enregistre dans data/processed/.

Usage : python scripts/prepare_data.py [--cell 5161]
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data.load import load_folder, aggregate_traffic  # noqa: E402

parser = argparse.ArgumentParser()
parser.add_argument("--cell", type=int, default=None, help="identifiant de cellule (sinon zone entière)")
args = parser.parse_args()

root = Path(__file__).resolve().parents[1]
raw = load_folder(root / "data" / "raw")
series = aggregate_traffic(raw, cell_id=args.cell, freq="1h")

name = f"traffic_cell_{args.cell}_1h.csv" if args.cell else "traffic_zone_1h.csv"
out = root / "data" / "processed" / name
series.to_csv(out)
print(f"{len(series)} points horaires, du {series.index.min()} au {series.index.max()}")
print(f"Enregistré : {out}")
