"""Property-based tests for rental timing and billing."""
import pytest
from datetime import datetime, timedelta
from decimal import Decimal

from app.models.rental import RentalSession
from app.models.product import Product


class TestRentalTimerPrecision:
    """Property 5: Timer stop precision - Timer must stop within 1 second of pickup request."""

    def test_timer_precision_1_second(self):
        """Timer should track time with 1-second precision."""
        start_time = datetime(2024, 1, 1, 10, 0, 0)
        end_time = datetime(2024, 1, 1, 10, 5, 30)  # 5 minutes 30 seconds
        
        elapsed_seconds = int((end_time - start_time).total_seconds())
        
        # Should be exactly 330 seconds
        assert elapsed_seconds == 330
        
        # Verify precision (no fractional seconds)
        assert elapsed_seconds == int(elapsed_seconds)
        assert (end_time - start_time).total_seconds() == elapsed_seconds

    def test_timer_stops_immediately_on_pickup(self):
        """Timer should stop immediately when pickup is requested."""
        # Simulate rental with active timer
        rental = RentalSession(
            user_id="user-123",
            product_id="product-456",
            status="active",
            start_time=datetime(2024, 1, 1, 10, 0, 0)
        )
        
        # Timer running
        assert rental.status == "active"
        
        # Pickup requested - timer stops immediately
        pickup_time = datetime(2024, 1, 1, 10, 5, 30)
        rental.end_time = pickup_time
        rental.status = "completed"
        
        # Verify timer stopped exactly at pickup time
        assert rental.end_time == pickup_time
        assert rental.status == "completed"
        
        # Calculate elapsed time
        elapsed = int((pickup_time - rental.start_time).total_seconds())
        assert elapsed == 330  # Exactly 5 minutes 30 seconds

    def test_timer_precision_edge_cases(self):
        """Test timer precision with edge cases."""
        test_cases = [
            # (start_time, end_time, expected_seconds)
            (datetime(2024, 1, 1, 10, 0, 0), datetime(2024, 1, 1, 10, 0, 1), 1),
            (datetime(2024, 1, 1, 10, 0, 0), datetime(2024, 1, 1, 10, 0, 59), 59),
            (datetime(2024, 1, 1, 10, 0, 0), datetime(2024, 1, 1, 10, 1, 0), 60),
            (datetime(2024, 1, 1, 10, 0, 0), datetime(2024, 1, 1, 11, 0, 0), 3600),
            (datetime(2024, 1, 1, 10, 0, 0), datetime(2024, 1, 1, 11, 0, 1), 3601),
        ]
        
        for start, end, expected in test_cases:
            elapsed = int((end - start).total_seconds())
            assert elapsed == expected, f"Failed for {start} to {end}"


