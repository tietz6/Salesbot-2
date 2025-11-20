
import json, re
from typing import List, Dict, Any, Optional
from core.voice_gateway.v1 import VoicePipeline

def _load_rules()->list:
    import os, json
    p = os.path.join(os.path.dirname(__file__), "data", "rules.json")
    with open(p,"r",encoding="utf-8") as f:
        return json.load(f)

RULES = _load_rules()

def _apply_rules(reply: str)->Dict[str,Any]:
    reply = reply or ""
    penalties = []
    minus = 0
    ctx = {"reply": reply}
    for r in RULES:
        hit = False
        if r.get("pattern"):
            if re.search(r["pattern"], reply, flags=re.IGNORECASE):
                hit = True
        if r.get("check"):
            try:
                if eval(r["check"], {}, ctx):
                    hit = True
            except Exception:
                pass
        if hit:
            penalties.append({"id": r["id"], "msg": r["msg"], "penalty": r["penalty"]})
            minus += int(r["penalty"])
    rule_score = max(0, min(10, 10 - minus))
    return {"penalties": penalties, "rule_score": rule_score}

def _llm_score(history: Optional[List[dict]], reply: str, stage: Optional[str])->Dict[str,Any]:
    # оцениваем смысловую сторону — кратко, 0..10 и 3 причины
    vp = VoicePipeline()
    msg = [
        {"role":"system","content":"Ты строгий экзаменатор продаж. Оцени ответ по шкале 0..10, 3 короткие причины. Формат JSON: {score:int, reasons:[str,str,str]}."},
        {"role":"user","content": json.dumps({"reply":reply, "stage":stage, "history":history or []}, ensure_ascii=False)[:2000]}
    ]
    j = (vp.llm.chat(msg) or "").strip()
    # попытка распарсить
    try:
        data = json.loads(j)
        score = int(data.get("score", 5))
        reasons = data.get("reasons", [])
        if not isinstance(reasons, list): reasons = [str(reasons)]
        score = max(0, min(10, score))
        return {"llm_score": score, "reasons": reasons[:3]}
    except Exception:
        return {"llm_score": 6, "reasons": ["Авто-оценка по умолчанию"]}

def _combined(rule_score: int, llm_score: int)->int:
    # комбинированная оценка, чуть больше веса у правил (они точные)
    return int(round(0.6*rule_score + 0.4*llm_score))

def analyze_reply(history: Optional[List[dict]], reply: str, stage: Optional[str]=None)->dict:
    r = _apply_rules(reply or "")
    l = _llm_score(history, reply or "", stage)
    combined = _combined(r["rule_score"], l["llm_score"])
    return {"ok": True, "rule": r, "llm": l, "combined": combined}

def suggest_fix(history: Optional[List[dict]], reply: str, stage: Optional[str]=None)->dict:
    # короткая «правильная» версия ответа
    vp = VoicePipeline()
    msg = [
        {"role":"system","content":"Ты строгий коуч. Перепиши ответ так, чтобы он соответствовал лучшей практике: ценность→короткий аргумент→уточняющий вопрос→мягкое CTA. 2–4 фразы."},
        {"role":"user","content": json.dumps({"bad_reply":reply, "stage":stage, "history":history or []}, ensure_ascii=False)[:2000]}
    ]
    fix = vp.llm.chat(msg)
    return {"ok": True, "suggestion": fix}
