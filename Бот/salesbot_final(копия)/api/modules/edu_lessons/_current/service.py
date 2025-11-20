
import os, json
from typing import List, Dict, Any, Optional
from modules.dialog_memory.v1.service import list_sessions

BASE = os.path.dirname(__file__)
LESSON_DIR = os.path.join(BASE, "lessons")

def _iter_lessons()->List[dict]:
    items = []
    for cat in ["master_path","objections","upsell","arena"]:
        cdir = os.path.join(LESSON_DIR, cat)
        if not os.path.isdir(cdir): 
            continue
        for fn in os.listdir(cdir):
            if fn.endswith(".json"):
                with open(os.path.join(cdir, fn),"r",encoding="utf-8") as f:
                    try:
                        items.append(json.load(f))
                    except:
                        pass
    return items

def list_catalog()->List[dict]:
    items = _iter_lessons()
    return [{
        "id": x["id"],
        "title": x["title"],
        "duration": x["duration"],
        "type": x["type"],
        "category": x["category"],
        "preview": x.get("preview","")
    } for x in items]

def get_lesson(lesson_id: str)->Optional[dict]:
    items = _iter_lessons()
    for x in items:
        if x["id"] == lesson_id:
            return x
    return None

def score_test(lesson: dict, answer_index: int)->dict:
    ok = (int(answer_index) == int(lesson["test"]["answer"]))
    return {"ok": ok, "correct": int(lesson["test"]["answer"])}

def recommend_lessons(manager_id: str)->List[str]:
    # На основе последних ошибок в dialog_memory
    sessions = list_sessions(manager_id)
    if not sessions:
        return ["master_path/greeting", "master_path/qualification"]
    last = sorted(sessions, key=lambda s: s.get("timestamp",0), reverse=True)[0]
    errs = " ".join(last.get("errors",[])).lower()
    rec = []
    if any(w in errs for w in ["дорог","цена"]):
        rec.append("objections/price")
    if any(w in errs for w in ["довер"]):
        rec.append("objections/trust")
    if any(w in errs for w in ["нет вопрос"]):
        rec.append("master_path/qualification")
    if any(w in errs for w in ["нет ценност","выгода"]):
        rec.append("master_path/offer")
    if not rec:
        rec = ["arena/psychotypes","upsell/value"]
    return rec[:3]
