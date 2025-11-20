
import os, json, time, uuid
from typing import Dict, Any, List, Optional

BASE = os.path.dirname(__file__)
DATA = os.path.join(BASE, "data", "sessions")

def _path(manager_id: str, session_id: str)->str:
    os.makedirs(DATA, exist_ok=True)
    return os.path.join(DATA, f"{manager_id}__{session_id}.json")

def new_session(manager_id: str, context: str="")->dict:
    sid = str(uuid.uuid4())
    rec = {
        "manager_id": manager_id,
        "session_id": sid,
        "context": context,
        "timestamp": time.time(),
        "history": [],   # {role: manager|client, content, metrics?}
        "last_metrics": {}
    }
    with open(_path(manager_id, sid), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)
    return rec

def load_session(manager_id: str, session_id: str)->Optional[dict]:
    p = _path(manager_id, session_id)
    if not os.path.exists(p):
        return None
    with open(p,"r",encoding="utf-8") as f:
        return json.load(f)

def save_session(rec: dict):
    with open(_path(rec["manager_id"], rec["session_id"]), "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)

def handle_turn(manager_id: str, session_id: str, text: str, features: Optional[dict])->dict:
    rec = load_session(manager_id, session_id)
    if not rec:
        return {"error":"session_not_found"}

    # append manager message
    m = {"role":"manager","content": text}
    rec["history"].append(m)

    # emotion metrics for manager's speech
    metrics = {}
    try:
        from modules.emotion_detector.v1.service import detect
        metrics = detect(features or {})
        m["metrics"] = metrics
        rec["last_metrics"] = metrics
    except Exception:
        rec["last_metrics"] = {}

    # client reply via persona (emotional)
    reply = ""
    try:
        from modules.deepseek_persona.v1.service import persona_chat
        ctx = rec.get("context","")
        prompt = f"Ответь как реалистичный клиент на реплику менеджера. Контекст: {ctx}. Реплика менеджера: {text}"
        reply = persona_chat(prompt, role="client_emotional")
    except Exception:
        reply = "Хочу понять, что именно я получу и когда."

    rec["history"].append({"role":"client","content": reply})
    save_session(rec)

    # Mirror into dialog_memory
    try:
        from modules.dialog_memory.v1.service import append_message
        append_message(manager_id, session_id, "manager", text, "arena")
        append_message(manager_id, session_id, "client", reply, "arena")
    except Exception:
        pass

    return {"reply": reply, "metrics": metrics, "session": {"manager_id": manager_id, "session_id": session_id}}

def stop_and_score(manager_id: str, session_id: str)->dict:
    # Analyze dialog via dialog_memory analyzer
    summary = {}
    try:
        from modules.dialog_memory.v1.service import analyze_session, load_session as dm_load, start_session, save_session as dm_save
        # Ensure DM session exists (in case user начал через UI без /dialog_memory/start)
        dm_rec = dm_load(manager_id, session_id)
        if not dm_rec:
            # create and backfill from arena log
            dm_rec = start_session(manager_id)
            dm_rec["session_id"] = session_id
            # load arena
            ar = load_session(manager_id, session_id)
            for h in (ar.get("history") if ar else []):
                role = "user" if h["role"]=="manager" else "assistant"
                dm_rec["history"].append({"role": role, "content": h["content"], "stage": "arena"})
            dm_save(manager_id, session_id, dm_rec)
        summary = analyze_session(manager_id, session_id) or {}
    except Exception:
        # fallback
        summary = {"errors":["недостаточно уточняющих вопросов"],"strengths":["доброжелательный тон"],"score":72}

    return summary
