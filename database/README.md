# Quick Tym SQLite Database

Complete SQLite database setup for the Quick Tym rental platform.

## Database Overview

**File:** `quick_tym.db`  
**Engine:** SQLite 3  
**Size:** ~448 KB (with sample data)  
**Tables:** 15  
**Records:** 53 (sample data)

## Quick Start

### Initialize Database

```bash
# Windows/Mac/Linux - Python method (recommended)
python database/init_auto.py

# Or use init.py for interactive mode
python database/init.py
```

The script will:
- Create all 15 tables with proper schema
- Add all necessary indexes for performance
- Insert realistic Bengaluru rental market data
- Verify data integrity

### Files in This Directory

| File | Purpose |
|------|---------|
| `quick_tym.db` | SQLite database file (auto-created) |
| `schema.sql` | Complete database schema with 15 tables |
| `seed.sql` | Realistic sample data for testing |
| `verify.sql` | Integrity verification queries |
| `init.py` | Interactive Python initialization script |
| `init_auto.py` | Auto-run initialization (no prompts) |
| `init.sh` | Bash initialization script (Unix/Mac) |
| `README.md` | This file |

## Database Schema

### Core Tables (15 total)

#### 1. **Categories** (6 records)
Product categories: Outdoor, Indoor, Sports, Tools, Party, Travel

```sql
SELECT * FROM categories;
```

#### 2. **Users** (4 records)
- Priya Sharma (Customer)
- Rajesh Kumar (Delivery Partner)
- Admin Bengaluru (Admin)
- Arun Singh (Customer)

```sql
SELECT * FROM users WHERE role = 'Customer';
```

#### 3. **Products** (8 records)
Sample products with Bengaluru pricing (₹50-₹500/hr):
- Camping Tent (₹150/hr)
- Bluetooth Speaker (₹80/hr)
- Power Drill Set (₹100/hr)
- Trekking Backpack (₹120/hr)
- Folding Table (₹90/hr)
- Ladder (₹70/hr)
- Action Camera (₹200/hr)
- Badminton Set (₹60/hr)

```sql
SELECT name, price_per_hour, category FROM products ORDER BY price_per_hour DESC;
```

#### 4. **Inventory** (8 records)
Stock levels for each product in Bengaluru

```sql
SELECT p.name, i.quantity, i.available_quantity FROM inventory i
JOIN products p ON i.product_id = p.id;
```

#### 5. **Rental Sessions** (2 records)
Complete rental workflow examples:
- Session 1: Tent rental (completed, ₹6,110 total)
- Session 2: Speaker rental (active)

```sql
SELECT * FROM rental_sessions;
```

#### 6. **Bookings** (1 record)
Scheduled bookings for future rentals

#### 7. **Payments** (2 records)
Payment transactions with status tracking

```sql
SELECT status, COUNT(*) FROM payments GROUP BY status;
```

#### 8. **Deliveries** (2 records)
Delivery logistics and tracking

#### 9. **Delivery Tasks** (3 records)
Individual delivery/pickup tasks

#### 10. **Pickup Requests** (2 records)
Pickup scheduling and status

#### 11. **Reviews** (1 record)
Customer reviews and ratings

#### 12. **Notifications** (5 records)
User notifications for rental events

#### 13. **AI Recommendations** (4 records)
Personalized product recommendations with affinity scores (0-100)

#### 14. **Demand Predictions** (8 records)
Daily demand forecasts for each product

#### 15. **Audit Logs** (0 records)
Audit trail for data changes (supporting table)

## Key Features

### Data Constraints
- ✓ Foreign key constraints enforced
- ✓ CHECK constraints for business rules
- ✓ UNIQUE constraints for identity fields
- ✓ NOT NULL constraints for required fields
- ✓ Price range validation (₹50-₹500)
- ✓ Role validation (Customer, Delivery_Partner, Admin)
- ✓ Category validation (Indoor, Outdoor)

### Indexes
- 67+ indexes for optimal query performance
- Indexes on all foreign keys
- Indexes on frequently queried columns (status, dates, locations)
- Composite indexes for common queries

