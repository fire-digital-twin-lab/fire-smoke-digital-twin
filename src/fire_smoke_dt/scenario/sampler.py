"""Controlled scenario sampling; avoids an uncontrolled Cartesian explosion."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from itertools import product
from typing import Any


def _estimate_cartesian_size(factors: Mapping[str, Sequence[Any]]) -> int:
    size = 1
    for values in factors.values():
        size *= len(values)
    return size


def _lazy_sample(
    factors: Mapping[str, Sequence[Any]], count: int, seed: int
) -> list[dict[str, Any]]:
    keys = list(factors)
    rng = random.Random(seed)
    
    # Reservoir sampling
    reservoir: list[dict[str, Any]] = []
    
    iterator = product(*(factors[k] for k in keys))
    
    for i, values in enumerate(iterator):
        item = dict(zip(keys, values, strict=True))
        if i < count:
            reservoir.append(item)
        else:
            j = rng.randint(0, i)
            if j < count:
                reservoir[j] = item
                
    # Shuffle at the end to ensure random order
    rng.shuffle(reservoir)
    return reservoir


def sample_scenarios(
    factors: Mapping[str, Sequence[Any]],
    *,
    count: int,
    seed: int,
) -> list[dict[str, Any]]:
    """Sample scenarios from the Cartesian product of factors.

    Always uses reservoir sampling — no materialization regardless of size.
    """
    total = _estimate_cartesian_size(factors)
    effective_count = min(count, total)
    return _lazy_sample(factors, effective_count, seed)
