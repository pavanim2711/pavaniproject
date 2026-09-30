# QuickTym - Quick Reference

## Run the Platform (From Project Root)

### Window 1: Start Backend
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

### Window 2: Start Frontend
```powershell
cd frontend
npm run dev
```

✓ Backend: http://localhost:8000
✓ Frontend: http://localhost:5173
✓ API Docs: http://localhost:8000/docs

---

## Test Flow (In Browser)

1. **Visit**: http://localhost:5173/register
2. **Fill out**: Name, Email, Password, Role (Customer)
3. **Click**: "Create account"
4. **Redirects to**: /login
5. **Enter**: Email & Password
6. **Click**: "Login"
7. **Now on**: Homepage with all products
8. **Click**: Any product → Detail page
9. **Click**: "Rent Now" → 3-step checkout

---

## API Test (PowerShell)

```powershell
# 1. Register
$body = @{ name="John"; email="john@test.com"; password="pass123"; role="Customer" } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/auth/register" -Method POST -Body $body -ContentType "application/json"

# 2. Login (get token)
$body = @{ email="john@test.com"; password="pass123" } | ConvertTo-Json
$login = Invoke-WebRequest -Uri "http://localhost:8000/api/v1/auth/login" -Method POST -Body $body -ContentType "application/json"
$token = ($login.Content | ConvertFrom-Json).access_token

# 3. Get products
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/products/"

# 4. Get single product
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/products/prod-1"
```

---

## Key Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/v1/auth/register` | POST | ✗ | Create new account |
| `/api/v1/auth/login` | POST | ✗ | Login & get JWT |
| `/api/v1/auth/me` | GET | ✓ | Get current user |
| `/api/v1/products/` | GET | ✗ | List all products |
| `/api/v1/products/{id}` | GET | ✗ | Get product detail |
| `/api/v1/rentals/` | GET | ✓ | User's rentals |
| `/api/v1/payments/` | POST | ✓ | Process payment |

---

## What Was Fixed Today

### Problem
Authentication endpoints returning **404 Not Found**:
- `POST /api/v1/auth/register` → 404
- `POST /api/v1/auth/login` → 404

### Root Cause
Router had duplicate prefix:
```python
# ❌ WRONG (double prefix)
router = APIRouter(prefix="/auth")  # In router file
app.include_router(router, prefix="/api/v1/auth")  # In main.py
# Results in: /api/v1/auth/auth/register
```

### Solution
Removed redundant prefix:
```python
# ✓ CORRECT (single prefix)
router = APIRouter()  # No prefix here
app.include_router(router, prefix="/api/v1/auth")  # Only here
# Results in: /api/v1/auth/register
```

### Files Changed
1. `backend/app/routers/auth.py` - Fixed router prefix
2. `backend/app/core/security.py` - Improved bcrypt handling
3. `frontend/.env` - Created API configuration

---

## Current Database

- **Location**: `database/quick_tym.db`
- **Tables**: 15 (users, products, rentals, payments, deliveries, reviews, etc.)
- **Records**: 53 sample records
- **Status**: ✓ Fully populated and accessible

### Sample Products
- Camping Tent (₹150/hr)
- Bluetooth Speaker (₹80/hr)
- Power Drill Set (₹100/hr)
- Portable Projector (₹200/hr)
- Folding Table (₹90/hr)
- And 8 more...

---

## Features Implemented

✓ User Registration & Login with JWT
✓ Product Catalog (15 products)
✓ Product Detail Pages
✓ 3-Step Rental Checkout
  - Step 1: Rental Details (dates, duration)
  - Step 2: Payment Info (card details)
  - Step 3: Order Confirmation
✓ Category Filtering
✓ Real Database (SQLite)
✓ Responsive UI (React + Tailwind)
✓ CORS Configured for local development
✓ Protected API Endpoints
✓ Automatic Token Management

---

## Troubleshooting

**Backend won't start**
```powershell
# Verify Python version (need 3.10+)
python --version

# Reinstall packages
cd backend && pip install -r requirements.txt

# Try again
python -m uvicorn app.main:app --reload --port 8000
```

**Frontend shows "Connection refused"**
```powershell
# Check backend is running
netstat -an | findstr 8000

# Verify .env in frontend folder has:
VITE_API_URL=http://localhost:8000/api/v1
```

**Auth endpoints still broken**
```powershell
# Restart backend (hot reload may have missed changes)
# Kill and restart the backend process
```

---

## Next Steps (When Ready)

1. **User Testing**: Register, login, browse products, rent items
2. **Payment Integration**: Connect real payment processor
3. **Email Notifications**: Send order confirmations & updates
4. **Admin Dashboard**: Manage products, view orders
5. **Delivery Features**: Track shipments, manage delivery partners
6. **Advanced Search**: Filter by price, rating, availability
7. **User Reviews**: Leave feedback on rentals

---

**Status**: ✓ MVP Complete - Ready to Test
**Last Updated**: August 14, 2026
