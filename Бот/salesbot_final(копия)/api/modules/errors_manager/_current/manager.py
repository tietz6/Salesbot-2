
import traceback, json, time
from core.db.v1 import DB

class ErrorsManager:
    def __init__(self):
        self.db = DB("salesbot.db")

    def log_error(self, module: str, e: Exception):
        info = {
            "module": module,
            "time": time.time(),
            "type": type(e).__name__,
            "message": str(e),
            "trace": traceback.format_exc()
        }
        key = f"error:{module}:{int(time.time())}"
        self.db.set(key, json.dumps(info, ensure_ascii=False))
        return info

    def list_errors(self):
        # naive scan: load all keys starting with 'error:'
        out=[]
        import sqlite3
        conn = sqlite3.connect("salesbot.db")
        cur = conn.execute("SELECT k,v FROM kv WHERE k LIKE 'error:%'")
        for k,v in cur.fetchall():
            try:
                out.append(json.loads(v))
            except Exception:
                pass
        conn.close()
        return out

    def clear(self):
        import sqlite3
        conn = sqlite3.connect("salesbot.db")
        conn.execute("DELETE FROM kv WHERE k LIKE 'error:%'")
        conn.commit()
        conn.close()
