"""Payment processor for handling rental payments."""
import secrets
import random
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any

from app.db.session import SessionLocal
from app.models.payment import Payment as PaymentModel
from app.models.rental import RentalSession
from app.services.billing_service import billing_service


class PaymentProcessor:
    """Mock payment processor with 90% success rate and OTP verification."""
    
    SUCCESS_RATE = 0.9  # 90% success rate
    OTP_LENGTH = 6
    GST_RATE = Decimal("0.18")  # 18% GST
    
    def __init__(self):
        self.mock_database: Dict[str, Dict[str, Any]] = {}
    
    def generate_otp(self, rental_id: str, amount: float) -> str:
        """Generate OTP for payment verification."""
        otp = secrets.token_hex(3).upper()[:self.OTP_LENGTH]
        self.mock_database[rental_id] = {
            "otp": otp,
            "amount": amount,
            "expires_at": datetime.utcnow().timestamp() + 300  # 5 minutes
        }
        return otp
    
    def verify_otp(self, rental_id: str, otp: str) -> bool:
        """Verify OTP for payment."""
        if rental_id not in self.mock_database:
            return False
        
        record = self.mock_database[rental_id]
        
        # Check expiry
        if datetime.utcnow().timestamp() > record["expires_at"]:
            del self.mock_database[rental_id]
            return False
        
        # Check OTP match
        if otp != record["otp"]:
            return False
        
        # OTP verified, remove from database
        del self.mock_database[rental_id]
        return True
    
    def process_payment(
        self,
        rental_id: str,
        amount: float,
        user_id: str,
        payment_method: str = "upi"
    ) -> Dict[str, Any]:
        """
        Process payment with 90% success rate.
        
        Args:
            rental_id: Rental session ID
            amount: Payment amount
            user_id: User ID
            payment_method: Payment method (upi, card, netbanking)
            
        Returns:
            Payment result with transaction ID or error
        """
        # Check if OTP is required (amount > 5000)
        otp_required = amount > 5000
        
        # Simulate 90% success rate
        success = random.random() < self.SUCCESS_RATE
        
        # Generate transaction ID
        transaction_id = f"TXN{secrets.token_hex(8).upper()}"
        
        # Calculate GST
        base_amount = Decimal(str(amount)) / (Decimal("1") + self.GST_RATE)
        gst_amount = Decimal(str(amount)) - base_amount
        
        # Round to 2 decimal places
        base_amount = float(base_amount.quantize(Decimal("0.01")))
        gst_amount = float(gst_amount.quantize(Decimal("0.01")))
        
        # Create payment record
        db = SessionLocal()
        try:
            payment = PaymentModel(
                rental_id=rental_id,
                transaction_id=transaction_id,
                amount=amount,
                base_amount=base_amount,
                gst_amount=gst_amount,
                status="pending" if otp_required else "completed",
                payment_method=payment_method,
                user_id=user_id
            )
            
            db.add(payment)
            db.commit()
            db.refresh(payment)
            
            if otp_required:
                # Generate OTP and store
                otp = self.generate_otp(rental_id, amount)
                return {
                    "success": True,
                    "transaction_id": transaction_id,
                    "payment_id": payment.id,
                    "amount": amount,
                    "otp_required": True,
                    "otp": otp,  # For MVP only
                    "message": "OTP sent for verification",
                    "payment_status": "pending"
                }
            else:
                return {
                    "success": success,
                    "transaction_id": transaction_id,
                    "payment_id": payment.id,
                    "amount": amount,
                    "otp_required": False,
                    "message": "Payment processed successfully" if success else "Payment failed",
                    "payment_status": "completed" if success else "failed"
                }
        finally:
            db.close()
    
    def complete_payment(self, rental_id: str, otp: str) -> Dict[str, Any]:
        """Complete payment after OTP verification."""
        db = SessionLocal()
        try:
            # Verify OTP
            if not self.verify_otp(rental_id, otp):
                return {
                    "success": False,
                    "message": "Invalid or expired OTP"
                }
            
            # Find payment record
            payment = db.query(PaymentModel).filter(
                PaymentModel.rental_id == rental_id
            ).first()
            
            if not payment:
                return {
                    "success": False,
                    "message": "Payment record not found"
                }
            
            # Update payment status
            payment.status = "completed"
            payment.completed_at = datetime.utcnow()
            
            # Update rental status
            rental = db.query(RentalSession).filter(
                RentalSession.id == rental_id
            ).first()
            
            if rental:
                rental.status = "payment_completed"
            
            db.commit()
            
            # Get billing details
            billing = billing_service.calculate_rental_cost(
                hourly_rate=float(rental.hourly_rate),
                start_time=rental.start_time,
                end_time=rental.end_time
            )
            
            invoice = billing_service.generate_invoice(rental, billing)
            
            return {
                "success": True,
                "transaction_id": payment.transaction_id,
                "payment_id": payment.id,
                "message": "Payment verified and rental completed",
                "payment_status": "completed",
                "invoice": invoice
            }
        finally:
            db.close()
    
    def get_payment_status(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status by ID."""
        db = SessionLocal()
        try:
            payment = db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
            
            if not payment:
                return {
                    "success": False,
                    "message": "Payment not found"
                }
            
            return {
                "success": True,
                "payment_id": payment.id,
                "transaction_id": payment.transaction_id,
                "rental_id": payment.rental_id,
                "amount": payment.amount,
                "status": payment.status,
                "payment_method": payment.payment_method,
                "created_at": payment.created_at.isoformat() if payment.created_at else None,
                "completed_at": payment.completed_at.isoformat() if payment.completed_at else None
            }
        finally:
            db.close()


# Singleton instance
payment_processor = PaymentProcessor()
