from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookingCreate(BaseModel):
    vehicle_id: int
    start_date: date
    end_date: date


class BookingStatusUpdate(BaseModel):
    status: str


class BookingOut(BaseModel):
    id: int
    user_id: int
    vehicle_id: int
    start_date: date
    end_date: date
    status: str
    total_price: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
