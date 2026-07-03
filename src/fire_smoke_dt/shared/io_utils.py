"""I/O helpers with explicit UTF-8 and deterministic JSON formatting."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from .paths import get_producer_version
from .schema import ArtifactEnvelope


def make_envelope(payload: dict[str, Any], config: dict[str, Any], *, schema_version: str) -> ArtifactEnvelope:
    import datetime
    import hashlib

    # Sort config to ensure deterministic hash
    config_json = json.dumps(config, sort_keys=True)
    config_hash = hashlib.sha256(config_json.encode("utf-8")).hexdigest()

    return ArtifactEnvelope(
        schema_version=schema_version,
        producer_version=get_producer_version(),
        config_hash=config_hash,
        created_at=datetime.datetime.now(datetime.UTC).isoformat(),
        payload=payload,
    )


def read_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def write_artifact(path: str | Path, envelope: ArtifactEnvelope) -> None:
    write_json(path, envelope.model_dump())


def read_artifact(path: str | Path) -> ArtifactEnvelope:
    data = read_json(path)
    return ArtifactEnvelope(**data)


def read_parquet(path: str | Path) -> pd.DataFrame:
    return pd.read_parquet(path)


def write_parquet(path: str | Path, frame: pd.DataFrame) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(target, index=False)
