from fastapi import APIRouter, HTTPException
from app.models import SubmitRequest
from app.utils.buffering import buffer_data

router = APIRouter(prefix="/submit", tags=["submit"])


@router.post("/", status_code=202)
async def submit_data(payload: SubmitRequest):
    try:
        buffer_data(payload.root)
        return {"message": "Data received and being processed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
