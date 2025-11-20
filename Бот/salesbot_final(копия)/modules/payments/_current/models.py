
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Invoice:
    id: str
    amount: float
    currency: str
    status: str = "pending"
    deal_id: Optional[str] = None

    def to_dict(self):
        return asdict(self)
