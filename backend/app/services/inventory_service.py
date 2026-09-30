"""Inventory management service for product availability tracking."""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from decimal import Decimal
import logging

from app.models.product import Product
from app.models.rental import RentalSession
from app.models.inventory import InventoryLog

logger = logging.getLogger(__name__)


class InventoryService:
    """Service for managing product inventory and availability."""
    
    def check_availability(
        self,
        db: Session,
        product_id: str,
        start_time: datetime,
        end_time: Optional[datetime] = None,
        quantity: int = 1
    ) -> Dict[str, Any]:
        """
        Check if a product is available for a given time period.
        
        Args:
            db: Database session
            product_id: Product ID
            start_time: Rental start time
            end_time: Rental end time (optional)
            quantity: Number of units needed
            
        Returns:
            Availability status with details
        """
        # Get product
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            return {
                "available": False,
                "reason": "Product not found"
            }
        
        if not product.is_available:
            return {
                "available": False,
                "reason": "Product is currently unavailable"
            }
        
        # Check stock quantity
        if product.stock_quantity < quantity:
            return {
                "available": False,
                "reason": f"Insufficient stock. Available: {product.stock_quantity}, Requested: {quantity}"
            }
        
        # If no end time, check for current availability only
        if not end_time:
            # Check for any active rentals
            active_rentals = db.query(RentalSession).filter(
                RentalSession.product_id == product_id,
                RentalSession.status.in_(["pending", "active", "confirmed"]),
                RentalSession.start_time <= datetime.utcnow()
            ).count()
            
            available_quantity = product.stock_quantity - active_rentals
            
            if available_quantity < quantity:
                return {
                    "available": False,
                    "reason": f"Only {available_quantity} units available for immediate rental"
                }
            
            return {
                "available": True,
                "available_quantity": available_quantity,
                "total_quantity": product.stock_quantity
            }
        
        # Check for conflicting rentals in the time period
        conflicting_rentals = db.query(RentalSession).filter(
            RentalSession.product_id == product_id,
            RentalSession.status.in_(["pending", "active", "confirmed"]),
            or_(
                and_(
                    RentalSession.start_time <= start_time,
                    or_(RentalSession.end_time >= start_time, RentalSession.end_time == None)
                ),
                and_(
                    RentalSession.start_time >= start_time,
                    RentalSession.start_time <= end_time
                )
            )
        ).count()
        
        available_quantity = product.stock_quantity - conflicting_rentals
        
        if available_quantity < quantity:
            return {
                "available": False,
                "reason": f"Only {available_quantity} units available for the selected time period",
                "next_available": self._find_next_availability(db, product_id, start_time, end_time)
            }
        
        return {
            "available": True,
            "available_quantity": available_quantity,
            "total_quantity": product.stock_quantity,
            "conflicting_rentals": conflicting_rentals
        }
    
    def _find_next_availability(
        self,
        db: Session,
        product_id: str,
        start_time: datetime,
        end_time: datetime
    ) -> Optional[datetime]:
        """Find the next available time slot for a product."""
        # Look for rentals ending soon
        next_available = db.query(RentalSession).filter(
            RentalSession.product_id == product_id,
            RentalSession.status.in_(["active", "confirmed"]),
            RentalSession.end_time >= datetime.utcnow()
        ).order_by(RentalSession.end_time).first()
        
        if next_available and next_available.end_time:
            return next_available.end_time
        
        return None
    
    def reserve_inventory(
        self,
        db: Session,
        product_id: str,
        rental_id: str,
        quantity: int = 1
    ) -> Dict[str, Any]:
        """
        Reserve inventory for a rental.
        
        Args:
            db: Database session
            product_id: Product ID
            rental_id: Rental session ID
            quantity: Quantity to reserve
            
        Returns:
            Reservation result
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }
        
        # Check availability
        availability = self.check_availability(
            db=db,
            product_id=product_id,
            start_time=datetime.utcnow(),
            quantity=quantity
        )
        
        if not availability["available"]:
            return {
                "success": False,
                "error": availability["reason"]
            }
        
        # Log reservation
        log = InventoryLog(
            product_id=product_id,
            rental_id=rental_id,
            change_type="reserve",
            quantity_change=-quantity,
            previous_quantity=product.stock_quantity,
            new_quantity=product.stock_quantity,
            reason=f"Reserved for rental {rental_id}"
        )
        
        db.add(log)
        db.commit()
        
        return {
            "success": True,
            "reserved_quantity": quantity,
            "remaining_quantity": product.stock_quantity
        }
    
    def release_inventory(
        self,
        db: Session,
        product_id: str,
        rental_id: str,
        quantity: int = 1
    ) -> Dict[str, Any]:
        """
        Release reserved inventory when rental completes or is cancelled.
        
        Args:
            db: Database session
            product_id: Product ID
            rental_id: Rental session ID
            quantity: Quantity to release
            
        Returns:
            Release result
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }
        
        # Log release
        log = InventoryLog(
            product_id=product_id,
            rental_id=rental_id,
            change_type="release",
            quantity_change=quantity,
            previous_quantity=product.stock_quantity,
            new_quantity=product.stock_quantity,
            reason=f"Released from rental {rental_id}"
        )
        
        db.add(log)
        db.commit()
        
        return {
            "success": True,
            "released_quantity": quantity,
            "available_quantity": product.stock_quantity
        }
    
    def update_stock(
        self,
        db: Session,
        product_id: str,
        new_quantity: int,
        reason: str = "Manual update"
    ) -> Dict[str, Any]:
        """
        Update product stock quantity.
        
        Args:
            db: Database session
            product_id: Product ID
            new_quantity: New stock quantity
            reason: Reason for update
            
        Returns:
            Update result
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            return {
                "success": False,
                "error": "Product not found"
            }
        
        old_quantity = product.stock_quantity
        product.stock_quantity = new_quantity
        
        # Log update
        log = InventoryLog(
            product_id=product_id,
            change_type="update",
            quantity_change=new_quantity - old_quantity,
            previous_quantity=old_quantity,
            new_quantity=new_quantity,
            reason=reason
        )
        
        db.add(log)
        db.commit()
        
        return {
            "success": True,
            "previous_quantity": old_quantity,
            "new_quantity": new_quantity,
            "change": new_quantity - old_quantity
        }
    
    def get_inventory_logs(
        self,
        db: Session,
        product_id: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get inventory change logs.
        
        Args:
            db: Database session
            product_id: Filter by product ID (optional)
            limit: Maximum number of logs to return
            
        Returns:
            List of inventory logs
        """
        query = db.query(InventoryLog)
        
        if product_id:
            query = query.filter(InventoryLog.product_id == product_id)
        
        logs = query.order_by(InventoryLog.created_at.desc()).limit(limit).all()
        
        return [
            {
                "id": str(log.id),
                "product_id": str(log.product_id),
                "rental_id": str(log.rental_id) if log.rental_id else None,
                "change_type": log.change_type,
                "quantity_change": log.quantity_change,
                "previous_quantity": log.previous_quantity,
                "new_quantity": log.new_quantity,
                "reason": log.reason,
                "created_at": log.created_at.isoformat()
            }
            for log in logs
        ]
    
    def get_availability_calendar(
        self,
        db: Session,
        product_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """
        Get availability calendar for a product.
        
        Args:
            db: Database session
            product_id: Product ID
            start_date: Start date
            end_date: End date
            
        Returns:
            Calendar with availability for each day
        """
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            return {
                "error": "Product not found"
            }
        
        # Get all rentals in the period
        rentals = db.query(RentalSession).filter(
            RentalSession.product_id == product_id,
            RentalSession.status.in_(["pending", "active", "confirmed"]),
            or_(
                RentalSession.start_time.between(start_date, end_date),
                RentalSession.end_time.between(start_date, end_date),
                and_(
                    RentalSession.start_time <= start_date,
                    or_(RentalSession.end_time >= end_date, RentalSession.end_time == None)
                )
            )
        ).all()
        
        # Build calendar
        calendar = []
        current_date = start_date
        
        while current_date <= end_date:
            day_rentals = [
                r for r in rentals
                if r.start_time.date() <= current_date.date() <= (r.end_time.date() if r.end_time else datetime.max.date())
            ]
            
            booked_quantity = len(day_rentals)
            available_quantity = max(0, product.stock_quantity - booked_quantity)
            
            calendar.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "available": available_quantity > 0,
                "available_quantity": available_quantity,
                "booked_quantity": booked_quantity
            })
            
            current_date += timedelta(days=1)
        
        return {
            "product_id": product_id,
            "stock_quantity": product.stock_quantity,
            "calendar": calendar
        }
    
    def get_low_stock_alerts(
        self,
        db: Session,
        threshold: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Get products with low stock.
        
        Args:
            db: Database session
            threshold: Stock quantity threshold
            
        Returns:
            List of low stock products
        """
        low_stock_products = db.query(Product).filter(
            Product.stock_quantity <= threshold,
            Product.is_available == True
        ).all()
        
        return [
            {
                "product_id": str(p.id),
                "product_name": p.name,
                "current_stock": p.stock_quantity,
                "threshold": threshold,
                "category": p.category
            }
            for p in low_stock_products
        ]


# Singleton instance
inventory_service = InventoryService()
