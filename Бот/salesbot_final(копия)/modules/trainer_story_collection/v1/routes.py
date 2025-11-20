
from fastapi import APIRouter, Request
from .service import evaluate_story

router = APIRouter(prefix="/trainer_story_collection/v1", tags=["trainer_story_collection"])

@router.post("/evaluate")
async def ev(req: Request):
    data = await req.json()
    return evaluate_story(data)
