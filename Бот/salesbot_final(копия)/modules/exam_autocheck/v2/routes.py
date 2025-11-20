
from fastapi import APIRouter, Request
from .engine import ExamAutoCheck

router = APIRouter(prefix="/exam/v2", tags=["exam"])

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
    ex = ExamAutoCheck(sid)
    result = ex.start()
    
    return {
        "ok": True,
        "sid": sid,
        "reply": f"📝 Автоматическая проверка экзамена!\n\n"
                 f"Модуль: {result['module']}\n\n"
                 f"Я буду задавать вопросы и оценивать твои ответы.\n"
                 f"Всего 5 вопросов. Начнём!"
    }

@router.post("/start/{sid}")
async def start(sid:str):
    ex=ExamAutoCheck(sid)
    return ex.start()

@router.post("/answer/{sid}")
async def answer(sid:str, text:str):
    ex=ExamAutoCheck(sid)
    return ex.answer(text)

@router.get("/result/{sid}")
async def result(sid:str):
    ex=ExamAutoCheck(sid)
    return ex.result()
