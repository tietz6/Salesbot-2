
import json, re
from typing import List, Dict, Any
from core.voice_gateway.v1 import VoicePipeline

def _load_rubric()->dict:
    import os, json
    p = os.path.join(os.path.dirname(__file__), "data", "rubrics.json")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

RUBRIC = _load_rubric()

# Простые эвристики для чеков (детерминированно)
def _check(text: str, check_id: str)->bool:
    t = (text or "").lower()
    if check_id == "tone_warm":
        return any(w in t for w in ["рад","приятно","здравствуйте","спасибо","что удобно"])
    if check_id == "intro_clear":
        return any(w in t for w in ["я","меня зовут","компания","мы занимаемся"])
    if check_id == "agenda":
        return any(w in t for w in ["предлагаю","план","давайте так","сначала","потом"])
    if check_id == "need_questions":
        return t.count("?") >= 2 or any(w in t for w in ["что важно","расскажите","поделитесь"])
    if check_id == "budget_timeline":
        return any(w in t for w in ["бюджет","сколько готовы","срок","когда планируете","дедлайн"])
    if check_id == "decision_process":
        return any(w in t for w in ["кто принимает","лицо принимающее решение","кто решает","комитет"])
    if check_id == "paraphrase":
        return any(w in t for w in ["правильно ли я понимаю","то есть вы","если верно понял"])
    if check_id == "proof":
        return any(w in t for w in ["кейс","пример","результат","цифр","покажу"])
    if check_id == "bridge":
        return any(w in t for w in ["свяжем","как раз решает","поэтому наш","это поможет"])
    if check_id == "value_driven":
        return any(w in t for w in ["результат","выгода","экономия","рост","ценность"])
    if check_id == "structure":
        return any(w in t for w in ["во-первых","во вторых","итак","структура","предлагаю пакет"])
    if check_id == "risk_reversal":
        return any(w in t for w in ["гарантия","без риска","договор","возврат","тест"])
    if check_id == "relevance":
        return any(w in t for w in ["под ваш кейс","пример из вашей отрасли","как у вас"])
    if check_id == "interaction":
        return t.count("?") >= 1
    if check_id == "cta_next":
        return any(w in t for w in ["предлагаю созвониться","приглашаю","перейдём к","шаг","старт"])
    if check_id == "summary":
        return any(w in t for w in ["итого","резюме","подведём итог"])
    if check_id == "clear_next":
        return any(w in t for w in ["встреч","завтра","в понедельник","в среду","числа","дата"])
    if check_id == "close":
        return any(w in t for w in ["готовы оформить","приступим","закроем","подтверждаете"])
    return False

def rubric_summary()->dict:
    return RUBRIC

def score_dialog(history: List[Dict[str,str]])->dict:
    # history: [{role, content, stage}]
    stages = {k: {"score":0.0, "checks":[]} for k in RUBRIC.keys()}
    issues = []
    tips = []
    total = 0.0

    # агрегируем по stage
    stage_texts = {k: [] for k in RUBRIC.keys()}
    for m in history or []:
        st = m.get("stage")
        if st in stage_texts and m.get("role") in ("assistant","user","client","manager"):
            stage_texts[st].append(m.get("content",""))

    # оценка по чек-листам
    for st, cfg in RUBRIC.items():
        text = " ".join(stage_texts.get(st) or [])[:5000]
        stage_score = 0.0
        checks_res = []
        for chk in cfg["checks"]:
            ok = _check(text, chk["id"])
            w = chk["weight"]
            if ok:
                stage_score += w
            else:
                issues.append({"stage": st, "check": chk["id"], "desc": chk["desc"]})
        # stage_score в 0..1, умножаем на weight*100
        stage_points = round(stage_score * cfg["weight"] * 100, 2)
        total += stage_points
        stages[st] = {"score": stage_points, "checks": checks_res}

    # LLM совет по улучшению (строгий коуч)
    try:
        vp = VoicePipeline()
        msg = [
            {"role":"system","content":"Ты строгий коуч продаж. Дай 3 короткие прицельные рекомендации по улучшению на основе списка проблем. Формат: маркированный список."},
            {"role":"user","content": json.dumps(issues, ensure_ascii=False)[:2000]}
        ]
        coach = vp.llm.chat(msg)
        tips = [t.strip(" -•") for t in coach.splitlines() if t.strip()][:5]
    except Exception:
        tips = []

    return {
        "stage_scores": stages,
        "total": round(total, 2),
        "issues": issues,
        "tips": tips
    }
