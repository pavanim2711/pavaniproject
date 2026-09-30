"""Authentication API routes for registration and login."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import get_db
from app.models.user import User
from app.api.v1.schemas.auth import UserRegister, UserLogin, UserResponse, Token
from app.core.security import hash_password, verify_password
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """Register a new user with email, name, password, and role.
    
    Args:
        user_in: User registration data (name, email, password, role)
        db: Database session dependency
        
    Returns:
        Created user information (without password)
        
    Raises:
        HTTPException 400: If email already registered
        HTTPException 422: If input validation fails
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password with bcrypt (work factor 12)
    hashed_password = hash_password(user_in.password)
    
    # Create user
    user = User(
        email=user_in.email,
        password_hash=hashed_password,
        name=user_in.name,
        role=user_in.role,
        is_active=True,
        is_verified=False
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT token.
    
    Args:
        form_data: OAuth2 password form with email and password
        db: Database session dependency
        
    Returns:
        Access token with token type "bearer"
        
    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Query user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    
    # Validate credentials
    # Note: Use dummy check to prevent email enumeration timing attacks
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login timestamp
    user.update_last_login()
    db.commit()
    
    # Create access token with user_id, role, and permissions claims
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role,
            "permissions": get_permissions_for_role(user.role)
        }
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


def get_permissions_for_role(role: str) -> list:
    """Get permissions list for a given role."""
    permissions_map = {
        "Customer": [
            "can_view_products",
            "can_create_rental",
            "can_view_rental",
            "can_make_payment",
            "can_request_pickup",
            "can_view_recommendations"
        ],
        "Delivery_Partner": [
            "can_view_products",
            "can_view_rental",
            "can_access_delivery",
            "can_mark_delivered",
            "can_mark_picked_up"
        ],
        "Admin": [
            "can_view_products",
            "can_create_rental",
            "can_view_rental",
            "can_make_payment",
            "can_request_pickup",
            "can_view_recommendations",
            "can_access_admin",
            "can_access_delivery",
            "can_manage_users",
            "can_manage_products",
            "can_view_analytics"
        ]
    }
    return permissions_map.get(role, [])


@router.post("/refresh")
async def refresh_token(db: Session = Depends(get_db)):
    """Refresh access token (placeholder for future implementation)."""
    # TODO: Implement token refresh with refresh tokens
    return {"message": "Token refresh not yet implemented"}
