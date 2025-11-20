
from fastapi import APIRouter, Request
from .service import new_session, turn, stop

router = APIRouter(prefix="/trainer_dialog_engine/v1", tags=["trainer_dialog_engine"])

@router.post("/start")
async def start(req: Request):
    data = await req.json()
    return new_session(data.get("manager_id","unknown"), data.get("scenario_id","cold_start_warm"))

@router.post("/turn")
async def go(req: Request):
    data = await req.json()
    return turn(data.get("sid"), data.get("text",""))

@router.post("/stop")
async def fin(req: Request):
    data = await req.json()
    return stop(data.get("sid"))
