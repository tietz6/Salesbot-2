
from fastapi import APIRouter
from .engine import ExamAutoCheck

router = APIRouter(prefix="/exam/v2", tags=["exam"])

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
