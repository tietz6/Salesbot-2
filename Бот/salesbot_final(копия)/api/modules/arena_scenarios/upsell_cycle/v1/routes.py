
from fastapi import APIRouter
from .service import list_scenarios, random_scenario

router = APIRouter(prefix="/arena_scenarios/upsell_cycle/v1", tags=["arena_scenarios"])

@router.get("/list")
async def ls():
    return list_scenarios()

@router.get("/random")
async def rnd():
    return random_scenario()
