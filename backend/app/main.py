"""
Quick Tym Rental Platform - Main Application Entry Point

This module initializes the FastAPI application with all configurations,
database connections, and API routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.db.base import Base
from app import routers


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="Quick Tym Rental API",
        description="AI-powered rental platform for short-term product rentals",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Include routers
    app.include_router(routers.auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(routers.products.router, prefix="/api/v1", tags=["Products"])
    app.include_router(routers.rentals.router, prefix="/api/v1", tags=["Rentals"])
    app.include_router(routers.deliveries.router, prefix="/api/v1", tags=["Deliveries"])
    app.include_router(routers.payments.router, prefix="/api/v1", tags=["Payments"])
    app.include_router(routers.admin.router, prefix="/api/v1/admin", tags=["Admin"])
    app.include_router(routers.ai.router, prefix="/api/v1/ai", tags=["AI Features"])
    app.include_router(routers.recommendations.router, prefix="/api/v1", tags=["AI Recommendations"])
    app.include_router(routers.reviews.router, prefix="/api/v1", tags=["Reviews"])
    app.include_router(routers.websocket.websocket, prefix="/ws", tags=["WebSocket"])
    app.include_router(routers.websocket.notifications_router, prefix="/api/v1", tags=["Notifications"])
    app.include_router(routers.inventory.router, prefix="/api/v1", tags=["Inventory"])
    app.include_router(routers.demand_prediction.router, prefix="/api/v1", tags=["Demand Prediction"])
    
    return app


# Create application instance
app = create_app()


@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy", "service": "quick-tym-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
