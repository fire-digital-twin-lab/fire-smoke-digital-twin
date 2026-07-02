"""Fallback graph construction from manually curated CSV tables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .graph_builder import build_graph


def load_manual_graph(nodes_csv: str | Path, edges_csv: str | Path):
    nodes = pd.read_csv(nodes_csv).to_dict(orient="records")
    edges = pd.read_csv(edges_csv).to_dict(orient="records")
    return build_graph(nodes, edges)
