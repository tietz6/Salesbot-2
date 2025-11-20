
import re

TYPES = ["price","trust","need","timing","doubts","competing"]

PATTERNS = {
    "price":[r"\bдорог|цена|сколько\b", r"\bдешев|слишком\b"],
    "trust":[r"\bне (верю|доверяю)\b", r"\bотзывы|гаранти"],
    "need":[r"\bне (нужно|надо)\b", r"\bзачем\b"],
    "timing":[r"\bне сейчас|потом| позже|через\b", r"\bсегодня не\b"],
    "doubts":[r"\bсомневаюсь|не уверен\b", r"\bне знаю\b"],
    "competing":[r"\bуже есть\b", r"\bдруг(ой|ая) (вариант|компания|сервис)\b"]
}

NEGATIVE_SIGNS = [
    (r"^\s*да\b.*\bно\b", 1, "да, но — оборона вместо прояснения"),
    (r"[!?]{2,}", 1, "повышенная эмоциональность"),
    (r"\bуспокойтесь\b|\bвы не правы\b", 3, "агрессивная лексика"),
    (r"^\s*[\w]{1,6}\s*$", 2, "слишком коротко, нет ценности"),
]

QUESTION_SIGN = r"\?"

def detect_type(text: str):
    text = (text or "").lower()
    hits = {}
    for t, regs in PATTERNS.items():
        for rgx in regs:
            if re.search(rgx, text):
                hits[t] = hits.get(t,0)+1
    if not hits:
        return None, 0, []
    best = max(hits, key=hits.get)
    reasons = [f"match:{k}={v}" for k,v in hits.items() if v>0]
    conf = min(0.9, 0.4 + 0.2*(hits[best]-1))
    return best, conf, reasons

def detect_penalties(text: str):
    text = text or ""
    penalties = []
    score_delta = 0
    for rgx,weight,reason in NEGATIVE_SIGNS:
        if re.search(rgx, text, flags=re.IGNORECASE):
            penalties.append({"rule": rgx, "weight": weight, "reason": reason})
            score_delta -= weight
    if not re.search(QUESTION_SIGN, text):
        penalties.append({"rule": "no_question", "weight": 1, "reason": "нет уточняющего вопроса"})
        score_delta -= 1
    if len(text.strip()) < 20:
        penalties.append({"rule": "too_short", "weight": 1, "reason": "короткий ответ — мало ценности"})
        score_delta -= 1
    return penalties, score_delta
