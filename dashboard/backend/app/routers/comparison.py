"""Comparison endpoint placeholder."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/comparison/{scenario_id}")
def get_comparison(scenario_id: str | None = None):
    raise HTTPException(status_code=501, detail="Artifact store not wired yet")
