
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, FileResponse
import os

router = APIRouter(prefix="/trainer_arena_pro/v1", tags=["trainer_arena_pro"])

BASE = os.path.dirname(__file__)
STATIC = os.path.join(BASE,"static")

@router.get("/static/pro.css")
async def css():
    return FileResponse(os.path.join(STATIC,"pro.css"))

@router.get("/dashboard", response_class=HTMLResponse)
async def dash():
    html = open(os.path.join(BASE,"templates","arena_pro.html"),"r",encoding="utf-8").read()
    # simple render (no jinja here to reduce deps)
    html = html.replace("{{ scenarios }}","7").replace("{{ avg_warmth }}","62").replace("{{ avg_empathy }}","58").replace("{{ avg_questions }}","47")
    return HTMLResponse(html)
