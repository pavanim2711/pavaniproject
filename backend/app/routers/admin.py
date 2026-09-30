"""admin router - placeholder for API routes."""
from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/")
async def list_admin():
    """List admin."""
    return {"message": "admin endpoint - MVP placeholder"}
