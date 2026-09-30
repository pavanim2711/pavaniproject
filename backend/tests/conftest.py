"""Pytest configuration and test fixtures for Quick Tym backend."""
import pytest
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from typing import AsyncGenerator

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session

# Import models and schemas
from app.core.config import Settings
from app.core.database import Base, get_db
from app.main import app


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_quick_tym.db"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    """Set up test database before running tests."""
    engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Cleanup - close connection and remove test database
    await engine.dispose()


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create database session for tests."""
    engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        await db.close()


@pytest.fixture
def test_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "name": "Test User",
        "role": "Customer",
        "phone": "9876543210",
        "address": {"city": "Bengaluru", "state": "Karnataka", "pincode": "560001"}
    }


@pytest.fixture
def test_product_data():
    """Sample product data for testing."""
    return {
        "name": "Test Product",
        "category": "Indoor",
        "description": "A test product for rental",
        "price_per_hour": Decimal("100.00"),
        "min_rental_hours": 1,
        "max_rental_hours": 24,
        "specifications": {"weight": "5kg", "dimensions": "10x10x10cm"},
        "image_url": "https://example.com/test-product.jpg"
    }


@pytest.fixture
def test_rental_data(test_user_data, test_product_data):
    """Sample rental session data for testing."""
    return {
        "user_id": "test-user-id",
        "product_id": "test-product-id",
        "status": "pending",
        "delivery_address": {"city": "Bengaluru", "state": "Karnataka"}
    }


@pytest.fixture
def test_delivery_data():
    """Sample delivery data for testing."""
    return {
        "rental_session_id": "test-rental-id",
        "status": "pending",
        "delivery_address": {"city": "Bengaluru", "state": "Karnataka"},
        "pickup_address": {"city": "Bengaluru", "state": "Karnataka"}
    }


@pytest.fixture
def test_payment_data():
    """Sample payment data for testing."""
    return {
        "rental_id": "test-rental-id",
        "user_id": "test-user-id",
        "amount": Decimal("118.00"),
        "currency": "INR",
        "payment_method": "credit_card",
        "card_last4": "1234",
        "card_brand": "Visa"
    }


@pytest.fixture
def client(db_session):
    """Create test client with override dependency."""
    from fastapi.testclient import TestClient
    
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_header(client, test_user_data):
    """Create authenticated header for tests."""
    # First register the user
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 201
    
    # Then login to get token
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
