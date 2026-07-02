"""Single source of truth for P0 smoke and arrival labels."""

from __future__ import annotations

import numpy as np


def smoke_label(
    obscuration: np.ndarray,
    *,
    threshold: float,
    persistence_steps: int,
) -> np.ndarray:
    """Return a binary label that is true after consecutive threshold exceedances.

    The input is ordered by time on the last axis. The returned array has the same shape.
    """
    values = np.asarray(obscuration, dtype=float)
    if persistence_steps < 1:
        raise ValueError("persistence_steps must be >= 1")
    above = values >= threshold
    out = np.zeros_like(above, dtype=np.int8)
    if persistence_steps == 1:
        return above.astype(np.int8)
    for t in range(persistence_steps - 1, above.shape[-1]):
        out[..., t] = np.all(above[..., t - persistence_steps + 1 : t + 1], axis=-1)
    return out


def arrival_time_abs(
    labels: np.ndarray,
    time_s: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Return first positive time and a validity mask for each series."""
    y = np.asarray(labels)
    ts = np.asarray(time_s, dtype=float)
    if y.shape[-1] != ts.shape[0]:
        raise ValueError("labels time axis and time_s length differ")
    valid = np.any(y == 1, axis=-1)
    first = np.argmax(y == 1, axis=-1)
    arrival = np.where(valid, ts[first], np.nan)
    return arrival, valid.astype(np.int8)


def time_to_arrival(arrival_s: np.ndarray, current_time_s: float) -> np.ndarray:
    """Compute max(arrival-current, 0), preserving NaN for invalid arrivals."""
    arrival = np.asarray(arrival_s, dtype=float)
    return np.where(np.isnan(arrival), np.nan, np.maximum(arrival - current_time_s, 0.0))
