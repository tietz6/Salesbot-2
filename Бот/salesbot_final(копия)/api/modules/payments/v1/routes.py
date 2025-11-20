
from fastapi import APIRouter, HTTPException
from .engine import PaymentsEngine
from .providers.fake import FakeProvider

router = APIRouter(prefix="/payments", tags=["payments"])
engine = PaymentsEngine()
provider = FakeProvider()

@router.post("/invoice")
async def create_invoice(amount: float, currency: str="KGS", deal_id: str|None=None):
    inv = engine.create_invoice(amount=amount, currency=currency, deal_id=deal_id)
    payment = provider.create_payment(inv.id, inv.amount, inv.currency)
    return {"ok": True, "invoice": inv.to_dict(), "payment": payment}

@router.post("/pay/{invoice_id}")
async def pay(invoice_id: str):
    inv = engine.get_invoice(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="invoice not found")
    res = provider.capture(invoice_id)
    if res.get("ok"):
        inv = engine.set_status(invoice_id, "paid")
    else:
        inv = engine.set_status(invoice_id, "failed")
    return {"ok": True, "invoice": inv.to_dict() if inv else None}

@router.get("/status/{invoice_id}")
async def status(invoice_id: str):
    inv = engine.get_invoice(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="invoice not found")
    return {"ok": True, "invoice": inv.to_dict()}
