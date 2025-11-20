
from fastapi import APIRouter, Request
from .service import compute_offer, suggest_upsell

router = APIRouter(prefix="/upsell_pricing/v1", tags=["upsell_pricing"])

@router.post("/compute")
async def compute(req: Request):
    data = await req.json()
    return compute_offer(
        catalog=data.get("catalog") or {},
        tier=data.get("tier","premium"),
        currency=data.get("currency","KGS"),
        discount=float(data.get("discount",0)),
        coupon=data.get("coupon"),
        vat=float(data.get("vat",0))
    )

@router.post("/suggest")
async def suggest(req: Request):
    data = await req.json()
    return suggest_upsell(
        catalog=data.get("catalog") or {},
        current_tier=data.get("current_tier","basic"),
        target_tier=data.get("target_tier","premium"),
        currency=data.get("currency","KGS"),
        discount=float(data.get("discount",0)),
        coupon=data.get("coupon"),
        vat=float(data.get("vat",0)),
        context=data.get("context")
    )
