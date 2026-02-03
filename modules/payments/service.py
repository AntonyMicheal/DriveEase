from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.bookings.model import Booking
from modules.payments.model import Payment
from modules.payments.schema import PaymentCreate


def list_payments(db: Session) -> list[Payment]:
    return db.query(Payment).order_by(Payment.id).all()


def get_payment(db: Session, payment_id: int) -> Payment | None:
    return db.query(Payment).filter(Payment.id == payment_id).first()


def create_payment(db: Session, data: PaymentCreate) -> Payment:
    booking = db.query(Booking).filter(Booking.id == data.booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    payment = Payment(
        booking_id=data.booking_id,
        amount=data.amount,
        currency=data.currency,
        status=data.status,
        provider=data.provider,
        provider_ref=data.provider_ref,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
