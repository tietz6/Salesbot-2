
import json, time, uuid
from typing import Optional, Dict, Any
from core.db.v1 import DB
from .models import Invoice

class PaymentsEngine:
    def __init__(self, db_file: str="salesbot.db"):
        self.db = DB(db_file)

    def _key(self, invoice_id: str)->str:
        return f"invoice:{invoice_id}"

    def create_invoice(self, amount: float, currency: str="KGS", deal_id: Optional[str]=None)->Invoice:
        inv = Invoice(id=str(uuid.uuid4()), amount=float(amount), currency=currency, status="pending", deal_id=deal_id)
        self.db.set(self._key(inv.id), json.dumps(inv.to_dict(), ensure_ascii=False))
        self._timeline(inv.id, f"created amount={amount} {currency}")
        return inv

    def get_invoice(self, invoice_id: str)->Optional[Invoice]:
        raw = self.db.get(self._key(invoice_id))
        if not raw: return None
        data = json.loads(raw)
        return Invoice(**data)

    def set_status(self, invoice_id: str, status: str)->Optional[Invoice]:
        inv = self.get_invoice(invoice_id)
        if not inv: return None
        inv.status = status
        self.db.set(self._key(inv.id), json.dumps(inv.to_dict(), ensure_ascii=False))
        self._timeline(inv.id, f"status={status}")
        return inv

    def _timeline(self, invoice_id: str, event: str):
        key = f"invoice_tl:{invoice_id}:{int(time.time())}"
        self.db.set(key, event)
