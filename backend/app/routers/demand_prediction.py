"""Demand Prediction router - ML-based demand forecasting."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.core.jwt import verify_access_token
from app.services.demand_prediction_service import demand_prediction_service

router = APIRouter(prefix="/demand-prediction", tags=["Demand Prediction"])


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


# ==================== Prediction Endpoints ====================

@router.get("/product/{product_id}")
async def predict_product_demand(
    product_id: str,
    days: int = Query(7, ge=1, le=30, description="Number of days to predict"),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get demand prediction for a specific product.
    
    Returns daily demand predictions with confidence intervals.
    """
    if token:
        user = get_current_user(token, db)
    
    result = demand_prediction_service.predict_demand(
        db=db,
        product_id=product_id,
        prediction_days=days
    )
    
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=result.get("error", "Prediction failed")
        )
    
    return result


@router.get("/all")
async def predict_all_products_demand(
    days: int = Query(7, ge=1, le=30, description="Number of days to predict"),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get demand predictions for all products.
    
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
            detail="Admin access required"
        )
    
    result = demand_prediction_service.predict_all_products(
        db=db,
        prediction_days=days
    )
    
    return result


@router.get("/trends")
async def get_demand_trends(
    category: Optional[str] = Query(None, description="Filter by category"),
    days: int = Query(30, ge=7, le=90, description="Days to analyze"),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get demand trends over time.
    
    Shows daily rental patterns and weekday averages.
    """
    if token:
        user = get_current_user(token, db)
    
    result = demand_prediction_service.get_demand_trends(
        db=db,
        category=category,
        days=days
    )
    
    return result


@router.get("/forecast-report")
async def get_demand_forecast_report(
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get comprehensive demand forecast report.
    
    Includes high-demand products, potential stockouts, and recommendations.
    
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
            detail="Admin access required"
        )
    
    result = demand_prediction_service.get_demand_forecast_report(db=db)
    
    return result


@router.get("/seasonal-factors")
async def get_seasonal_factors():
    """
    Get seasonal demand factors for each month.
    
    Useful for planning inventory and promotions.
    """
    factors = {
        "January": 1.0,
        "February": 0.9,
        "March": 1.0,
        "April": 1.1,
        "May": 1.2,
        "June": 1.3,
        "July": 1.3,
        "August": 1.2,
        "September": 1.0,
        "October": 1.1,
        "November": 1.0,
        "December": 1.2
    }
    
    peak_months = ["June", "July", "December"]
    low_months = ["February"]
    
    return {
        "monthly_factors": factors,
        "peak_demand_months": peak_months,
        "low_demand_months": low_months,
        "explanation": {
            "summer_peak": "June-August see higher demand due to vacations and outdoor activities",
            "holiday_peak": "December sees increased rentals for holiday events",
            "low_season": "February typically has lower demand"
        }
    }
