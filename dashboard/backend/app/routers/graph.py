"""Graph endpoint placeholder."""

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/graph/{scenario_id}")
def get_graph(scenario_id: str | None = None):
    raise HTTPException(status_code=501, detail="Artifact store not wired yet")
