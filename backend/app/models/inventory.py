"""Inventory Model - Track stock and availability."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, DECIMAL, Index
from sqlalchemy.orm import relationship
import uuid

from app.db.session import Base


class InventoryLog(Base):
    """Track inventory changes for products."""
    __tablename__ = "inventory_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    rental_id = Column(String(36), ForeignKey("rental_sessions.id"), nullable=True, index=True)
    
    # Change details
    change_type = Column(String(20), nullable=False)  # reserve, release, update, restock
    quantity_change = Column(Integer, nullable=False)  # Can be negative
    previous_quantity = Column(Integer, nullable=False)
    new_quantity = Column(Integer, nullable=False)
    
    reason = Column(Text, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    created_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    __table_args__ = (
        Index("idx_product_created", "product_id", "created_at"),
    )
    
    product = relationship("Product", backref="inventory_logs")
    rental = relationship("RentalSession", backref="inventory_logs")
    user = relationship("User", backref="inventory_logs")
    
    def __repr__(self) -> str:
        return f"<InventoryLog(product={self.product_id}, change={self.quantity_change})>"


class ProductAvailability(Base):
    """Track date-based availability for products."""
    __tablename__ = "product_availability"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    
    # Date range
    unavailable_start = Column(DateTime, nullable=False, index=True)
    unavailable_end = Column(DateTime, nullable=True, index=True)
    
    reason = Column(String(200), nullable=True)  # maintenance, holiday, etc.
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_product_date_range", "product_id", "unavailable_start", "unavailable_end"),
    )
    
    product = relationship("Product", backref="availability_blocks")
    
    def __repr__(self) -> str:
        return f"<ProductAvailability(product={self.product_id}, start={self.unavailable_start})>"
