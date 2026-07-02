"""Orchestrate clean -> noisy stream while preserving masks and provenance."""

from __future__ import annotations

import numpy as np

from .noise_models import apply_missing, delay, gaussian


def simulate(values, preset: dict, *, seed: int) -> dict[str, np.ndarray]:
    rng = np.random.default_rng(seed)
    out = np.asarray(values, dtype=float).copy()
    out = gaussian(out, float(preset.get("gaussian_sigma", 0.0)), rng=rng)
    out = delay(out, int(preset.get("delay_steps", 0)))
    out, missing_mask = apply_missing(out, float(preset.get("missing_probability", 0.0)), rng=rng)
    return {"values": out, "missing_mask": missing_mask}
