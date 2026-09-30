"""Reviews router - User reviews and ratings system."""

from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from datetime import datetime
from typing import Optional, List, Dict, Any

from app.db.session import get_db
from app.models.user import User
from app.models.product import Product
from app.models.review import Review, ReviewHelpful
from app.models.rental import RentalSession
from app.core.jwt import verify_access_token
from app.services.notification_integration import notification_integration

router = APIRouter(prefix="/reviews", tags=["Reviews"])


# ==================== Request/Response Models ====================

class ReviewCreate(BaseModel):
    """Request model for creating a review."""
    product_id: str = Field(..., description="Product ID")
    rental_id: Optional[str] = Field(None, description="Rental ID (for verified reviews)")
    rating: int = Field(..., ge=1, le=5, description="Rating (1-5 stars)")
    title: Optional[str] = Field(None, max_length=200, description="Review title")
    comment: Optional[str] = Field(None, max_length=2000, description="Review comment")


class ReviewUpdate(BaseModel):
    """Request model for updating a review."""
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating (1-5 stars)")
    title: Optional[str] = Field(None, max_length=200, description="Review title")
    comment: Optional[str] = Field(None, max_length=2000, description="Review comment")


class ReviewResponse(BaseModel):
    """Response model for review."""
    id: str
    user_id: str
    user_name: str
    product_id: str
    product_name: str
    rental_id: Optional[str]
    rating: int
    title: Optional[str]
    comment: Optional[str]
    is_verified: bool
    helpful_count: int
    admin_response: Optional[str]
    created_at: str
    updated_at: str


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


# ==================== Review Endpoints ====================

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_review(
    review_in: ReviewCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    token: str = None
):
    """
    Create a new review for a product.
    
    Users can only review products they have rented (verified reviews).
    One review per product per user.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    # Check if product exists
    product = db.query(Product).filter(Product.id == review_in.product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Check if user already reviewed this product
    existing_review = db.query(Review).filter(
        Review.user_id == user.id,
        Review.product_id == review_in.product_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product"
        )
    
    # Check if this is a verified purchase
    is_verified = False
    if review_in.rental_id:
        rental = db.query(RentalSession).filter(
            RentalSession.id == review_in.rental_id,
            RentalSession.user_id == user.id,
            RentalSession.product_id == review_in.product_id,
            RentalSession.status == "completed"
        ).first()
        
        if rental:
            is_verified = True
    else:
        # Check if user has any completed rental for this product
        rental = db.query(RentalSession).filter(
            RentalSession.user_id == user.id,
            RentalSession.product_id == review_in.product_id,
            RentalSession.status == "completed"
        ).first()
        
        if rental:
            is_verified = True
            review_in.rental_id = str(rental.id)
    
    # Create review
    review = Review(
        user_id=user.id,
        product_id=review_in.product_id,
        rental_id=review_in.rental_id,
        rating=review_in.rating,
        title=review_in.title,
        comment=review_in.comment,
        is_verified=1 if is_verified else 0
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    # Update product rating
    await update_product_rating(db, review_in.product_id)
    
    return {
        "id": str(review.id),
        "user_id": str(review.user_id),
        "user_name": user.name,
        "product_id": str(review.product_id),
        "product_name": product.name,
        "rental_id": str(review.rental_id) if review.rental_id else None,
        "rating": review.rating,
        "title": review.title,
        "comment": review.comment,
        "is_verified": bool(review.is_verified),
        "helpful_count": review.helpful_count,
        "admin_response": review.admin_response,
        "created_at": review.created_at.isoformat(),
        "updated_at": review.updated_at.isoformat()
    }


@router.get("/product/{product_id}", response_model=Dict[str, Any])
async def get_product_reviews(
    product_id: str,
    rating: Optional[int] = Query(None, ge=1, le=5, description="Filter by rating"),
    verified_only: bool = Query(False, description="Show only verified reviews"),
    sort_by: str = Query("recent", description="Sort by: recent, helpful, rating_high, rating_low"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """
    Get all reviews for a product with filtering and sorting.
    
    Includes rating summary statistics.
    """
    # Build query
    query = db.query(Review).filter(Review.product_id == product_id, Review.is_published == 1)
    
    if rating:
        query = query.filter(Review.rating == rating)
    
    if verified_only:
        query = query.filter(Review.is_verified == 1)
    
    # Sorting
    if sort_by == "recent":
        query = query.order_by(desc(Review.created_at))
    elif sort_by == "helpful":
        query = query.order_by(desc(Review.helpful_count))
    elif sort_by == "rating_high":
        query = query.order_by(desc(Review.rating))
    elif sort_by == "rating_low":
        query = query.order_by(Review.rating)
    
    # Get total count
    total_count = query.count()
    
    # Pagination
    offset = (page - 1) * page_size
    reviews = query.offset(offset).limit(page_size).all()
    
    # Get rating distribution
    rating_dist = db.query(
        Review.rating,
        func.count(Review.id).label('count')
    ).filter(
        Review.product_id == product_id,
        Review.is_published == 1
    ).group_by(Review.rating).all()
    
    rating_distribution = {i: 0 for i in range(1, 6)}
    for r, count in rating_dist:
        rating_distribution[r] = count
    
    # Calculate average rating
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.product_id == product_id,
        Review.is_published == 1
    ).scalar()
    
    # Format reviews
    review_list = []
    for review in reviews:
        user = db.query(User).filter(User.id == review.user_id).first()
        product = db.query(Product).filter(Product.id == review.product_id).first()
        
        review_list.append({
            "id": str(review.id),
            "user_id": str(review.user_id),
            "user_name": user.name if user else "Anonymous",
            "product_id": str(review.product_id),
            "product_name": product.name if product else "Unknown",
            "rental_id": str(review.rental_id) if review.rental_id else None,
            "rating": review.rating,
            "title": review.title,
            "comment": review.comment,
            "is_verified": bool(review.is_verified),
            "helpful_count": review.helpful_count,
            "admin_response": review.admin_response,
            "created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        })
    
    return {
        "reviews": review_list,
        "summary": {
            "average_rating": round(float(avg_rating), 2) if avg_rating else 0,
            "total_reviews": total_count,
            "rating_distribution": rating_distribution
        },
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_pages": (total_count + page_size - 1) // page_size,
            "has_next": page * page_size < total_count
        }
    }


@router.get("/user/me", response_model=List[ReviewResponse])
async def get_my_reviews(
    db: Session = Depends(get_db),
    token: str = None
):
    """Get all reviews by the current user."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    reviews = db.query(Review).filter(
        Review.user_id == user.id
    ).order_by(desc(Review.created_at)).all()
    
    result = []
    for review in reviews:
        product = db.query(Product).filter(Product.id == review.product_id).first()
        
        result.append({
            "id": str(review.id),
            "user_id": str(review.user_id),
            "user_name": user.name,
            "product_id": str(review.product_id),
            "product_name": product.name if product else "Unknown",
            "rental_id": str(review.rental_id) if review.rental_id else None,
            "rating": review.rating,
            "title": review.title,
            "comment": review.comment,
            "is_verified": bool(review.is_verified),
            "helpful_count": review.helpful_count,
            "admin_response": review.admin_response,
            "created_at": review.created_at.isoformat(),
            "updated_at": review.updated_at.isoformat()
        })
    
    return result


@router.patch("/{review_id}", response_model=ReviewResponse)
async def update_review(
    review_id: str,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
    token: str = None
):
    """Update an existing review (only by the author)."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own reviews"
        )
    
    # Update fields
    if review_update.rating is not None:
        review.rating = review_update.rating
    if review_update.title is not None:
        review.title = review_update.title
    if review_update.comment is not None:
        review.comment = review_update.comment
    
    review.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(review)
    
    # Update product rating
    await update_product_rating(db, str(review.product_id))
    
    product = db.query(Product).filter(Product.id == review.product_id).first()
    
    return {
        "id": str(review.id),
        "user_id": str(review.user_id),
        "user_name": user.name,
        "product_id": str(review.product_id),
        "product_name": product.name if product else "Unknown",
        "rental_id": str(review.rental_id) if review.rental_id else None,
        "rating": review.rating,
        "title": review.title,
        "comment": review.comment,
        "is_verified": bool(review.is_verified),
        "helpful_count": review.helpful_count,
        "admin_response": review.admin_response,
        "created_at": review.created_at.isoformat(),
        "updated_at": review.updated_at.isoformat()
    }


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Delete a review (only by the author)."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    if review.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own reviews"
        )
    
    product_id = str(review.product_id)
    
    db.delete(review)
    db.commit()
    
    # Update product rating
    await update_product_rating(db, product_id)


@router.post("/{review_id}/helpful", status_code=status.HTTP_200_OK)
async def mark_review_helpful(
    review_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Mark a review as helpful."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Check if already marked
    existing = db.query(ReviewHelpful).filter(
        ReviewHelpful.review_id == review_id,
        ReviewHelpful.user_id == user.id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already marked this review as helpful"
        )
    
    # Mark as helpful
    helpful_mark = ReviewHelpful(
        review_id=review_id,
        user_id=user.id
    )
    
    db.add(helpful_mark)
    
    # Increment helpful count
    review.helpful_count += 1
    
    db.commit()
    
    return {
        "success": True,
        "helpful_count": review.helpful_count
    }


async def update_product_rating(db: Session, product_id: str):
    """Update product's average rating based on all reviews."""
    avg_rating = db.query(func.avg(Review.rating)).filter(
        Review.product_id == product_id,
        Review.is_published == 1
    ).scalar()
    
    review_count = db.query(func.count(Review.id)).filter(
        Review.product_id == product_id,
        Review.is_published == 1
    ).scalar()
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        product.average_rating = avg_rating if avg_rating else 0
        product.review_count = review_count
        db.commit()


# ==================== Admin Endpoints ====================

@router.post("/{review_id}/respond", status_code=status.HTTP_200_OK)
async def add_admin_response(
    review_id: str,
    response: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Add admin response to a review (admin only)."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    if user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can respond to reviews"
        )
    
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    review.admin_response = response
    review.admin_response_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Response added successfully"
    }


@router.post("/{review_id}/hide", status_code=status.HTTP_200_OK)
async def hide_review(
    review_id: str,
    db: Session = Depends(get_db),
    token: str = None
):
    """Hide a review (admin only)."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    user = get_current_user(token, db)
    
    if user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can hide reviews"
        )
    
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    review.is_published = 0
    db.commit()
    
    # Update product rating
    await update_product_rating(db, str(review.product_id))
    
    return {
        "success": True,
        "message": "Review hidden successfully"
    }
