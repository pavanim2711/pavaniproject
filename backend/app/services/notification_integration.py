"""Integration module to send notifications from various services."""

from typing import Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session

from app.services.notification_service import notification_service
from app.models.rental import RentalSession
from app.models.product import Product
from app.models.user import User
from app.models.delivery import Delivery


class NotificationIntegration:
    """Helper class to send notifications for various events."""
    
    @staticmethod
    async def on_user_registered(user: User):
        """Send welcome notification on user registration."""
        await notification_service.send_registration_welcome(
            user_email=user.email,
            user_name=user.name
        )
    
    @staticmethod
    async def on_rental_created(db: Session, rental: RentalSession):
        """Send rental confirmation notification."""
        # Get user and product details
        user = db.query(User).filter(User.id == rental.user_id).first()
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        
        if not user or not product:
            return
        
        await notification_service.send_rental_confirmation(
            user_email=user.email,
            user_name=user.name,
            rental_id=str(rental.id),
            product_name=product.name,
            start_time=rental.start_time.strftime("%Y-%m-%d %H:%M") if rental.start_time else "Pending",
            hourly_rate=float(product.price_per_hour),
            delivery_address=rental.pickup_address or "To be confirmed"
        )
    
    @staticmethod
    async def on_rental_started(db: Session, rental: RentalSession):
        """Send notification when rental starts."""
        user = db.query(User).filter(User.id == rental.user_id).first()
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        
        if not user or not product:
            return
        
        # Send delivery update
        await notification_service.send_delivery_update(
            user_email=user.email,
            user_name=user.name,
            rental_id=str(rental.id),
            product_name=product.name,
            status="rental_started",
            delivery_partner_name="QuickTym Partner",
            delivery_partner_phone="+91-XXXX-XXXX",
            estimated_time="Product delivered and rental started"
        )
    
    @staticmethod
    async def on_rental_completed(db: Session, rental: RentalSession):
        """Send notification when rental completes."""
        user = db.query(User).filter(User.id == rental.user_id).first()
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        
        if not user or not product:
            return
        
        # Calculate duration
        duration_str = "N/A"
        if rental.total_seconds:
            hours = rental.total_seconds // 3600
            minutes = (rental.total_seconds % 3600) // 60
            duration_str = f"{hours}h {minutes}m"
        
        await notification_service.send_rental_completed(
            user_email=user.email,
            user_name=user.name,
            rental_id=str(rental.id),
            product_name=product.name,
            total_duration=duration_str,
            total_amount=float(rental.total_amount),
            payment_status="pending"
        )
    
    @staticmethod
    async def on_rental_cancelled(
        db: Session,
        rental: RentalSession,
        reason: Optional[str] = None
    ):
        """Send notification when rental is cancelled."""
        user = db.query(User).filter(User.id == rental.user_id).first()
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        
        if not user or not product:
            return
        
        await notification_service.send_rental_cancellation(
            user_email=user.email,
            user_name=user.name,
            rental_id=str(rental.id),
            product_name=product.name,
            reason=reason
        )
    
    @staticmethod
    async def on_delivery_assigned(db: Session, delivery: Delivery):
        """Send notification to delivery partner on new assignment."""
        partner = db.query(User).filter(User.id == delivery.delivery_partner_id).first()
        rental = db.query(RentalSession).filter(RentalSession.id == delivery.rental_id).first()
        
        if not partner or not rental:
            return
        
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        customer = db.query(User).filter(User.id == rental.user_id).first()
        
        if not product or not customer:
            return
        
        await notification_service.send_delivery_partner_assignment(
            partner_email=partner.email,
            partner_name=partner.name,
            delivery_id=str(delivery.id),
            product_name=product.name,
            customer_name=customer.name,
            pickup_address=delivery.pickup_address or "To be confirmed",
            delivery_address=delivery.delivery_address or "To be confirmed",
            contact_phone=customer.phone or "N/A"
        )
    
    @staticmethod
    async def on_delivery_status_update(
        db: Session,
        delivery: Delivery,
        status: str,
        estimated_time: Optional[str] = None
    ):
        """Send delivery status update to customer."""
        rental = db.query(RentalSession).filter(RentalSession.id == delivery.rental_id).first()
        
        if not rental:
            return
        
        user = db.query(User).filter(User.id == rental.user_id).first()
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        partner = db.query(User).filter(User.id == delivery.delivery_partner_id).first()
        
        if not user or not product or not partner:
            return
        
        await notification_service.send_delivery_update(
            user_email=user.email,
            user_name=user.name,
            rental_id=str(rental.id),
            product_name=product.name,
            status=status,
            delivery_partner_name=partner.name,
            delivery_partner_phone=partner.phone or "N/A",
            estimated_time=estimated_time
        )
    
    @staticmethod
    async def on_payment_success(
        db: Session,
        rental_id: str,
        amount: float,
        transaction_id: str,
        payment_method: str
    ):
        """Send payment success notification."""
        rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
        
        if not rental:
            return
        
        user = db.query(User).filter(User.id == rental.user_id).first()
        
        if not user:
            return
        
        await notification_service.send_payment_success(
            user_email=user.email,
            user_name=user.name,
            rental_id=rental_id,
            amount=amount,
            transaction_id=transaction_id,
            payment_method=payment_method
        )
    
    @staticmethod
    async def on_payment_failure(
        db: Session,
        rental_id: str,
        amount: float,
        failure_reason: str
    ):
        """Send payment failure notification."""
        rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
        
        if not rental:
            return
        
        user = db.query(User).filter(User.id == rental.user_id).first()
        
        if not user:
            return
        
        await notification_service.send_payment_failure(
            user_email=user.email,
            user_name=user.name,
            rental_id=rental_id,
            amount=amount,
            failure_reason=failure_reason
        )
    
    @staticmethod
    async def on_refund_processed(
        db: Session,
        rental_id: str,
        refund_amount: float,
        refund_id: str
    ):
        """Send refund confirmation."""
        rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
        
        if not rental:
            return
        
        user = db.query(User).filter(User.id == rental.user_id).first()
        
        if not user:
            return
        
        await notification_service.send_refund_processed(
            user_email=user.email,
            user_name=user.name,
            rental_id=rental_id,
            refund_amount=refund_amount,
            refund_id=refund_id
        )
    
    @staticmethod
    async def on_review_request(db: Session, rental_id: str):
        """Send review request after rental completion."""
        rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
        
        if not rental:
            return
        
        user = db.query(User).filter(User.id == rental.user_id).first()
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        
        if not user or not product:
            return
        
        await notification_service.send_review_request(
            user_email=user.email,
            user_name=user.name,
            rental_id=rental_id,
            product_name=product.name
        )
    
    @staticmethod
    async def send_pickup_reminder(db: Session, rental_id: str):
        """Send pickup reminder for long-running rental."""
        rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
        
        if not rental:
            return
        
        user = db.query(User).filter(User.id == rental.user_id).first()
        product = db.query(Product).filter(Product.id == rental.product_id).first()
        
        if not user or not product:
            return
        
        # Calculate duration
        if rental.start_time:
            duration_hours = (datetime.utcnow() - rental.start_time).total_seconds() / 3600
            current_cost = duration_hours * float(rental.hourly_rate)
        else:
            duration_hours = 0
            current_cost = 0
        
        await notification_service.send_pickup_reminder(
            user_email=user.email,
            user_name=user.name,
            rental_id=rental_id,
            product_name=product.name,
            duration_hours=duration_hours,
            current_cost=current_cost
        )


# Singleton instance
notification_integration = NotificationIntegration()
