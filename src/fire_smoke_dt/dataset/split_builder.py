"""Group-aware split creation by base_scenario_id."""

from __future__ import annotations

import random


def split_groups(groups: list[str], *, train: float, val: float, seed: int) -> dict[str, list[str]]:
    if not 0 < train < 1 or not 0 <= val < 1 or train + val >= 1:
        raise ValueError("Invalid split ratios")
    unique = sorted(set(groups))
    random.Random(seed).shuffle(unique)
    n_train = round(len(unique) * train)
    n_val = round(len(unique) * val)
    return {
        "train": unique[:n_train],
        "validation": unique[n_train : n_train + n_val],
        "test": unique[n_train + n_val :],
    }
