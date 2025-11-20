
from fastapi import APIRouter, Request
from .service import start_session, append_message, analyze_session, list_sessions

router = APIRouter(prefix="/dialog_memory/v1", tags=["dialog_memory"])

@router.post("/start")
async def start(req: Request):
    data = await req.json()
    # Support both manager_id and chat_id for telegram compatibility
    manager_id = data.get("manager_id") or data.get("chat_id")
    if manager_id is not None:
        manager_id = str(manager_id)
    else:
        manager_id = "unknown"
    
    # Quick response for probe requests (discovery)
    probe = data.get("probe", False)
    if probe:
        return {"ok": True, "available": True}
    
    result = start_session(manager_id)
    
    # For telegram, add a user-friendly reply
    if data.get("chat_id"):
        result["reply"] = f"💾 Память диалогов активирована!\n\n" \
                          f"Сессия: {result.get('session_id', 'unknown')}\n\n" \
                          f"Все диалоги будут сохраняться для анализа."
    
    return result

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
