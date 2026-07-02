"""Centralized project paths; do not scatter relative paths across modules."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = Path(os.getenv("FIRE_SMOKE_DATA_DIR", PROJECT_ROOT / "data"))
OUTPUT_DIR = Path(os.getenv("FIRE_SMOKE_OUTPUT_DIR", PROJECT_ROOT / "outputs"))
CONFIG_DIR = PROJECT_ROOT / "configs"
