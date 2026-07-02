"""Request/response models for the dashboard API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    scenario_id: str
    prediction_time_s: float = Field(ge=0)
    history: list[dict]


class NodePrediction(BaseModel):
    node_id: str
    smoke_probability: float = Field(ge=0, le=1)
    time_to_arrival_s: float | None = Field(default=None, ge=0)
