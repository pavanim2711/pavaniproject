"""Products router - Advanced search, filtering, and product management."""
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import text, or_, and_, func, desc, asc
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field

from app.db.session import get_db
from app.models.product import Product

# Mapping of product IDs to image filenames
PRODUCT_IMAGE_MAP = {
    'prod-1': '/images/tent.jfif',
    'prod-2': '/images/bluetooth speaker.jfif',
    'prod-3': '/images/electric-drill-500x500.webp',
    'prod-4': '/images/images.jfif',
    'prod-5': '/images/folding table.webp',
    'prod-6': '/images/ladder.jpg',
    'prod-7': '/images/action camera.jfif',
    'prod-8': '/images/badmiton set.avif',
    # Also support numeric IDs
    '1': '/images/tent.jfif',
    '2': '/images/bluetooth speaker.jfif',
    '3': '/images/electric-drill-500x500.webp',
    '4': '/images/images.jfif',
    '5': '/images/folding table.webp',
    '6': '/images/ladder.jpg',
    '7': '/images/action camera.jfif',
    '8': '/images/badmiton set.avif',
}

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/")
async def list_products(
    # Basic filters
    category: Optional[str] = Query(None, description="Filter by category"),
    
    # Price range filters
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price per hour"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price per hour"),
    
    # Search query
    search: Optional[str] = Query(None, description="Search in product name and description"),
    
    # Sorting
    sort_by: Optional[str] = Query("popularity", description="Sort by: price, popularity, rating, newest"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    
    # Pagination
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    
    # Availability filter
    available_only: bool = Query(True, description="Show only available products"),
    
    # Location filter
    location: Optional[str] = Query(None, description="Filter by location"),
    
    # Rating filter
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    
    db: Session = Depends(get_db)
):
    """
    Advanced product search with multiple filters.
    
    Supports:
    - Category filtering
    - Price range filtering
    - Full-text search
    - Sorting (price, popularity, rating, newest)
    - Pagination
    - Availability filtering
    - Location filtering
    - Rating filtering
    """
    try:
        # Build base query
        base_sql = """
            SELECT 
                p.id, 
                p.name, 
                p.description, 
                p.category, 
                p.price_per_hour, 
                p.image_url,
                p.is_available,
                p.average_rating,
                p.rental_count,
                p.location,
                p.created_at
            FROM products p
            WHERE 1=1
        """
        
        params = {}
        
        # Add filters
        if category:
            base_sql += " AND p.category = :category"
            params["category"] = category
        
        if min_price is not None:
            base_sql += " AND p.price_per_hour >= :min_price"
            params["min_price"] = min_price
        
        if max_price is not None:
            base_sql += " AND p.price_per_hour <= :max_price"
            params["max_price"] = max_price
        
        if search:
            base_sql += " AND (p.name LIKE :search OR p.description LIKE :search)"
            params["search"] = f"%{search}%"
        
        if available_only:
            base_sql += " AND p.is_available = 1"
        
        if location:
            base_sql += " AND p.location LIKE :location"
            params["location"] = f"%{location}%"
        
        if min_rating is not None:
            base_sql += " AND p.average_rating >= :min_rating"
            params["min_rating"] = min_rating
        
        # Add sorting
        sort_column = {
            "price": "p.price_per_hour",
            "popularity": "p.rental_count",
            "rating": "p.average_rating",
            "newest": "p.created_at"
        }.get(sort_by, "p.rental_count")
        
        order = "DESC" if sort_order.lower() == "desc" else "ASC"
        base_sql += f" ORDER BY {sort_column} {order}"
        
        # Add pagination
        offset = (page - 1) * page_size
        base_sql += f" LIMIT {page_size} OFFSET {offset}"
        
        # Execute query
        result = db.execute(text(base_sql), params)
        rows = result.fetchall()
        
        # Get total count for pagination
        count_sql = "SELECT COUNT(*) FROM products p WHERE 1=1"
        if category:
            count_sql += f" AND p.category = '{category}'"
        if min_price is not None:
            count_sql += f" AND p.price_per_hour >= {min_price}"
        if max_price is not None:
            count_sql += f" AND p.price_per_hour <= {max_price}"
        if search:
            count_sql += f" AND (p.name LIKE '%{search}%' OR p.description LIKE '%{search}%')"
        if available_only:
            count_sql += " AND p.is_available = 1"
        if location:
            count_sql += f" AND p.location LIKE '%{location}%'"
        if min_rating is not None:
            count_sql += f" AND p.average_rating >= {min_rating}"
        
        total_count = db.execute(text(count_sql)).scalar()
        
        # Format products
        products = []
        for row in rows:
            product_id = row[0]
            image_url = PRODUCT_IMAGE_MAP.get(product_id, f'/images/product-{product_id}.jpg')
            
            products.append({
                "id": product_id,
                "name": row[1],
                "description": row[2] or "",
                "category": row[3],
                "price_per_hour": float(row[4]) if row[4] else 0,
                "image_url": image_url,
                "is_available": bool(row[6]) if row[6] is not None else True,
                "rating": float(row[7]) if row[7] else 4.5,
                "rental_count": row[8] or 0,
                "location": row[9] or "Bengaluru",
                "created_at": str(row[10]) if row[10] else None
            })
        
        return {
            "products": products,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": (total_count + page_size - 1) // page_size,
                "has_next": page * page_size < total_count,
                "has_previous": page > 1
            },
            "filters_applied": {
                "category": category,
                "price_range": {"min": min_price, "max": max_price},
                "search": search,
                "sort_by": sort_by,
                "sort_order": sort_order,
                "available_only": available_only,
                "location": location,
                "min_rating": min_rating
            }
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "products": [],
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": 0,
                "total_pages": 0,
                "has_next": False,
                "has_previous": False
            },
            "error": str(e)
        }

