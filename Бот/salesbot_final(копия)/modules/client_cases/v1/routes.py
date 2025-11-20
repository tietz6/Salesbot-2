
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os, json
from .service import list_cases, get_case, top_seller_reply, coach_generate_pitch, arena_context

router = APIRouter(prefix="/client_cases/v1", tags=["client_cases"])

BASE = os.path.dirname(__file__)
TPL = os.path.join(BASE, "templates")
STATIC = os.path.join(BASE, "static")

env = Environment(loader=FileSystemLoader(TPL), autoescape=select_autoescape(["html","xml"]))

@router.get("/static/cases.css")
async def css():
    return FileResponse(os.path.join(STATIC, "cases.css"))

@router.get("/list")
async def api_list(goal: str = None, budget: str = None, persona: str = None):
    return list_cases(goal, budget, persona)

@router.get("/get/{case_id}")
async def api_get(case_id: str):
    c = get_case(case_id)
    if not c:
        return JSONResponse({"error":"not found"}, status_code=404)
    return c

@router.get("/catalog", response_class=HTMLResponse)
async def catalog(goal: str = None, budget: str = None, persona: str = None):
    items = list_cases(goal, budget, persona)
    t = env.get_template("catalog.html")
    return HTMLResponse(t.render(cases=items))

@router.get("/view/{case_id}", response_class=HTMLResponse)
async def view(case_id: str):
    c = get_case(case_id)
    if not c:
        return HTMLResponse("<h3>Кейс не найден</h3>", status_code=404)
    t = env.get_template("view.html")
    return HTMLResponse(t.render(case=c))

@router.get("/top_seller/{case_id}")
async def top_seller(case_id: str):
    c = get_case(case_id)
    if not c:
        return JSONResponse({"error":"not found"}, status_code=404)
    return {"answer": top_seller_reply(c)}

@router.get("/coach_pitch/{case_id}")
async def coach_pitch(case_id: str, tone: str = "firm"):
    c = get_case(case_id)
    if not c:
        return JSONResponse({"error":"not found"}, status_code=404)
    return {"pitch": coach_generate_pitch(c, tone)}

@router.get("/arena/{case_id}")
async def case_to_arena(case_id: str):
    c = get_case(case_id)
    if not c:
        return JSONResponse({"error":"not found"}, status_code=404)
    # отдаём контекст, который можно напрямую скормить spawn в arena_psychotypes
    return {"open": "/arena_psy/v1/spawn", "payload": {"difficulty":"hard","context": arena_context(c)}}
