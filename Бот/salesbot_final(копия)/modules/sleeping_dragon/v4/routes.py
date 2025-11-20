
from fastapi import APIRouter, Request
from .engine import DragonEngine

router = APIRouter(prefix="/sleeping_dragon/v4", tags=["sleeping_dragon"])

@router.post("/start")
async def start_telegram(req: Request):
    """Telegram bot integration endpoint - accepts chat_id"""
    data = await req.json()
    chat_id = data.get("chat_id")
    probe = data.get("probe", False)
    
    # Quick response for probe requests (discovery)
    if probe:
        return {"ok": True, "available": True}
    
    if not chat_id:
        return {"error": "chat_id required"}
    
    # Use chat_id as session ID for telegram users
    sid = str(chat_id)
    eng = DragonEngine(sid)
    eng.reset()
    
    return {
        "ok": True,
        "sid": sid,
        "reply": "🐉 Спящий дракон активирован!\n\n"
                 "Я буду выявлять твои ошибки в диалоге и давать рекомендации.\n"
                 "Начинай говорить как менеджер - я буду анализировать каждую фразу."
    }

@router.post("/start/{sid}")
async def start(sid:str):
    eng=DragonEngine(sid)
    eng.reset()
    return {"ok":True,"sid":sid}

@router.post("/handle/{sid}")
async def handle(sid:str, text:str):
    eng=DragonEngine(sid)
    return eng.handle(text)

@router.get("/snapshot/{sid}")
async def snapshot(sid:str):
    eng=DragonEngine(sid)
    return eng.snapshot()
