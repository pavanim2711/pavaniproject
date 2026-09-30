"""Rental workflow service for managing rental lifecycle."""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from decimal import Decimal
import logging

from app.models.rental import RentalSession
from app.models.product import Product
from app.models.user import User
from app.services.billing_service import billing_service

logger = logging.getLogger(__name__)


class RentalWorkflowService:
    """Service for managing complete rental workflow."""
    
    # Cancellation fee percentages
    CANCELLATION_FEE_BEFORE_START = 10  # 10% if cancelled before start
    CANCELLATION_FEE_AFTER_START = 25   # 25% if cancelled after start
    
    # Late fee settings
    LATE_FEE_PER_HOUR = 50  # ₹50 per hour late
    LATE_FEE_GRACE_PERIOD = 30  # 30 minutes grace period
    
    async def cancel_rental(
        self,
        db: Session,
        rental_id: str,
        cancelled_by: str,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Cancel a rental session.
        
        Args:
            db: Database session
            rental_id: Rental ID to cancel
            cancelled_by: Who cancelled (user_id or 'system')
            reason: Cancellation reason
            
        Returns:
            Cancellation result with refund details
        """
        rental = db.query(RentalSession).filter(
            RentalSession.id == rental_id
        ).first()
        
        if not rental:
            return {
                "success": False,
                "error": "Rental not found"
            }
        
        # Check if rental can be cancelled
        if rental.status in ["completed", "cancelled"]:
            return {
                "success": False,
                "error": f"Cannot cancel rental with status: {rental.status}"
            }
        
        # Calculate cancellation fee
        cancellation_fee = self._calculate_cancellation_fee(rental)
        
        # Calculate refund amount
        total_paid = float(rental.total_amount or 0)
        refund_amount = max(0, total_paid - cancellation_fee)
        
        # Update rental status
        old_status = rental.status
        rental.status = "cancelled"
        rental.cancelled_at = datetime.utcnow()
        rental.cancelled_by = cancelled_by
        rental.cancellation_reason = reason
        rental.refund_amount = Decimal(str(refund_amount))
        
        # Update product stock
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        if product:
            product.stock_quantity = (product.stock_quantity or 0) + 1
        
        db.commit()
        db.refresh(rental)
        
        logger.info(f"Rental {rental_id} cancelled by {cancelled_by}. Refund: ₹{refund_amount}")
        
        return {
            "success": True,
            "rental_id": str(rental.id),
            "old_status": old_status,
            "new_status": "cancelled",
            "cancellation_fee": cancellation_fee,
            "refund_amount": refund_amount,
            "refund_status": "pending" if refund_amount > 0 else "not_applicable",
            "cancelled_at": rental.cancelled_at.isoformat()
        }
    
    def _calculate_cancellation_fee(self, rental: RentalSession) -> float:
        """Calculate cancellation fee based on rental status."""
        if rental.status == "pending":
            # No fee if cancelled before confirmation
            return 0
        
        if rental.status in ["confirmed", "payment_completed"]:
            # 10% fee if cancelled before start
            return float(rental.total_amount or 0) * (self.CANCELLATION_FEE_BEFORE_START / 100)
        
        if rental.status == "active":
            # 25% fee + charges for time used
            base_fee = float(rental.total_amount or 0) * (self.CANCELLATION_FEE_AFTER_START / 100)
            
            # Calculate charges for time used
            if rental.start_time:
                hours_used = (datetime.utcnow() - rental.start_time).total_seconds() / 3600
                time_charges = hours_used * float(rental.hourly_rate or 0)
                return base_fee + time_charges
            
            return base_fee
        
        return 0
    
    async def complete_rental(
        self,
        db: Session,
        rental_id: str,
        end_time: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Complete a rental session.
        
        Args:
            db: Database session
            rental_id: Rental ID
            end_time: Actual end time (default: now)
            
        Returns:
            Completion result with final billing
        """
        rental = db.query(RentalSession).filter(
            RentalSession.id == rental_id
        ).first()
        
        if not rental:
            return {
                "success": False,
                "error": "Rental not found"
            }
        
        if rental.status != "active":
            return {
                "success": False,
                "error": f"Cannot complete rental with status: {rental.status}"
            }
        
        end_time = end_time or datetime.utcnow()
        
        # Calculate final billing
        if rental.start_time:
            total_seconds = int((end_time - rental.start_time).total_seconds())
            hours = total_seconds / 3600
            
            billing = billing_service.calculate_rental_cost(
                hourly_rate=float(rental.hourly_rate),
                start_time=rental.start_time,
                end_time=end_time
            )
            
            # Check for late fees
            estimated_end = rental.start_time + timedelta(hours=rental.estimated_hours or 0)
            late_fee = 0
            
            if end_time > estimated_end:
                late_hours = (end_time - estimated_end).total_seconds() / 3600
                late_fee = self._calculate_late_fee(late_hours)
            
            rental.total_seconds = total_seconds
            rental.total_amount = Decimal(str(billing["total_amount"] + late_fee))
            rental.late_fee = Decimal(str(late_fee))
        
        # Update status
        rental.status = "completed"
        rental.end_time = end_time
        
        # Update product stock and rental count
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        if product:
            product.stock_quantity = (product.stock_quantity or 0) + 1
            product.rental_count = (product.rental_count or 0) + 1
        
        db.commit()
        db.refresh(rental)
        
        logger.info(f"Rental {rental_id} completed. Total: ₹{rental.total_amount}")
        
        return {
            "success": True,
            "rental_id": str(rental.id),
            "status": "completed",
            "total_seconds": rental.total_seconds,
            "total_amount": float(rental.total_amount),
            "late_fee": float(rental.late_fee or 0),
            "completed_at": rental.end_time.isoformat()
        }
    
    def _calculate_late_fee(self, late_hours: float) -> float:
        """Calculate late return fee."""
        # Apply grace period
        if late_hours * 60 <= self.LATE_FEE_GRACE_PERIOD:
            return 0
        
        return late_hours * self.LATE_FEE_PER_HOUR
    
    async def extend_rental(
        self,
        db: Session,
        rental_id: str,
        additional_hours: int
    ) -> Dict[str, Any]:
        """
        Extend a rental session.
        
        Args:
            db: Database session
            rental_id: Rental ID
            additional_hours: Hours to extend
            
        Returns:
            Extension result with updated billing
        """
        rental = db.query(RentalSession).filter(
            RentalSession.id == rental_id
        ).first()
        
        if not rental:
            return {
                "success": False,
                "error": "Rental not found"
            }
        
        if rental.status != "active":
            return {
                "success": False,
                "error": "Can only extend active rentals"
            }
        
        # Check product availability for extension
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }
        
        if product.stock_quantity and product.stock_quantity < 1:
            # Check if there's stock available for extension
            return {
                "success": False,
                "error": "Product not available for extension - booked by others"
            }
        
        # Calculate extension cost
        extension_cost = additional_hours * float(rental.hourly_rate)
        
        # Update rental
        rental.estimated_hours = (rental.estimated_hours or 0) + additional_hours
        rental.total_amount = (rental.total_amount or 0) + Decimal(str(extension_cost))
        
        db.commit()
        db.refresh(rental)
        
        logger.info(f"Rental {rental_id} extended by {additional_hours} hours. Additional cost: ₹{extension_cost}")
        
        return {
            "success": True,
            "rental_id": str(rental.id),
            "additional_hours": additional_hours,
            "extension_cost": extension_cost,
            "new_total_amount": float(rental.total_amount),
            "new_estimated_hours": rental.estimated_hours
        }
    
    async def report_damage(
        self,
        db: Session,
        rental_id: str,
        damage_description: str,
        damage_amount: float
    ) -> Dict[str, Any]:
        """
        Report product damage during rental.
        
        Args:
            db: Database session
            rental_id: Rental ID
            damage_description: Description of damage
            damage_amount: Estimated damage cost
            
        Returns:
            Damage report result
        """
        rental = db.query(RentalSession).filter(
            RentalSession.id == rental_id
        ).first()
        
        if not rental:
            return {
                "success": False,
                "error": "Rental not found"
            }
        
        # Add damage charge
        rental.damage_fee = Decimal(str(damage_amount))
        rental.damage_description = damage_description
        rental.total_amount = (rental.total_amount or 0) + rental.damage_fee
        
        db.commit()
        db.refresh(rental)
        
        logger.info(f"Damage reported for rental {rental_id}. Fee: ₹{damage_amount}")
        
        return {
            "success": True,
            "rental_id": str(rental.id),
            "damage_fee": float(rental.damage_fee),
            "new_total_amount": float(rental.total_amount),
            "message": "Damage reported and fee added to rental"
        }


# Singleton instance
rental_workflow_service = RentalWorkflowService()
