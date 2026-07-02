"""Scenario identifiers and catalog serialization."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def stable_scenario_id(payload: dict[str, Any], *, prefix: str = "SCN") -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return f"{prefix}-{hashlib.sha256(canonical.encode()).hexdigest()[:12]}"
