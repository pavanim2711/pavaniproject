"""Payment gateway configuration for multiple providers."""

from pydantic_settings import BaseSettings
from typing import Optional


class PaymentSettings(BaseSettings):
    """Payment gateway settings."""
    
    # Razorpay Configuration (India-focused)
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    RAZORPAY_WEBHOOK_SECRET: Optional[str] = None
    RAZORPAY_ENABLED: bool = False
    
    # Stripe Configuration (International)
    STRIPE_SECRET_KEY: Optional[str] = None
    STRIPE_PUBLISHABLE_KEY: Optional[str] = None
    STRIPE_WEBHOOK_SECRET: Optional[str] = None
    STRIPE_ENABLED: bool = False
    
    # General Payment Settings
    PAYMENT_CURRENCY: str = "INR"
    PAYMENT_PROVIDER: str = "razorpay"  # razorpay or stripe
    PAYMENT_MOCK_MODE: bool = True  # Set to False in production
    
    # Tax Settings
    GST_RATE: float = 0.18  # 18% GST
    CGST_RATE: float = 0.09  # 9% CGST
    SGST_RATE: float = 0.09  # 9% SGST
    
    # Payment Security
    OTP_REQUIRED_THRESHOLD: float = 5000.0  # OTP required for payments > ₹5000
    OTP_EXPIRY_MINUTES: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True


payment_settings = PaymentSettings()
