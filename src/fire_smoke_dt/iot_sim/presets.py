"""Load and validate named noise presets."""

from __future__ import annotations

from pathlib import Path

import yaml


def load_presets(path: str | Path) -> dict:
    payload = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if "presets" not in payload:
        raise ValueError("noise preset config must contain 'presets'")
    return payload["presets"]
