
from fastapi import APIRouter, Request
from .service import start_session, append_message, analyze_session, list_sessions

router = APIRouter(prefix="/dialog_memory/v1", tags=["dialog_memory"])

@router.post("/start")
async def start(req: Request):
    data = await req.json()
    manager_id = data.get("manager_id", "unknown")
    return start_session(manager_id)

@router.post("/append")
async def append(req: Request):
    data = await req.json()
    return append_message(
        data.get("manager_id"),
        data.get("session_id"),
        data.get("role"),
        data.get("content"),
        data.get("stage")
    )

@router.post("/analyze")
async def analyze(req: Request):
    data = await req.json()
    return analyze_session(data.get("manager_id"), data.get("session_id"))

@router.get("/list/{manager_id}")
async def list_all(manager_id: str):
    return list_sessions(manager_id)
