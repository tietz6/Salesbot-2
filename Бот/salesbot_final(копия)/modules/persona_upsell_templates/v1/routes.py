
from fastapi import APIRouter
from .service import load, sample
router = APIRouter(prefix="/persona_upsell/v1", tags=["persona_upsell"])

@router.get("/persona")
async def persona():
    return load()

@router.get("/sample/{key}")
async def pick(key: str):
    return {"text": sample(key)}
