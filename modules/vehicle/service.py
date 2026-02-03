from sqlalchemy.orm import Session
from modules.vehicle.model import Vehicle
from modules.vehicle.schema import VehicleCreate, VehicleUpdate

def create_vehicle(db: Session, data: VehicleCreate):
    vehicle = Vehicle(**data.dict())
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def get_vehicle(db: Session, vehicle_id: int) -> Vehicle | None:
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()


def list_vehicles(db: Session) -> list[Vehicle]:
    return db.query(Vehicle).order_by(Vehicle.id).all()


def update_vehicle(db: Session, vehicle: Vehicle, data: VehicleUpdate) -> Vehicle:
    payload = data.dict(exclude_unset=True)
    for key, value in payload.items():
        setattr(vehicle, key, value)
    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)
    return vehicle


def delete_vehicle(db: Session, vehicle: Vehicle) -> None:
    db.delete(vehicle)
    db.commit()
