
from fastapi import APIRouter, Request
from .engine import PaymentsEngine

router = APIRouter(prefix="/payments/v2", tags=["payments_v2"])

@router.post("/invoice/{deal_id}")
async def invoice(deal_id: str, req: Request):
    data = await req.json()
    eng = PaymentsEngine(deal_id)
    return eng.create_invoice(data.get("amount",0), data.get("currency","KGS"))

@router.post("/webhook")
async def webhook(req: Request):
    data = await req.json()
    deal_id = data.get("deal_id")
    eng = PaymentsEngine(deal_id)
    return eng.process_webhook(data)

@router.get("/status/{deal_id}")
async def status(deal_id: str):
    eng = PaymentsEngine(deal_id)
    return eng.get_status()
