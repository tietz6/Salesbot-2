
from fastapi import APIRouter, Request
from .service import detect

router = APIRouter(prefix="/emotion_detector/v1", tags=["emotion_detector"])

@router.post("/analyze")
async def analyze(req: Request):
    data = await req.json()
    return detect(data)