### Sample Data Highlights
**Complete Rental Flow:**
- Tent rental from customer (Priya) to delivery partner (Rajesh)
- Rental session with precise 1-second timing
- Delivery with task tracking
- Payment processing (success)
- Pickup request
- Customer review

**Active Rental:**
- Speaker rental with delivery in-progress
- Real-time tracking capability

## Query Examples

### Get Popular Products
```sql
SELECT name, rental_count, average_rating 
FROM products 
ORDER BY rental_count DESC 
LIMIT 5;
```

### Customer Rental History
```sql
SELECT r.id, p.name, r.start_time, r.end_time, r.total_amount 
FROM rental_sessions r
JOIN products p ON r.product_id = p.id
WHERE r.user_id = 'user-1'
ORDER BY r.created_at DESC;
```

### Delivery Partner Performance
```sql
SELECT u.name, COUNT(d.id) as deliveries, AVG(u.rating) as avg_rating
FROM deliveries d
JOIN users u ON d.assigned_partner_id = u.id
GROUP BY d.assigned_partner_id;
```

### AI Recommendations by User
```sql
SELECT u.name, p.name, ar.affinity_score, ar.recommendation_type
FROM ai_recommendations ar
JOIN users u ON ar.user_id = u.id
JOIN products p ON ar.product_id = p.id
WHERE ar.was_clicked = 1;
```

### Demand Forecast
```sql
SELECT p.name, dp.predicted_demand, dp.confidence_interval_lower, dp.confidence_interval_upper
FROM demand_predictions dp
JOIN products p ON dp.product_id = p.id
WHERE dp.prediction_date = DATE('now');
```

## API Integration

The database is configured for FastAPI backend integration:

```python
DATABASE_URL = "sqlite:///../database/quick_tym.db"
```

See `backend/app/models.py` for SQLAlchemy ORM model definitions.

## Backup & Recovery

### Backup Database
```bash
# Simple copy
cp database/quick_tym.db database/quick_tym.db.backup

# Or use SQLite backup
sqlite3 database/quick_tym.db ".backup database/quick_tym.db.backup"
```

### Restore Database
```bash
cp database/quick_tym.db.backup database/quick_tym.db
```

## Performance Considerations

### Query Optimization
- All tables have appropriate indexes
- Foreign key indexes for joins
- Status columns indexed for filtering
- Date columns indexed for time-range queries

### SQLite Pragmas
```sql
PRAGMA foreign_keys = ON;        -- Enforce referential integrity
PRAGMA journal_mode = WAL;        -- Write-Ahead Logging for better concurrency
PRAGMA synchronous = NORMAL;      -- Balanced durability/performance
PRAGMA cache_size = -64000;       -- 64MB cache
```

## Development Workflow

### 1. Initialize Database
```bash
python database/init_auto.py
```

### 2. Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 3. Start Frontend
```bash
cd frontend
npm run dev
```

### 4. Access Application
- Frontend: http://localhost:5173
- Backend API: http://127.0.0.1:8000
- API Docs: http://127.0.0.1:8000/docs

## Troubleshooting

### Database Locked
```sql
-- Check for uncommitted transactions
PRAGMA integrity_check;

-- Re-initialize if necessary
python database/init_auto.py
```

### Foreign Key Violations
Ensure all `init_auto.py` steps complete successfully:
```bash
python database/init_auto.py
```

### Indexes Not Found
Verify schema applied:
```bash
sqlite3 quick_tym.db ".indexes"
```

## Migration to Production

### PostgreSQL Migration
For production, migrate to PostgreSQL:
1. Use Alembic for database migrations
2. Update `DATABASE_URL` in `.env`
3. Run migration scripts
4. Update connection pooling settings

### Data Export
```bash
# Export to CSV
sqlite3 quick_tym.db ".mode csv" ".output products.csv" "SELECT * FROM products;"
```

## Support

- Database errors: Check logs in `backend/logs/`
- Schema questions: See `.kiro/specs/quick-tym/design.md`
- API integration: See `backend/app/models.py`

## License

Quick Tym © 2024. All rights reserved.
