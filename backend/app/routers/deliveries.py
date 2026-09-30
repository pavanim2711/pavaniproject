"""Deliveries router - Delivery management with geolocation."""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.models.rental import RentalSession
from app.models.delivery import Delivery
from app.core.jwt import verify_access_token
from app.services.delivery_assignment_service import delivery_assignment_service

router = APIRouter(prefix="/deliveries", tags=["Deliveries"])

class DeliveryCreateRequest(BaseModel):
    """Request model for creating a delivery."""
    rental_id: str = Field(..., description="Rental session ID")
    pickup_address: str = Field(..., description="Pickup location address")
    delivery_address: str = Field(..., description="Delivery location address")
    notes: Optional[str] = Field(None, description="Delivery notes")


class DeliveryUpdateRequest(BaseModel):
    """Request model for updating delivery status."""
    status: str = Field(..., description="New delivery status")


class PartnerLocationUpdate(BaseModel):
    """Request model for updating partner location."""
    latitude: float = Field(..., ge=-90, le=90, description="Current latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Current longitude")


class AssignDeliveryRequest(BaseModel):
    """Request model for manual delivery assignment."""
    partner_id: Optional[str] = Field(None, description="Partner ID to assign (None for auto-assign)")


class DeliveryResponse(BaseModel):
    """Response model for delivery."""
    id: str
    rental_id: str
    user_id: str
    status: str
    pickup_address: str
    delivery_address: str
    pickup_time: Optional[str]
    delivery_time: Optional[str]
    distance_km: Optional[float]
    partner_rating: Optional[float]
    delivery_fee: float
    notes: Optional[str]
    created_at: str


def get_current_user(token: str, db: Session):
    """Get current authenticated user from token."""
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.post("/", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
async def create_delivery(
    delivery_in: DeliveryCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    token: str = None
):
    """Create a new delivery assignment."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    rental = db.query(RentalSession).filter(RentalSession.id == delivery_in.rental_id).first()
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental session not found"
        )
    
    if user_id and rental.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create delivery for this rental"
        )
    
    delivery = Delivery(
        rental_id=rental.id,
        user_id=rental.user_id,
        status="pending",
        pickup_address=delivery_in.pickup_address,
        delivery_address=delivery_in.delivery_address,
        distance_km=Decimal("0.00"),
        partner_rating=Decimal("0.00"),
        delivery_fee=Decimal("0.00"),
        notes=delivery_in.notes
    )
    
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    
    # Auto-assign delivery in background
    background_tasks.add_task(
        delivery_assignment_service.assign_delivery,
        db=db,
        delivery_id=str(delivery.id),
        auto_assign=True
    )
    
    return {
        "id": delivery.id,
        "rental_id": delivery.rental_id,
        "user_id": delivery.user_id,
        "status": delivery.status,
        "pickup_address": delivery.pickup_address,
        "delivery_address": delivery.delivery_address,
        "pickup_time": None,
        "delivery_time": None,
        "distance_km": float(delivery.distance_km) if delivery.distance_km else None,
        "partner_rating": float(delivery.partner_rating) if delivery.partner_rating else None,
        "delivery_fee": float(delivery.delivery_fee),
        "notes": delivery.notes,
        "created_at": delivery.created_at.isoformat()
    }


@router.get("/", response_model=List[DeliveryResponse])
async def list_deliveries(
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None,
    token: str = None
):
    """List deliveries for the current user."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    query = db.query(Delivery)
    
    if user_id:
        query = query.filter(Delivery.user_id == user_id)
    
    if status_filter:
        query = query.filter(Delivery.status == status_filter)
    
    deliveries = query.order_by(Delivery.created_at.desc()).all()
    
    result = []
    for delivery in deliveries:
        result.append({
            "id": delivery.id,
            "rental_id": delivery.rental_id,
            "user_id": delivery.user_id,
            "status": delivery.status,
            "pickup_address": delivery.pickup_address,
            "delivery_address": delivery.delivery_address,
            "pickup_time": delivery.pickup_time.isoformat() if delivery.pickup_time else None,
            "delivery_time": delivery.delivery_time.isoformat() if delivery.delivery_time else None,
            "distance_km": float(delivery.distance_km) if delivery.distance_km else None,
            "partner_rating": float(delivery.partner_rating) if delivery.partner_rating else None,
            "delivery_fee": float(delivery.delivery_fee),
            "notes": delivery.notes,
            "created_at": delivery.created_at.isoformat()
        })
    
    return result


@router.get("/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery(
    delivery_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Get delivery details by ID."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Delivery not found"
        )
    
    if user_id and delivery.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this delivery"
        )
    
    return {
        "id": delivery.id,
        "rental_id": delivery.rental_id,
        "user_id": delivery.user_id,
        "status": delivery.status,
        "pickup_address": delivery.pickup_address,
        "delivery_address": delivery.delivery_address,
        "pickup_time": delivery.pickup_time.isoformat() if delivery.pickup_time else None,
        "delivery_time": delivery.delivery_time.isoformat() if delivery.delivery_time else None,
        "distance_km": float(delivery.distance_km) if delivery.distance_km else None,
        "partner_rating": float(delivery.partner_rating) if delivery.partner_rating else None,
        "delivery_fee": float(delivery.delivery_fee),
        "notes": delivery.notes,
        "created_at": delivery.created_at.isoformat()
    }


