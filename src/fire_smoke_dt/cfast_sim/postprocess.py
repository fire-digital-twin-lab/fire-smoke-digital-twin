"""Normalize raw CFAST outputs to node and sensor time-series contracts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_raw_output(path: str | Path) -> pd.DataFrame:
    """Load one raw output file; exact column mapping is finalized after the debug case."""
    return pd.read_csv(path)


def normalize_output(raw: pd.DataFrame, *, scenario_id: str) -> pd.DataFrame:
    raise NotImplementedError("Define the CFAST column map and units from the first real output")
