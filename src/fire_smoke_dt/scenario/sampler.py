"""Controlled scenario sampling; avoids an uncontrolled Cartesian explosion."""

from __future__ import annotations

import random
from collections.abc import Mapping, Sequence
from itertools import product
from typing import Any


def sample_scenarios(
    factors: Mapping[str, Sequence[Any]],
    *,
    count: int,
    seed: int,
) -> list[dict[str, Any]]:
    keys = list(factors)
    candidates = [
        dict(zip(keys, values, strict=True)) for values in product(*(factors[k] for k in keys))
    ]
    rng = random.Random(seed)
    if count >= len(candidates):
        rng.shuffle(candidates)
        return candidates
    return rng.sample(candidates, count)
