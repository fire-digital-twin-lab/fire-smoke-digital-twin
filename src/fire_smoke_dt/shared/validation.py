"""Validation helpers for module boundary artifacts."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def require_columns(frame: pd.DataFrame, required: Iterable[str], *, name: str) -> None:
    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"{name} is missing required columns: {missing}")


def require_unique(frame: pd.DataFrame, keys: list[str], *, name: str) -> None:
    if frame.duplicated(keys).any():
        raise ValueError(f"{name} contains duplicate key rows for {keys}")


def validate_split_disjoint(train: set[str], val: set[str], test: set[str]) -> None:
    if train & val or train & test or val & test:
        raise ValueError("Split sets overlap")


def validate_envelope(envelope: object) -> None:
    """Validate an artifact envelope has required metadata."""
    units = getattr(envelope, "units", None)
    if units is None:
        raise ValueError("ArtifactEnvelope is missing required field: units")
    if not units:
        raise ValueError("ArtifactEnvelope.units must not be empty")

