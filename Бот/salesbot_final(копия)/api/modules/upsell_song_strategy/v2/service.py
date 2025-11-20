
import json, os
from typing import Dict, Any, List

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data", "upsell_scripts.json")

def _load()->Dict[str, Any]:
    with open(DATA, "r", encoding="utf-8") as f:
        return json.load(f)

def warmup_message()->str:
    return _load().get("warmup_before_texts","")

def after_texts_message()->str:
    return _load().get("after_texts_double_demo","")

def ladder_offer()->Dict[str, Any]:
    return _load().get("ladder_2_to_4",{})

def cross_sell()->List[dict]:
    return _load().get("cross_sell_products", [])

def phases()->List[dict]:
    return _load().get("phases", [])

def suggest_next_phase(current_id: str)->dict:
    ph = phases()
    ids = [p["id"] for p in ph]
    if current_id in ids:
        i = ids.index(current_id)
        if i+1 < len(ph):
            return ph[i+1]
    return {"id":"step1_first_touch", "goal":"доверие", "script": ph[0]["script"] if ph else ""}
