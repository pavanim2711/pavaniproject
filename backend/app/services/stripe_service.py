"""Stripe payment gateway integration for international payments."""

import secrets
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional

import stripe
from sqlalchemy.orm import Session

from app.core.payment_config import payment_settings
from app.models.payment import Payment as PaymentModel


class StripeService:
    """Stripe payment gateway service."""
    
    def __init__(self):
        self.enabled = payment_settings.STRIPE_ENABLED
        
        if self.enabled and payment_settings.STRIPE_SECRET_KEY:
            stripe.api_key = payment_settings.STRIPE_SECRET_KEY
    
    def create_payment_intent(
        self,
        amount: float,
        currency: str = "inr",
        rental_id: str = None,
        user_id: str = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe payment intent.
        
        Args:
            amount: Amount in specified currency
            currency: Currency code (default inr)
            rental_id: Rental session ID
            user_id: User ID
            db: Database session
            
        Returns:
            Payment intent details including client_secret for frontend
        """
        if not self.enabled:
            return self._create_mock_payment_intent(amount, rental_id, user_id, db)
        
        try:
            # Stripe expects amount in smallest currency unit (paise for INR, cents for USD)
            amount_smallest = int(amount * 100)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_smallest,
                currency=currency,
                metadata={
                    "rental_id": rental_id,
                    "user_id": user_id
                },
                automatic_payment_methods={
                    "enabled": True
                }
            )
            
            # Create payment record
            payment = PaymentModel(
                rental_id=rental_id,
                transaction_id=intent["id"],
                amount=Decimal(str(amount)),
                base_amount=Decimal(str(amount)) / (1 + Decimal(str(payment_settings.GST_RATE))),
                gst_amount=Decimal(str(amount)) * Decimal(str(payment_settings.GST_RATE)) / (1 + Decimal(str(payment_settings.GST_RATE))),
                status="pending",
                payment_method="stripe",
                user_id=user_id
            )
            
            if db:
                db.add(payment)
                db.commit()
                db.refresh(payment)
            
            return {
                "success": True,
                "client_secret": intent["client_secret"],
                "payment_intent_id": intent["id"],
                "payment_id": payment.id if db else None,
                "amount": amount,
                "currency": currency,
                "publishable_key": payment_settings.STRIPE_PUBLISHABLE_KEY,
                "provider": "stripe"
            }
            
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create Stripe payment intent"
            }
    
    def confirm_payment(
        self,
        payment_intent_id: str,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Confirm Stripe payment.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            db: Database session
            
        Returns:
            Confirmation result
        """
        if not self.enabled:
            return self._confirm_mock_payment(payment_intent_id, db)
        
        try:
            # Retrieve payment intent
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            # Check if payment succeeded
            if intent["status"] != "succeeded":
                return {
                    "success": False,
                    "status": intent["status"],
                    "message": f"Payment status: {intent['status']}"
                }
            
            # Update payment record
            if db:
                payment = db.query(PaymentModel).filter(
                    PaymentModel.transaction_id == payment_intent_id
                ).first()
                
                if payment:
                    payment.status = "completed"
                    payment.completed_at = datetime.utcnow()
                    db.commit()
                    db.refresh(payment)
            
            return {
                "success": True,
                "payment_intent_id": payment_intent_id,
                "status": "completed",
                "amount": intent["amount"] / 100,
                "currency": intent["currency"].upper(),
                "message": "Payment confirmed successfully"
            }
            
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Payment confirmation failed"
            }
    
    def create_refund(
        self,
        payment_intent_id: str,
        amount: Optional[float] = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Create a refund for a payment.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            amount: Amount to refund (None for full refund)
            db: Database session
            
        Returns:
            Refund details
        """
        if not self.enabled:
            return self._mock_refund(payment_intent_id, db)
        
        try:
            refund_data = {"payment_intent": payment_intent_id}
            if amount:
                refund_data["amount"] = int(amount * 100)
            
            refund = stripe.Refund.create(**refund_data)
            
            # Update payment record
            if db:
                payment = db.query(PaymentModel).filter(
                    PaymentModel.transaction_id == payment_intent_id
                ).first()
                
                if payment:
                    payment.status = "refunded"
                    db.commit()
            
            return {
                "success": True,
                "refund_id": refund["id"],
                "payment_intent_id": payment_intent_id,
                "amount": refund["amount"] / 100,
                "status": refund["status"],
                "message": "Refund processed successfully"
            }
            
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Refund failed"
            }
    
    def handle_webhook(
        self,
        payload: bytes,
        sig_header: str,
        db: Session = None
    ) -> Dict[str, Any]:
        """
        Handle Stripe webhook events.
        
        Args:
            payload: Raw payload from Stripe
            sig_header: Stripe signature header
            db: Database session
            
        Returns:
            Webhook processing result
        """
        if not self.enabled or not payment_settings.STRIPE_WEBHOOK_SECRET:
            return {"success": False, "message": "Webhook not configured"}
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, payment_settings.STRIPE_WEBHOOK_SECRET
            )
            
            # Handle different event types
            if event["type"] == "payment_intent.succeeded":
                payment_intent = event["data"]["object"]
                
                if db:
                    payment = db.query(PaymentModel).filter(
                        PaymentModel.transaction_id == payment_intent["id"]
                    ).first()
                    
                    if payment:
                        payment.status = "completed"
                        payment.completed_at = datetime.utcnow()
                        db.commit()
                
                return {
                    "success": True,
                    "event": "payment_intent.succeeded",
                    "payment_intent_id": payment_intent["id"]
                }
            
            elif event["type"] == "payment_intent.payment_failed":
                payment_intent = event["data"]["object"]
                
                if db:
                    payment = db.query(PaymentModel).filter(
                        PaymentModel.transaction_id == payment_intent["id"]
                    ).first()
                    
                    if payment:
                        payment.status = "failed"
                        payment.failure_reason = payment_intent.get("last_payment_error", {}).get("message", "Unknown error")
                        db.commit()
                
                return {
                    "success": True,
                    "event": "payment_intent.payment_failed",
                    "payment_intent_id": payment_intent["id"]
                }
            
            return {"success": True, "event": event["type"]}
            
        except ValueError as e:
            return {"success": False, "error": "Invalid payload"}
        except stripe.error.SignatureVerificationError as e:
            return {"success": False, "error": "Invalid signature"}
    
    # Mock methods for development/testing
    def _create_mock_payment_intent(self, amount: float, rental_id: str, user_id: str, db: Session) -> Dict[str, Any]:
        """Create mock payment intent for testing."""
        intent_id = f"pi_{secrets.token_hex(12)}"
        
        payment = PaymentModel(
            rental_id=rental_id,
            transaction_id=intent_id,
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
            "client_secret": f"{intent_id}_secret_{secrets.token_hex(8)}",
            "payment_intent_id": intent_id,
            "payment_id": payment.id if db else None,
            "amount": amount,
            "currency": "inr",
            "publishable_key": "mock_publishable_key",
            "provider": "mock",
            "mock_mode": True
        }
    
    def _confirm_mock_payment(self, payment_intent_id: str, db: Session) -> Dict[str, Any]:
        """Confirm mock payment for testing."""
        if db:
            payment = db.query(PaymentModel).filter(
                PaymentModel.transaction_id == payment_intent_id
            ).first()
            
            if payment:
                payment.status = "completed"
                payment.completed_at = datetime.utcnow()
                db.commit()
        
        return {
            "success": True,
            "payment_intent_id": payment_intent_id,
            "status": "completed",
            "message": "Mock payment confirmed",
            "mock_mode": True
        }
    
    def _mock_refund(self, payment_intent_id: str, db: Session) -> Dict[str, Any]:
        """Process mock refund for testing."""
        if db:
            payment = db.query(PaymentModel).filter(
                PaymentModel.transaction_id == payment_intent_id
            ).first()
            
            if payment:
                payment.status = "refunded"
                db.commit()
        
        return {
            "success": True,
            "refund_id": f"re_{secrets.token_hex(12)}",
            "payment_intent_id": payment_intent_id,
            "status": "succeeded",
            "message": "Mock refund processed",
            "mock_mode": True
        }


# Singleton instance
stripe_service = StripeService()
