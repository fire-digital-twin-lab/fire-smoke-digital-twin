"""Join graph, scenario, sensor and labels into model-ready artifacts."""

from __future__ import annotations

from pathlib import Path


def build_dataset(*, source_dir: str | Path, target_dir: str | Path) -> None:
    """Implement joins only after all upstream column contracts are locked."""
    raise NotImplementedError(
        "See docs/data_contracts.md and add contract tests before implementation"
    )