@router.patch("/{delivery_id}", response_model=DeliveryResponse)
async def update_delivery(
    delivery_id: str,
    delivery_update: DeliveryUpdateRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """Update delivery status (pending -> assigned -> in_transit -> delivered)."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
        partner_id = user_id if user.role == "Delivery_Partner" else None
    else:
        user_id = None
        partner_id = None
    
    # Use delivery assignment service for status update
    result = await delivery_assignment_service.update_delivery_status(
        db=db,
        delivery_id=delivery_id,
        new_status=delivery_update.status,
        partner_id=partner_id
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to update delivery status")
        )
    
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    
    return {
        "id": delivery.id,
        "rental_id": delivery.rental_id,
        "user_id": delivery.user_id,
        "status": delivery.status,
        "pickup_address": delivery.pickup_address,
        "delivery_address": delivery.delivery_address,
        "pickup_time": delivery.pickup_time.isoformat() if delivery.pickup_time else None,
        "delivery_time": delivery.delivery_time.isoformat() if delivery.delivery_time else None,
        "distance_km": float(delivery.distance_km) if delivery.distance_km else None,
        "partner_rating": float(delivery.partner_rating) if delivery.partner_rating else None,
        "delivery_fee": float(delivery.delivery_fee),
        "notes": delivery.notes,
        "created_at": delivery.created_at.isoformat()
    }


@router.post("/{delivery_id}/assign")
async def assign_delivery_partner(
    delivery_id: str,
    assign_request: AssignDeliveryRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Assign delivery to a partner.
    If partner_id is not provided, auto-assign to best available partner.
    """
    if token:
        user = get_current_user(token, db)
    
    result = await delivery_assignment_service.assign_delivery(
        db=db,
        delivery_id=delivery_id,
        auto_assign=(assign_request.partner_id is None)
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to assign delivery")
        )
    
    return result


@router.post("/partner/location")
async def update_partner_location(
    location_update: PartnerLocationUpdate,
    db: Session = Depends(get_db),
    token: str = None
):
    """Update delivery partner's current location."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    if user.role != "Delivery_Partner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only delivery partners can update location"
        )
    
    result = await delivery_assignment_service.update_partner_location(
        db=db,
        partner_id=str(user.id),
        latitude=location_update.latitude,
        longitude=location_update.longitude
    )
    
    return result


@router.get("/partner/active", response_model=List[Dict[str, Any]])
async def get_partner_active_deliveries(
    db: Session = Depends(get_db),
    token: str = None
):
    """Get all active deliveries for the authenticated delivery partner."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    if user.role != "Delivery_Partner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only delivery partners can access this endpoint"
        )
    
    deliveries = await delivery_assignment_service.get_partner_active_deliveries(
        db=db,
        partner_id=str(user.id)
    )
    
    return deliveries


@router.get("/{delivery_id}/eligible-partners")
async def get_eligible_partners(
    delivery_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Get list of eligible delivery partners for manual assignment."""
    if token:
        user = get_current_user(token, db)
    
    result = await delivery_assignment_service.assign_delivery(
        db=db,
        delivery_id=delivery_id,
        auto_assign=False
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to get eligible partners")
        )
    
    return result
