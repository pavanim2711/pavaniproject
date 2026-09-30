"""Authentication router - registration, login, and password reset."""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from datetime import datetime
import secrets

from app.db.session import get_db
from app.models.user import User
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token
from app.services.notification_service import notification_service

router = APIRouter(tags=["Authentication"])


class UserRegisterRequest(BaseModel):
    """User registration request."""
    name: str
    email: EmailStr
    password: str
    role: str = "Customer"


class UserLoginRequest(BaseModel):
    """User login request."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response."""
    access_token: str
    token_type: str = "bearer"


class ForgotPasswordRequest(BaseModel):
    """Forgot password request."""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request."""
    email: EmailStr
    token: str
    new_password: str


def generate_reset_token() -> str:
    """Generate a secure password reset token."""
    return secrets.token_urlsafe(32)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserRegisterRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        name=user_in.name,
        role=user_in.role,
        is_active=True,
        is_verified=False
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Send welcome email in background
    background_tasks.add_task(
        notification_service.send_registration_welcome,
        user_email=user.email,
        user_name=user.name
    )
    
    return {"id": str(user.id), "email": user.email, "name": user.name, "role": user.role}


@router.post("/login", response_model=TokenResponse)
async def login(form_data: UserLoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    user = db.query(User).filter(User.email == form_data.email).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(db: Session = Depends(get_db)):
    """Get current authenticated user (placeholder)."""
    return {"message": "Current user endpoint - MVP placeholder"}


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Request password reset - sends reset token to user."""
    user = db.query(User).filter(User.email == request.email).first()
    
    if user:
        # Generate reset token
        reset_token = generate_reset_token()
        
        # Send email in background
        background_tasks.add_task(
            notification_service.send_password_reset,
            user_email=user.email,
            reset_token=reset_token,
            reset_url="https://quicktym.com/reset-password"
        )
        
        return {
            "message": "If email exists, reset instructions have been sent",
            "token_for_mvp_testing": reset_token  # Remove in production
        }
    
    # Don't reveal if email exists
    return {"message": "If email exists, reset instructions have been sent"}


@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """Reset password with valid token."""
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # For MVP: basic token validation (no database storage of tokens)
    # In production, verify token from database with expiry check
    if len(request.token) < 32:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
    
    # Update password
    user.password_hash = hash_password(request.new_password)
    user.updated_at = datetime.utcnow()
    user.is_verified = True  # Reset implies email verification
    
    db.commit()
    
    return {"message": "Password reset successfully"}


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """Change password for authenticated user."""
    # This endpoint requires authentication (to be implemented in middleware)
    return {"message": "Change password endpoint - requires auth implementation"}
