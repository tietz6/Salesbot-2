
from fastapi import APIRouter, Request
from .service import evaluate

router = APIRouter(prefix="/trainer_core/v1", tags=["trainer_core"])

@router.post("/evaluate")
async def ev(req: Request):
    data = await req.json()
    text = data.get("text","")
    return evaluate(text)
