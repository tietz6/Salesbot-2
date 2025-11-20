
import os, json, time, uuid
from typing import List, Dict, Any, Optional
from core.voice_gateway.v1 import VoicePipeline

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "sessions")
os.makedirs(DATA_DIR, exist_ok=True)

def _session_path(manager_id: str, session_id: str):
    return os.path.join(DATA_DIR, f"{manager_id}__{session_id}.json")

def save_session(manager_id: str, session_id: str, record: dict):
    path = _session_path(manager_id, session_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return True

def load_session(manager_id: str, session_id: str):
    path = _session_path(manager_id, session_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def start_session(manager_id: str):
    session_id = str(uuid.uuid4())
    record = {
        "manager_id": manager_id,
        "session_id": session_id,
        "timestamp": time.time(),
        "history": [],
        "errors": [],
        "strengths": [],
        "score": None,
        "next_recommendations": []
    }
    save_session(manager_id, session_id, record)
    return record

def append_message(manager_id: str, session_id: str, role: str, content: str, stage: Optional[str]):
    record = load_session(manager_id, session_id)
    if not record:
        return None
    record["history"].append({"role": role, "content": content, "stage": stage})
    save_session(manager_id, session_id, record)
    return record

def analyze_session(manager_id: str, session_id: str):
    record = load_session(manager_id, session_id)
    if not record:
        return None

    vp = VoicePipeline()
    msg = [
        {"role": "system",
         "content": "Ты анализируешь диалог менеджера. Выдели 3 ошибки, 3 сильные стороны и итоговый балл (0..100). Формат JSON: {errors:[], strengths:[], score:int}"},
        {"role": "user", "content": json.dumps(record["history"], ensure_ascii=False)[:3000]}
    ]
    j = vp.llm.chat(msg)
    try:
        data = json.loads(j)
        record["errors"] = data.get("errors", [])
        record["strengths"] = data.get("strengths", [])
        record["score"] = int(data.get("score", 70))
    except:
        record["errors"] = ["Автоматическая ошибка"]
        record["strengths"] = ["Хороший тон"]
        record["score"] = 70

    # Recommendations:
    msg2 = [
        {"role":"system", 
         "content": "Дай 3 короткие рекомендации, как улучшить навыки менеджеру. Сильно, чётко."},
        {"role":"user","content": json.dumps(record["errors"], ensure_ascii=False)}
    ]
    rec = vp.llm.chat(msg2)
    record["next_recommendations"] = rec.split("\n")[:3]

    save_session(manager_id, session_id, record)
    return record

def list_sessions(manager_id: str):
    files = os.listdir(DATA_DIR)
    sessions = []
    for f in files:
        if f.startswith(manager_id+"__") and f.endswith(".json"):
            with open(os.path.join(DATA_DIR, f), "r", encoding="utf-8") as ff:
                try:
                    sessions.append(json.load(ff))
                except:
                    pass
    return sessions
