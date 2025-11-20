
from fastapi import APIRouter, Request
from .service import track_error, get_errors, clear_errors

router = APIRouter(prefix="/errors/v1", tags=["errors_manager"])

@router.get("/health")
async def health():
    return {"ok": True, "version": "v1"}

@router.get("/list")
async def list_errors(limit: int = 200):
    return {"ok": True, "items": get_errors(limit=limit)}

@router.post("/clear")
async def clear():
    return clear_errors()

@router.post("/track")
async def track(req: Request):
    data = await req.json()
    return track_error(
        module=data.get("module","unknown"),
        context=data.get("context") or {},
        exc=data.get("error","error"),
        level=data.get("level","error"),
        push_to_crm=bool(data.get("push_to_crm", False)),
        deal_id=data.get("deal_id")
    )
