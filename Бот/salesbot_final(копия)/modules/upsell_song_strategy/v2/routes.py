
from fastapi import APIRouter
from .service import warmup_message, after_texts_message, ladder_offer, cross_sell, phases, suggest_next_phase

router = APIRouter(prefix="/upsell_song_strategy/v2", tags=["upsell_song_strategy"])

@router.get("/phases")
async def get_phases():
    return phases()

@router.get("/warmup")
async def get_warmup():
    return {"text": warmup_message()}

@router.get("/after_texts")
async def get_after_texts():
    return {"text": after_texts_message()}

@router.get("/ladder")
async def get_ladder():
    return ladder_offer()

@router.get("/cross_sell")
async def get_cross():
    return cross_sell()

@router.get("/next/{current_id}")
async def next_phase(current_id: str):
    return suggest_next_phase(current_id)
