
from fastapi import APIRouter, Request
from .service import grade

router = APIRouter(prefix="/trainer_exam/v1", tags=["trainer_exam"])

@router.post("/grade")
async def g(req: Request):
    data = await req.json()
    return grade(data)
