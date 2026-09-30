"""Rentals router - Rental session management with complete workflow."""
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List

from app.db.session import get_db
from app.models.user import User
from app.models.product import Product
from app.models.rental import RentalSession, Booking
from app.core.jwt import verify_access_token
from app.services.billing_service import billing_service
from app.services.inventory_service import inventory_service
from app.services.notification_integration import notification_integration

router = APIRouter(prefix="/rentals", tags=["Rentals"])


# Pydantic models
class RentalCreateRequest(BaseModel):
    """Request model for creating a rental."""
    product_id: str = Field(..., description="Product ID to rent")
    start_time: datetime = Field(..., description="Expected start time")
    estimated_hours: int = Field(default=1, ge=1, le=24, description="Estimated rental hours (1-24)")
    pickup_address: Optional[str] = Field(None, description="Pickup location address")
    delivery_address: Optional[str] = Field(None, description="Delivery location address")


class RentalCancelRequest(BaseModel):
    """Request model for cancelling a rental."""
    reason: Optional[str] = Field(None, description="Cancellation reason")
    cancel_by: str = Field(default="user", description="Who cancelled: user, admin, or system")


class RentalExtendRequest(BaseModel):
    """Request model for extending a rental."""
    additional_hours: int = Field(..., ge=1, le=24, description="Additional hours to extend")


class RentalResponse(BaseModel):
    """Response model for rental."""
    id: str
    product_id: str
    product_name: str
    status: str
    start_time: Optional[str]
    end_time: Optional[str]
    total_seconds: int
    total_amount: float
    hourly_rate: float
    estimated_cost: Optional[float]


class RentalStartRequest(BaseModel):
    """Request model for starting rental."""
    actual_start_time: Optional[datetime] = Field(None, description="Actual start time")


class RentalStopRequest(BaseModel):
    """Request model for stopping rental."""
    actual_end_time: Optional[datetime] = Field(None, description="Actual end time")


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


@router.post("/", response_model=RentalResponse, status_code=status.HTTP_201_CREATED)
async def create_rental(
    rental_in: RentalCreateRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    token: str = None
):
    """Create a new rental session."""
    if token:
        user = get_current_user(token, db)
    else:
        user = None
    
    product = db.query(Product).filter(Product.id == rental_in.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if not (50 <= float(product.price_per_hour) <= 500):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product price out of valid range"
        )
    
    # Check availability
    availability = inventory_service.check_availability(
        db=db,
        product_id=product.id,
        start_time=rental_in.start_time,
        quantity=1
    )
    
    if not availability["available"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=availability["reason"]
        )
    
    estimated_cost = billing_service.estimate_cost(
        product_id=rental_in.product_id,
        hours=rental_in.estimated_hours
    )
    
    rental = RentalSession(
        user_id=user.id if user else "anonymous",
        product_id=product.id,
        status="pending",
        start_time=rental_in.start_time,
        total_seconds=0,
        total_amount=Decimal(str(estimated_cost["cost_breakdown"]["total_amount"])),
        hourly_rate=Decimal(str(product.price_per_hour)),
        estimated_cost=Decimal(str(estimated_cost["cost_breakdown"]["total_amount"])),
        pickup_address=rental_in.pickup_address,
        delivery_address=rental_in.delivery_address
    )
    
    db.add(rental)
    db.commit()
    db.refresh(rental)
    
    # Reserve inventory
    inventory_service.reserve_inventory(
        db=db,
        product_id=product.id,
        rental_id=str(rental.id),
        quantity=1
    )
    
    # Send notification
    background_tasks.add_task(
        notification_integration.on_rental_created,
        db=db,
        rental=rental
    )
    
    return {
        "id": rental.id,
        "product_id": rental.product_id,
        "product_name": product.name,
        "status": rental.status,
        "start_time": rental.start_time.isoformat() if rental.start_time else None,
        "end_time": None,
        "total_seconds": 0,
        "total_amount": float(rental.total_amount),
        "hourly_rate": float(rental.hourly_rate),
        "estimated_cost": float(rental.estimated_cost)
    }


