
import json, time, traceback
from typing import List, Dict, Any
from core.state.v1 import StateStore

try:
    from bridges.crm_sync.v1 import CRMSync  # optional
    _CRM_AVAILABLE = True
except Exception:
    _CRM_AVAILABLE = False
    CRMSync = None  # type: ignore

KV_PATH = "salesbot.db"
PREFIX = "err:"

def _key(module: str)->str:
    ts = f"{time.time():.6f}"
    return f"{PREFIX}{ts}:{module}"

def track_error(module: str, context: Dict[str,Any]|None, exc: Any, level: str = "error", push_to_crm: bool = False, deal_id: str | None = None)->dict:
    ctx = context or {}
    payload = {
        "module": module,
        "level": level,
        "ts": time.time(),
        "context": ctx,
    }
    if isinstance(exc, Exception):
        payload["error"] = {
            "type": exc.__class__.__name__,
            "msg": str(exc),
            "trace": traceback.format_exc()[:4000]
        }
    else:
        payload["error"] = {"msg": str(exc)}

    kv = StateStore(KV_PATH)
    kv.set(_key(module), json.dumps(payload, ensure_ascii=False))

    pushed = None
    if push_to_crm and _CRM_AVAILABLE and deal_id:
        try:
            CRMSync().push_timeline(deal_id, "error", {"module": module, "level": level, "context": ctx, "err": payload.get("error")})
            pushed = True
        except Exception as e:
            pushed = False

    return {"ok": True, "logged": True, "pushed_to_crm": pushed}

def get_errors(prefix: str = PREFIX, limit: int = 200)->List[dict]:
    kv = StateStore(KV_PATH)
    items = kv.scan(prefix, limit=limit)
    res = []
    for k,v in items:
        try:
            res.append(json.loads(v))
        except Exception:
            res.append({"key": k, "raw": v})
    # сортировка по времени (ts)
    res.sort(key=lambda x: x.get("ts", 0), reverse=True)
    return res

def clear_errors(prefix: str = PREFIX)->dict:
    kv = StateStore(KV_PATH)
    items = kv.scan(prefix, limit=10000)
    n = 0
    for k,_ in items:
        n += kv.delete(k)
    return {"ok": True, "deleted": n}
