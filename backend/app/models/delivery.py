"""Delivery Model - Complete implementation."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, DECIMAL, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
import uuid

from app.db.session import Base


class Delivery(Base):
    """Delivery model for product delivery management."""
    __tablename__ = "deliverys"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rental_id = Column(String(36), ForeignKey("rental_sessions.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    delivery_partner_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(String(20), nullable=False, default="pending")
    pickup_address = Column(Text, nullable=False)
    delivery_address = Column(Text, nullable=False)
    pickup_time = Column(DateTime, nullable=True)
    delivery_time = Column(DateTime, nullable=True)
    distance_km = Column(DECIMAL(5, 2), nullable=True)
    partner_rating = Column(DECIMAL(3, 2), nullable=True)
    delivery_fee = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'assigned', 'in_transit', 'delivered', 'cancelled')", name="chk_delivery_status"),
        CheckConstraint("distance_km IS NULL OR distance_km >= 0", name="chk_delivery_distance_non_negative"),
    )
    
    rental = relationship("RentalSession", back_populates="delivery")
    user = relationship("User", foreign_keys=[user_id], backref="deliveries")
    partner = relationship("User", foreign_keys=[delivery_partner_id])
    
    def __repr__(self) -> str:
        return f"<Delivery(id={self.id}, status='{self.status}')>"
