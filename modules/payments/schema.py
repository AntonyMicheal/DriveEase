from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    currency: str = "USD"
    status: str = "pending"
    provider: Optional[str] = None
    provider_ref: Optional[str] = None


class PaymentOut(BaseModel):
    id: int
    booking_id: int
    amount: float
    currency: str
    status: str
    provider: Optional[str] = None
    provider_ref: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
