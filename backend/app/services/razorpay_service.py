"""Razorpay payment gateway integration for Indian market."""

import hmac
import hashlib
import secrets
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional

import razorpay
from sqlalchemy.orm import Session

from app.core.payment_config import payment_settings
from app.models.payment import Payment as PaymentModel


class RazorpayService:
    """Razorpay payment gateway service."""
    
    def __init__(self):
        self.client = None
        self.enabled = payment_settings.RAZORPAY_ENABLED
        
        if self.enabled and payment_settings.RAZORPAY_KEY_ID and payment_settings.RAZORPAY_KEY_SECRET:
            self.client = razorpay.Client(
                auth=(payment_settings.RAZORPAY_KEY_ID, payment_settings.RAZORPAY_KEY_SECRET)
            )
    
    def create_order(
        self,
        amount: float,
        currency: str = "INR",
        rental_id: str = None,
        user_id: str = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Create a Razorpay order.
        
        Args:
            amount: Amount in INR
            currency: Currency code (default INR)
            rental_id: Rental session ID
            user_id: User ID
            db: Database session
            
        Returns:
            Order details including order_id for frontend
        """
        if not self.enabled or not self.client:
            return self._create_mock_order(amount, rental_id, user_id, db)
        
        try:
            # Razorpay expects amount in paise (multiply by 100)
            amount_paise = int(amount * 100)
            
            # Create order
            order_data = {
                "amount": amount_paise,
                "currency": currency,
                "payment_capture": 1,  # Auto-capture
                "notes": {
                    "rental_id": rental_id,
                    "user_id": user_id
                }
            }
            
            order = self.client.order.create(data=order_data)
            
            # Create payment record
            payment = PaymentModel(
                rental_id=rental_id,
                transaction_id=order["id"],
                amount=Decimal(str(amount)),
                base_amount=Decimal(str(amount)) / (1 + Decimal(str(payment_settings.GST_RATE))),
                gst_amount=Decimal(str(amount)) * Decimal(str(payment_settings.GST_RATE)) / (1 + Decimal(str(payment_settings.GST_RATE))),
                status="pending",
                payment_method="razorpay",
                user_id=user_id
            )
            
            if db:
                db.add(payment)
                db.commit()
                db.refresh(payment)
            
            return {
                "success": True,
                "order_id": order["id"],
                "payment_id": payment.id if db else None,
                "amount": amount,
                "currency": currency,
                "key_id": payment_settings.RAZORPAY_KEY_ID,
                "provider": "razorpay"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create Razorpay order"
            }
    
    def verify_payment(
        self,
        order_id: str,
        payment_id: str,
        signature: str,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Verify Razorpay payment signature.
        
        Args:
            order_id: Razorpay order ID
            payment_id: Razorpay payment ID
            signature: Payment signature from Razorpay
            db: Database session
            
        Returns:
            Verification result
        """
        if not self.enabled or not self.client:
            return self._verify_mock_payment(order_id, payment_id, db)
        
        try:
            # Verify signature
            message = f"{order_id}|{payment_id}"
            expected_signature = hmac.new(
                payment_settings.RAZORPAY_KEY_SECRET.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            
            if not hmac.compare_digest(signature, expected_signature):
                return {
                    "success": False,
                    "message": "Invalid payment signature"
                }
            
            # Fetch payment details from Razorpay
            payment_details = self.client.payment.fetch(payment_id)
            
            # Update payment record
            if db:
                payment = db.query(PaymentModel).filter(
                    PaymentModel.transaction_id == order_id
                ).first()
                
                if payment:
                    payment.status = "completed"
                    payment.transaction_id = payment_id  # Update with actual payment ID
                    payment.completed_at = datetime.utcnow()
                    payment.invoice_url = payment_details.get("invoice_id", None)
                    db.commit()
                    db.refresh(payment)
            
            return {
                "success": True,
                "payment_id": payment_id,
                "order_id": order_id,
                "status": "completed",
                "payment_method": payment_details.get("method", "unknown"),
                "message": "Payment verified successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Payment verification failed"
            }
    
    def refund_payment(
        self,
        payment_id: str,
        amount: Optional[float] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Refund a payment.
        
        Args:
            payment_id: Razorpay payment ID
            amount: Amount to refund (None for full refund)
            db: Database session
            
        Returns:
            Refund details
        """
        if not self.enabled or not self.client:
            return self._mock_refund(payment_id, db)
        
        try:
            refund_data = {}
            if amount:
                refund_data["amount"] = int(amount * 100)  # Convert to paise
            
            refund = self.client.payment.refund(payment_id, refund_data)
            
            # Update payment record
            if db:
                payment = db.query(PaymentModel).filter(
                    PaymentModel.transaction_id == payment_id
                ).first()
                
                if payment:
                    payment.status = "refunded"
                    db.commit()
            
            return {
                "success": True,
                "refund_id": refund["id"],
                "payment_id": payment_id,
                "amount": refund.get("amount", 0) / 100,
                "status": "refunded",
                "message": "Refund processed successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Refund failed"
            }
    
    def get_payment_details(self, payment_id: str) -> Dict[str, Any]:
        """Fetch payment details from Razorpay."""
        if not self.enabled or not self.client:
            return {
                "success": False,
                "message": "Razorpay not configured"
            }
        
        try:
            payment = self.client.payment.fetch(payment_id)
            return {
                "success": True,
                "payment_id": payment["id"],
                "amount": payment["amount"] / 100,
                "currency": payment["currency"],
                "status": payment["status"],
                "method": payment["method"],
                "created_at": datetime.fromtimestamp(payment["created_at"]).isoformat()
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    # Mock methods for development/testing
    def _create_mock_order(self, amount: float, rental_id: str, user_id: str, db: Session) -> Dict[str, Any]:
        """Create mock order for testing."""
        order_id = f"order_{secrets.token_hex(8)}"
        
        payment = PaymentModel(
            rental_id=rental_id,
            transaction_id=order_id,
            amount=Decimal(str(amount)),
            base_amount=Decimal(str(amount)) / (1 + Decimal(str(payment_settings.GST_RATE))),
            gst_amount=Decimal(str(amount)) * Decimal(str(payment_settings.GST_RATE)) / (1 + Decimal(str(payment_settings.GST_RATE))),
            status="pending",
            payment_method="mock",
            user_id=user_id
        )
        
        if db:
            db.add(payment)
            db.commit()
            db.refresh(payment)
        
        return {
            "success": True,
            "order_id": order_id,
            "payment_id": payment.id if db else None,
            "amount": amount,
            "currency": "INR",
            "key_id": "mock_key_id",
            "provider": "mock",
            "mock_mode": True
        }
    
    def _verify_mock_payment(self, order_id: str, payment_id: str, db: Session) -> Dict[str, Any]:
        """Verify mock payment for testing."""
        if db:
            payment = db.query(PaymentModel).filter(
                PaymentModel.transaction_id == order_id
            ).first()
            
            if payment:
                payment.status = "completed"
                payment.transaction_id = payment_id
                payment.completed_at = datetime.utcnow()
                db.commit()
        
        return {
            "success": True,
            "payment_id": payment_id,
            "order_id": order_id,
            "status": "completed",
            "message": "Mock payment verified",
            "mock_mode": True
        }
    
    def _mock_refund(self, payment_id: str, db: Session) -> Dict[str, Any]:
        """Process mock refund for testing."""
        if db:
            payment = db.query(PaymentModel).filter(
                PaymentModel.transaction_id == payment_id
            ).first()
            
            if payment:
                payment.status = "refunded"
                db.commit()
        
        return {
            "success": True,
            "refund_id": f"refund_{secrets.token_hex(8)}",
            "payment_id": payment_id,
            "status": "refunded",
            "message": "Mock refund processed",
            "mock_mode": True
        }


# Singleton instance
razorpay_service = RazorpayService()