@router.get("/", response_model=List[RentalResponse])
async def list_user_rentals(
    db: Session = Depends(get_db),
    status_filter: Optional[str] = None,
    token: str = None
):
    """List rentals for the current user."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    query = db.query(RentalSession)
    
    if user_id:
        query = query.filter(RentalSession.user_id == user_id)
    
    if status_filter:
        query = query.filter(RentalSession.status == status_filter)
    
    rentals = query.order_by(RentalSession.created_at.desc()).all()
    
    result = []
    for rental in rentals:
        product_name = rental.product.name if rental.product else "Unknown"
        
        result.append({
            "id": rental.id,
            "product_id": rental.product_id,
            "product_name": product_name,
            "status": rental.status,
            "start_time": rental.start_time.isoformat() if rental.start_time else None,
            "end_time": rental.end_time.isoformat() if rental.end_time else None,
            "total_seconds": rental.total_seconds,
            "total_amount": float(rental.total_amount),
            "hourly_rate": float(rental.hourly_rate),
            "estimated_cost": float(rental.estimated_cost) if rental.estimated_cost else None
        })
    
    return result


@router.get("/{rental_id}", response_model=RentalResponse)
async def get_rental(
    rental_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Get rental details by ID."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental not found"
        )
    
    if user_id and rental.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this rental"
        )
    
    product_name = rental.product.name if rental.product else "Unknown"
    
    return {
        "id": rental.id,
        "product_id": rental.product_id,
        "product_name": product_name,
        "status": rental.status,
        "start_time": rental.start_time.isoformat() if rental.start_time else None,
        "end_time": rental.end_time.isoformat() if rental.end_time else None,
        "total_seconds": rental.total_seconds,
        "total_amount": float(rental.total_amount),
        "hourly_rate": float(rental.hourly_rate),
        "estimated_cost": float(rental.estimated_cost) if rental.estimated_cost else None
    }


@router.post("/{rental_id}/start", response_model=RentalResponse)
async def start_rental(
    rental_id: str,
    rental_start: RentalStartRequest = None,
    db: Session = Depends(get_db),
    token: str = None
):
    """Start a rental session timer."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental not found"
        )
    
    if user_id and rental.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to start this rental"
        )
    
    if rental.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rental must be pending to start. Current status: {rental.status}"
        )
    
    start_time = rental_start.actual_start_time if rental_start else datetime.utcnow()
    rental.start_time = start_time
    rental.status = "active"
    
    db.commit()
    db.refresh(rental)
    
    product_name = rental.product.name if rental.product else "Unknown"
    
    return {
        "id": rental.id,
        "product_id": rental.product_id,
        "product_name": product_name,
        "status": rental.status,
        "start_time": rental.start_time.isoformat(),
        "end_time": None,
        "total_seconds": 0,
        "total_amount": float(rental.total_amount),
        "hourly_rate": float(rental.hourly_rate),
        "estimated_cost": float(rental.estimated_cost) if rental.estimated_cost else None
    }


@router.post("/{rental_id}/stop", response_model=RentalResponse)
async def stop_rental(
    rental_id: str,
    rental_stop: RentalStopRequest = None,
    db: Session = Depends(get_db),
    token: str = None
):
    """Stop a rental session timer (pickup request)."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental not found"
        )
    
    if user_id and rental.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to stop this rental"
        )
    
    if rental.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rental must be active to stop. Current status: {rental.status}"
        )
    
    end_time = rental_stop.actual_end_time if rental_stop else datetime.utcnow()
    rental.end_time = end_time
    
    billing = billing_service.calculate_rental_cost(
        hourly_rate=float(rental.hourly_rate),
        start_time=rental.start_time,
        end_time=rental.end_time
    )
    
    rental.total_seconds = billing["total_seconds"]
    rental.total_amount = Decimal(str(billing["total_amount"]))
    rental.status = "completed"
    
    db.commit()
    db.refresh(rental)
    
    product_name = rental.product.name if rental.product else "Unknown"
    
    return {
        "id": rental.id,
        "product_id": rental.product_id,
        "product_name": product_name,
        "status": rental.status,
        "start_time": rental.start_time.isoformat() if rental.start_time else None,
        "end_time": rental.end_time.isoformat() if rental.end_time else None,
        "total_seconds": rental.total_seconds,
        "total_amount": float(rental.total_amount),
        "hourly_rate": float(rental.hourly_rate),
        "estimated_cost": float(rental.estimated_cost) if rental.estimated_cost else None
    }


@router.post("/{rental_id}/complete", response_model=RentalResponse)
async def complete_rental(
    rental_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Complete rental and generate invoice."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        user_id = None
    
    rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
    if not rental:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rental not found"
        )
    
    if user_id and rental.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to complete this rental"
        )
    
    invoice = billing_service.process_rental_completion(rental_id)
    
    db.refresh(rental)
    
    product_name = rental.product.name if rental.product else "Unknown"
    
    return {
        "id": rental.id,
        "product_id": rental.product_id,
        "product_name": product_name,
        "status": rental.status,
        "start_time": rental.start_time.isoformat() if rental.start_time else None,
        "end_time": rental.end_time.isoformat() if rental.end_time else None,
        "total_seconds": rental.total_seconds,
        "total_amount": float(rental.total_amount),
        "hourly_rate": float(rental.hourly_rate),
        "estimated_cost": float(rental.estimated_cost) if rental.estimated_cost else None,
        "invoice": invoice
    }
