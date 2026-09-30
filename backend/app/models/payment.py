"""Payment Model - Complete implementation."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, DECIMAL, ForeignKey, Text, CheckConstraint
from sqlalchemy.orm import relationship
import uuid

from app.db.session import Base


class Payment(Base):
    """Payment model for rental payment processing."""
    __tablename__ = "payments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rental_id = Column(String(36), ForeignKey("rental_sessions.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    transaction_id = Column(String(50), unique=True, nullable=False, index=True)
    amount = Column(DECIMAL(12, 2), nullable=False)
    base_amount = Column(DECIMAL(12, 2), nullable=False)
    gst_amount = Column(DECIMAL(12, 2), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    payment_method = Column(String(20), nullable=False, default="upi")
    otp_hash = Column(String(100), nullable=True)
    otp_verified = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    failure_reason = Column(Text, nullable=True)
    invoice_url = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("status IN ('pending', 'completed', 'failed', 'refunded')", name="chk_payment_status"),
        CheckConstraint("payment_method IN ('upi', 'card', 'netbanking', 'wallet')", name="chk_payment_method"),
    )
    
    rental = relationship("RentalSession", back_populates="payment")
    user = relationship("User", backref="payments")
    
    def __repr__(self) -> str:
        return f"<Payment(id={self.id}, status='{self.status}')>"