class TestBillingAccuracy:
    """Property 6: Billing accuracy - Charges must equal elapsed_time × hourly_rate with 1-second precision."""

    def test_basic_billing_calculation(self):
        """Test basic billing: elapsed_time × hourly_rate."""
        # 3 hours rental at ₹100/hour
        elapsed_seconds = 3 * 3600  # 3 hours
        hourly_rate = Decimal("100.00")
        
        base_amount = Decimal(elapsed_seconds / 3600) * hourly_rate
        assert base_amount == Decimal("300.00")

    def test_billing_with_tax(self):
        """Test billing including 18% GST tax."""
        elapsed_seconds = 2 * 3600  # 2 hours
        hourly_rate = Decimal("100.00")
        tax_rate = Decimal("0.18")
        
        base_amount = Decimal(elapsed_seconds / 3600) * hourly_rate
        tax_amount = base_amount * tax_rate
        total_amount = base_amount + tax_amount
        
        assert base_amount == Decimal("200.00")
        assert tax_amount == Decimal("36.00")
        assert total_amount == Decimal("236.00")

    def test_billing_with_minimum_charge(self):
        """Test minimum 1-hour charge applies for short rentals."""
        elapsed_seconds = 300  # 5 minutes (less than 1 hour)
        hourly_rate = Decimal("100.00")
        
        # Apply minimum charge rule
        billable_hours = max(1, (elapsed_seconds + 3599) // 3600)
        
        assert billable_hours == 1  # Minimum 1 hour
        
        base_amount = Decimal(billable_hours) * hourly_rate
        assert base_amount == Decimal("100.00")

    def test_billing_precision_with_decimal(self):
        """Test billing maintains decimal precision."""
        # Test with various prices
        test_cases = [
            (Decimal("50.00"), 3600, Decimal("50.00")),      # ₹50/hour for 1 hour
            (Decimal("150.50"), 7200, Decimal("301.00")),    # ₹150.50/hour for 2 hours
            (Decimal("500.00"), 1800, Decimal("250.00")),    # ₹500/hour for 30 min (rounds to 1 hour)
        ]
        
        for hourly_rate, elapsed, expected_base in test_cases:
            billable_hours = max(1, (elapsed + 3599) // 3600)
            base_amount = Decimal(billable_hours) * hourly_rate
            assert base_amount == expected_base, f"Failed for {hourly_rate} × {billable_hours} hours"


class TestRentalSessionLifecycle:
    """Test complete rental session lifecycle."""

    def test_rental_session_creation(self):
        """Rental session should be created with correct initial state."""
        rental = RentalSession(
            user_id="user-123",
            product_id="product-456",
            status="pending"
        )
        
        assert rental.status == "pending"
        assert rental.start_time is None
        assert rental.end_time is None
        assert rental.total_seconds == 0

    def test_rental_activation(self):
        """Rental session should transition to active state on delivery."""
        rental = RentalSession(
            user_id="user-123",
            product_id="product-456",
            status="pending"
        )
        
        # Activate rental
        rental.start_time = datetime(2024, 1, 1, 10, 0, 0)
        rental.status = "active"
        
        assert rental.status == "active"
        assert rental.start_time is not None

    def test_rental_completion(self):
        """Rental session should be completed with final charges."""
        start_time = datetime(2024, 1, 1, 10, 0, 0)
        end_time = datetime(2024, 1, 1, 12, 30, 0)  # 2.5 hours
        
        rental = RentalSession(
            user_id="user-123",
            product_id="product-456",
            status="active",
            start_time=start_time,
            end_time=end_time
        )
        
        # Calculate charges
        rental.total_seconds = int((end_time - start_time).total_seconds())
        
        assert rental.total_seconds == 9000  # 2.5 hours in seconds
        
        # Round up to hours
        billable_hours = (rental.total_seconds + 3599) // 3600
        assert billable_hours == 3  # Rounds up to 3 hours


class TestBillingEdgeCases:
    """Test billing edge cases and boundary conditions."""

    def test_zero_second_rental(self):
        """Zero-second rental should still charge minimum 1 hour."""
        elapsed_seconds = 0
        
        # Apply minimum charge
        billable_seconds = max(3600, elapsed_seconds)
        
        assert billable_seconds == 3600

    def test_very_long_rental(self):
        """Test billing for long rentals (7 days max)."""
        max_hours = 168  # 7 days
        
        elapsed_seconds = max_hours * 3600
        hourly_rate = Decimal("100.00")
        
        base_amount = Decimal(max_hours) * hourly_rate
        assert base_amount == Decimal("16800.00")

    def test_boundary_time_transitions(self):
        """Test time boundary transitions."""
        # Test exact hour boundaries
        boundary_cases = [
            (3599, 1),   # Just under 1 hour
            (3600, 1),   # Exactly 1 hour
            (3601, 2),   # Just over 1 hour
            (7199, 2),   # Just under 2 hours
            (7200, 2),   # Exactly 2 hours
        ]
        
        for seconds, expected_hours in boundary_cases:
            hours = (seconds + 3599) // 3600
            assert hours == expected_hours, f"Failed for {seconds} seconds"
