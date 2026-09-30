# QuickTym Project - Troubleshooting Guide

## 🆘 Common Issues & Solutions

### 1. Frontend Won't Start (Port 5173)

**Error:** `EADDRINUSE: address already in use :::5173`

**Solution:**
```bash
# Option 1: Kill process using port 5173
# On Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Option 2: Use different port
cd frontend
npm run dev -- --port 5174
```

---

### 2. Backend Won't Start (Port 8000)

**Error:** `Address already in use` or `ModuleNotFoundError`

**Solution:**
```bash
# Kill existing process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall

# Start backend
python -m uvicorn app.main:app --reload --port 8000
```

---

### 3. Database Connection Failed

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'database/quick_tym.db'`

**Solution:**
```bash
# Verify database exists
dir database\quick_tym.db

# If missing, recreate it:
cd database
python init.py

# Verify connection:
python verify_tables.py
```

---

### 4. Module Not Found Errors (Python)

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
cd backend

# Clear pip cache and reinstall
pip cache purge
pip install -r requirements.txt --no-cache-dir

# Verify installation
pip list | findstr fastapi
```

---

### 5. npm Dependencies Issues

**Error:** `Failed to load PostCSS config` or `SyntaxError in package.json`

**Solution:**
```bash
cd frontend

# Clear node_modules and reinstall
rmdir /s /q node_modules
del package-lock.json
npm install

# Approve pending scripts
npm approve-scripts esbuild
```

---

### 6. CORS Error (Frontend → Backend)

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
- Verify backend is running on port 8000
- Check `vite.config.ts` has proxy configured:
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  },
}
```
- Ensure backend CORS allows localhost:5173 in `app/main.py`

---

### 7. TypeScript Compilation Errors

**Error:** Various TypeScript errors in frontend

**Solution:**
```bash
cd frontend

# Clear Vite cache
rmdir /s /q node_modules\.vite

# Reinstall
npm install

# Rebuild
npm run build
```

---

### 8. Database Tables Not Found

**Error:** `sqlite3.OperationalError: no such table: users`

**Solution:**
```bash
# Verify tables
cd database
python verify_tables.py

# If missing, initialize:
python init.py

# Check schema
python -c "import sqlite3; db = sqlite3.connect('quick_tym.db'); print([t[0] for t in db.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")])"
```

---

### 9. Port Already in Use (Both Servers)

**Solution for Windows:**
```powershell
# Find and kill process by port
netstat -ano | findstr :5173  # Frontend
netstat -ano | findstr :8000  # Backend

taskkill /PID <PID> /F

# Or use automatic startup script that handles this
.\START_PROJECT.ps1
```

---

### 10. API Returns 404 on Frontend Requests

**Error:** API calls returning 404 Not Found

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check proxy configuration in `vite.config.ts`
3. Ensure API paths are correct (e.g., `/api/v1/products`)
4. Check backend routers are registered in `app/main.py`

```bash
# Test API directly
curl http://localhost:8000/api/v1/products
```

---

## 🔍 Verification Commands

### Check if Servers are Running
```bash
# Frontend
curl http://localhost:5173 || echo "Frontend not running"

# Backend
curl http://localhost:8000/health || echo "Backend not running"
```

### Check Database
```bash
python database/verify_tables.py
```

### Test API
```bash
# Health check
curl http://localhost:8000/health

# Get products
curl http://localhost:8000/api/v1/products

# Login
curl -X POST http://localhost:8000/api/v1/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"john@example.com\",\"password\":\"Password123\"}"
```

### View Logs
```bash
# Frontend logs are shown in the terminal where npm run dev is running
# Backend logs are shown in the terminal where uvicorn is running

# Or view system event logs
Get-EventLog -LogName Application -Source uvicorn
```

---

## 🛠️ Complete Reset (If Nothing Works)

```bash
# 1. Stop all servers (kill processes on ports 5173 and 8000)
netstat -ano | findstr :5173
taskkill /PID <PID> /F
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# 2. Clean frontend
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
npm approve-scripts esbuild

# 3. Clean backend cache
cd ../backend
rmdir /s /q __pycache__
rmdir /s /q app/__pycache__
pip cache purge
pip install -r requirements.txt --force-reinstall

# 4. Reset database (CAUTION: This deletes data!)
cd ../database
del quick_tym.db
python init.py

# 5. Restart both servers
# Terminal 1:
cd frontend && npm run dev

# Terminal 2:
cd backend && python -m uvicorn app.main:app --reload --port 8000
```

---

## 📞 Additional Resources

- **Vite Docs:** https://vitejs.dev/
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **SQLite Docs:** https://www.sqlite.org/docs.html

---

## ✅ Verification Checklist

Before submitting, verify:

- [ ] Frontend running on localhost:5173
- [ ] Backend running on localhost:8000
- [ ] Database file exists at `database/quick_tym.db`
- [ ] All 15 tables created in database
- [ ] Sample data loaded (53 records)
- [ ] API health check returns 200 OK
- [ ] Frontend can load without errors
- [ ] No CORS errors in browser console
- [ ] Login page loads and is accessible
- [ ] API documentation available at localhost:8000/docs

---

**Last Updated:** 2026-08-14
