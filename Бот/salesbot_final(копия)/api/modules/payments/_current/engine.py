
import json, time
from dataclasses import dataclass, asdict
from core.state.v1 import StateStore
from integrations.patch_v4.payment_gateway import PaymentGateway
from bridges.crm_sync.v1 import CRMSync

@dataclass
class PaymentDeal:
    deal_id: str
    payment_id: str
    amount: int
    currency: str
    redirect_url: str
    status: str

class PaymentsEngine:
    def __init__(self, deal_id: str):
        self.key = f"payment:{deal_id}"
        self.store = StateStore("salesbot.db")
        self.pg = PaymentGateway()
        self.crm = CRMSync()
        raw = self.store.get(self.key)
        if raw:
            self.state = PaymentDeal(**json.loads(raw))
        else:
            self.state = None

    def _save(self):
        self.store.set(self.key, json.dumps(asdict(self.state), ensure_ascii=False))

    def create_invoice(self, amount: int, currency: str="KGS")->dict:
        r = self.pg.create_payment(amount, currency)
        if not r.get("ok"):
            return r
        data = r["data"]
        self.state = PaymentDeal(
            deal_id=self.key.split("payment:")[1],
            payment_id=data["payment_id"],
            amount=amount,
            currency=currency,
            redirect_url=data["redirect_url"],
            status="waiting_payment"
        )
        self._save()
        self.crm.sync_status(self.state.deal_id, "waiting_payment")
        self.crm.push_timeline(self.state.deal_id, "invoice_created", {
            "amount": amount,
            "currency": currency,
            "payment_id": data["payment_id"]
        })
        return {"ok": True, "invoice": asdict(self.state)}

    def process_webhook(self, payload: dict)->dict:
        pid = payload.get("payment_id")
        status = payload.get("status","paid")
        if not self.state or self.state.payment_id != pid:
            return {"ok": False, "error":"unknown payment"}

        self.state.status = "paid" if status=="paid" else "failed"
        self._save()

        if self.state.status=="paid":
            self.crm.sync_status(self.state.deal_id, "paid")
            self.crm.push_timeline(self.state.deal_id, "payment_success", payload)
        else:
            self.crm.sync_status(self.state.deal_id, "failed")
            self.crm.push_timeline(self.state.deal_id, "payment_failed", payload)

        return {"ok": True, "deal_id": self.state.deal_id, "status": self.state.status}

    def get_status(self)->dict:
        if not self.state:
            return {"ok": False, "error":"not found"}
        return {"ok": True, "status": self.state.status, "invoice": asdict(self.state)}
