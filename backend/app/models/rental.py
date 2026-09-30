"""Rental Model - SQLite compatible."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, DECIMAL, ForeignKey, Index, CheckConstraint, JSON
from sqlalchemy.orm import relationship
import uuid

from app.db.session import Base


class RentalSession(Base):
    """Rental session model tracking product rentals."""
    __tablename__ = "rental_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    booking_id = Column(String(36), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    total_seconds = Column(Integer, nullable=False, default=0)
    total_amount = Column(DECIMAL(12, 2), nullable=False, default=0.00)
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    estimated_cost = Column(DECIMAL(12, 2), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'active', 'completed', 'cancelled')", name="chk_rental_status"),
        CheckConstraint("total_seconds >= 0", name="chk_rental_total_seconds_non_negative"),
    )
    
    user = relationship("User", backref="rental_sessions")
    product = relationship("Product", backref="rental_sessions")
    booking = relationship("Booking", back_populates="rental_session")
    payment = relationship("Payment", back_populates="rental", uselist=False)
    delivery = relationship("Delivery", back_populates="rental", uselist=False)
    
    def __repr__(self) -> str:
        return f"<RentalSession(id={self.id}, status='{self.status}')>"


class Booking(Base):
    """Booking model for advance rental reservations."""
    __tablename__ = "bookings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_reference = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    total_hours = Column(Integer, nullable=False)
    estimated_cost = Column(DECIMAL(12, 2), nullable=False)
    confirmed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'confirmed', 'cancelled', 'completed')", name="chk_booking_status"),
    )
    
    user = relationship("User", backref="bookings")
    product = relationship("Product", backref="bookings")
    rental_session = relationship("RentalSession", back_populates="booking")
    
    def __repr__(self) -> str:
        return f"<Booking(id={self.id}, reference='{self.booking_reference}')>"
