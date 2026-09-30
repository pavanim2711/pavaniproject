"""Recommendation service for personalized product suggestions."""
from typing import List, Dict, Any, Optional
from datetime import datetime
from decimal import Decimal

from app.db.session import SessionLocal
from app.models.product import Product
from app.models.user import User
from app.models.rental import RentalSession

class RecommendationService:
    """Rule-based recommendation service with affinity scores."""
    
    def __init__(self):
        self.affinity_scores: Dict[str, Dict[str, float]] = {}
    
    def get_user_affinity(self, user_id: str, product_id: str) -> float:
        """Calculate user affinity for a product based on history."""
        if user_id not in self.affinity_scores:
            self.affinity_scores[user_id] = {}
        
        if product_id in self.affinity_scores[user_id]:
            return self.affinity_scores[user_id][product_id]
        
        return 0.0
    
    def update_affinity(
        self,
        user_id: str,
        product_id: str,
        rental_hours: float,
        rating: float = 4.5
    ) -> None:
        """Update user affinity score for a product."""
        if user_id not in self.affinity_scores:
            self.affinity_scores[user_id] = {}
        
        base_score = min(rental_hours / 24.0, 1.0) * 0.5
        rating_boost = (rating / 5.0) * 0.3
        popularity_factor = 0.2
        
        current_score = self.affinity_scores[user_id].get(product_id, 0.0)
        new_score = current_score * 0.7 + (base_score + rating_boost + popularity_factor) * 0.3
        
        self.affinity_scores[user_id][product_id] = min(new_score, 1.0)
    
    def get_recommendations(
        self,
        user_id: str,
        limit: int = 5,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get personalized recommendations for a user."""
        db = SessionLocal()
        try:
            user_rentals = db.query(RentalSession).filter(
                RentalSession.user_id == user_id,
                RentalSession.status == "completed"
            ).all()
            
            user_categories = {}
            for rental in user_rentals:
                category_name = rental.product.category
                user_categories[category_name] = user_categories.get(category_name, 0) + 1
            
            preferred_category = None
            if user_categories:
                preferred_category = max(user_categories, key=user_categories.get)
            
            query = db.query(Product).filter(Product.is_available == True)
            
            if category:
                query = query.filter(Product.category == category)
            elif preferred_category:
                query = query.filter(Product.category == preferred_category)
            
            products = query.order_by(
                Product.popularity_score.desc(),
                Product.rental_count.desc()
            ).limit(limit * 2).all()
            
            recommendations = []
            for product in products:
                affinity = self.get_user_affinity(user_id, product.id)
                
                if preferred_category and product.category == preferred_category:
                    affinity += 0.2
                
                if affinity >= 0.3:
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
                        "affinity_score": round(affinity, 3),
                        "reason": f"Based on your interest in {product.category}"
                    })
                
                if len(recommendations) >= limit:
                    break
            
            if len(recommendations) < limit:
                remaining = limit - len(recommendations)
                fallback_products = db.query(Product).filter(
                    Product.is_available == True
                ).order_by(
                    Product.popularity_score.desc(),
                    Product.rental_count.desc()
                ).limit(remaining).all()
                
                for product in fallback_products:
                    if product.id not in [r["product"]["id"] for r in recommendations]:
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
            
        finally:
            db.close()
    
    def get_demand_predictions(self, product_id: Optional[str] = None) -> Dict[str, Any]:
        """Get demand predictions for products."""
        db = SessionLocal()
        try:
            if product_id:
                product = db.query(Product).filter(Product.id == product_id).first()
                
                if not product:
                    return {"error": "Product not found"}
                
                return {
                    "product_id": product.id,
                    "product_name": product.name,
                    "current_demand_score": float(product.popularity_score),
                    "rental_count": product.rental_count,
                    "predicted_demand": self._calculate_demand_trend(product),
                    "factors": {
                        "seasonal_factor": self._get_seasonal_factor(),
                        "day_of_week_factor": self._get_day_factor(),
                        "recent_trend": "increasing" if product.rental_count > 10 else "stable"
                    }
                }
            else:
                products = db.query(Product).filter(Product.is_available == True).all()
                
                predictions = []
                for product in products:
                    predictions.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "current_demand_score": float(product.popularity_score),
                        "predicted_demand": self._calculate_demand_trend(product),
                        "rental_count": product.rental_count,
                        "category": product.category
                    })
                
                return {
                    "predictions": predictions,
                    "total_products": len(predictions)
                }
        finally:
            db.close()
    
    def _calculate_demand_trend(self, product: Product) -> str:
        """Calculate demand trend based on rental count."""
        if product.rental_count > 50:
            return "high"
        elif product.rental_count > 20:
            return "moderate"
        elif product.rental_count > 5:
            return "low"
        else:
            return "very_low"
    
    def _get_seasonal_factor(self) -> float:
        """Get seasonal demand factor."""
        month = datetime.utcnow().month
        if month in [12, 1, 2]:
            return 1.1
        elif month in [3, 4, 5]:
            return 0.9
        elif month in [6, 7, 8]:
            return 1.0
        else:
            return 1.05
    
    def _get_day_factor(self) -> float:
        """Get day-of-week demand factor."""
        weekday = datetime.utcnow().weekday()
        if weekday >= 5:
            return 1.2
        else:
            return 0.8


recommendation_service = RecommendationService()
