
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os, io
import matplotlib.pyplot as plt
from .service import compute_report

router = APIRouter(prefix="/salary_reports/v1", tags=["salary_reports"])

BASE = os.path.dirname(__file__)
TPL = os.path.join(BASE, "templates")
STATIC = os.path.join(BASE, "static")

env = Environment(loader=FileSystemLoader(TPL), autoescape=select_autoescape(["html","xml"]))

@router.get("/static/salary.css")
async def css():
    return FileResponse(os.path.join(STATIC,"salary.css"))

@router.get("/summary/{manager_id}", response_class=HTMLResponse)
async def summary(manager_id: str, period: str="month"):
    data = compute_report(manager_id, period)
    tpl = env.get_template("report.html")
    return HTMLResponse(tpl.render(manager_id=manager_id, period=period, **data))

@router.get("/chart/{manager_id}")
async def chart(manager_id: str, period: str="month"):
    data = compute_report(manager_id, period)
    amounts = [d["amount"] for d in data["deals"]]
    plt.figure(figsize=(6,3))
    if amounts:
        plt.plot(amounts, linewidth=2)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    return FileResponse(buf, media_type="image/png")

@router.get("/health")
async def health():
    return {"ok": True, "version": "v1"}

@router.get("/report/{manager_id}")
async def report_json(manager_id: str, period: str="month"):
    return compute_report(manager_id, period)
