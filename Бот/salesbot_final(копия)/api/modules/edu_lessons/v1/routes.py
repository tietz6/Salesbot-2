
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os, json
from .service import list_catalog, get_lesson, score_test, recommend_lessons

router = APIRouter(prefix="/edu_lessons/v1", tags=["edu_lessons"])

BASE = os.path.dirname(__file__)
TPL = os.path.join(BASE, "templates")
STATIC = os.path.join(BASE, "static")

env = Environment(loader=FileSystemLoader(TPL), autoescape=select_autoescape(["html","xml"]))

@router.get("/static/edu.css")
async def css():
    return FileResponse(os.path.join(STATIC,"edu.css"))

@router.get("/catalog", response_class=HTMLResponse)
async def catalog():
    items = list_catalog()
    t = env.get_template("catalog.html")
    return HTMLResponse(t.render(lessons=items))

@router.get("/view/{cat}/{name}", response_class=HTMLResponse)
async def view(cat: str, name: str):
    lid = f"{cat}/{name}"
    l = get_lesson(lid)
    if not l:
        return HTMLResponse("<h3>Урок не найден</h3>", status_code=404)
    t = env.get_template("view.html")
    return HTMLResponse(t.render(lesson=l))

@router.get("/test/{cat}/{name}", response_class=HTMLResponse)
async def test_view(cat: str, name: str):
    lid = f"{cat}/{name}"
    l = get_lesson(lid)
    if not l:
        return HTMLResponse("<h3>Урок не найден</h3>", status_code=404)
    t = env.get_template("test.html")
    return HTMLResponse(t.render(lesson=l))

@router.get("/list")
async def api_list():
    return list_catalog()

@router.get("/lesson/{cat}/{name}")
async def api_lesson(cat: str, name: str):
    lid = f"{cat}/{name}"
    l = get_lesson(lid)
    if not l:
        return JSONResponse({"error":"not found"}, status_code=404)
    return l

@router.post("/test/{cat}/{name}")
async def api_test(cat: str, name: str, req: Request):
    lid = f"{cat}/{name}"
    l = get_lesson(lid)
    if not l:
        return JSONResponse({"error":"not found"}, status_code=404)
    data = await req.json()
    ans = data.get("answer")
    return score_test(l, ans)

@router.get("/recommend/{manager_id}")
async def api_recommend(manager_id: str):
    return {"recommend": recommend_lessons(manager_id)}
