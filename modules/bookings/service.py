from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from modules.availability.model import AvailabilityBlock
from modules.bookings.model import Booking
from modules.bookings.schema import BookingCreate
from modules.vehicle.model import Vehicle

ACTIVE_BOOKING_STATUSES = ["pending", "confirmed"]


def list_bookings(db: Session) -> list[Booking]:
    return db.query(Booking).order_by(Booking.id).all()


def list_bookings_for_user(db: Session, user_id: int) -> list[Booking]:
    return (
        db.query(Booking)
        .filter(Booking.user_id == user_id)
        .order_by(Booking.id)
        .all()
    )


def get_booking(db: Session, booking_id: int) -> Booking | None:
    return db.query(Booking).filter(Booking.id == booking_id).first()


def _validate_dates(start_date: date, end_date: date) -> None:
    if start_date > end_date:
        raise HTTPException(status_code=400, detail="Invalid date range")


def _has_overlap(db: Session, vehicle_id: int, start_date: date, end_date: date) -> bool:
    booking_conflict = (
        db.query(Booking)
        .filter(
            Booking.vehicle_id == vehicle_id,
            Booking.status.in_(ACTIVE_BOOKING_STATUSES),
            Booking.start_date <= end_date,
            Booking.end_date >= start_date,
        )
        .first()
    )
    if booking_conflict:
        return True

    block_conflict = (
        db.query(AvailabilityBlock)
        .filter(
            AvailabilityBlock.vehicle_id == vehicle_id,
            AvailabilityBlock.start_date <= end_date,
            AvailabilityBlock.end_date >= start_date,
        )
        .first()
    )
    return block_conflict is not None


def create_booking(db: Session, user_id: int, data: BookingCreate) -> Booking:
    _validate_dates(data.start_date, data.end_date)

    vehicle = db.query(Vehicle).filter(Vehicle.id == data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    if not vehicle.is_available:
        raise HTTPException(status_code=400, detail="Vehicle is not available")

    if _has_overlap(db, vehicle.id, data.start_date, data.end_date):
        raise HTTPException(status_code=409, detail="Vehicle already booked")

    total_days = (data.end_date - data.start_date).days + 1
    total_price = max(total_days, 1) * (vehicle.daily_rate or 0)

    booking = Booking(
        user_id=user_id,
        vehicle_id=vehicle.id,
        start_date=data.start_date,
        end_date=data.end_date,
        status="pending",
        total_price=total_price,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(db: Session, booking: Booking) -> Booking:
    booking.status = "cancelled"
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def update_status(db: Session, booking: Booking, status: str) -> Booking:
    booking.status = status
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking
