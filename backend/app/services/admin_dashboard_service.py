"""Admin dashboard service for analytics and statistics."""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc
from decimal import Decimal
import logging

from app.models.user import User
from app.models.product import Product
from app.models.rental import RentalSession
from app.models.payment import Payment
from app.models.delivery import Delivery
from app.models.review import Review

logger = logging.getLogger(__name__)


class AdminDashboardService:
    """Service for admin dashboard analytics and statistics."""
    
    def get_dashboard_overview(self, db: Session) -> Dict[str, Any]:
        """
        Get comprehensive dashboard overview statistics.
        
        Returns:
            Dashboard overview with key metrics
        """
        # Time periods
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        this_week = today - timedelta(days=today.weekday())
        this_month = today.replace(day=1)
        
        # User statistics
        total_customers = db.query(User).filter(User.role == "Customer").count()
        total_delivery_partners = db.query(User).filter(User.role == "Delivery_Partner").count()
        new_users_today = db.query(User).filter(
            User.created_at >= today
        ).count()
        
        # Product statistics
        total_products = db.query(Product).count()
        available_products = db.query(Product).filter(Product.is_available == True).count()
        low_stock_products = db.query(Product).filter(
            Product.stock_quantity <= 3,
            Product.is_available == True
        ).count()
        
        # Rental statistics
        active_rentals = db.query(RentalSession).filter(
            RentalSession.status == "active"
        ).count()
        
        rentals_today = db.query(RentalSession).filter(
            RentalSession.created_at >= today
        ).count()
        
        completed_rentals = db.query(RentalSession).filter(
            RentalSession.status == "completed"
        ).count()
        
        # Revenue statistics
        today_revenue = db.query(func.sum(Payment.amount)).filter(
            Payment.status == "completed",
            Payment.completed_at >= today
        ).scalar() or 0
        
        month_revenue = db.query(func.sum(Payment.amount)).filter(
            Payment.status == "completed",
            Payment.completed_at >= this_month
        ).scalar() or 0
        
        total_revenue = db.query(func.sum(Payment.amount)).filter(
            Payment.status == "completed"
        ).scalar() or 0
        
        # Delivery statistics
        active_deliveries = db.query(Delivery).filter(
            Delivery.status.in_(["assigned", "in_transit"])
        ).count()
        
        pending_deliveries = db.query(Delivery).filter(
            Delivery.status == "pending"
        ).count()
        
        return {
            "users": {
                "total_customers": total_customers,
                "total_delivery_partners": total_delivery_partners,
                "new_users_today": new_users_today
            },
            "products": {
                "total": total_products,
                "available": available_products,
                "low_stock_alerts": low_stock_products
            },
            "rentals": {
                "active": active_rentals,
                "today": rentals_today,
                "completed": completed_rentals
            },
            "revenue": {
                "today": float(today_revenue),
                "this_month": float(month_revenue),
                "total": float(total_revenue)
            },
            "deliveries": {
                "active": active_deliveries,
                "pending": pending_deliveries
            }
        }
    
    def get_revenue_analytics(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        group_by: str = "day"
    ) -> Dict[str, Any]:
        """
        Get revenue analytics for a date range.
        
        Args:
            db: Database session
            start_date: Start date
            end_date: End date
            group_by: Grouping (day, week, month)
            
        Returns:
            Revenue analytics with trends
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        
        if not end_date:
            end_date = datetime.utcnow()
        
        # Get payments in date range
        payments = db.query(Payment).filter(
            Payment.status == "completed",
            Payment.completed_at >= start_date,
            Payment.completed_at <= end_date
        ).order_by(Payment.completed_at).all()
        
        # Group payments
        revenue_by_period = {}
        
        for payment in payments:
            if not payment.completed_at:
                continue
            
            if group_by == "day":
                period_key = payment.completed_at.strftime("%Y-%m-%d")
            elif group_by == "week":
                period_key = f"{payment.completed_at.year}-W{payment.completed_at.isocalendar()[1]}"
            else:  # month
                period_key = payment.completed_at.strftime("%Y-%m")
            
            if period_key not in revenue_by_period:
                revenue_by_period[period_key] = 0
            
            revenue_by_period[period_key] += float(payment.amount)
        
        # Calculate statistics
        total_revenue = sum(revenue_by_period.values())
        average_revenue = total_revenue / len(revenue_by_period) if revenue_by_period else 0
        
        return {
            "total_revenue": total_revenue,
            "average_revenue": round(average_revenue, 2),
            "periods": [
                {
                    "period": period,
                    "revenue": round(revenue, 2)
                }
                for period, revenue in sorted(revenue_by_period.items())
            ]
        }
    
    def get_rental_analytics(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get rental analytics.
        
        Returns:
            Rental statistics and trends
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        
        if not end_date:
            end_date = datetime.utcnow()
        
        # Rental status distribution
        status_distribution = db.query(
            RentalSession.status,
            func.count(RentalSession.id).label('count')
        ).filter(
            RentalSession.created_at >= start_date,
            RentalSession.created_at <= end_date
        ).group_by(RentalSession.status).all()
        
        # Popular products
        popular_products = db.query(
            Product.id,
            Product.name,
            func.count(RentalSession.id).label('rental_count')
        ).join(
            RentalSession, Product.id == RentalSession.product_id
        ).filter(
            RentalSession.created_at >= start_date,
            RentalSession.created_at <= end_date
        ).group_by(Product.id).order_by(desc('rental_count')).limit(10).all()
        
        # Category distribution
        category_distribution = db.query(
            Product.category,
            func.count(RentalSession.id).label('count')
        ).join(
            RentalSession, Product.id == RentalSession.product_id
        ).filter(
            RentalSession.created_at >= start_date,
            RentalSession.created_at <= end_date
        ).group_by(Product.category).all()
        
        # Average rental duration
        avg_duration = db.query(
            func.avg(RentalSession.total_seconds)
        ).filter(
            RentalSession.status == "completed",
            RentalSession.total_seconds > 0,
            RentalSession.created_at >= start_date,
            RentalSession.created_at <= end_date
        ).scalar()
        
        return {
            "status_distribution": [
                {"status": status, "count": count}
                for status, count in status_distribution
            ],
            "popular_products": [
                {
                    "product_id": str(pid),
                    "product_name": name,
                    "rental_count": count
                }
                for pid, name, count in popular_products
            ],
            "category_distribution": [
                {"category": cat, "count": count}
                for cat, count in category_distribution
            ],
            "average_duration_hours": round((avg_duration or 0) / 3600, 2)
        }
    
    def get_user_analytics(
        self,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get user analytics.
        
        Returns:
            User statistics and trends
        """
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=30)
        
        if not end_date:
            end_date = datetime.utcnow()
        
        # New users per day
        new_users_by_day = db.query(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('count')
        ).filter(
            User.created_at >= start_date,
            User.created_at <= end_date
        ).group_by(func.date(User.created_at)).all()
        
        # Active users (with rentals)
        active_users = db.query(User).join(RentalSession).filter(
            RentalSession.created_at >= start_date,
            RentalSession.created_at <= end_date
        ).distinct().count()
        
        # Top customers
        top_customers = db.query(
            User.id,
            User.name,
            User.email,
            func.count(RentalSession.id).label('rental_count'),
            func.sum(RentalSession.total_amount).label('total_spent')
        ).join(
            RentalSession, User.id == RentalSession.user_id
        ).filter(
            RentalSession.created_at >= start_date,
            RentalSession.created_at <= end_date
        ).group_by(User.id).order_by(desc('total_spent')).limit(10).all()
        
        # Top delivery partners
        top_partners = db.query(
            User.id,
            User.name,
            User.rating,
            func.count(Delivery.id).label('delivery_count')
        ).join(
            Delivery, User.id == Delivery.delivery_partner_id
        ).filter(
            Delivery.created_at >= start_date,
            Delivery.created_at <= end_date,
            User.role == "Delivery_Partner"
        ).group_by(User.id).order_by(desc('delivery_count')).limit(10).all()
        
        return {
            "new_users_by_day": [
                {"date": str(date), "count": count}
                for date, count in new_users_by_day
            ],
            "active_users": active_users,
            "top_customers": [
                {
                    "user_id": str(uid),
                    "name": name,
                    "email": email,
                    "rental_count": rental_count,
                    "total_spent": float(total_spent or 0)
                }
                for uid, name, email, rental_count, total_spent in top_customers
            ],
            "top_delivery_partners": [
                {
                    "partner_id": str(pid),
                    "name": name,
                    "rating": float(rating or 0),
                    "delivery_count": delivery_count
                }
                for pid, name, rating, delivery_count in top_partners
            ]
        }
    
    def get_product_analytics(
        self,
        db: Session
    ) -> Dict[str, Any]:
        """
        Get product analytics.
        
        Returns:
            Product statistics
        """
        # Category distribution
        category_stats = db.query(
            Product.category,
            func.count(Product.id).label('product_count'),
            func.avg(Product.price_per_hour).label('avg_price'),
            func.avg(Product.average_rating).label('avg_rating')
        ).group_by(Product.category).all()
        
        # Most rented products
        most_rented = db.query(
            Product.id,
            Product.name,
            Product.rental_count,
            Product.average_rating
        ).order_by(desc(Product.rental_count)).limit(10).all()
        
        # Top rated products
        top_rated = db.query(
            Product.id,
            Product.name,
            Product.average_rating,
            Product.review_count
        ).filter(
            Product.review_count >= 5
        ).order_by(desc(Product.average_rating)).limit(10).all()
        
        # Products needing attention (low stock, no rentals)
        needs_attention = db.query(Product).filter(
            or_(
                Product.stock_quantity <= 3,
                Product.rental_count == 0
            )
        ).limit(20).all()
        
        return {
            "category_stats": [
                {
                    "category": cat,
                    "product_count": count,
                    "avg_price": float(avg_price or 0),
                    "avg_rating": float(avg_rating or 0)
                }
                for cat, count, avg_price, avg_rating in category_stats
            ],
            "most_rented": [
                {
                    "product_id": str(pid),
                    "name": name,
                    "rental_count": rental_count,
                    "rating": float(rating or 0)
                }
                for pid, name, rental_count, rating in most_rented
            ],
            "top_rated": [
                {
                    "product_id": str(pid),
                    "name": name,
                    "rating": float(rating),
                    "review_count": review_count
                }
                for pid, name, rating, review_count in top_rated
            ],
            "needs_attention": [
                {
                    "product_id": str(p.id),
                    "name": p.name,
                    "stock_quantity": p.stock_quantity,
                    "rental_count": p.rental_count,
                    "reason": "Low stock" if p.stock_quantity <= 3 else "No rentals"
                }
                for p in needs_attention
            ]
        }
    
    def get_recent_activity(
        self,
        db: Session,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get recent activity for dashboard.
        
        Returns:
            List of recent activities
        """
        activities = []
        
        # Recent rentals
        recent_rentals = db.query(RentalSession).order_by(
            desc(RentalSession.created_at)
        ).limit(10).all()
        
        for rental in recent_rentals:
            user = db.query(User).filter(User.id == rental.user_id).first()
            product = db.query(Product).filter(Product.id == rental.product_id).first()
            
            activities.append({
                "type": "rental_created",
                "timestamp": rental.created_at.isoformat(),
                "user_name": user.name if user else "Unknown",
                "details": f"Rented {product.name if product else 'Unknown'}",
                "rental_id": str(rental.id)
            })
        
        # Recent payments
        recent_payments = db.query(Payment).filter(
            Payment.status == "completed"
        ).order_by(desc(Payment.completed_at)).limit(10).all()
        
        for payment in recent_payments:
            rental = db.query(RentalSession).filter(
                RentalSession.id == payment.rental_id
            ).first()
            
            activities.append({
                "type": "payment_completed",
                "timestamp": payment.completed_at.isoformat() if payment.completed_at else payment.created_at.isoformat(),
                "details": f"Payment of ₹{payment.amount} received",
                "payment_id": str(payment.id),
                "rental_id": str(payment.rental_id)
            })
        
        # Recent users
        recent_users = db.query(User).order_by(desc(User.created_at)).limit(10).all()
        
        for user in recent_users:
            activities.append({
                "type": "user_registered",
                "timestamp": user.created_at.isoformat(),
                "user_name": user.name,
                "details": f"New {user.role} registered",
                "user_id": str(user.id)
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return activities[:limit]


# Singleton instance
admin_dashboard_service = AdminDashboardService()
