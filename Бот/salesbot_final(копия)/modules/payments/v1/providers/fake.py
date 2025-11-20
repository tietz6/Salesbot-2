
from .schema import ProviderBase

class FakeProvider(ProviderBase):
    name = "fake"

    def create_payment(self, invoice_id: str, amount: float, currency: str):
        # In real life return redirect URL; here we just emulate
        return {"ok": True, "provider": self.name, "invoice_id": invoice_id}

    def capture(self, invoice_id: str):
        return {"ok": True, "status": "paid", "invoice_id": invoice_id}
