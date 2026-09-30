"""Inventory router - Stock and availability management."""

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.models.product import Product
from app.services.inventory_service import inventory_service
from app.core.jwt import verify_access_token

router = APIRouter(prefix="/inventory", tags=["Inventory"])


# ==================== Request/Response Models ====================

class AvailabilityCheckRequest(BaseModel):
    """Request model for checking availability."""
    product_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    quantity: int = Field(default=1, ge=1)


class StockUpdateRequest(BaseModel):
    """Request model for updating stock."""
    quantity: int = Field(..., ge=0)
    reason: Optional[str] = None


class AvailabilityBlockRequest(BaseModel):
    """Request model for blocking availability."""
    product_id: str
    unavailable_start: datetime
    unavailable_end: Optional[datetime] = None
    reason: Optional[str] = None


# ==================== Helper Functions ====================

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


# ==================== Availability Endpoints ====================

@router.post("/check-availability")
async def check_product_availability(
    request: AvailabilityCheckRequest,
    db: Session = Depends(get_db)
):
    """
    Check if a product is available for a given time period.
    
    Returns availability status with details about stock and conflicting rentals.
    """
    result = inventory_service.check_availability(
        db=db,
        product_id=request.product_id,
        start_time=request.start_time,
        end_time=request.end_time,
        quantity=request.quantity
    )
    
    return result


@router.get("/{product_id}/calendar")
async def get_availability_calendar(
    product_id: str,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    days: int = Query(30, ge=1, le=90, description="Number of days to show"),
    db: Session = Depends(get_db)
):
    """
    Get availability calendar for a product.
    
    Shows day-by-day availability for the specified period.
    """
    # Parse dates
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d")
    else:
        start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d")
    else:
        end = start + timedelta(days=days)
    
    result = inventory_service.get_availability_calendar(
        db=db,
        product_id=product_id,
        start_date=start,
        end_date=end
    )
    
    return result


# ==================== Stock Management Endpoints ====================

@router.get("/{product_id}/stock")
async def get_product_stock(
    product_id: str,
    db: Session = Depends(get_db)
):
    """Get current stock information for a product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "stock_quantity": product.stock_quantity,
        "is_available": product.is_available
    }


@router.patch("/{product_id}/stock")
async def update_product_stock(
    product_id: str,
    update: StockUpdateRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Update product stock quantity.
    
    Admin only.
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
            detail="Only admins can update stock"
        )
    
    result = inventory_service.update_stock(
        db=db,
        product_id=product_id,
        new_quantity=update.quantity,
        reason=update.reason or "Manual update"
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("error", "Failed to update stock")
        )
    
    return result


@router.get("/low-stock-alerts")
async def get_low_stock_alerts(
    threshold: int = Query(3, ge=1, le=20, description="Stock threshold"),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get products with stock below threshold.
    
    Admin only.
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
            detail="Only admins can view stock alerts"
        )
    
    alerts = inventory_service.get_low_stock_alerts(db=db, threshold=threshold)
    
    return {
        "threshold": threshold,
        "alerts": alerts,
        "total_alerts": len(alerts)
    }


# ==================== Inventory Logs ====================

@router.get("/{product_id}/logs")
async def get_inventory_logs(
    product_id: str,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get inventory change logs for a product.
    
    Admin only.
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
            detail="Only admins can view inventory logs"
        )
    
    logs = inventory_service.get_inventory_logs(
        db=db,
        product_id=product_id,
        limit=limit
    )
    
    return {
        "product_id": product_id,
        "logs": logs,
        "total_logs": len(logs)
    }


@router.get("/logs/all")
async def get_all_inventory_logs(
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get all inventory change logs.
    
    Admin only.
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
            detail="Only admins can view inventory logs"
        )
    
    logs = inventory_service.get_inventory_logs(db=db, limit=limit)
    
    return {
        "logs": logs,
        "total_logs": len(logs)
    }


# ==================== Availability Blocking ====================

@router.post("/block")
async def block_product_availability(
    block: AvailabilityBlockRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Block product availability for maintenance or other reasons.
    
    Admin only.
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
            detail="Only admins can block availability"
        )
    
    from app.models.inventory import ProductAvailability
    
    availability_block = ProductAvailability(
        product_id=block.product_id,
        unavailable_start=block.unavailable_start,
        unavailable_end=block.unavailable_end,
        reason=block.reason
    )
    
    db.add(availability_block)
    db.commit()
    db.refresh(availability_block)
    
    return {
        "success": True,
        "block_id": str(availability_block.id),
        "product_id": block.product_id,
        "unavailable_start": block.unavailable_start.isoformat(),
        "unavailable_end": block.unavailable_end.isoformat() if block.unavailable_end else None
    }


@router.delete("/block/{block_id}")
async def remove_availability_block(
    block_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Remove an availability block."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    if user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can remove availability blocks"
        )
    
    from app.models.inventory import ProductAvailability
    
    block = db.query(ProductAvailability).filter(
        ProductAvailability.id == block_id
    ).first()
    
    if not block:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability block not found"
        )
    
    db.delete(block)
    db.commit()
    
    return {
        "success": True,
        "message": "Availability block removed"
    }
