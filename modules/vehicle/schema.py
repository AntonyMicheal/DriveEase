from typing import Optional

from pydantic import BaseModel, ConfigDict

class VehicleCreate(BaseModel):
    name: str
    type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    daily_rate: float = 0
    battery_range_km: Optional[int] = None
    location: Optional[str] = None
    image_url: Optional[str] = None


class VehicleUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    daily_rate: Optional[float] = None
    battery_range_km: Optional[int] = None
    location: Optional[str] = None
    is_available: Optional[bool] = None
    image_url: Optional[str] = None

class VehicleOut(BaseModel):
    id: int
    name: str
    type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    daily_rate: float
    battery_range_km: Optional[int] = None
    location: Optional[str] = None
    is_available: bool
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
