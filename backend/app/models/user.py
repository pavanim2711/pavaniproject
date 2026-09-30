"""User model for Quick Tym authentication and authorization."""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Boolean, Text, DECIMAL, Integer
import uuid

from app.db.session import Base


class User(Base):
    """User model representing all system users with role-based permissions."""
    
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, index=True, default="Customer")
    phone = Column(String(15), unique=True, nullable=True)
    address = Column(Text, nullable=True, default="{}")
    location = Column(String(100), default="Bengaluru")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Delivery partner specific fields
    partner_rating = Column(DECIMAL(3, 2), nullable=True, default=5.0)
    total_deliveries = Column(Integer, nullable=True, default=0)
    current_deliveries = Column(Integer, nullable=True, default=0)
    current_latitude = Column(DECIMAL(10, 8), nullable=True)  # For delivery partner location
    current_longitude = Column(DECIMAL(11, 8), nullable=True)  # For delivery partner location
    last_location_update = Column(DateTime, nullable=True)
    
    # Validation for role
    VALID_ROLES = ["Customer", "Delivery_Partner", "Admin"]
    
    def __init__(
        self,
        email: str,
        password_hash: str,
        name: str,
        role: str = "Customer",
        phone: Optional[str] = None,
        address: Optional[str] = None,
        location: Optional[str] = "Bengaluru",
        is_active: bool = True,
        is_verified: bool = False,
        last_login: Optional[datetime] = None,
        partner_rating: Optional[float] = None,
        total_deliveries: int = 0,
        current_deliveries: int = 0,
        current_latitude: Optional[float] = None,
        current_longitude: Optional[float] = None
    ):
        # Validate role
        if role not in self.VALID_ROLES:
            raise ValueError(f"Invalid role '{role}'. Must be one of: {self.VALID_ROLES}")
        
        self.email = email
        self.password_hash = password_hash
        self.name = name
        self.role = role
        self.phone = phone
        self.address = address or "{}"
        self.location = location
        self.is_active = is_active
        self.is_verified = is_verified
        self.last_login = last_login
        self.partner_rating = partner_rating
        self.total_deliveries = total_deliveries
        self.current_deliveries = current_deliveries
        self.current_latitude = current_latitude
        self.current_longitude = current_longitude
    
    def update_last_login(self):
        """Update the last login timestamp."""
        self.last_login = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert user to dictionary (excluding password)."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "phone": self.phone,
            "address": self.address,
            "location": self.location,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "partner_rating": float(self.partner_rating) if self.partner_rating else None,
            "total_deliveries": self.total_deliveries,
            "current_deliveries": self.current_deliveries,
            "current_latitude": float(self.current_latitude) if self.current_latitude else None,
            "current_longitude": float(self.current_longitude) if self.current_longitude else None
        }