@router.get("/{product_id}")
async def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get product details."""
    try:
        # Try to find by the exact ID first (could be prod-1 or 1)
        sql = "SELECT id, name, description, category, price_per_hour, image_url, created_at FROM products WHERE id = :id"
        result = db.execute(text(sql), {"id": product_id})
        row = result.fetchone()
        
        # If not found and product_id is numeric, try with prod- prefix
        if not row and product_id.isdigit():
            prod_id = f'prod-{product_id}'
            result = db.execute(text(sql), {"id": prod_id})
            row = result.fetchone()
        
        # If still not found and product_id starts with prod-, try without prefix
        if not row and product_id.startswith('prod-'):
            numeric_id = product_id.replace('prod-', '')
            result = db.execute(text(sql), {"id": numeric_id})
            row = result.fetchone()
        
        if not row:
            return {"error": "Product not found"}
        
        product_id_key = row[0]  # Get actual ID from database
        image_url = PRODUCT_IMAGE_MAP.get(product_id_key, f'/images/product-{product_id_key}.jpg')
        
        return {
            "id": product_id_key,
            "name": row[1],
            "description": row[2] or "",
            "category": row[3],
            "price_per_hour": float(row[4]) if row[4] else 0,
            "min_rental_hours": 1,
            "max_rental_hours": 24,
            "specifications": {},
            "features": ["Available"],
            "image_url": image_url,
            "gallery_urls": [],
            "availability": {
                "is_available": True,
                "available_from": None,
                "available_until": None
            },
            "location": "Bengaluru",
            "rating": 4.5,
            "review_count": 0,
            "created_at": str(row[6]) if row[6] else None
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}


@router.get("/categories/list")
async def list_categories(db: Session = Depends(get_db)):
    """Get all product categories with product counts."""
    try:
        sql = """
            SELECT 
                category, 
                COUNT(*) as product_count,
                AVG(price_per_hour) as avg_price,
                AVG(average_rating) as avg_rating
            FROM products
            WHERE is_available = 1
            GROUP BY category
            ORDER BY product_count DESC
        """
        
        result = db.execute(text(sql))
        rows = result.fetchall()
        
        categories = []
        for row in rows:
            categories.append({
                "name": row[0],
                "product_count": row[1],
                "avg_price": round(float(row[2]), 2) if row[2] else 0,
                "avg_rating": round(float(row[3]), 2) if row[3] else 4.5
            })
        
        return {
            "categories": categories,
            "total_categories": len(categories)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"categories": [], "total_categories": 0, "error": str(e)}


@router.get("/search/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=20, description="Number of suggestions"),
    db: Session = Depends(get_db)
):
    """Get search suggestions based on query."""
    try:
        sql = """
            SELECT DISTINCT name, category
            FROM products
            WHERE name LIKE :query OR category LIKE :query
            LIMIT :limit
        """
        
        result = db.execute(text(sql), {
            "query": f"%{q}%",
            "limit": limit
        })
        rows = result.fetchall()
        
        suggestions = []
        for row in rows:
            suggestions.append({
                "name": row[0],
                "category": row[1],
                "type": "product" if q.lower() in row[0].lower() else "category"
            })
        
        return {
            "query": q,
            "suggestions": suggestions
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"query": q, "suggestions": []}


@router.get("/popular")
async def get_popular_products(
    limit: int = Query(10, ge=1, le=50, description="Number of products"),
    time_period: str = Query("week", description="Time period: day, week, month, all"),
    db: Session = Depends(get_db)
):
    """Get most popular products based on rental count."""
    try:
        sql = """
            SELECT 
                p.id, 
                p.name, 
                p.description, 
                p.category, 
                p.price_per_hour, 
                p.image_url,
                p.rental_count,
                p.average_rating
            FROM products p
            WHERE p.is_available = 1
            ORDER BY p.rental_count DESC
            LIMIT :limit
        """
        
        result = db.execute(text(sql), {"limit": limit})
        rows = result.fetchall()
        
        products = []
        for row in rows:
            product_id = row[0]
            image_url = PRODUCT_IMAGE_MAP.get(product_id, f'/images/product-{product_id}.jpg')
            
            products.append({
                "id": product_id,
                "name": row[1],
                "description": row[2] or "",
                "category": row[3],
                "price_per_hour": float(row[4]) if row[4] else 0,
                "image_url": image_url,
                "rental_count": row[6] or 0,
                "rating": float(row[7]) if row[7] else 4.5
            })
        
        return {
            "products": products,
            "time_period": time_period
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"products": [], "time_period": time_period, "error": str(e)}


@router.get("/price-range")
async def get_price_range(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """Get min and max prices for products."""
    try:
        sql = """
            SELECT 
                MIN(price_per_hour) as min_price,
                MAX(price_per_hour) as max_price,
                AVG(price_per_hour) as avg_price
            FROM products
            WHERE is_available = 1
        """
        
        params = {}
        if category:
            sql += " AND category = :category"
            params["category"] = category
        
        result = db.execute(text(sql), params)
        row = result.fetchone()
        
        return {
            "min_price": float(row[0]) if row[0] else 0,
            "max_price": float(row[1]) if row[1] else 500,
            "avg_price": round(float(row[2]), 2) if row[2] else 100,
            "category": category
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"min_price": 0, "max_price": 500, "avg_price": 100, "error": str(e)}
