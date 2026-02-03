from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AvailabilityCreate(BaseModel):
    vehicle_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None


class AvailabilityOut(BaseModel):
    id: int
    vehicle_id: int
    start_date: date
    end_date: date
    reason: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
