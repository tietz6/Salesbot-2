
from fastapi import APIRouter, Request
from .service import spawn_persona, step_dialog

router = APIRouter(prefix="/arena_psy/v1", tags=["arena_psychotypes"])

@router.get("/health")
async def health():
    return {"ok": True, "psy": 8, "levels": ["easy","medium","hard","nightmare"]}

@router.post("/spawn")
async def spawn(req: Request):
    data = await req.json()
    return spawn_persona(
        difficulty=data.get("difficulty","medium"),
        psy_type=data.get("type"),
        context=data.get("context")
    )

@router.post("/step")
async def step(req: Request):
    data = await req.json()
    return step_dialog(data.get("state") or {}, data.get("manager_reply",""))
