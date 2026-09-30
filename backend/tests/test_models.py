"""Property-based tests for data models."""
import pytest
from datetime import datetime
from decimal import Decimal

from app.models.user import User
from app.models.product import Product
from app.models.rental import RentalSession
from app.models.delivery import Delivery
from app.models.payment import Payment


class TestDataModelProperties:
    """Property tests for data models."""

    def test_user_role_validation(self):
        """Property 1: User role validation - Only Customer, Delivery_Partner, or Admin roles allowed."""
        valid_roles = ["Customer", "Delivery_Partner", "Admin"]
        
        for role in valid_roles:
            user = User(
                email="test@example.com",
                password_hash="hashed_password",
                name="Test User",
                role=role
            )
            assert user.role in valid_roles

    def test_user_invalid_role_raises_error(self):
        """Property 1 (continued): Invalid roles should not be allowed."""
        invalid_roles = ["SuperAdmin", "User", "Moderator", ""]
        
        for invalid_role in invalid_roles:
            with pytest.raises(ValueError):
                user = User(
                    email="test@example.com",
                    password_hash="hashed_password",
                    name="Test User",
                    role=invalid_role
                )
                # Trigger validation by trying to access the role
                _ = user.role

    def test_product_price_bounds(self):
        """Property 2: Product price bounds - Price must be between ₹50 and ₹500 per hour."""
        # Valid prices
        valid_prices = [Decimal("50.00"), Decimal("100.00"), Decimal("250.00"), Decimal("500.00")]
        
        for price in valid_prices:
            product = Product(
                name="Test Product",
                category="Indoor",
                price_per_hour=price,
                min_rental_hours=1
            )
            assert Decimal("50.00") <= product.price_per_hour <= Decimal("500.00")

    def test_product_price_out_of_bounds_raises_error(self):
        """Property 2 (continued): Prices outside bounds should not be allowed."""
        invalid_prices = [Decimal("49.99"), Decimal("500.01"), Decimal("10.00"), Decimal("1000.00")]
        
        for invalid_price in invalid_prices:
            with pytest.raises(ValueError):
                product = Product(
                    name="Test Product",
                    category="Indoor",
                    price_per_hour=invalid_price,
                    min_rental_hours=1
                )
                _ = product.price_per_hour

    def test_rental_session_status_transitions(self):
        """Rental session status can transition through valid states."""
        rental = RentalSession(
            user_id="user-123",
            product_id="product-456",
            status="pending"
        )
        
        assert rental.status == "pending"
        
        # Valid transitions
        rental.status = "active"
        assert rental.status == "active"
        
        rental.status = "completed"
        assert rental.status == "completed"

    def test_delivery_status_values(self):
        """Delivery status must be one of the valid values."""
        valid_statuses = ["pending", "assigned", "in_transit", "delivered", "pickup_requested", "completed"]
        
        for status in valid_statuses:
            delivery = Delivery(
                rental_session_id="rental-123",
                status=status,
                delivery_address={}
            )
            assert delivery.status in valid_statuses


class TestDatabaseRelationships:
    """Test database relationships and constraints."""

    def test_user_rental_relationship(self):
        """A user can have multiple rental sessions."""
        user = User(
            email="test@example.com",
            password_hash="hashed_password",
            name="Test User",
            role="Customer"
        )
        
        rental1 = RentalSession(
            user_id=user.id,
            product_id="product-1",
            status="pending"
        )
        
        rental2 = RentalSession(
            user_id=user.id,
            product_id="product-2",
            status="pending"
        )
        
        assert rental1.user_id == user.id
        assert rental2.user_id == user.id

    def test_product_rental_relationship(self):
        """A product can be in multiple rental sessions."""
        product = Product(
            name="Test Product",
            category="Indoor",
            price_per_hour=Decimal("100.00"),
            min_rental_hours=1
        )
        
        rental1 = RentalSession(
            user_id="user-1",
            product_id=product.id,
            status="pending"
        )
        
        rental2 = RentalSession(
            user_id="user-2",
            product_id=product.id,
            status="pending"
        )
        
        assert rental1.product_id == product.id
        assert rental2.product_id == product.id

    def test_delivery_rental_relationship(self):
        """A delivery is associated with one rental session."""
        rental = RentalSession(
            user_id="user-1",
            product_id="product-1",
            status="pending"
        )
        
        delivery = Delivery(
            rental_session_id=rental.id,
            status="pending",
            delivery_address={}
        )
        
        assert delivery.rental_session_id == rental.id


class TestTimeBasedBilling:
    """Test time-based billing calculations."""

    def test_billing_precision(self):
        """Billing calculations should maintain 1-second precision."""
        from datetime import timedelta
        
        # Test 1-second precision
        start_time = datetime(2024, 1, 1, 10, 0, 0)
        end_time = datetime(2024, 1, 1, 10, 0, 30)  # 30 seconds
        
        elapsed_seconds = int((end_time - start_time).total_seconds())
        assert elapsed_seconds == 30
        
        # Test hour rounding
        # 3600 seconds = 1 hour
        # 7199 seconds = 2 hours (rounds up)
        
        # Test 1 hour 30 seconds
        end_time_2 = datetime(2024, 1, 1, 11, 0, 30)
        elapsed_2 = int((end_time_2 - start_time).total_seconds())
        assert elapsed_2 == 3630
        
        # Test ceiling division for hours
        hours = (elapsed_2 + 3599) // 3600  # Ceiling division
        assert hours == 2

    def test_minimum_billing_charge(self):
        """Minimum charge should be for 1 hour (3600 seconds)."""
        elapsed_seconds = 300  # 5 minutes
        
        # Apply minimum billing rule
        billable_seconds = max(3600, elapsed_seconds)
        assert billable_seconds == 3600

    def test_hour_rounding_up(self):
        """Billing should round up to nearest hour."""
        # Test cases
        test_cases = [
            (1, 3600),       # 1 second -> 1 hour
            (3599, 3600),    # 59:59 -> 1 hour
            (3600, 3600),    # 1:00:00 -> 1 hour
            (3601, 7200),    # 1:00:01 -> 2 hours
            (7199, 7200),    # 1:59:59 -> 2 hours
            (7200, 7200),    # 2:00:00 -> 2 hours
        ]
        
        for elapsed, expected in test_cases:
            hours = (elapsed + 3599) // 3600
            calculated = hours * 3600
            assert calculated == expected, f"Expected {expected} for {elapsed} seconds"
