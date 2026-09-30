"""Authentication schemas for registration and login."""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re


class UserRegister(BaseModel):
    """Schema for user registration request."""
    name: str = Field(..., min_length=2, max_length=50, description="User's full name (2-50 characters)")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters with uppercase, lowercase, and number)")
    role: str = Field(default="Customer", description="User role: Customer, Delivery_Partner, or Admin")
    
    @validator("password")
    def validate_password_strength(cls, v: str) -> str:
        """Validate password strength requirements."""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        
        return v
    
    @validator("role")
    def validate_role(cls, v: str) -> str:
        """Validate role is one of the allowed values."""
        valid_roles = ["Customer", "Delivery_Partner", "Admin"]
        if v not in valid_roles:
            raise ValueError(f"Role must be one of: {valid_roles}")
        return v


class UserLogin(BaseModel):
    """Schema for user login request."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """Schema for user response (excluding password)."""
    id: str
    email: str
    name: str
    role: str
    phone: Optional[str] = None
    address: str = "{}"
    location: str = "Bengaluru"
    is_active: bool = True
    is_verified: bool = False
    created_at: str
    last_login: Optional[str] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Schema for decoded token payload."""
    sub: str
    role: str
    permissions: list
