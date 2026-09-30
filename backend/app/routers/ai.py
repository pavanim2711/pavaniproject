"""AI router - Recommendations and demand predictions."""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.models.product import Product
from app.core.jwt import verify_access_token
from app.services.recommendation_service import recommendation_service

router = APIRouter(prefix="/ai", tags=["AI"])


class RecommendationRequest(BaseModel):
    """Request model for recommendations."""
    limit: int = Field(default=5, ge=1, le=20, description="Number of recommendations")
    category: Optional[str] = Field(None, description="Category filter")


class RecommendationResponse(BaseModel):
    """Response model for a single recommendation."""
    product_id: str
    product_name: str
    product_description: Optional[str]
    category: str
    price_per_hour: float
    image_url: Optional[str]
    rating: float
    affinity_score: float
    reason: str


class DemandPredictionRequest(BaseModel):
    """Request model for demand predictions."""
    product_id: Optional[str] = Field(None, description="Product ID for specific prediction")


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

@router.get("/recommendations", response_model=List[Dict[str, Any]])
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    token: str = None
):
    """Get personalized recommendations for a user."""
    if token:
        user = get_current_user(token, db)
        user_id = user.id
    else:
        # For MVP, return popular products for unauthenticated users
        user_id = None
    
    if user_id:
        # Get personalized recommendations
        recommendations = recommendation_service.get_recommendations(
            user_id=user_id,
            limit=request.limit,
            category=request.category
        )
    else:
        # Get popular products
        query = db.query(Product).filter(Product.is_available == True)
        
        if request.category:
            query = query.filter(Product.category == request.category)
        
        products = query.order_by(
            Product.popularity_score.desc(),
            Product.rental_count.desc()
        ).limit(request.limit).all()
        
        recommendations = []
        for product in products:
            recommendations.append({
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "category": product.category,
                    "price_per_hour": float(product.price_per_hour),
                    "image_url": product.image_url,
                    "rating": float(product.average_rating) if product.average_rating else 4.5
                },
                "affinity_score": 0.5,
                "reason": "Popular choice"
            })
    
    return recommendations


@router.get("/demand-predictions", response_model=Dict[str, Any])
async def get_demand_predictions(
    request: DemandPredictionRequest = None,
    db: Session = Depends(get_db),
    token: str = None
):
    """Get demand predictions for products."""
    if request and request.product_id:
        # Get prediction for specific product
        result = recommendation_service.get_demand_predictions(
            product_id=request.product_id
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["error"]
            )
        
        return result
    else:
        # Get predictions for all products
        return recommendation_service.get_demand_predictions()
