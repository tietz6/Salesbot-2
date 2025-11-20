
import json, os

def _load_tiers():
    p = os.path.join(os.path.dirname(__file__),"data","tiers.json")
    with open(p,"r",encoding="utf-8") as f:
        return json.load(f)

TIERS = _load_tiers()

def calculate_percent(sales_count:int)->float:
    for t in TIERS:
        if sales_count>=t["min"] and sales_count<t["max"]:
            return t["percent"]
    return TIERS[-1]["percent"]

def calculate_income(sales_count:int, price_per_sale:float):
    pct = calculate_percent(sales_count)
    total = sales_count*price_per_sale
    income = total*(pct/100.0)
    return {
        "sales": sales_count,
        "price_per_sale": price_per_sale,
        "tier_percent": pct,
        "total_sales_amount": total,
        "income_manager": income,
        "income_generator": total*0.05
    }
