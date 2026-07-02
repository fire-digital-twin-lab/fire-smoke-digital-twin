"""Time and sensor alignment helpers."""

from __future__ import annotations

import pandas as pd


def align_on_time(
    left: pd.DataFrame, right: pd.DataFrame, *, time_col: str = "time_s"
) -> tuple[pd.DataFrame, pd.DataFrame]:
    common = sorted(set(left[time_col]).intersection(right[time_col]))
    return left[left[time_col].isin(common)].copy(), right[right[time_col].isin(common)].copy()
