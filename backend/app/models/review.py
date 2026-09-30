"""Review Model - User reviews and ratings for products."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, DECIMAL, CheckConstraint, Index
from sqlalchemy.orm import relationship
import uuid

from app.db.session import Base


class Review(Base):
    """Review model for user product reviews and ratings."""
    __tablename__ = "reviews"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False, index=True)
    rental_id = Column(String(36), ForeignKey("rental_sessions.id"), nullable=True, index=True)
    
    # Rating (1-5 stars)
    rating = Column(Integer, nullable=False)
    
    # Review content
    title = Column(String(200), nullable=True)
    comment = Column(Text, nullable=True)
    
    # Review metadata
    is_verified = Column(Integer, default=0)  # 0 = not verified, 1 = verified purchase
    is_published = Column(Integer, default=1)  # 0 = hidden, 1 = published
    helpful_count = Column(Integer, default=0)
    
    # Admin response
    admin_response = Column(Text, nullable=True)
    admin_response_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="chk_rating_range"),
        CheckConstraint("is_verified IN (0, 1)", name="chk_is_verified"),
        CheckConstraint("is_published IN (0, 1)", name="chk_is_published"),
        Index("idx_product_rating", "product_id", "rating"),
        Index("idx_user_product", "user_id", "product_id"),
    )
    
    user = relationship("User", backref="reviews")
    product = relationship("Product", backref="reviews")
    rental = relationship("RentalSession", backref="review")
    
    def __repr__(self) -> str:
        return f"<Review(id={self.id}, rating={self.rating}, product={self.product_id})>"
    
    def to_dict(self) -> dict:
        """Convert review to dictionary."""
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "product_id": str(self.product_id),
            "rental_id": str(self.rental_id) if self.rental_id else None,
            "rating": self.rating,
            "title": self.title,
            "comment": self.comment,
            "is_verified": bool(self.is_verified),
            "is_published": bool(self.is_published),
            "helpful_count": self.helpful_count,
            "admin_response": self.admin_response,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ReviewHelpful(Base):
    """Track which users found reviews helpful."""
    __tablename__ = "review_helpful"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    review_id = Column(String(36), ForeignKey("reviews.id"), nullable=False, index=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_review_user_unique", "review_id", "user_id", unique=True),
    )
    
    review = relationship("Review", backref="helpful_marks")
    user = relationship("User", backref="marked_helpful")
    
    def __repr__(self) -> str:
        return f"<ReviewHelpful(review={self.review_id}, user={self.user_id})>"
