"""Shared enums and typed records used at module boundaries."""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class NodeType(StrEnum):
    ROOM = "room"
    CORRIDOR = "corridor"
    STAIR = "stair"
    SHAFT = "shaft"
    LOBBY = "lobby"
    OUTSIDE = "outside"


class EdgeType(StrEnum):
    DOOR = "door"
    WINDOW = "window"
    OPENING = "opening"
    CORRIDOR_LINK = "corridor_link"
    STAIR_VERTICAL = "stair_vertical"
    SHAFT_VERTICAL = "shaft_vertical"
    OUTSIDE_CONNECTION = "outside_connection"


class SensorType(StrEnum):
    SMOKE = "smoke"
    TEMPERATURE = "temperature"
    DOOR_STATE = "door_state"
    ALARM = "alarm"
    CO = "co"


class NodeStatic(BaseModel):
    node_id: str
    ifc_global_id: str | None = None
    node_type: NodeType
    floor_id: str
    area_m2: float | None = Field(default=None, ge=0)
    volume_m3: float | None = Field(default=None, ge=0)
    ceiling_height_m: float | None = Field(default=None, ge=0)
    properties: dict[str, Any] = Field(default_factory=dict)


class EdgeStatic(BaseModel):
    edge_id: str
    source: str
    target: str
    edge_type: EdgeType
    opening_area_m2: float | None = Field(default=None, ge=0)
    opening_height_m: float | None = Field(default=None, ge=0)
    is_vertical: bool = False
    properties: dict[str, Any] = Field(default_factory=dict)


class ScenarioMetadata(BaseModel):
    building_id: str
    scenario_id: str
    base_scenario_id: str
    fire_node: str
    fire_floor: str
    t_end_s: float = Field(gt=0)
    dt_out_s: float = Field(gt=0)
    config: dict[str, Any] = Field(default_factory=dict)


class ArtifactEnvelope(BaseModel):
    schema_version: str
    producer_version: str
    config_hash: str
    created_at: str
    units: dict[str, str]
    payload: dict[str, Any]
