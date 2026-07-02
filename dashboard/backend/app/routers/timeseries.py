"""Timeseries endpoint placeholder."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/timeseries/{scenario_id}")
def get_timeseries(scenario_id: str | None = None):
    raise HTTPException(status_code=501, detail="Artifact store not wired yet")
