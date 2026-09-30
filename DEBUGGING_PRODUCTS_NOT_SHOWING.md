# Debugging: Products Not Showing

## Quick Debug Steps

### Step 1: Open Browser Console
1. Press **F12** to open DevTools
2. Go to **Console** tab
3. Look for any error messages (they'll be in red)

### Step 2: Check What API URL is Being Used
In the Console, paste this and press Enter:
```javascript
console.log('API URL being used:', window.location.origin + '/api/v1/products/')
```

### Step 3: Check Network Tab
1. Open DevTools (F12)
2. Click **Network** tab
3. Reload the page (F5)
4. Look for any red requests (errors)
5. Click on `/api/v1/products/` request
6. Check the Response tab to see the actual data

### Step 4: Manual API Test
In the Console, paste this:
```javascript
fetch('/api/v1/products/')
  .then(r => r.json())
  .then(d => console.log('Products:', d))
  .catch(e => console.error('Error:', e))
```

---

## What Should Happen

### If API Works
- Console should show the products array
- Network tab shows `/api/v1/products/` with status 200
- Products should display on the page

### If API Fails
- Console shows error
- Network tab shows `/api/v1/products/` with status 4xx or 5xx
- Mock products should display as fallback

---

## Common Issues & Solutions

### Issue 1: "Failed to load products" message shows
**Cause**: API returns error, but mock fallback not showing
**Solution**: Refresh page, clear localStorage

### Issue 2: Products are empty
**Cause**: Backend has no products in database
**Solution**: Run this query:
```bash
curl http://172.30.224.1:8000/api/v1/products/
```
If it returns empty array, database needs to be populated.

### Issue 3: 404 error
**Cause**: Backend not accessible or wrong URL
**Solution**: Test direct API:
```bash
# In PowerShell
Invoke-WebRequest -Uri "http://172.30.224.1:8000/api/v1/products/"
```

---

## Frontend Code Changes Made

### File: `frontend/src/pages/HomePage.tsx`
- Changed error handling to use mock products as fallback
- Added console logging for debugging
- Removed error message display

### File: `frontend/src/services/api.ts`
- Added debug logging of API URL
- Uses environment variable `VITE_API_URL`
- Falls back to `http://172.30.224.1:8000/api/v1`

### File: `frontend/.env`
- Set `VITE_API_URL=http://172.30.224.1:8000/api/v1`

### File: `frontend/vite.config.ts`
- Set `host: '0.0.0.0'` to listen on all interfaces
- Proxy configured for `/api/*` routes

---

## Step-by-Step Troubleshooting

1. **Refresh browser** (Ctrl+F5 or Cmd+Shift+R)
2. **Check browser console** (F12 → Console)
3. **Look at network requests** (F12 → Network)
4. **Test API directly** from PowerShell
5. **Check backend logs** for errors
6. **Restart frontend** if .env changed

---

## API Endpoints to Test

```
Direct (from any computer on network):
GET http://172.30.224.1:8000/api/v1/products/

Via Proxy (from browser on same network):
GET http://172.30.224.1:5173/api/v1/products/

Via Vite Dev Proxy:
GET /api/v1/products/  (in browser)
```

---

## Expected Response

Should be a JSON array with products:
```json
[
  {
    "id": "prod-1",
    "name": "Camping Tent (4-person)",
    "price_per_hour": 150,
    "category": "Outdoor",
    ...
  },
  ...
]
```

---

## Files to Check

1. `frontend/.env` - API URL configuration
2. `frontend/vite.config.ts` - Dev server config
3. `frontend/src/services/api.ts` - Axios instance
4. `frontend/src/pages/HomePage.tsx` - Product fetching logic
5. Backend logs - Incoming requests

---

## Contact Points

- Frontend Port: 5173
- Backend Port: 8000
- Frontend IP: 172.30.224.1
- Backend IP: 172.30.224.1
