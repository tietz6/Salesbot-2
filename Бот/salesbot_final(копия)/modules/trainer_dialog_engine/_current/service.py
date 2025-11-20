
import os, json, time, uuid

SESS_PATH = os.path.join(os.path.dirname(__file__), "data")

def _path(sid: str):
    return os.path.join(SESS_PATH, f"{sid}.json")

def new_session(manager_id: str, scenario_id: str):
    sid = str(uuid.uuid4())
    rec = {"sid": sid, "manager_id": manager_id, "scenario_id": scenario_id, "history": [], "created": time.time()}
    with open(_path(sid),"w",encoding="utf-8") as f:
        json.dump(rec,f,ensure_ascii=False,indent=2)
    return rec

def _persona_reply(user_text: str) -> str:
    try:
        from modules.deepseek_persona.v1.service import persona_chat
        return persona_chat(f"Ответь как клиент бренда на: {user_text}", role="client_emotional")
    except Exception:
        return "Интересно, а как это будет звучать? И сколько по времени?"

def _evaluate(text: str):
    try:
        from modules.trainer_core.v1.service import evaluate
        return evaluate(text)
    except Exception:
        return {"scores":{"warmth":50,"empathy":50,"questions":50},"stage":"generic","tips":["добавь тёплую фразу"]}

def turn(sid: str, text: str):
    p = _path(sid)
    if not os.path.exists(p):
        return {"error":"session_not_found"}
    rec = json.load(open(p,"r",encoding="utf-8"))
    eval_res = _evaluate(text)
    rec["history"].append({"role":"manager","text":text,"eval":eval_res})
    reply = _persona_reply(text)
    rec["history"].append({"role":"client","text":reply})
    json.dump(rec, open(p,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    return {"reply": reply, "eval": eval_res, "sid": sid}

def stop(sid: str):
    p = _path(sid)
    if not os.path.exists(p):
        return {"error":"session_not_found"}
    rec = json.load(open(p,"r",encoding="utf-8"))
    scores = [h.get("eval",{}).get("scores",{}) for h in rec["history"] if h["role"]=="manager"]
    def avg(key):
        vals = [s.get(key,0) for s in scores]
        return int(sum(vals)/len(vals)) if vals else 0
    summary = {"avg_warmth":avg("warmth"),"avg_empathy":avg("empathy"),"avg_questions":avg("questions")}
    return {"sid": sid, "summary": summary, "tips": ["сохраняй тепло и вопросы на каждом шаге"]}
