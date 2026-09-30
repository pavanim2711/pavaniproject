"""Billing service for rental calculations."""
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from app.models.rental import RentalSession
from app.models.product import Product
from app.models.user import User
from app.db.session import SessionLocal


class BillingService:
    """Service for calculating rental charges and generating invoices."""
    
    MIN_RENTAL_HOURS = 1
    GST_RATE = Decimal("0.18")  # 18% GST
    
    @staticmethod
    def calculate_rental_cost(
        hourly_rate: float,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        min_hours: int = 1
    ) -> dict:
        """
        Calculate rental cost with minimum 1-hour charge and round up to nearest hour.
        
        Args:
            hourly_rate: Hourly rate in rupees
            start_time: Rental start time
            end_time: Rental end time (current time if None)
            min_hours: Minimum rental hours (default: 1)
            
        Returns:
            Dictionary with billing details
        """
        if end_time is None:
            end_time = datetime.utcnow()
        
        # Calculate duration
        duration = end_time - start_time
        total_seconds = max(0, int(duration.total_seconds()))
        
        # Calculate hours (round up to nearest hour, minimum 1 hour)
        if total_seconds == 0:
            billed_hours = min_hours
        else:
            # Round up to nearest hour
            billed_hours = (total_seconds + 3599) // 3600  # ceil(total_seconds / 3600)
            billed_hours = max(min_hours, billed_hours)
        
        # Calculate amounts
        base_amount = Decimal(str(hourly_rate)) * Decimal(str(billed_hours))
        gst_amount = base_amount * BillingService.GST_RATE
        total_amount = base_amount + gst_amount
        
        # Round to 2 decimal places
        base_amount = base_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        gst_amount = gst_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        total_amount = total_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        return {
            "hourly_rate": float(hourly_rate),
            "total_seconds": total_seconds,
            "billed_hours": billed_hours,
            "base_amount": float(base_amount),
            "gst_amount": float(gst_amount),
            "total_amount": float(total_amount)
        }
    
    def process_rental_completion(self, rental_id: str) -> dict:
        """
        Complete a rental session and generate invoice.
        
        Args:
            rental_id: Rental session ID
            
        Returns:
            Invoice details
        """
        db = SessionLocal()
        try:
            # Get rental session
            rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
            if not rental:
                raise ValueError(f"Rental session not found: {rental_id}")
            
            if rental.status != "active":
                raise ValueError(f"Rental must be active to complete. Current status: {rental.status}")
            
            # Set end time
            rental.end_time = datetime.utcnow()
            
            # Calculate cost
            billing = self.calculate_rental_cost(
                hourly_rate=float(rental.hourly_rate),
                start_time=rental.start_time,
                end_time=rental.end_time
            )
            
            # Update rental
            rental.total_seconds = billing["total_seconds"]
            rental.total_amount = Decimal(str(billing["total_amount"]))
            rental.status = "completed"
            
            db.commit()
            db.refresh(rental)
            
            # Generate invoice
            invoice = self.generate_invoice(rental, billing)
            
            return invoice
            
        finally:
            db.close()
    
    def generate_invoice(self, rental: RentalSession, billing: dict) -> dict:
        """Generate invoice for completed rental."""
        return {
            "invoice_id": f"INV-{rental.id[:8].upper()}",
            "rental_id": rental.id,
            "booking_id": rental.booking_id,
            "user": {
                "id": rental.user.id,
                "name": rental.user.name,
                "email": rental.user.email
            },
            "product": {
                "id": rental.product.id,
                "name": rental.product.name,
                "category": rental.product.category
            },
            "billing": {
                "start_time": rental.start_time.isoformat() if rental.start_time else None,
                "end_time": rental.end_time.isoformat() if rental.end_time else None,
                "total_seconds": billing["total_seconds"],
                "billed_hours": billing["billed_hours"],
                "hourly_rate": billing["hourly_rate"]
            },
            "amounts": {
                "base_amount": billing["base_amount"],
                "gst_rate": 18,
                "gst_amount": billing["gst_amount"],
                "total_amount": billing["total_amount"]
            },
            "status": rental.status,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    def estimate_cost(self, product_id: str, hours: int) -> dict:
        """
        Estimate rental cost for a product.
        
        Args:
            product_id: Product ID
            hours: Estimated rental hours
            
        Returns:
            Cost estimation details
        """
        db = SessionLocal()
        try:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                raise ValueError(f"Product not found: {product_id}")
            
            hourly_rate = float(product.price_per_hour)
            
            # Apply minimum hours constraint
            effective_hours = max(self.MIN_RENTAL_HOURS, hours)
            
            # Calculate estimated cost
            base_amount = Decimal(str(hourly_rate)) * Decimal(str(effective_hours))
            gst_amount = base_amount * self.GST_RATE
            total_amount = base_amount + gst_amount
            
            # Round to 2 decimal places
            base_amount = float(base_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            gst_amount = float(gst_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            total_amount = float(total_amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
            
            return {
                "product_id": product_id,
                "product_name": product.name,
                "hourly_rate": hourly_rate,
                "estimated_hours": effective_hours,
                "cost_breakdown": {
                    "base_amount": base_amount,
                    "gst_rate": 18,
                    "gst_amount": gst_amount,
                    "total_amount": total_amount
                }
            }
        finally:
            db.close()


# Singleton instance
billing_service = BillingService()
