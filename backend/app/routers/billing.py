"""Billing router - Discounts, coupons, and billing calculations."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.core.jwt import verify_access_token
from app.services.billing_service_enhanced import enhanced_billing_service

router = APIRouter(prefix="/billing", tags=["Billing"])


class CalculateBillRequest(BaseModel):
    """Request model for calculating bill."""
    product_id: str
    hourly_rate: float
    start_time: datetime
    end_time: datetime
    coupon_code: Optional[str] = None


class CreateCouponRequest(BaseModel):
    """Request model for creating a coupon."""
    code: str = Field(..., min_length=3, max_length=20)
    discount_type: str = Field(..., description="percentage or fixed")
    discount_value: float = Field(..., gt=0)
    min_order_amount: float = Field(default=0, ge=0)
    max_discount: Optional[float] = Field(None, gt=0)
    valid_days: int = Field(default=30, ge=1, le=365)
    usage_limit: Optional[int] = Field(None, ge=1)
    first_time_only: bool = Field(default=False)
    
    @validator('discount_type')
    def validate_discount_type(cls, v):
        if v not in ['percentage', 'fixed']:
            raise ValueError('discount_type must be "percentage" or "fixed"')
        return v


class ValidateCouponRequest(BaseModel):
    """Request model for validating coupon."""
    coupon_code: str
    order_amount: float


def get_current_user(token: str, db: Session) -> User:
    """Get current authenticated user from token."""
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.post("/calculate")
async def calculate_bill(
    request: CalculateBillRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Calculate rental bill with discounts.
    
    Applies:
    - Subscription discounts (if applicable)
    - Coupon discounts (if valid)
    - GST (18%)
    """
    user_id = None
    if token:
        user = get_current_user(token, db)
        user_id = str(user.id)
    
    result = enhanced_billing_service.calculate_rental_cost_with_discount(
        hourly_rate=request.hourly_rate,
        start_time=request.start_time,
        end_time=request.end_time,
        coupon_code=request.coupon_code,
        user_id=user_id,
        db=db
    )
    
    return result


@router.post("/coupons/create")
async def create_coupon(
    request: CreateCouponRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Create a new coupon code.
    
    Admin only.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    if user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create coupons"
        )
    
    result = enhanced_billing_service.create_coupon(
        code=request.code,
        discount_type=request.discount_type,
        discount_value=request.discount_value,
        min_order_amount=request.min_order_amount,
        max_discount=request.max_discount,
        valid_days=request.valid_days,
        usage_limit=request.usage_limit,
        first_time_only=request.first_time_only
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to create coupon")
        )
    
    return result


@router.post("/coupons/validate")
async def validate_coupon(
    request: ValidateCouponRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Validate a coupon code.
    
    Checks:
    - Coupon exists
    - Not expired
    - Minimum order amount met
    - Usage limit not reached
    """
    user_id = None
    if token:
        user = get_current_user(token, db)
        user_id = str(user.id)
    
    result = enhanced_billing_service.validate_coupon(
        coupon_code=request.coupon_code,
        order_amount=request.order_amount,
        user_id=user_id
    )
    
    return result


@router.get("/coupons/available")
async def get_available_coupons():
    """
    Get list of available coupon codes.
    
    Returns all active, valid coupons.
    """
    coupons = enhanced_billing_service.get_available_coupons()
    
    return {
        "coupons": coupons,
        "total": len(coupons)
    }


@router.get("/subscription-plans")
async def get_subscription_plans():
    """
    Get available subscription plans.
    
    Shows benefits and pricing for each plan.
    """
    return {
        "plans": enhanced_billing_service.SUBSCRIPTION_PLANS
    }


@router.post("/referral-code/generate")
async def generate_referral_code(
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Generate a unique referral code.
    
    Share with friends to earn discounts.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    code = enhanced_billing_service.generate_referral_code()
    
    # In production, store the code associated with user
    
    return {
        "referral_code": code,
        "bonus_details": enhanced_billing_service.calculate_referral_bonus(code)
    }
