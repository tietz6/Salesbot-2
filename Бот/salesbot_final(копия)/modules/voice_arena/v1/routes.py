
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from .service import new_session, load_session, handle_turn, stop_and_score

router = APIRouter(prefix="/voice_arena/v1", tags=["voice_arena"])

BASE = os.path.dirname(__file__)
TPL = os.path.join(BASE, "templates")
STATIC = os.path.join(BASE, "static")

env = Environment(loader=FileSystemLoader(TPL), autoescape=select_autoescape(["html","xml"]))

@router.get("/static/arena.css")
async def css():
    return FileResponse(os.path.join(STATIC,"arena.css"))

@router.post("/start")
async def start(req: Request):
    data = await req.json()
    manager_id = data.get("manager_id","unknown")
    ctx = data.get("context","")
    # also create dialog_memory session for same id so we can append later
    rec = new_session(manager_id, ctx)
    try:
        from modules.dialog_memory.v1.service import start_session as dm_start
        dm_start(manager_id)  # returns new id, но в service.stop_and_score делаем бэкофф по arena-id
    except Exception:
        pass
    return rec

@router.get("/start_ui/{manager_id}", response_class=HTMLResponse)
async def start_ui(manager_id: str):
    rec = new_session(manager_id, "Voice Arena")
    s = load_session(manager_id, rec["session_id"]) or rec
    tpl = env.get_template("arena.html")
    return HTMLResponse(tpl.render(manager_id=manager_id, session_id=rec["session_id"], ctx=s.get("context",""), history=s.get("history",[]), last=s.get("last_metrics",{})))

@router.post("/turn")
async def turn(req: Request):
    data = await req.json()
    out = handle_turn(data.get("manager_id"), data.get("session_id"), data.get("text",""), data.get("features") or {})
    return out

@router.get("/ui/{manager_id}/{session_id}", response_class=HTMLResponse)
async def ui(manager_id: str, session_id: str):
    s = load_session(manager_id, session_id)
    if not s:
        return HTMLResponse("<h3>Сессия не найдена</h3>", status_code=404)
    tpl = env.get_template("arena.html")
    return HTMLResponse(tpl.render(manager_id=manager_id, session_id=session_id, ctx=s.get("context",""), history=s.get("history",[]), last=s.get("last_metrics",{})))

@router.get("/stop/{manager_id}/{session_id}")
async def stop(manager_id: str, session_id: str):
    return stop_and_score(manager_id, session_id)
