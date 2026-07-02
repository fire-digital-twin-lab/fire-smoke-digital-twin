"""Reference comparison metrics with explicit masks."""

from __future__ import annotations

import numpy as np


def mae(a, b, mask=None) -> float:
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    valid = np.isfinite(x) & np.isfinite(y)
    if mask is not None:
        valid &= np.asarray(mask, dtype=bool)
    if not np.any(valid):
        return float("nan")
    return float(np.mean(np.abs(x[valid] - y[valid])))


def rmse(a, b, mask=None) -> float:
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    valid = np.isfinite(x) & np.isfinite(y)
    if mask is not None:
        valid &= np.asarray(mask, dtype=bool)
    if not np.any(valid):
        return float("nan")
    return float(np.sqrt(np.mean((x[valid] - y[valid]) ** 2)))
