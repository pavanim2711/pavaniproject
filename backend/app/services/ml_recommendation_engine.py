"""Machine Learning-based recommendation engine."""

import json
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, desc
from collections import defaultdict
import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from app.models.product import Product
from app.models.user import User
from app.models.rental import RentalSession
from app.models.review import Review
from app.models.ai_models import AIRecommendation, UserBehaviorLog, ProductEmbedding

logger = logging.getLogger(__name__)


class MLRecommendationEngine:
    """Advanced ML-based recommendation system."""
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
        self.scaler = MinMaxScaler()
        
    # ==================== COLLABORATIVE FILTERING ====================
    
    async def collaborative_filtering(
        self,
        db: Session,
        user_id: str,
        n_recommendations: int = 10
    ) -> List[Dict[str, Any]]:
        """
        User-based collaborative filtering.
        Find similar users and recommend products they liked.
        
        Args:
            db: Database session
            user_id: Target user ID
            n_recommendations: Number of recommendations to return
            
        Returns:
            List of recommended products with scores
        """
        # Get all users who have rented products
        all_rentals = db.query(RentalSession).filter(
            RentalSession.status.in_(["completed", "active"])
        ).all()
        
        # Create user-item matrix
        user_items = defaultdict(lambda: defaultdict(float))
        item_users = defaultdict(set)
        
        for rental in all_rentals:
            user_items[rental.user_id][rental.product_id] += 1.0
            item_users[rental.product_id].add(rental.user_id)
        
        # If target user has no history, return empty
        if user_id not in user_items:
            return []
        
        # Calculate user similarity using cosine similarity
        target_user_items = user_items[user_id]
        similar_users = []
        
        for other_user_id, other_items in user_items.items():
            if other_user_id == user_id:
                continue
            
            # Find common products
            common_products = set(target_user_items.keys()) & set(other_items.keys())
            
            if len(common_products) == 0:
                continue
            
            # Calculate cosine similarity
            target_vector = [target_user_items[p] for p in common_products]
            other_vector = [other_items[p] for p in common_products]
            
            similarity = self._cosine_similarity(target_vector, other_vector)
            
            if similarity > 0.3:  # Threshold for similarity
                similar_users.append((other_user_id, similarity))
        
        # Sort by similarity
        similar_users.sort(key=lambda x: x[1], reverse=True)
        
        # Get products rented by similar users but not by target user
        recommendations = defaultdict(float)
        target_product_ids = set(target_user_items.keys())
        
        for similar_user_id, similarity in similar_users[:20]:  # Top 20 similar users
            for product_id, count in user_items[similar_user_id].items():
                if product_id not in target_product_ids:
                    recommendations[product_id] += similarity * count
        
        # Sort recommendations by score
        sorted_recommendations = sorted(
            recommendations.items(),
            key=lambda x: x[1],
            reverse=True
        )[:n_recommendations]
        
        # Fetch product details
        result = []
        for product_id, score in sorted_recommendations:
            product = db.query(Product).filter(Product.id == product_id).first()
            if product and product.is_available:
                result.append({
                    "product_id": str(product.id),
                    "product_name": product.name,
                    "category": product.category,
                    "price_per_hour": float(product.price_per_hour),
                    "image_url": product.image_url,
                    "score": round(score, 3),
                    "recommendation_type": "collaborative",
                    "reason": "Users with similar preferences also rented this"
                })
        
        return result
    
    # ==================== CONTENT-BASED FILTERING ====================
    
    async def content_based_filtering(
        self,
        db: Session,
        user_id: str,
        n_recommendations: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Content-based filtering using product features.
        Recommend products similar to what user has rented before.
        
        Args:
            db: Database session
            user_id: Target user ID
            n_recommendations: Number of recommendations
            
        Returns:
            List of recommended products
        """
        # Get user's rental history
        user_rentals = db.query(RentalSession).filter(
            RentalSession.user_id == user_id,
            RentalSession.status.in_(["completed", "active"])
        ).all()
        
        if not user_rentals:
            return []
        
        # Get products user has rented
        rented_product_ids = [r.product_id for r in user_rentals]
        rented_products = db.query(Product).filter(
            Product.id.in_(rented_product_ids)
        ).all()
        
        # Get all available products
        all_products = db.query(Product).filter(
            Product.is_available == True,
            ~Product.id.in_(rented_product_ids)
        ).all()
        
        if not all_products:
            return []
        
        # Create TF-IDF vectors for product descriptions
        all_products_with_rented = rented_products + all_products
        descriptions = [
            f"{p.name} {p.description} {p.category}"
            for p in all_products_with_rented
        ]
        
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(descriptions)
            
            # Calculate similarity between rented products and all products
            n_rented = len(rented_products)
            rented_vectors = tfidf_matrix[:n_rented]
            all_vectors = tfidf_matrix[n_rented:]
            
            # Average similarity across all rented products
            similarity_scores = np.mean(
                cosine_similarity(rented_vectors, all_vectors),
                axis=0
            )
            
            # Get top N recommendations
            top_indices = np.argsort(similarity_scores)[::-1][:n_recommendations]
            
            result = []
            for idx in top_indices:
                product = all_products[idx]
                result.append({
                    "product_id": str(product.id),
                    "product_name": product.name,
                    "category": product.category,
                    "price_per_hour": float(product.price_per_hour),
                    "image_url": product.image_url,
                    "score": round(float(similarity_scores[idx]), 3),
                    "recommendation_type": "content",
                    "reason": f"Similar to products you've rented before"
                })
            
            return result
            
        except Exception as e:
            logger.error(f"Content-based filtering error: {e}")
            return []
    
    # ==================== TRENDING & POPULARITY ====================
    
    async def get_trending_products(
        self,
        db: Session,
        category: Optional[str] = None,
        time_window_days: int = 30,
        n_products: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get trending products based on recent rental activity.
        
        Args:
            db: Database session
            category: Filter by category (optional)
            time_window_days: Time window for trend calculation
            n_products: Number of products to return
            
        Returns:
            List of trending products
        """
        # Calculate date threshold
        threshold_date = datetime.utcnow() - timedelta(days=time_window_days)
        
        # Query recent rentals
        query = db.query(
            RentalSession.product_id,
            func.count(RentalSession.id).label('rental_count'),
            func.avg(RentalSession.total_amount).label('avg_revenue')
        ).filter(
            RentalSession.created_at >= threshold_date,
            RentalSession.status.in_(["completed", "active"])
        ).group_by(RentalSession.product_id)
        
        rentals = query.order_by(desc('rental_count')).all()
        
        recommendations = []
        for product_id, rental_count, avg_revenue in rentals[:n_products * 2]:
            product = db.query(Product).filter(Product.id == product_id).first()
            
            if not product or not product.is_available:
                continue
            
            if category and product.category != category:
                continue
            
            # Calculate trending score
            trending_score = self._calculate_trending_score(
                rental_count=rental_count,
                avg_revenue=float(avg_revenue or 0),
                rating=float(product.average_rating or 4.0)
            )
            
            recommendations.append({
                "product_id": str(product.id),
                "product_name": product.name,
                "category": product.category,
                "price_per_hour": float(product.price_per_hour),
                "image_url": product.image_url,
                "score": round(trending_score, 3),
                "recommendation_type": "trending",
                "reason": f"Trending in {product.category}",
                "rental_count": rental_count
            })
            
            if len(recommendations) >= n_products:
                break
        
        return recommendations
    
    # ==================== HYBRID RECOMMENDATION ====================
    
    async def get_hybrid_recommendations(
        self,
        db: Session,
        user_id: str,
        n_recommendations: int = 10,
        weights: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Hybrid recommendation combining multiple strategies.
        
        Args:
            db: Database session
            user_id: Target user ID
            n_recommendations: Number of recommendations
            weights: Weights for different strategies (collaborative, content, trending)
            
        Returns:
            Combined and ranked recommendations
        """
        if weights is None:
            weights = {
                "collaborative": 0.4,
                "content": 0.35,
                "trending": 0.25
            }
        
        # Get recommendations from each strategy
        collaborative_recs = await self.collaborative_filtering(db, user_id, n_recommendations * 2)
        content_recs = await self.content_based_filtering(db, user_id, n_recommendations * 2)
        trending_recs = await self.get_trending_products(db, n_products=n_recommendations * 2)
        
        # Combine recommendations with weights
        combined_scores = defaultdict(lambda: {
            "product_id": None,
            "product_name": None,
            "category": None,
            "price_per_hour": None,
            "image_url": None,
            "weighted_score": 0.0,
            "reasons": []
        })
        
        # Process collaborative recommendations
        for rec in collaborative_recs:
            pid = rec["product_id"]
            combined_scores[pid]["product_id"] = pid
            combined_scores[pid]["product_name"] = rec["product_name"]
            combined_scores[pid]["category"] = rec["category"]
            combined_scores[pid]["price_per_hour"] = rec["price_per_hour"]
            combined_scores[pid]["image_url"] = rec["image_url"]
            combined_scores[pid]["weighted_score"] += rec["score"] * weights["collaborative"]
            combined_scores[pid]["reasons"].append(rec["reason"])
        
        # Process content-based recommendations
        for rec in content_recs:
            pid = rec["product_id"]
            if combined_scores[pid]["product_id"] is None:
                combined_scores[pid]["product_id"] = pid
                combined_scores[pid]["product_name"] = rec["product_name"]
                combined_scores[pid]["category"] = rec["category"]
                combined_scores[pid]["price_per_hour"] = rec["price_per_hour"]
                combined_scores[pid]["image_url"] = rec["image_url"]
            combined_scores[pid]["weighted_score"] += rec["score"] * weights["content"]
            combined_scores[pid]["reasons"].append(rec["reason"])
        
        # Process trending recommendations
        for rec in trending_recs:
            pid = rec["product_id"]
            if combined_scores[pid]["product_id"] is None:
                combined_scores[pid]["product_id"] = pid
                combined_scores[pid]["product_name"] = rec["product_name"]
                combined_scores[pid]["category"] = rec["category"]
                combined_scores[pid]["price_per_hour"] = rec["price_per_hour"]
                combined_scores[pid]["image_url"] = rec["image_url"]
            combined_scores[pid]["weighted_score"] += rec["score"] * weights["trending"]
            combined_scores[pid]["reasons"].append(rec["reason"])
        
        # Sort by weighted score
        sorted_recommendations = sorted(
            [v for v in combined_scores.values() if v["product_id"] is not None],
            key=lambda x: x["weighted_score"],
            reverse=True
        )[:n_recommendations]
        
        # Format final recommendations
        result = []
        for rec in sorted_recommendations:
            result.append({
                "product_id": rec["product_id"],
                "product_name": rec["product_name"],
                "category": rec["category"],
                "price_per_hour": rec["price_per_hour"],
                "image_url": rec["image_url"],
                "score": round(rec["weighted_score"], 3),
                "recommendation_type": "hybrid",
                "reasons": list(set(rec["reasons"]))[:3]  # Top 3 unique reasons
            })
        
        return result
    
    # ==================== BEHAVIOR TRACKING ====================
    
    async def log_user_behavior(
        self,
        db: Session,
        user_id: str,
        action_type: str,
        product_id: Optional[str] = None,
        search_query: Optional[str] = None,
        category_viewed: Optional[str] = None,
        time_spent_seconds: Optional[int] = None,
        device_type: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> None:
        """
        Log user behavior for model training.
        
        Args:
            db: Database session
            user_id: User ID
            action_type: Type of action (view, search, rent, rate, click)
            product_id: Product ID (if applicable)
            search_query: Search query (if applicable)
            category_viewed: Category viewed
            time_spent_seconds: Time spent on page
            device_type: Device type
            session_id: Session ID
        """
        behavior_log = UserBehaviorLog(
            user_id=user_id,
            product_id=product_id,
            action_type=action_type,
            search_query=search_query,
            category_viewed=category_viewed,
            time_spent_seconds=time_spent_seconds,
            device_type=device_type,
            session_id=session_id
        )
        
        db.add(behavior_log)
        db.commit()
    
    # ==================== HELPER METHODS ====================
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def _calculate_trending_score(
        self,
        rental_count: int,
        avg_revenue: float,
        rating: float,
        max_rental_count: int = 100
    ) -> float:
        """
        Calculate trending score for a product.
        
        Factors:
        - Rental count (normalized)
        - Average revenue
        - Rating
        """
        # Normalize rental count (0-1)
        normalized_count = min(rental_count / max_rental_count, 1.0)
        
        # Normalize rating (0-1)
        normalized_rating = rating / 5.0
        
        # Calculate weighted score
        score = (
            normalized_count * 0.4 +
            normalized_rating * 0.3 +
            min(avg_revenue / 1000, 1.0) * 0.3
        )
        
        return min(score, 1.0)


# Singleton instance
ml_recommendation_engine = MLRecommendationEngine()
