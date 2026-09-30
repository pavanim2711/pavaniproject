"""AI Recommendation and Prediction Models."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Float, Integer, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
import uuid

from app.db.session import Base


class AIRecommendation(Base):
    """AI-generated product recommendations for users."""
    __tablename__ = "ai_recommendations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    affinity_score = Column(DECIMAL(5, 4), nullable=False, default=0.0)
    recommendation_type = Column(String(50), nullable=False)  # 'collaborative', 'content', 'trending', 'seasonal'
    confidence_score = Column(DECIMAL(5, 4), nullable=False, default=0.0)
    reason = Column(Text, nullable=True)
    context_data = Column(Text, nullable=True)  # JSON string with additional context
    is_active = Column(Integer, default=1)  # 1 = active, 0 = dismissed
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", backref="ai_recommendations")
    product = relationship("Product", backref="ai_recommendations")
    
    def __repr__(self) -> str:
        return f"<AIRecommendation(user={self.user_id}, product={self.product_id}, score={self.affinity_score})>"


class DemandPrediction(Base):
    """Demand prediction for products."""
    __tablename__ = "demand_predictions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    prediction_date = Column(String(10), nullable=False, index=True)  # YYYY-MM-DD
    predicted_demand = Column(Integer, nullable=False, default=0)
    confidence_interval_lower = Column(Integer, nullable=True)
    confidence_interval_upper = Column(Integer, nullable=True)
    prediction_model = Column(String(50), nullable=False, default="arima")  # arima, lstm, prophet
    factors = Column(Text, nullable=True)  # JSON string with prediction factors
    accuracy_score = Column(DECIMAL(5, 4), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    product = relationship("Product", backref="demand_predictions")
    
    def __repr__(self) -> str:
        return f"<DemandPrediction(product={self.product_id}, date={self.prediction_date}, demand={self.predicted_demand})>"


class UserBehaviorLog(Base):
    """User behavior tracking for ML model training."""
    __tablename__ = "user_behavior_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=True, index=True)
    action_type = Column(String(50), nullable=False, index=True)  # view, search, rent, rate, click
    search_query = Column(String(200), nullable=True)
    category_viewed = Column(String(50), nullable=True)
    time_spent_seconds = Column(Integer, nullable=True)
    page_depth = Column(Integer, nullable=True)
    device_type = Column(String(20), nullable=True)  # mobile, desktop, tablet
    referrer = Column(String(200), nullable=True)
    session_id = Column(String(100), nullable=True, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    user = relationship("User", backref="behavior_logs")
    product = relationship("Product", backref="behavior_logs")
    
    def __repr__(self) -> str:
        return f"<UserBehaviorLog(user={self.user_id}, action={self.action_type})>"


class ProductEmbedding(Base):
    """Product embeddings for similarity-based recommendations."""
    __tablename__ = "product_embeddings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String(36), ForeignKey("products.id"), unique=True, nullable=False)
    embedding_vector = Column(Text, nullable=False)  # JSON string of embedding vector
    model_version = Column(String(50), nullable=False, default="v1")
    last_updated = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    product = relationship("Product", backref="embedding")
    
    def __repr__(self) -> str:
        return f"<ProductEmbedding(product={self.product_id})>"
