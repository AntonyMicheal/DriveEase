from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_db
from modules.auth.dependencies import get_current_admin
from modules.availability import schema, service

router = APIRouter(prefix="/availability", tags=["Availability"])


@router.post("/", response_model=schema.AvailabilityOut)
def create_block(
    payload: schema.AvailabilityCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    if payload.start_date > payload.end_date:
        raise HTTPException(status_code=400, detail="Invalid date range")
    return service.create_block(db, payload)


@router.get("/", response_model=list[schema.AvailabilityOut])
def list_blocks(
    vehicle_id: int | None = None,
    db: Session = Depends(get_db),
):
    return service.list_blocks(db, vehicle_id=vehicle_id)


@router.delete("/{block_id}")
def delete_block(
    block_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    block = service.get_block(db, block_id)
    if not block:
        raise HTTPException(status_code=404, detail="Block not found")
    service.delete_block(db, block)
    return {"status": "deleted"}
