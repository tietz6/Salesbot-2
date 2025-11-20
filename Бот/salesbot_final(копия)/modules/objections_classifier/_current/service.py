
import json
from typing import List, Dict, Any
from .rules import detect_type, detect_penalties, TYPES
from core.voice_gateway.v1 import VoicePipeline

def _load_patterns()->dict:
    import json, os
    p = os.path.join(os.path.dirname(__file__), "data", "patterns.json")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

PATTERNS = _load_patterns()

def classify(utterance: str, history: List[Dict[str,str]]|None=None)->dict:
    obj_type, conf, reasons = detect_type(utterance or "")
    advice = None
    if not obj_type:
        # fallback в LLM для распознавания типа
        vp = VoicePipeline()
        msg = [
            {"role":"system","content":"Классифицируй тип возражения: price/trust/need/timing/doubts/competing. Ответи только типом."},
            {"role":"user","content": utterance or ""}
        ]
        guess = (vp.llm.chat(msg) or "").strip().lower()
        if guess in TYPES:
            obj_type = guess
            conf = max(conf, 0.55)
            reasons.append("llm:guess")
        else:
            obj_type = "doubts"
            conf = 0.4
            reasons.append("fallback:doubts")
    advice = PATTERNS.get(obj_type, {}).get("coach")

    return {
        "type": obj_type,
        "confidence": round(conf, 2),
        "reasons": reasons,
        "advice": advice
    }

def apply_patterns(obj_type: str, history: List[Dict[str,str]]|None, last_reply: str)->dict:
    pat = PATTERNS.get(obj_type) or {}
    template = pat.get("template")
    coach = pat.get("coach")
    # LLM перефраз дерева шаблона под контекст
    vp = VoicePipeline()
    msg = [
        {"role":"system","content":"Ты строгий коуч продаж. Переформулируй шаблон ответа под реплику клиента и историю диалога. Сделай 2-3 внятные фразы + один уточняющий вопрос."},
        {"role":"user","content": f"Шаблон: {template}\nРеплика клиента: {last_reply}\nИстория: {json.dumps(history or [])[:600]}"}
    ]
    coach_reply = vp.llm.chat(msg)
    return {
        "template": template,
        "coach_reply": coach_reply or coach
    }

def score_response(last_reply: str)->dict:
    penalties, delta = detect_penalties(last_reply or "")
    base = 0
    score = max(0, base + 5 + delta)  # 0..10 шкала (5 базовая, штрафы снижают)
    return {"penalties": penalties, "score_delta": delta, "score": score}
