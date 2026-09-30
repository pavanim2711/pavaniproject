"""AI Recommendations router - ML-powered product recommendations."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.core.jwt import verify_access_token
from app.services.ml_recommendation_engine import ml_recommendation_engine

router = APIRouter(prefix="/recommendations", tags=["AI Recommendations"])


class BehaviorLogRequest(BaseModel):
    """Request model for logging user behavior."""
    action_type: str = Field(..., description="Action type: view, search, rent, rate, click")
    product_id: Optional[str] = Field(None, description="Product ID (if applicable)")
    search_query: Optional[str] = Field(None, description="Search query (if applicable)")
    category_viewed: Optional[str] = Field(None, description="Category viewed")
    time_spent_seconds: Optional[int] = Field(None, description="Time spent on page")
    device_type: Optional[str] = Field(None, description="Device type: mobile, desktop, tablet")
    session_id: Optional[str] = Field(None, description="Session ID")


class RecommendationResponse(BaseModel):
    """Response model for recommendations."""
    product_id: str
    product_name: str
    category: str
    price_per_hour: float
    image_url: Optional[str]
    score: float
    recommendation_type: str
    reasons: Optional[List[str]] = None


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


@router.get("/hybrid", response_model=List[RecommendationResponse])
async def get_hybrid_recommendations(
    n_recommendations: int = Query(10, ge=1, le=50, description="Number of recommendations"),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get hybrid recommendations combining collaborative filtering,
    content-based filtering, and trending products.
    
    This is the main recommendation endpoint that provides the best
    personalized results.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    recommendations = await ml_recommendation_engine.get_hybrid_recommendations(
        db=db,
        user_id=str(user.id),
        n_recommendations=n_recommendations
    )
    
    return recommendations


@router.get("/collaborative", response_model=List[RecommendationResponse])
async def get_collaborative_recommendations(
    n_recommendations: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get recommendations based on collaborative filtering.
    
    Finds users with similar rental patterns and recommends
    products they have rented.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    recommendations = await ml_recommendation_engine.collaborative_filtering(
        db=db,
        user_id=str(user.id),
        n_recommendations=n_recommendations
    )
    
    return recommendations


@router.get("/content-based", response_model=List[RecommendationResponse])
async def get_content_based_recommendations(
    n_recommendations: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get recommendations based on content similarity.
    
    Recommends products similar to what the user has rented before,
    based on product features and descriptions.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    recommendations = await ml_recommendation_engine.content_based_filtering(
        db=db,
        user_id=str(user.id),
        n_recommendations=n_recommendations
    )
    
    return recommendations


@router.get("/trending", response_model=List[RecommendationResponse])
async def get_trending_recommendations(
    category: Optional[str] = Query(None, description="Filter by category"),
    time_window_days: int = Query(30, ge=1, le=365, description="Time window in days"),
    n_products: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get trending products based on recent rental activity.
    
    Returns products with highest rental activity in the specified
    time window.
    """
    recommendations = await ml_recommendation_engine.get_trending_products(
        db=db,
        category=category,
        time_window_days=time_window_days,
        n_products=n_products
    )
    
    return recommendations


@router.post("/behavior", status_code=status.HTTP_201_CREATED)
async def log_user_behavior(
    behavior_log: BehaviorLogRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Log user behavior for ML model training.
    
    Track user actions like views, searches, rentals, and ratings
    to improve recommendation quality.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    await ml_recommendation_engine.log_user_behavior(
        db=db,
        user_id=str(user.id),
        action_type=behavior_log.action_type,
        product_id=behavior_log.product_id,
        search_query=behavior_log.search_query,
        category_viewed=behavior_log.category_viewed,
        time_spent_seconds=behavior_log.time_spent_seconds,
        device_type=behavior_log.device_type,
        session_id=behavior_log.session_id
    )
    
    return {
        "success": True,
        "message": "Behavior logged successfully"
    }


@router.get("/similar/{product_id}", response_model=List[RecommendationResponse])
async def get_similar_products(
    product_id: str,
    n_products: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get products similar to a specific product.
    
    Uses content-based filtering to find products with similar
    features and descriptions.
    """
    from app.models.product import Product
    
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Get all products in same category
    similar_products = db.query(Product).filter(
        Product.category == product.category,
        Product.id != product_id,
        Product.is_available == True
    ).limit(n_products * 2).all()
    
    # Score based on price similarity and rating
    recommendations = []
    for p in similar_products:
        price_diff = abs(float(p.price_per_hour) - float(product.price_per_hour))
        price_score = max(0, 1 - (price_diff / 100))  # Normalize price difference
        
        rating_score = float(p.average_rating or 4.0) / 5.0
        
        combined_score = (price_score * 0.4) + (rating_score * 0.6)
        
        recommendations.append({
            "product_id": str(p.id),
            "product_name": p.name,
            "category": p.category,
            "price_per_hour": float(p.price_per_hour),
            "image_url": p.image_url,
            "score": round(combined_score, 3),
            "recommendation_type": "similar",
            "reasons": [f"Similar to {product.name}"]
        })
    
    # Sort by score and return top N
    recommendations.sort(key=lambda x: x["score"], reverse=True)
    
    return recommendations[:n_products]


@router.get("/category-preferences")
async def get_user_category_preferences(
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Get user's category preferences based on rental history.
    
    Returns categories the user has rented from most frequently.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    from app.models.rental import RentalSession
    from sqlalchemy import func
    
    # Get rental counts by category
    category_counts = db.query(
        Product.category,
        func.count(RentalSession.id).label('rental_count')
    ).join(
        RentalSession, Product.id == RentalSession.product_id
    ).filter(
        RentalSession.user_id == user.id
    ).group_by(
        Product.category
    ).order_by(
        func.count(RentalSession.id).desc()
    ).all()
    
    total_rentals = sum(count for _, count in category_counts)
    
    preferences = []
    for category, count in category_counts:
        preferences.append({
            "category": category,
            "rental_count": count,
            "percentage": round((count / total_rentals * 100), 1) if total_rentals > 0 else 0
        })
    
    return {
        "total_rentals": total_rentals,
        "preferences": preferences
    }
