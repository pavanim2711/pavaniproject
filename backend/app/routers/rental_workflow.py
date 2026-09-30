"""Rental Workflow router - Cancellation, completion, and extension."""

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.db.session import get_db
from app.models.user import User
from app.core.jwt import verify_access_token
from app.services.rental_workflow_service import rental_workflow_service

router = APIRouter(prefix="/rentals", tags=["Rental Workflow"])


class CancelRentalRequest(BaseModel):
    """Request model for cancelling a rental."""
    reason: Optional[str] = Field(None, description="Cancellation reason")


class ExtendRentalRequest(BaseModel):
    """Request model for extending a rental."""
    additional_hours: int = Field(..., ge=1, le=24, description="Hours to extend")


class DamageReportRequest(BaseModel):
    """Request model for reporting damage."""
    description: str = Field(..., description="Damage description")
    estimated_amount: float = Field(..., ge=0, description="Estimated damage cost")


def get_current_user(token: str, db: Session) -> User:
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


@router.post("/{rental_id}/cancel")
async def cancel_rental(
    rental_id: str,
    cancel_request: CancelRentalRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Cancel a rental session.
    
    - Pending rentals: No cancellation fee
    - Confirmed rentals: 10% cancellation fee
    - Active rentals: 25% fee + charges for time used
    
    Refund will be processed automatically.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    result = await rental_workflow_service.cancel_rental(
        db=db,
        rental_id=rental_id,
        cancelled_by=str(user.id),
        reason=cancel_request.reason
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Cancellation failed")
        )
    
    return result


@router.post("/{rental_id}/complete")
async def complete_rental(
    rental_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Complete a rental session.
    
    Calculates final billing including:
    - Hourly charges
    - Late fees (if applicable)
    - Updates product rental count
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    result = await rental_workflow_service.complete_rental(
        db=db,
        rental_id=rental_id
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Completion failed")
        )
    
    return result


@router.post("/{rental_id}/extend")
async def extend_rental(
    rental_id: str,
    extend_request: ExtendRentalRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Extend an active rental.
    
    Checks product availability for the extended period.
    Additional charges apply for the extension.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    result = await rental_workflow_service.extend_rental(
        db=db,
        rental_id=rental_id,
        additional_hours=extend_request.additional_hours
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Extension failed")
        )
    
    return result


@router.post("/{rental_id}/report-damage")
async def report_damage(
    rental_id: str,
    damage_request: DamageReportRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Report product damage during rental.
    
    Admin only. Adds damage fee to rental total.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    if user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can report damage"
        )
    
    result = await rental_workflow_service.report_damage(
        db=db,
        rental_id=rental_id,
        damage_description=damage_request.description,
        damage_amount=damage_request.estimated_amount
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Damage report failed")
        )
    
    return result
