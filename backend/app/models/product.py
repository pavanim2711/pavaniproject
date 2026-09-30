"""Product Model - SQLite compatible."""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Integer, DECIMAL, JSON, ForeignKey, Text, Index, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
import uuid

from app.db.session import Base


class Category(Base):
    """Product category for organizing the catalog."""
    __tablename__ = "categories"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    parent_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", back_populates="category_ref")
    
    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}')>"


class Product(Base):
    """Product model representing rentable items."""
    __tablename__ = "products"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(20), nullable=False)
    price_per_hour = Column(DECIMAL(10, 2), nullable=False)
    min_rental_hours = Column(Integer, nullable=False, default=1)
    max_rental_hours = Column(Integer, nullable=False, default=24)
    specifications = Column(JSON, nullable=False, default={})
    image_url = Column(String(500), nullable=True)
    popularity_score = Column(DECIMAL(5, 4), nullable=False, default=0.0)
    rental_count = Column(Integer, nullable=False, default=0)
    average_rating = Column(DECIMAL(3, 2), nullable=False, default=0.0)
    stock_quantity = Column(Integer, nullable=False, default=10)
    is_available = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("category IN ('Indoor', 'Outdoor')", name="chk_product_category"),
        CheckConstraint("price_per_hour >= 50 AND price_per_hour <= 500", name="chk_product_price_bounds"),
    )
    
    category_ref = relationship("Category", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False)
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', price={self.price_per_hour})>"


class Inventory(Base):
    """Inventory model tracking stock levels."""
    __tablename__ = "inventory"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    min_stock = Column(Integer, nullable=False, default=5)
    max_stock = Column(Integer, nullable=False, default=100)
    last_restocked = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="chk_inventory_quantity_non_negative"),
    )
    
    product = relationship("Product", back_populates="inventory")
    
    def __repr__(self) -> str:
        return f"<Inventory(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
