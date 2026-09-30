@echo off
REM QuickTym Project Startup Script
REM This script starts both frontend and backend servers

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   QuickTym Project Startup
echo ========================================
echo.

REM Get the project root directory
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%"

REM Check if Node.js is installed
where /q node
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Check if Python is installed
where /q python
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python first.
    pause
    exit /b 1
)

echo ✅ Node.js found: 
node --version
echo.
echo ✅ Python found: 
python --version
echo.

REM Check if database exists
if not exist "%PROJECT_ROOT%database\quick_tym.db" (
    echo ⚠️  Database not found. Please run the database setup first.
    echo    See: database/SETUP_SUMMARY.md
    pause
    exit /b 1
)

echo ✅ Database found at: database\quick_tym.db
echo.

REM Start backend
echo Starting backend server on port 8000...
start "QuickTym Backend" cmd /k "cd backend && python -m uvicorn app.main:app --reload --port 8000"
timeout /t 3 /nobreak

REM Start frontend
echo Starting frontend server on port 5173...
start "QuickTym Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   ✅ QuickTym is starting!
echo ========================================
echo.
echo 📍 Frontend:    http://localhost:5173
echo 📍 Backend:     http://localhost:8000
echo 📍 API Docs:    http://localhost:8000/docs
echo.
echo Press Ctrl+C in either window to stop the server.
echo.
pause
