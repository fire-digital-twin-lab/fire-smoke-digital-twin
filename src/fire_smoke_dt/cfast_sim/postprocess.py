"""Normalize raw CFAST outputs to node and sensor time-series contracts."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_raw_output(path: str | Path) -> pd.DataFrame:
    """Load one raw output file."""
    # CFAST spreadsheet output is typically a CSV
    # Skip rows that are just headers/metadata if necessary
    # Assuming standard pandas read_csv works for the simplified output format
    return pd.read_csv(path)


def normalize_output(raw: pd.DataFrame, *, scenario_id: str) -> pd.DataFrame:
    """Parse output CSV of CFAST to Pandas DataFrame standard form."""
    if raw.empty:
        return raw
        
    df = raw.copy()
    
    # Clean up column names
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    # If time isn't explicitly named, assume first column is time
    if "time" not in df.columns and len(df.columns) > 0:
        first_col = df.columns[0]
        if "s" in first_col or "time" in first_col:
            df.rename(columns={first_col: "time"}, inplace=True)
            
    # Add scenario_id for tracking
    df["scenario_id"] = scenario_id
    
    return df
