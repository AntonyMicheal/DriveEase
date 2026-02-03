from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_db
from modules.auth.dependencies import get_current_active_user, get_current_admin
from modules.bookings import schema, service

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("/", response_model=schema.BookingOut)
def create_booking(
    payload: schema.BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return service.create_booking(db, current_user.id, payload)


@router.get("/me", response_model=list[schema.BookingOut])
def my_bookings(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return service.list_bookings_for_user(db, current_user.id)


@router.get("/", response_model=list[schema.BookingOut])
def list_all(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    return service.list_bookings(db)


@router.get("/{booking_id}", response_model=schema.BookingOut)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    booking = service.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return booking


@router.patch("/{booking_id}/cancel", response_model=schema.BookingOut)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    booking = service.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return service.cancel_booking(db, booking)


@router.patch("/{booking_id}/status", response_model=schema.BookingOut)
def update_status(
    booking_id: int,
    payload: schema.BookingStatusUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    booking = service.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return service.update_status(db, booking, payload.status)
