"""Model inference endpoint."""

from fastapi import APIRouter, HTTPException

from ..schemas import InferenceRequest

router = APIRouter()


@router.post("/inference")
def inference(request: InferenceRequest):
    if not request.history:
        raise HTTPException(status_code=422, detail="history window must not be empty")
    raise HTTPException(status_code=501, detail="Model service not wired yet")
