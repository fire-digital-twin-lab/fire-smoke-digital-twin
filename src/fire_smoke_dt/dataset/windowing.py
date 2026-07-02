"""Create causal time windows that never look beyond the prediction time."""

from __future__ import annotations

import numpy as np


def causal_windows(values, history_steps: int, horizon_steps: int):
    x = np.asarray(values)
    if history_steps < 1 or horizon_steps < 1:
        raise ValueError("history_steps and horizon_steps must be positive")
    inputs, targets = [], []
    for end in range(history_steps - 1, len(x) - horizon_steps):
        inputs.append(x[end - history_steps + 1 : end + 1])
        targets.append(x[end + horizon_steps])
    return np.asarray(inputs), np.asarray(targets)
