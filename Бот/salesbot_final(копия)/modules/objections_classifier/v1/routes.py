
from fastapi import APIRouter, Request
from .service import classify, apply_patterns, score_response

router = APIRouter(prefix="/objections_classifier/v1", tags=["objections_classifier"])

@router.post("/classify")
async def r_classify(req: Request):
    data = await req.json()
    return classify(data.get("utterance",""), data.get("history"))

@router.post("/patterns")
async def r_patterns(req: Request):
    data = await req.json()
    return apply_patterns(data.get("type","doubts"), data.get("history"), data.get("last_reply",""))

@router.post("/score")
async def r_score(req: Request):
    data = await req.json()
    return score_response(data.get("last_reply",""))
