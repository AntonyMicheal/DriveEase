from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False, index=True)
    amount = Column(Float, default=0)
    currency = Column(String, default="USD")
    status = Column(String, default="pending")
    provider = Column(String, nullable=True)
    provider_ref = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    booking = relationship("Booking", back_populates="payments")
