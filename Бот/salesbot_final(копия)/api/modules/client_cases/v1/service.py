
import os, json, random
from typing import List, Dict, Any, Optional
from core.voice_gateway.v1 import VoicePipeline

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data", "cases.json")

def _load()->List[dict]:
    with open(DATA,"r",encoding="utf-8") as f:
        return json.load(f)

def list_cases(goal: Optional[str]=None, budget: Optional[str]=None, persona: Optional[str]=None)->List[dict]:
    items = _load()
    def ok(x):
        if goal and x["goal"] != goal: return False
        if persona and x["persona"] != persona: return False
        if budget:
            key = x["budget"]["key"]
            if budget != key: return False
        return True
    out=[]
    for x in items:
        if ok(x): out.append(x)
    return out

def get_case(case_id: str)->Optional[dict]:
    for x in _load():
        if x["id"] == case_id:
            return x
    return None

def top_seller_reply(case: dict)->str:
    return case.get("top_seller_answer") or case.get("best_practice_answer")

def coach_generate_pitch(case: dict, tone: str="firm")->str:
    vp = VoicePipeline()
    sys = "Ты топ-продажник бренда «На Счастье». Короткий питч: ценность→структура→вопрос. 2–3 фразы."
    msg = [{"role":"system","content":sys},{"role":"user","content": json.dumps(case, ensure_ascii=False)[:2000]}]
    try:
        return vp.llm.chat(msg)
    except Exception:
        return top_seller_reply(case)

def arena_context(case: dict)->str:
    return f"Кейс: {case['title']}. Цель: {case['goal']}. Бюджет: {case['budget']['min']}-{case['budget']['max']} KGS. Дедлайн: {case['deadline_days']} дн. История: {case['story']}"

