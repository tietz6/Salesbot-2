
from fastapi import APIRouter, Request
from .service import score_dialog, rubric_summary

router = APIRouter(prefix="/master_path_rubrics/v1", tags=["master_path_rubrics"])

@router.get("/rubric")
async def rubric():
    return rubric_summary()

@router.post("/score")
async def score(req: Request):
    data = await req.json()
    return score_dialog(data.get("history", []))
