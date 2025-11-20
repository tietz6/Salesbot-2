
import json, random, re
from typing import Dict, Any, Optional
from core.voice_gateway.v1 import VoicePipeline

EMO_STATES = ["calm","neutral","annoyed","angry"]
DIFF_COEF = {"easy":0.6,"medium":1.0,"hard":1.4,"nightmare":1.8}

def _load_psy()->dict:
    import os, json
    p = os.path.join(os.path.dirname(__file__), "data", "psychotypes.json")
    with open(p,"r",encoding="utf-8") as f:
        return json.load(f)

PSY = _load_psy()

def _penalty(reply: str)->int:
    t = (reply or "").lower()
    score = 0
    if len(t.strip()) < 20: score += 1
    if "?" not in t: score += 1
    if re.search(r"!{2,}|\?{2,}", t): score += 1
    if re.search(r"успокойтесь|вы не правы", t): score += 2
    return score

def spawn_persona(difficulty: str = "medium", psy_type: Optional[str] = None, context: Optional[str] = None)->dict:
    if difficulty not in DIFF_COEF: difficulty = "medium"
    psy_type = psy_type or random.choice(list(PSY.keys()))
    persona = {
        "type": psy_type,
        "difficulty": difficulty,
        "emotion": "neutral",
        "pressure": 0.0,
        "turn": 0,
        "context": context or ""
    }
    # стартовая реплика
    vp = VoicePipeline()
    msg = [
        {"role":"system","content": f"Ты играешь роль клиента типа {psy_type}. Говори кратко, натурально. Первая реплика — обозначь позицию."},
        {"role":"user","content": context or "Запрос: обсуждаем покупку медиа-продукта «На Счастье»."}
    ]
    first = vp.llm.chat(msg)
    persona["last_client"] = first
    return {"ok": True, "state": persona, "client_reply": first}

def _next_emotion(emotion: str, penalty: int, diff: str)->str:
    idx = EMO_STATES.index(emotion)
    shift = 0
    if penalty == 0:
        shift = -1 if idx>0 else 0
    elif penalty == 1:
        shift = 0
    else:
        coef = DIFF_COEF.get(diff,1.0)
        shift = 1 if penalty*coef < 2.0 else 2
    idx = max(0, min(len(EMO_STATES)-1, idx + shift))
    return EMO_STATES[idx]

def step_dialog(state: Dict[str,Any], manager_reply: str)->dict:
    st = dict(state or {})
    if not st:
        return {"ok": False, "error":"empty state"}
    penalty = _penalty(manager_reply)
    st["turn"] = int(st.get("turn",0)) + 1
    st["pressure"] = max(0.0, float(st.get("pressure",0.0)) + penalty * 0.2)
    st["emotion"] = _next_emotion(st.get("emotion","neutral"), penalty, st.get("difficulty","medium"))
    psy = st.get("type","cold")

    # шаблон реакции
    sys_style = f"Ты клиент {psy}. Эмоция: {st['emotion']}. Давление: {st['pressure']:.1f}. Отвечай естественно, 1-3 фразы, соответствуя типу и эмоции. Если менеджер слаб — стань жестче; если хорош — смягчайся и продвигайся к следующему шагу."
    vp = VoicePipeline()
    msg = [
        {"role":"system","content": sys_style},
        {"role":"assistant","content": st.get("last_client","")},
        {"role":"user","content": manager_reply}
    ]
    reply = vp.llm.chat(msg)
    st["last_client"] = reply

    return {"ok": True, "state": st, "client_reply": reply, "penalty": penalty}
