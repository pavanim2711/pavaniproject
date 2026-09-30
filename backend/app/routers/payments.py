"""Payments router - Payment processing with Razorpay and Stripe integration."""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.models.rental import RentalSession
from app.models.payment import Payment
from app.core.jwt import verify_access_token
from app.core.payment_config import payment_settings
from app.services.razorpay_service import razorpay_service
from app.services.stripe_service import stripe_service

router = APIRouter(prefix="/payments", tags=["Payments"])

class PaymentCreateRequest(BaseModel):
    """Request model for creating a payment."""
    rental_id: str = Field(..., description="Rental session ID")
    payment_method: str = Field(default="upi", description="Payment method: upi, card, netbanking, wallet")
    provider: str = Field(default="razorpay", description="Payment provider: razorpay or stripe")


class RazorpayVerifyRequest(BaseModel):
    """Request model for Razorpay payment verification."""
    order_id: str = Field(..., description="Razorpay order ID")
    payment_id: str = Field(..., description="Razorpay payment ID")
    signature: str = Field(..., description="Payment signature")


class StripeConfirmRequest(BaseModel):
    """Request model for Stripe payment confirmation."""
    payment_intent_id: str = Field(..., description="Stripe payment intent ID")


class RefundRequest(BaseModel):
    """Request model for refund."""
    amount: Optional[float] = Field(None, description="Refund amount (None for full refund)")


class VerifyOTPRequest(BaseModel):
    """Request model for OTP verification."""
    otp: str = Field(..., description="OTP to verify")


class PaymentResponse(BaseModel):
    """Response model for payment."""
    id: str
    rental_id: str
    transaction_id: str
    amount: float
    base_amount: float
    gst_amount: float
    status: str
    payment_method: str
    created_at: str
    completed_at: Optional[str]


def get_current_user(token: str, db: Session):
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

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_in: PaymentCreateRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Create a payment order with Razorpay or Stripe.
    
    Returns order details needed for frontend payment processing.
    """
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    rental = db.query(RentalSession).filter(RentalSession.id == payment_in.rental_id).first()
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental session not found"
        )
    
    if user_id and rental.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to process payment for this rental"
        )
    
    amount = float(rental.total_amount)
    
    # Choose payment provider
    if payment_in.provider == "stripe" and payment_settings.STRIPE_ENABLED:
        result = stripe_service.create_payment_intent(
            amount=amount,
            currency=payment_settings.PAYMENT_CURRENCY.lower(),
            rental_id=rental.id,
            user_id=user_id,
            db=db
        )
    else:
        # Default to Razorpay
        result = razorpay_service.create_order(
            amount=amount,
            currency=payment_settings.PAYMENT_CURRENCY,
            rental_id=rental.id,
            user_id=user_id,
            db=db
        )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Failed to create payment order")
        )
    
    return result


@router.post("/razorpay/verify", response_model=PaymentResponse)
async def verify_razorpay_payment(
    verify_in: RazorpayVerifyRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """Verify Razorpay payment after successful payment on frontend."""
    if token:
        user = get_current_user(token, db)
    
    result = razorpay_service.verify_payment(
        order_id=verify_in.order_id,
        payment_id=verify_in.payment_id,
        signature=verify_in.signature,
        db=db
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Payment verification failed")
        )
    
    payment = db.query(Payment).filter(
        Payment.transaction_id == verify_in.payment_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment record not found"
        )
    
    return {
        "id": payment.id,
        "rental_id": payment.rental_id,
        "transaction_id": payment.transaction_id,
        "amount": payment.amount,
        "base_amount": payment.base_amount,
        "gst_amount": payment.gst_amount,
        "status": payment.status,
        "payment_method": payment.payment_method,
        "created_at": payment.created_at.isoformat(),
        "completed_at": payment.completed_at.isoformat() if payment.completed_at else None
    }


@router.post("/stripe/confirm", response_model=PaymentResponse)
async def confirm_stripe_payment(
    confirm_in: StripeConfirmRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """Confirm Stripe payment after successful payment on frontend."""
    if token:
        user = get_current_user(token, db)
    
    result = stripe_service.confirm_payment(
        payment_intent_id=confirm_in.payment_intent_id,
        db=db
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Payment confirmation failed")
        )
    
    payment = db.query(Payment).filter(
        Payment.transaction_id == confirm_in.payment_intent_id
    ).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment record not found"
        )
    
    return {
        "id": payment.id,
        "rental_id": payment.rental_id,
        "transaction_id": payment.transaction_id,
        "amount": payment.amount,
        "base_amount": payment.base_amount,
        "gst_amount": payment.gst_amount,
        "status": payment.status,
        "payment_method": payment.payment_method,
        "created_at": payment.created_at.isoformat(),
        "completed_at": payment.completed_at.isoformat() if payment.completed_at else None
    }


@router.post("/{payment_id}/refund")
async def refund_payment(
    payment_id: str,
    refund_in: RefundRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """Process a refund for a completed payment."""
    if token:
        user = get_current_user(token, db)
    
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    if payment.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only completed payments can be refunded"
        )
    
    # Choose provider based on payment method
    if payment.payment_method == "stripe":
        result = stripe_service.create_refund(
            payment_intent_id=payment.transaction_id,
            amount=refund_in.amount,
            db=db
        )
    else:
        result = razorpay_service.refund_payment(
            payment_id=payment.transaction_id,
            amount=refund_in.amount,
            db=db
        )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Refund failed")
        )
    
    return result





@router.post("/{payment_id}/webhook/stripe")
async def stripe_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle Stripe webhook events."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    result = stripe_service.handle_webhook(
        payload=payload,
        sig_header=sig_header,
        db=db
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Webhook processing failed")
        )
    
    return {"status": "success", "event": result.get("event")}


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Get payment status by ID."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    rental = db.query(RentalSession).filter(RentalSession.id == payment.rental_id).first()
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental session not found"
        )
    
    if user_id and rental.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )
    
    return {
        "id": payment.id,
        "rental_id": payment.rental_id,
        "transaction_id": payment.transaction_id,
        "amount": payment.amount,
        "base_amount": payment.base_amount,
        "gst_amount": payment.gst_amount,
        "status": payment.status,
        "payment_method": payment.payment_method,
        "created_at": payment.created_at.isoformat(),
        "completed_at": payment.completed_at.isoformat() if payment.completed_at else None
    }
