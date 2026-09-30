# QuickTym Project Startup Script (PowerShell)
# Usage: .\START_PROJECT.ps1

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   QuickTym Project Startup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Get project root
$projectRoot = Split-Path -Parent $PSCommandPath
Set-Location $projectRoot

# Check Node.js
$nodeCheck = node --version 2>$null
if ($null -eq $nodeCheck) {
    Write-Host "❌ Node.js is not installed. Please install Node.js first." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Node.js found: $nodeCheck" -ForegroundColor Green

# Check Python
$pythonCheck = python --version 2>$null
if ($null -eq $pythonCheck) {
    Write-Host "❌ Python is not installed. Please install Python first." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Python found: $pythonCheck" -ForegroundColor Green
Write-Host ""

# Check database
$dbPath = "$projectRoot\database\quick_tym.db"
if (-not (Test-Path $dbPath)) {
    Write-Host "❌ Database not found at: $dbPath" -ForegroundColor Red
    Write-Host "   Please run the database setup first. See: database/SETUP_SUMMARY.md" -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Database found at: $dbPath" -ForegroundColor Green
Write-Host ""

# Start backend
Write-Host "Starting backend server on port 8000..." -ForegroundColor Yellow
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\backend'; python -m uvicorn app.main:app --reload --port 8000"
Start-Sleep -Seconds 2

# Start frontend
Write-Host "Starting frontend server on port 5173..." -ForegroundColor Yellow
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$projectRoot\frontend'; npm run dev"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "   ✅ QuickTym is starting!" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "📍 Frontend:    http://localhost:5173" -ForegroundColor Green
Write-Host "📍 Backend:     http://localhost:8000" -ForegroundColor Green
Write-Host "📍 API Docs:    http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C in either window to stop the server." -ForegroundColor Yellow
Write-Host ""

# Keep main window open
Read-Host "Press Enter to exit this window"
