# Database to API Integration Guide

This guide explains how to integrate the Quick Tym SQLite database with the FastAPI backend.

## Quick Setup

### 1. Backend Configuration

Update `backend/.env`:
```env
DATABASE_URL=sqlite:///../database/quick_tym.db
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
```

### 2. SQLAlchemy Models

The backend uses SQLAlchemy ORM for database access. Models are defined in `backend/app/models.py`.

Example model:
```python
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category_id = Column(String, ForeignKey("categories.id"))
    name = Column(String(200), nullable=False)
    price_per_hour = Column(Float, nullable=False)
    category = Column(String(20), nullable=False)
    description = Column(String)
    image_url = Column(String(500))
    inventory = relationship("Inventory", back_populates="product")
    rental_sessions = relationship("RentalSession", back_populates="product")
```

### 3. Database Session

FastAPI uses dependency injection for database sessions:

```python
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# In route handlers:
@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products
```

## API Endpoints

### Products API

#### Get All Products
```http
GET /api/products
```

**Response:**
```json
{
  "products": [
    {
      "id": "prod-1",
      "name": "Camping Tent (4-person)",
      "price_per_hour": 150,
      "category": "Outdoor",
      "description": "Waterproof 4-person camping tent...",
      "image_url": "/images/tent.jfif",
      "rental_count": 28,
      "average_rating": 4.6
    }
  ]
}
```

**Backend Implementation:**
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api", tags=["products"])

@router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_active == True).all()
    return {"products": products}
```

#### Get Product by Category
```http
GET /api/products?category=Outdoor
```

**Backend Implementation:**
```python
@router.get("/products")
def get_products(category: str = None, db: Session = Depends(get_db)):
    query = db.query(Product).filter(Product.is_active == True)
    if category:
        query = query.filter(Product.category == category)
    return {"products": query.all()}
```

#### Get Single Product
```http
GET /api/products/{product_id}
```

**Backend Implementation:**
```python
@router.get("/products/{product_id}")
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
```

### Rental Sessions API

#### Start Rental
```http
POST /api/rentals
Content-Type: application/json

{
  "user_id": "user-1",
  "product_id": "prod-1",
  "delivery_address": {"area": "Koramangala", "street": "Tech Park Road"},
  "pickup_address": {"area": "Indiranagar", "street": "100 Feet Road"}
}
```

**Backend Implementation:**
```python
from fastapi import HTTPException
from pydantic import BaseModel
from decimal import Decimal

class RentalCreateRequest(BaseModel):
    user_id: str
    product_id: str
    delivery_address: dict
    pickup_address: dict

@router.post("/rentals")
def create_rental(req: RentalCreateRequest, db: Session = Depends(get_db)):
    # Validate user and product exist
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    product = db.query(Product).filter(Product.id == req.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create rental session
    from datetime import datetime
    rental = RentalSession(
        id=str(uuid.uuid4()),
        user_id=req.user_id,
        product_id=req.product_id,
        status="pending",
        start_time=datetime.utcnow(),
        delivery_address=json.dumps(req.delivery_address),
        pickup_address=json.dumps(req.pickup_address),
        location="Bengaluru"
    )
    
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental
```

#### Get Rental Status
```http
GET /api/rentals/{rental_id}
```

**Backend Implementation:**
```python
@router.get("/rentals/{rental_id}")
def get_rental(rental_id: str, db: Session = Depends(get_db)):
    rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental
```

#### End Rental / Request Pickup
```http
POST /api/rentals/{rental_id}/end
```

**Backend Implementation:**
```python
@router.post("/rentals/{rental_id}/end")
def end_rental(rental_id: str, db: Session = Depends(get_db)):
    rental = db.query(RentalSession).filter(RentalSession.id == rental_id).first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")
    
    # Calculate duration and cost
    end_time = datetime.utcnow()
    duration_seconds = int((end_time - rental.start_time).total_seconds())
    
    product = db.query(Product).filter(Product.id == rental.product_id).first()
    
    # Calculate amount (per hour)
    hours = duration_seconds / 3600
    base_amount = Decimal(hours) * Decimal(product.price_per_hour)
    tax_amount = base_amount * Decimal("0.10")  # 10% tax
    
    rental.end_time = end_time
    rental.total_seconds = duration_seconds
    rental.base_amount = base_amount
    rental.tax_amount = tax_amount
    rental.total_amount = base_amount + tax_amount
    rental.status = "completed"
    
    db.commit()
    return rental
```

### AI Recommendations API

#### Get Recommendations for User
```http
GET /api/users/{user_id}/recommendations
```

**Backend Implementation:**
```python
@router.get("/users/{user_id}/recommendations")
def get_recommendations(user_id: str, limit: int = 5, db: Session = Depends(get_db)):
    recommendations = db.query(AIRecommendation)\
        .filter(AIRecommendation.user_id == user_id)\
        .filter(AIRecommendation.expires_at > datetime.utcnow())\
        .order_by(AIRecommendation.affinity_score.desc())\
        .limit(limit)\
        .all()
    
    # Include product details
    result = []
    for rec in recommendations:
        product = db.query(Product).filter(Product.id == rec.product_id).first()
        result.append({
            "recommendation": rec,
            "product": product
        })
    
    return {"recommendations": result}
```

### Demand Predictions API

#### Get Demand Forecast
```http
GET /api/demand-forecast?date=2024-01-15
```

**Backend Implementation:**
```python
@router.get("/demand-forecast")
def get_demand_forecast(date: str = None, db: Session = Depends(get_db)):
    from datetime import datetime, date as datetype
    
    if not date:
        date = datetype.today().isoformat()
    
    predictions = db.query(DemandPrediction)\
        .filter(DemandPrediction.prediction_date == date)\
        .all()
    
    result = []
    for pred in predictions:
        product = db.query(Product).filter(Product.id == pred.product_id).first()
        result.append({
            "product": product.name,
            "predicted_demand": pred.predicted_demand,
            "confidence_interval": {
                "lower": pred.confidence_interval_lower,
                "upper": pred.confidence_interval_upper
            }
        })
    
    return {"forecast_date": date, "predictions": result}
```

## Frontend Integration

### Using API Service Layer

Create `frontend/src/services/api.ts`:

```typescript
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000/api';

export const productsAPI = {
  getAll: (category?: string) => {
    const url = category ? `${API_BASE}/products?category=${category}` : `${API_BASE}/products`;
    return axios.get(url);
  },
  
  getById: (id: string) => axios.get(`${API_BASE}/products/${id}`),
};

export const rentalsAPI = {
  create: (data: any) => axios.post(`${API_BASE}/rentals`, data),
  getById: (id: string) => axios.get(`${API_BASE}/rentals/${id}`),
  end: (id: string) => axios.post(`${API_BASE}/rentals/${id}/end`),
};

export const recommendationsAPI = {
  getForUser: (userId: string) => 
    axios.get(`${API_BASE}/users/${userId}/recommendations`),
};
```

### Update HomePage Component

```typescript
import { useEffect, useState } from 'react';
import { productsAPI } from '@services/api';

export function HomePage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    productsAPI.getAll()
      .then(res => setProducts(res.data.products))
      .catch(err => console.error('Failed to fetch products:', err))
      .finally(() => setLoading(false));
  }, []);
  
  if (loading) return <div>Loading products...</div>;
  
  return (
    // Render products from database instead of MOCK_PRODUCTS
    <>
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </>
  );
}
```

## Data Flow

### Complete Rental Flow

1. **User Browse Products**
   - GET `/api/products` → Display from database
   - Frontend renders real products with images from DB

2. **User Selects Product**
   - GET `/api/products/{id}` → Show details, inventory, reviews

3. **User Initiates Rental**
   - POST `/api/rentals` → Create session in DB
   - Trigger delivery assignment
   - Send notification to user

4. **Delivery Partner Accepts**
   - Delivery status updates to "in_transit"
   - Real-time notification to customer

5. **Product Delivered**
   - POST `/api/deliveries/{id}/complete`
   - Rental status changes to "active"
   - Timer starts

6. **User Requests Pickup**
   - POST `/api/rentals/{id}/end` → End rental
   - Calculate charges, add to payments
   - Send pickup request to partner

7. **Payment Processing**
   - POST `/api/payments` → Process payment
   - Rental status = "paid"
   - Send confirmation

8. **Review & Feedback**
   - POST `/api/reviews` → Add review
   - Update product ratings in DB

## Query Performance Tips

### Common Queries

Get user's active rentals:
```python
active_rentals = db.query(RentalSession)\
    .filter(RentalSession.user_id == user_id)\
    .filter(RentalSession.status == "active")\
    .all()
```

Get trending products:
```python
trending = db.query(Product)\
    .filter(Product.is_active == True)\
    .order_by(Product.rental_count.desc())\
    .limit(10)\
    .all()
```

Get delivery partner stats:
```python
stats = db.query(
    User.id,
    User.name,
    func.count(Delivery.id).label('total_deliveries'),
    func.avg(User.rating).label('avg_rating')
).filter(User.role == 'Delivery_Partner')\
 .outerjoin(Delivery)\
 .group_by(User.id)\
 .all()
```

## Testing

### Pytest Examples

```python
# tests/test_products.py
def test_get_all_products(client, db):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(response.json()["products"]) == 8

def test_get_product_by_id(client, db):
    response = client.get("/api/products/prod-1")
    assert response.status_code == 200
    assert response.json()["name"] == "Camping Tent (4-person)"

def test_create_rental(client, db):
    response = client.post("/api/rentals", json={
        "user_id": "user-1",
        "product_id": "prod-1",
        "delivery_address": {"area": "Koramangala"},
        "pickup_address": {"area": "Indiranagar"}
    })
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
```

## Troubleshooting

### Database Not Found
```
FileNotFoundError: [Errno 2] No such file or directory: '../database/quick_tym.db'
```
Solution: Run `python database/init_auto.py` to create database

### Foreign Key Constraint Error
```
sqlalchemy.exc.IntegrityError: (sqlite3.IntegrityError) FOREIGN KEY constraint failed
```
Solution: Ensure all referenced records exist before inserting

### No Models Found
```
sqlalchemy.exc.NoInspectionAvailable: No inspection system has been configured
```
Solution: Import all models before creating engine: `from app.models import *`

## Resources

- [SQLAlchemy ORM Documentation](https://docs.sqlalchemy.org/)
- [FastAPI Database Documentation](https://fastapi.tiangolo.com/advanced/sql-databases/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- Design Spec: `.kiro/specs/quick-tym/design.md`
