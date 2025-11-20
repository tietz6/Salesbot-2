
import re

WARM_WORDS = ["🥰","🌸","💛","💫","❤️","Прекрасно","Чудесно","рада","помочь","красиво","трогательно","спасибо","тепло"]
EMPATHY_KEYS = ["понимаю","представляю","трогательно","как здорово","спасибо вам","это чудесно","какая история","слышно, что для вас важно"]
QUESTION_HINTS = ["как","когда","что","кто","почему","зачем","какой","какая","какие"]

def score_warmth(text: str) -> int:
    return min(100, sum(text.count(w) for w in WARM_WORDS) * 8)

def score_empathy(text: str) -> int:
    return min(100, sum(text.lower().count(k) for k in EMPATHY_KEYS) * 12)

def score_questions(text: str) -> int:
    qs = text.count("?")
    # +bonus for open questions
    bonus = sum(1 for h in QUESTION_HINTS if h in text.lower())
    return min(100, qs*15 + bonus*3)

def detect_stage(text: str) -> str:
    t = text.lower()
    if "как зовут" in t or "расскажите" in t or "истори" in t:
        return "story_collection"
    if "предоплат" in t or "оплат" in t:
        return "payment"
    if "демо" in t:
        return "demo"
    if "подар" in t or "акци" in t or "в подарок" in t:
        return "upsell"
    return "generic"

def evaluate(text: str):
    warm = score_warmth(text)
    emp = score_empathy(text)
    q = score_questions(text)
    stage = detect_stage(text)
    tips = []
    if q < 40:
        tips.append("Добавь 1–2 открытых вопроса, чтобы углубить историю.")
    if warm < 40:
        tips.append("Чуть больше тепла бренда: 1 короткая тёплая фраза.")
    if stage == "payment" and emp < 30:
        tips.append("При оплате сохрани мягкость: уверенно, но заботливо.")
    return {
        "scores": {"warmth": warm, "empathy": emp, "questions": q},
        "stage": stage,
        "tips": tips,
        "ok": True
    }
