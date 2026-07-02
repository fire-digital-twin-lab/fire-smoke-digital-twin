"""Scenarios endpoint placeholder."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/scenarios")
def get_scenarios(scenario_id: str | None = None):
    raise HTTPException(status_code=501, detail="Artifact store not wired yet")
