
from fastapi import APIRouter, Request
from .service import analyze_reply, suggest_fix

router = APIRouter(prefix="/sleep_dragon_rules/v1", tags=["sleeping_dragon_rules"])

@router.post("/score")
async def score(req: Request):
    data = await req.json()
    return analyze_reply(data.get("history"), data.get("reply",""), data.get("stage"))

@router.post("/suggest")
async def suggest(req: Request):
    data = await req.json()
    return suggest_fix(data.get("history"), data.get("reply",""), data.get("stage"))
