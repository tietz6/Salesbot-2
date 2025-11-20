
import os, json, math, statistics, time
from typing import Dict, Any, List

# Read from crm_bridge mock store if exists
CRM_LEADS = os.path.join(os.path.dirname(__file__), "..","..","..","bridges","crm_leads_bridge","v2","data","leads.json")

def _load_leads()->List[dict]:
    try:
        with open(CRM_LEADS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _calc_percent_by_tiers(count:int)->float:
    tiers = [
        (1,10,10.0),
        (10,15,12.5),
        (15,20,15.0),
        (20,40,20.0),
        (40,10**9,25.0)
    ]
    for mn,mx,p in tiers:
        if count>=mn and count<mx:
            return p
    return 25.0

def _won_deals_for_manager(manager_id:str, period:str)->List[dict]:
    # period: day|week|month; here we just filter by status=won for simplicity (no dates in mock)
    return [d for d in _load_leads() if d.get("assigned_to")==manager_id and d.get("status")=="won"]

def _avg(items: List[float])->float:
    return round(float(statistics.mean(items)), 2) if items else 0.0

def compute_report(manager_id: str, period: str="month")->Dict[str, Any]:
    deals = _won_deals_for_manager(manager_id, period)
    amounts = [float(d.get("amount_final") or d.get("amount_est") or 0) for d in deals]
    sales_count = len(deals)
    avg_check = _avg(amounts)
    percent = _calc_percent_by_tiers(sales_count) if sales_count>0 else 0.0
    total_amount = sum(amounts)
    manager_income = round(total_amount * (percent/100.0), 2)
    generator_income = round(total_amount * 0.05, 2)

    # progress to next tier
    tiers = [10,15,20,40,10**9]
    next_level = next(x for x in tiers if sales_count < x)
    to_next = max(0, next_level - sales_count)
    next_percent = _calc_percent_by_tiers(next_level)

    # naive forecast: assume same average check and +to_next sales
    forecast_income = round((sales_count+to_next)* (avg_check or 1000) * (next_percent/100.0), 2)

    return {
        "kpi": {
            "sales": sales_count,
            "avg_check": avg_check,
            "percent": percent,
            "manager_income": manager_income,
            "generator_income": generator_income
        },
        "deals": [{
            "id": d.get("id"),
            "client": d.get("client","—"),
            "amount": float(d.get("amount_final") or d.get("amount_est") or 0),
            "status": d.get("status")
        } for d in deals],
        "forecast": {
            "to_next_level": to_next,
            "next_percent": next_percent,
            "forecast_income": forecast_income
        }
    }
