"""Enhanced billing service with discounts and coupons."""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging
import secrets
import string

from app.models.rental import RentalSession
from app.models.product import Product
from app.models.user import User

logger = logging.getLogger(__name__)


class Coupon:
    """Coupon/discount code model."""
    def __init__(
        self,
        code: str,
        discount_type: str,  # percentage, fixed
        discount_value: float,
        min_order_amount: float = 0,
        max_discount: float = None,
        valid_from: datetime = None,
        valid_until: datetime = None,
        usage_limit: int = None,
        first_time_only: bool = False
    ):
        self.code = code
        self.discount_type = discount_type
        self.discount_value = discount_value
        self.min_order_amount = min_order_amount
        self.max_discount = max_discount
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.usage_limit = usage_limit
        self.first_time_only = first_time_only
        self.used_count = 0


class EnhancedBillingService:
    """Enhanced billing with discounts, coupons, and subscription support."""
    
    # Store active coupons (in production, use database)
    coupons: Dict[str, Coupon] = {}
    
    # Subscription plans
    SUBSCRIPTION_PLANS = {
        "basic": {
            "name": "Basic",
            "monthly_fee": 299,
            "discount_percent": 5,
            "free_delivery_count": 2
        },
        "premium": {
            "name": "Premium",
            "monthly_fee": 599,
            "discount_percent": 10,
            "free_delivery_count": 5
        },
        "enterprise": {
            "name": "Enterprise",
            "monthly_fee": 999,
            "discount_percent": 15,
            "free_delivery_count": 999
        }
    }
    
    def __init__(self):
        # Initialize default coupons
        self._init_default_coupons()
    
    def _init_default_coupons(self):
        """Initialize default promotional coupons."""
        # Welcome coupon for new users
        self.coupons["WELCOME10"] = Coupon(
            code="WELCOME10",
            discount_type="percentage",
            discount_value=10,
            min_order_amount=100,
            max_discount=100,
            first_time_only=True
        )
        
        # Weekend special
        self.coupons["WEEKEND20"] = Coupon(
            code="WEEKEND20",
            discount_type="percentage",
            discount_value=20,
            min_order_amount=200,
            max_discount=200
        )
        
        # Fixed discount coupon
        self.coupons["FLAT50"] = Coupon(
            code="FLAT50",
            discount_type="fixed",
            discount_value=50,
            min_order_amount=150
        )
    
    def calculate_rental_cost_with_discount(
        self,
        hourly_rate: float,
        start_time: datetime,
        end_time: datetime,
        coupon_code: Optional[str] = None,
        user_id: Optional[str] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """
        Calculate rental cost with discounts applied.
        
        Args:
            hourly_rate: Hourly rate of the product
            start_time: Rental start time
            end_time: Rental end time
            coupon_code: Optional discount coupon
            user_id: User ID for subscription benefits
            db: Database session
            
        Returns:
            Detailed cost breakdown with discounts
        """
        # Calculate base cost
        duration_seconds = int((end_time - start_time).total_seconds())
        hours = duration_seconds / 3600
        base_amount = Decimal(str(hours * hourly_rate))
        
        # Calculate taxes
        gst_rate = Decimal("0.18")
        gst_amount = base_amount * gst_rate
        
        # Initialize discount
        discount_amount = Decimal("0")
        discount_details = {}
        
        # Apply subscription discount
        if user_id and db:
            subscription_discount = self._get_subscription_discount(db, user_id)
            if subscription_discount > 0:
                discount_amount += base_amount * Decimal(str(subscription_discount / 100))
                discount_details["subscription"] = {
                    "type": "percentage",
                    "value": subscription_discount,
                    "amount": float(base_amount * Decimal(str(subscription_discount / 100)))
                }
        
        # Apply coupon discount
        if coupon_code:
            coupon_result = self._apply_coupon(
                coupon_code=coupon_code,
                order_amount=float(base_amount),
                user_id=user_id,
                db=db
            )
            
            if coupon_result["valid"]:
                coupon_discount = Decimal(str(coupon_result["discount_amount"]))
                discount_amount += coupon_discount
                discount_details["coupon"] = {
                    "code": coupon_code,
                    "type": coupon_result["discount_type"],
                    "value": coupon_result["discount_value"],
                    "amount": coupon_result["discount_amount"]
                }
        
        # Calculate final amount
        subtotal = base_amount + gst_amount - discount_amount
        
        return {
            "base_amount": float(base_amount),
            "duration_hours": round(hours, 2),
            "gst_amount": float(gst_amount),
            "gst_rate": float(gst_rate),
            "discount_amount": float(discount_amount),
            "discount_details": discount_details,
            "subtotal": max(0, float(subtotal)),
            "total_amount": max(0, float(subtotal)),
            "currency": "INR"
        }
    
    def _apply_coupon(
        self,
        coupon_code: str,
        order_amount: float,
        user_id: Optional[str] = None,
        db: Optional[Session] = None
    ) -> Dict[str, Any]:
        """Apply and validate a coupon code."""
        coupon = self.coupons.get(coupon_code.upper())
        
        if not coupon:
            return {
                "valid": False,
                "error": "Invalid coupon code"
            }
        
        # Check minimum order amount
        if order_amount < coupon.min_order_amount:
            return {
                "valid": False,
                "error": f"Minimum order amount: ₹{coupon.min_order_amount}"
            }
        
        # Check validity period
        now = datetime.utcnow()
        if coupon.valid_from and now < coupon.valid_from:
            return {
                "valid": False,
                "error": "Coupon not yet valid"
            }
        
        if coupon.valid_until and now > coupon.valid_until:
            return {
                "valid": False,
                "error": "Coupon has expired"
            }
        
        # Check usage limit
        if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
            return {
                "valid": False,
                "error": "Coupon usage limit reached"
            }
        
        # Check first-time user restriction
        if coupon.first_time_only and user_id and db:
            rental_count = db.query(RentalSession).filter(
                RentalSession.user_id == user_id
            ).count()
            
            if rental_count > 0:
                return {
                    "valid": False,
                    "error": "This coupon is for first-time users only"
                }
        
        # Calculate discount
        if coupon.discount_type == "percentage":
            discount_amount = order_amount * (coupon.discount_value / 100)
            
            # Apply max discount limit
            if coupon.max_discount:
                discount_amount = min(discount_amount, coupon.max_discount)
        else:
            discount_amount = min(coupon.discount_value, order_amount)
        
        return {
            "valid": True,
            "discount_type": coupon.discount_type,
            "discount_value": coupon.discount_value,
            "discount_amount": round(discount_amount, 2)
        }
    
    def _get_subscription_discount(self, db: Session, user_id: str) -> float:
        """Get subscription discount for user."""
        # In production, check user's subscription from database
        # For now, return 0
        return 0
    
    def create_coupon(
        self,
        code: str,
        discount_type: str,
        discount_value: float,
        min_order_amount: float = 0,
        max_discount: float = None,
        valid_days: int = 30,
        usage_limit: int = None,
        first_time_only: bool = False
    ) -> Dict[str, Any]:
        """
        Create a new coupon code.
        
        Admin only.
        """
        if code.upper() in self.coupons:
            return {
                "success": False,
                "error": "Coupon code already exists"
            }
        
        valid_from = datetime.utcnow()
        valid_until = valid_from + timedelta(days=valid_days)
        
        coupon = Coupon(
            code=code.upper(),
            discount_type=discount_type,
            discount_value=discount_value,
            min_order_amount=min_order_amount,
            max_discount=max_discount,
            valid_from=valid_from,
            valid_until=valid_until,
            usage_limit=usage_limit,
            first_time_only=first_time_only
        )
        
        self.coupons[code.upper()] = coupon
        
        return {
            "success": True,
            "coupon_code": code.upper(),
            "discount_type": discount_type,
            "discount_value": discount_value,
            "valid_until": valid_until.isoformat()
        }
    
    def validate_coupon(
        self,
        coupon_code: str,
        order_amount: float,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Validate a coupon without applying it."""
        return self._apply_coupon(
            coupon_code=coupon_code,
            order_amount=order_amount,
            user_id=user_id
        )
    
    def get_available_coupons(self) -> List[Dict[str, Any]]:
        """Get list of available coupons."""
        coupons = []
        
        for code, coupon in self.coupons.items():
            # Check if coupon is still valid
            now = datetime.utcnow()
            
            if coupon.valid_from and now < coupon.valid_from:
                continue
            
            if coupon.valid_until and now > coupon.valid_until:
                continue
            
            if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                continue
            
            coupons.append({
                "code": code,
                "discount_type": coupon.discount_type,
                "discount_value": coupon.discount_value,
                "min_order_amount": coupon.min_order_amount,
                "max_discount": coupon.max_discount,
                "valid_until": coupon.valid_until.isoformat() if coupon.valid_until else None
            })
        
        return coupons
    
    def generate_referral_code(self) -> str:
        """Generate a unique referral code."""
        chars = string.ascii_uppercase + string.digits
        return ''.join(secrets.choice(chars) for _ in range(8))
    
    def calculate_referral_bonus(self, referral_code: str) -> Dict[str, Any]:
        """Calculate referral bonus for both parties."""
        # Both referrer and referee get ₹50 off
        return {
            "referrer_bonus": 50,
            "referee_bonus": 50,
            "bonus_type": "fixed",
            "valid_for_days": 30
        }


# Singleton instance
enhanced_billing_service = EnhancedBillingService()
