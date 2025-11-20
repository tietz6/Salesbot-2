
from abc import ABC, abstractmethod

class ProviderBase(ABC):
    name = "base"
    @abstractmethod
    def create_payment(self, invoice_id: str, amount: float, currency: str): ...
    @abstractmethod
    def capture(self, invoice_id: str): ...
