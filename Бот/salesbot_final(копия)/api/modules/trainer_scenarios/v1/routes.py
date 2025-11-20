
from fastapi import APIRouter
from .service import list_scenarios, random_scenario, rubric

router = APIRouter(prefix="/trainer_scenarios/v1", tags=["trainer_scenarios"])

@router.get("/list")
async def ls():
    return list_scenarios()

@router.get("/random")
async def rnd():
    return random_scenario()

@router.get("/rubric")
async def rb():
    return rubric()
