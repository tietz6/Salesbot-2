
from fastapi import APIRouter, Request
from .service import advise

router = APIRouter(prefix="/trainer_upsell_master/v1", tags=["trainer_upsell_master"])

@router.post("/advise")
async def a(req: Request):
    data = await req.json()
    return advise(data)
