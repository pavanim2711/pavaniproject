"""Intelligent delivery assignment service with geolocation."""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
import logging
import asyncio

from app.models.user import User
from app.models.delivery import Delivery
from app.models.rental import RentalSession
from app.services.geolocation_service import geolocation_service
from app.services.notification_integration import notification_integration

logger = logging.getLogger(__name__)


class DeliveryAssignmentService:
    """Service for intelligent delivery partner assignment."""
    
    # Configuration
    MAX_DELIVERY_RADIUS_KM = 15.0  # Maximum distance for assignment
    MAX_ACTIVE_DELIVERIES = 3      # Maximum concurrent deliveries per partner
    ASSIGNMENT_TIMEOUT_MINUTES = 10  # Time to accept assignment
    MIN_PARTNER_RATING = 3.5       # Minimum rating to receive assignments
    
    async def find_available_partners(
        self,
        db: Session,
        pickup_location: Tuple[float, float],
        delivery_location: Tuple[float, float],
        max_distance: float = MAX_DELIVERY_RADIUS_KM
    ) -> List[Dict[str, Any]]:
        """
        Find available delivery partners near pickup location.
        
        Args:
            db: Database session
            pickup_location: (lat, lon) of pickup
            delivery_location: (lat, lon) of delivery
            max_distance: Maximum distance from pickup in km
            
        Returns:
            List of eligible partners with distances and scores
        """
        # Query all active delivery partners
        partners = db.query(User).filter(
            User.role == "Delivery_Partner",
            User.is_active == True,
            User.current_deliveries < self.MAX_ACTIVE_DELIVERIES,
            or_(User.rating == None, User.rating >= self.MIN_PARTNER_RATING)
        ).all()
        
        eligible_partners = []
        
        for partner in partners:
            # Check if partner has location data
            if not partner.current_latitude or not partner.current_longitude:
                continue
            
            partner_location = (partner.current_latitude, partner.current_longitude)
            
            # Calculate distance to pickup
            distance_to_pickup = geolocation_service.calculate_distance(
                partner_location, pickup_location
            )
            
            # Skip if too far
            if distance_to_pickup > max_distance:
                continue
            
            # Calculate total delivery distance
            total_distance = geolocation_service.calculate_distance(
                pickup_location, delivery_location
            )
            
            # Calculate partner score (higher is better)
            score = self._calculate_partner_score(
                partner=partner,
                distance_to_pickup=distance_to_pickup,
                total_distance=total_distance
            )
            
            eligible_partners.append({
                "partner_id": str(partner.id),
                "name": partner.name,
                "phone": partner.phone,
                "rating": float(partner.rating) if partner.rating else 5.0,
                "total_deliveries": partner.total_deliveries or 0,
                "current_deliveries": partner.current_deliveries or 0,
                "distance_to_pickup": distance_to_pickup,
                "total_distance": total_distance,
                "score": score,
                "location": partner_location
            })
        
        # Sort by score (descending)
        eligible_partners.sort(key=lambda x: x["score"], reverse=True)
        
        return eligible_partners
    
    def _calculate_partner_score(
        self,
        partner: User,
        distance_to_pickup: float,
        total_distance: float
    ) -> float:
        """
        Calculate partner score for assignment priority.
        
        Higher score = better candidate
        
        Factors:
        - Rating (40% weight)
        - Proximity to pickup (30% weight)
        - Experience (20% weight)
        - Current workload (10% weight)
        """
        score = 0.0
        
        # Rating score (0-40 points)
        rating = float(partner.rating) if partner.rating else 5.0
        score += (rating / 5.0) * 40
        
        # Proximity score (0-30 points) - closer is better
        max_distance = self.MAX_DELIVERY_RADIUS_KM
        proximity_score = max(0, (max_distance - distance_to_pickup) / max_distance) * 30
        score += proximity_score
        
        # Experience score (0-20 points)
        total_deliveries = partner.total_deliveries or 0
        experience_score = min(total_deliveries / 100, 1.0) * 20
        score += experience_score
        
        # Workload score (0-10 points) - fewer current deliveries is better
        current_deliveries = partner.current_deliveries or 0
        workload_score = ((self.MAX_ACTIVE_DELIVERIES - current_deliveries) / 
                         self.MAX_ACTIVE_DELIVERIES) * 10
        score += workload_score
        
        return round(score, 2)
    
    async def assign_delivery(
        self,
        db: Session,
        delivery_id: str,
        auto_assign: bool = True
    ) -> Dict[str, Any]:
        """
        Assign a delivery to the best available partner.
        
        Args:
            db: Database session
            delivery_id: Delivery ID to assign
            auto_assign: If True, automatically assign to best partner
            
        Returns:
            Assignment result
        """
        # Get delivery details
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        
        if not delivery:
            return {
                "success": False,
                "error": "Delivery not found"
            }
        
        if delivery.status != "pending":
            return {
                "success": False,
                "error": f"Delivery already {delivery.status}"
            }
        
        # Geocode addresses
        pickup_coords = await geolocation_service.geocode_address(delivery.pickup_address)
        delivery_coords = await geolocation_service.geocode_address(delivery.delivery_address)
        
        if not pickup_coords or not delivery_coords:
            # Use default coordinates (Bangalore center)
            logger.warning(f"Could not geocode addresses for delivery {delivery_id}")
            pickup_coords = (12.9716, 77.5946)  # Default to Bangalore
            delivery_coords = (12.9716, 77.5946)
        
        # Find available partners
        eligible_partners = await self.find_available_partners(
            db=db,
            pickup_location=pickup_coords,
            delivery_location=delivery_coords
        )
        
        if not eligible_partners:
            return {
                "success": False,
                "error": "No available delivery partners in your area",
                "retry_after": 5  # minutes
            }
        
        # Calculate delivery distance and fee
        distance = geolocation_service.calculate_distance(pickup_coords, delivery_coords)
        fee = geolocation_service.calculate_delivery_fee(distance)
        
        # Update delivery with distance and fee
        delivery.distance_km = Decimal(str(distance))
        delivery.delivery_fee = Decimal(str(fee))
        
        if auto_assign:
            # Auto-assign to best partner
            best_partner = eligible_partners[0]
            
            delivery.delivery_partner_id = best_partner["partner_id"]
            delivery.status = "assigned"
            delivery.pickup_time = datetime.utcnow()
            
            # Update partner's current deliveries
            partner = db.query(User).filter(User.id == best_partner["partner_id"]).first()
            if partner:
                partner.current_deliveries = (partner.current_deliveries or 0) + 1
            
            db.commit()
            db.refresh(delivery)
            
            # Send notification to partner
            await notification_integration.on_delivery_assigned(db, delivery)
            
            # Send notification to customer
            await notification_integration.on_delivery_status_update(
                db=db,
                delivery=delivery,
                status="assigned",
                estimated_time=f"{geolocation_service.estimate_travel_time(distance)} minutes"
            )
            
            return {
                "success": True,
                "delivery_id": str(delivery.id),
                "partner": {
                    "id": best_partner["partner_id"],
                    "name": best_partner["name"],
                    "phone": best_partner["phone"],
                    "rating": best_partner["rating"]
                },
                "distance_km": distance,
                "delivery_fee": fee,
                "estimated_time_minutes": geolocation_service.estimate_travel_time(distance),
                "status": "assigned"
            }
        else:
            # Return list of eligible partners for manual selection
            return {
                "success": True,
                "auto_assign": False,
                "eligible_partners": eligible_partners[:5],  # Top 5 candidates
                "distance_km": distance,
                "delivery_fee": fee
            }
    
    async def update_partner_location(
        self,
        db: Session,
        partner_id: str,
        latitude: float,
        longitude: float
    ) -> Dict[str, Any]:
        """
        Update delivery partner's current location.
        
        Args:
            db: Database session
            partner_id: Partner's user ID
            latitude: Current latitude
            longitude: Current longitude
            
        Returns:
            Update result
        """
        partner = db.query(User).filter(User.id == partner_id).first()
        
        if not partner:
            return {
                "success": False,
                "error": "Partner not found"
            }
        
        partner.current_latitude = latitude
        partner.current_longitude = longitude
        partner.last_location_update = datetime.utcnow()
        
        db.commit()
        
        return {
            "success": True,
            "message": "Location updated",
            "coordinates": (latitude, longitude)
        }
    
    async def get_partner_active_deliveries(
        self,
        db: Session,
        partner_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get all active deliveries for a partner.
        
        Args:
            db: Database session
            partner_id: Partner's user ID
            
        Returns:
            List of active deliveries
        """
        deliveries = db.query(Delivery).filter(
            Delivery.delivery_partner_id == partner_id,
            Delivery.status.in_(["assigned", "in_transit"])
        ).all()
        
        result = []
        for delivery in deliveries:
            result.append({
                "delivery_id": str(delivery.id),
                "rental_id": str(delivery.rental_id),
                "status": delivery.status,
                "pickup_address": delivery.pickup_address,
                "delivery_address": delivery.delivery_address,
                "distance_km": float(delivery.distance_km) if delivery.distance_km else 0,
                "delivery_fee": float(delivery.delivery_fee),
                "pickup_time": delivery.pickup_time.isoformat() if delivery.pickup_time else None
            })
        
        return result
    
    async def update_delivery_status(
        self,
        db: Session,
        delivery_id: str,
        new_status: str,
        partner_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update delivery status with notifications.
        
        Args:
            db: Database session
            delivery_id: Delivery ID
            new_status: New status (assigned, in_transit, delivered, cancelled)
            partner_id: Partner ID (for verification)
            
        Returns:
            Update result
        """
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        
        if not delivery:
            return {
                "success": False,
                "error": "Delivery not found"
            }
        
        # Verify partner
        if partner_id and delivery.delivery_partner_id != partner_id:
            return {
                "success": False,
                "error": "Not authorized to update this delivery"
            }
        
        # Validate status transition
        valid_transitions = {
            "pending": ["assigned", "cancelled"],
            "assigned": ["in_transit", "cancelled"],
            "in_transit": ["delivered", "cancelled"],
            "delivered": [],
            "cancelled": []
        }
        
        if new_status not in valid_transitions.get(delivery.status, []):
            return {
                "success": False,
                "error": f"Invalid transition from {delivery.status} to {new_status}"
            }
        
        # Update status
        old_status = delivery.status
        delivery.status = new_status
        delivery.updated_at = datetime.utcnow()
        
        # Handle status-specific actions
        if new_status == "in_transit":
            delivery.pickup_time = datetime.utcnow()
        
        elif new_status == "delivered":
            delivery.delivery_time = datetime.utcnow()
            
            # Update partner stats
            partner = db.query(User).filter(User.id == delivery.delivery_partner_id).first()
            if partner:
                partner.total_deliveries = (partner.total_deliveries or 0) + 1
                partner.current_deliveries = max(0, (partner.current_deliveries or 0) - 1)
        
        elif new_status == "cancelled":
            # Update partner availability
            partner = db.query(User).filter(User.id == delivery.delivery_partner_id).first()
            if partner:
                partner.current_deliveries = max(0, (partner.current_deliveries or 0) - 1)
        
        db.commit()
        db.refresh(delivery)
        
        # Send notification
        estimated_time = None
        if new_status == "in_transit":
            estimated_time = f"{geolocation_service.estimate_travel_time(float(delivery.distance_km or 0))} minutes"
        
        await notification_integration.on_delivery_status_update(
            db=db,
            delivery=delivery,
            status=new_status,
            estimated_time=estimated_time
        )
        
        return {
            "success": True,
            "delivery_id": str(delivery.id),
            "old_status": old_status,
            "new_status": new_status,
            "updated_at": delivery.updated_at.isoformat()
        }


# Singleton instance
delivery_assignment_service = DeliveryAssignmentService()
