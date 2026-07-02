"""Reduce FDS device/field output to aligned node/sensor series."""

from __future__ import annotations

import pandas as pd


def align_devices(
    devices: pd.DataFrame, sensor_schema: pd.DataFrame, *, dt_out_s: float
) -> pd.DataFrame:
    raise NotImplementedError(
        "Map FDS devices to the shared sensor schema and interpolate to dt_out"
    )
