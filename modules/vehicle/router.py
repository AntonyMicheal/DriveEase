from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.dependencies import get_db
from modules.vehicle import service, schema
from modules.auth.dependencies import get_current_admin

router = APIRouter(prefix="/vehicles", tags=["Vehicles"])

@router.post("/", response_model=schema.VehicleOut)
def add_vehicle(
    payload: schema.VehicleCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    return service.create_vehicle(db, payload)


@router.get("/", response_model=list[schema.VehicleOut])
def list_vehicles(db: Session = Depends(get_db)):
    return service.list_vehicles(db)


@router.get("/{vehicle_id}", response_model=schema.VehicleOut)
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    vehicle = service.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@router.patch("/{vehicle_id}", response_model=schema.VehicleOut)
def update_vehicle(
    vehicle_id: int,
    payload: schema.VehicleUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    vehicle = service.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return service.update_vehicle(db, vehicle, payload)


@router.delete("/{vehicle_id}")
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    vehicle = service.get_vehicle(db, vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    service.delete_vehicle(db, vehicle)
    return {"status": "deleted"}
