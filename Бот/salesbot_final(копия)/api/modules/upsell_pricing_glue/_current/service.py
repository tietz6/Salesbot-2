
import json, math
from typing import Dict, Any, List, Optional
from core.voice_gateway.v1 import VoicePipeline

def _sum_items(items: List[dict])->float:
    return float(sum(max(0.0, float(x.get("price",0))) for x in (items or [])))

def _apply_discount(subtotal: float, discount: float)->float:
    return max(0.0, subtotal * (1.0 - max(0.0, min(discount, 0.95))))

def _apply_coupon(subtotal: float, coupon: Optional[dict])->float:
    if not coupon:
        return subtotal
    if "percent" in coupon:
        return _apply_discount(subtotal, float(coupon["percent"])/100.0)
    if "amount" in coupon:
        return max(0.0, subtotal - float(coupon["amount"]))
    return subtotal

def _apply_vat(subtotal: float, vat_rate: float)->float:
    return round(subtotal * (1.0 + max(0.0, vat_rate)), 2)

def compute_offer(catalog: Dict[str,Any], tier: str="premium", currency: str="KGS", discount: float=0.0, coupon: Optional[dict]=None, vat: float=0.0)->dict:
    tier = tier if tier in catalog else "premium"
    items = catalog[tier]["items"]
    title = catalog[tier].get("title", tier)
    base = _sum_items(items)
    after_disc = _apply_discount(base, discount)
    after_coupon = _apply_coupon(after_disc, coupon)
    total = _apply_vat(after_coupon, vat)
    return {
        "tier": tier,
        "title": title,
        "currency": currency,
        "base": round(base,2),
        "after_discount": round(after_disc,2),
        "after_coupon": round(after_coupon,2),
        "vat_rate": vat,
        "total": total
    }

def _format_savings(offer: dict)->str:
    base = offer["base"]
    total = offer["total"]
    save = max(0.0, base - total)
    if save <= 0.01:
        return "Предложение без скидки — платишь только за ценность."
    return f"Экономия {save:.0f} {offer['currency']} от базовой суммы {base:.0f} {offer['currency']}."

def suggest_upsell(catalog: Dict[str,Any], current_tier: str="basic", target_tier: str="premium", currency: str="KGS", discount: float=0.0, coupon: Optional[dict]=None, vat: float=0.0, context: Optional[str]=None)->dict:
    cur = compute_offer(catalog, current_tier, currency, discount, coupon, vat)
    tgt = compute_offer(catalog, target_tier, currency, discount, coupon, vat)
    diff = max(0.0, tgt["total"] - cur["total"])
    vp = VoicePipeline()
    prompt = [
        {"role":"system","content":"Ты жёсткий коуч продаж. Объясни выгоду апгрейда с учётом цены, результата и примеров. Стиль: уверенно, по делу, 2-3 фразы + 1 вопрос."},
        {"role":"user","content": json.dumps({"current":cur,"target":tgt,"context":context}, ensure_ascii=False)}
    ]
    pitch = vp.llm.chat(prompt)
    return {
        "current": cur,
        "target": tgt,
        "difference": round(diff,2),
        "pitch": pitch,
        "savings": _format_savings(tgt)
    }
