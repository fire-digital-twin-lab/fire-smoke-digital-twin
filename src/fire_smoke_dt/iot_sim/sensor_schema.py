



"""IoT Sensor configurations mapping."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field

from fire_smoke_dt.shared.schema import SensorType


class SensorDevice(BaseModel):
    """Configuration for a single IoT sensor deployed in a building."""
    
    device_id: str
    node_id: str
    sensor_type: SensorType
    height_m: float = Field(default=2.5, ge=0.0)
    x_m: float | None = None
    y_m: float | None = None
    properties: dict[str, Any] = Field(default_factory=dict)


class SensorConfig(BaseModel):
    """Collection of IoT sensors deployed in a scenario or building."""
    
    devices: list[SensorDevice] = Field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: str | Path) -> SensorConfig:
        with Path(path).open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return cls(**data)
