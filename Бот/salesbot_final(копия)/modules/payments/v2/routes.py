
from fastapi import APIRouter, Request
from .engine import PaymentsEngine

router = APIRouter(prefix="/payments/v2", tags=["payments_v2"])

@router.post("/start")
async def start_telegram(req: Request):
    """Telegram bot integration endpoint - accepts chat_id"""
    data = await req.json()
    chat_id = data.get("chat_id")
    probe = data.get("probe", False)
    
    # Quick response for probe requests (discovery)
    if probe:
        return {"ok": True, "available": True}
    
    if not chat_id:
        return {"error": "chat_id required"}
    
    # Payments module provides information
    return {
        "ok": True,
        "reply": "💳 Модуль платежей\n\n"
                 "Этот модуль используется для создания платёжных счетов.\n"
                 "Для создания счета используй:\n"
                 "/payments/v2/invoice/{deal_id}\n\n"
                 "Пример:\n"
                 'POST /payments/v2/invoice/deal123\n'
                 '{"amount": 1000, "currency": "KGS"}'
    }

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
