"""Composable virtual IoT degradation functions."""

from __future__ import annotations

import numpy as np


def gaussian(values, sigma: float, *, rng: np.random.Generator):
    x = np.asarray(values, dtype=float)
    return x + rng.normal(0.0, sigma, size=x.shape)


def delay(values, steps: int, *, fill_value=np.nan):
    x = np.asarray(values)
    if steps < 0:
        raise ValueError("steps must be non-negative")
    if steps == 0:
        return x.copy()
    out = np.empty_like(x, dtype=float)
    out[:steps] = fill_value
    out[steps:] = x[:-steps]
    return out


def apply_missing(values, probability: float, *, rng: np.random.Generator):
    x = np.asarray(values, dtype=float).copy()
    mask = rng.random(x.shape) < probability
    x[mask] = np.nan
    return x, mask


def stuck(values, start_index: int):
    x = np.asarray(values, dtype=float).copy()
    if 0 <= start_index < len(x):
        x[start_index:] = x[start_index]
    return x
