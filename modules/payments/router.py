from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.dependencies import get_db
from modules.auth.dependencies import get_current_active_user, get_current_admin
from modules.bookings.service import get_booking
from modules.payments import schema, service

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=schema.PaymentOut)
def create_payment(
    payload: schema.PaymentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    booking = get_booking(db, payload.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return service.create_payment(db, payload)


@router.get("/", response_model=list[schema.PaymentOut])
def list_all(db: Session = Depends(get_db), _: str = Depends(get_current_admin)):
    return service.list_payments(db)


@router.get("/{payment_id}", response_model=schema.PaymentOut)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    payment = service.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.booking.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")
    return payment
