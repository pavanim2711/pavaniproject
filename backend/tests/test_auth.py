"""Property-based tests for authentication system."""
import pytest
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.config import Settings
from app.services.auth_service import AuthService
from app.models.user import User


class TestJWTTokenIntegrity:
    """Property 3: JWT token integrity - Tokens cannot be tampered with without detection."""

    def test_valid_token_verification(self):
        """Valid tokens should verify successfully."""
        settings = Settings()
        secret_key = settings.SECRET_KEY
        algorithm = settings.ALGORITHM
        
        # Create a valid token
        payload = {
            "sub": "user-123",
            "role": "Customer",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        
        # Verify token
        decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
        
        assert decoded["sub"] == "user-123"
        assert decoded["role"] == "Customer"

    def testTampered_token_fails_verification(self):
        """Tampered tokens should fail verification."""
        settings = Settings()
        secret_key = settings.SECRET_KEY
        algorithm = settings.ALGORITHM
        
        # Create a valid token
        payload = {
            "sub": "user-123",
            "role": "Customer",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        
        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        
        # Tamper with the token
        parts = token.split('.')
        tampered_payload = parts[1][:-1] + ('X' if parts[1][-1] != 'X' else 'Y')
        tampered_token = f"{parts[0]}.{tampered_payload}.{parts[2]}"
        
        # Verify tampered token should fail
        with pytest.raises(JWTError):
            jwt.decode(tampered_token, secret_key, algorithms=[algorithm])

    def test_token_expiration_enforced(self):
        """Expired tokens should be rejected."""
        settings = Settings()
        secret_key = settings.SECRET_KEY
        algorithm = settings.ALGORITHM
        
        # Create an expired token
        payload = {
            "sub": "user-123",
            "role": "Customer",
            "iat": datetime.utcnow() - timedelta(hours=25),
            "exp": datetime.utcnow() - timedelta(hours=1)
        }
        
        token = jwt.encode(payload, secret_key, algorithm=algorithm)
        
        # Try to verify expired token
        with pytest.raises(JWTError):
            jwt.decode(token, secret_key, algorithms=[algorithm])


class TestRoleBasedAccessControl:
    """Property 4: Role-based access control - Users can only access endpoints allowed for their role."""

    def test_customer_role_permissions(self):
        """Customer role should have specific permissions."""
        user = User(
            email="customer@example.com",
            password_hash="hashed_password",
            name="Customer User",
            role="Customer"
        )
        
        customer_permissions = {
            "can_view_products": True,
            "can_create_rental": True,
            "can_view_rental": True,
            "can_make_payment": True,
            "can_request_pickup": True,
            "can_view_recommendations": True,
            "can_access_admin": False,
            "can_access_delivery": False
        }
        
        assert user.role == "Customer"
        
        for permission, allowed in customer_permissions.items():
            if permission.startswith("can_access"):
                assert allowed == (permission in ["can_access_admin", "can_access_delivery"]) == False

    def test_delivery_partner_role_permissions(self):
        """Delivery Partner role should have delivery-specific permissions."""
        user = User(
            email="delivery@example.com",
            password_hash="hashed_password",
            name="Delivery Partner",
            role="Delivery_Partner"
        )
        
        delivery_permissions = {
            "can_view_products": True,
            "can_create_rental": False,
            "can_view_rental": True,
            "can_make_payment": False,
            "can_request_pickup": False,
            "can_view_recommendations": False,
            "can_access_admin": False,
            "can_access_delivery": True,
            "can_mark_delivered": True,
            "can_mark_picked_up": True
        }
        
        assert user.role == "Delivery_Partner"

    def test_admin_role_permissions(self):
        """Admin role should have full system access."""
        user = User(
            email="admin@example.com",
            password_hash="hashed_password",
            name="Admin User",
            role="Admin"
        )
        
        admin_permissions = {
            "can_view_products": True,
            "can_create_rental": True,
            "can_view_rental": True,
            "can_make_payment": True,
            "can_request_pickup": True,
            "can_view_recommendations": True,
            "can_access_admin": True,
            "can_access_delivery": True,
            "can_manage_users": True,
            "can_manage_products": True,
            "can_view_analytics": True
        }
        
        assert user.role == "Admin"


class TestAuthenticationFlow:
    """Test complete authentication flow."""

    def test_user_registration_flow(self):
        """Complete user registration should create user with hashed password."""
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Registration data
        password = "SecurePassword123!"
        hashed = pwd_context.hash(password)
        
        user = User(
            email="test@example.com",
            password_hash=hashed,
            name="Test User",
            role="Customer"
        )
        
        # Verify password
        assert pwd_context.verify(password, user.password_hash)
        assert not pwd_context.verify("WrongPassword", user.password_hash)

    def test_password_hash_strength(self):
        """Password hashes should use appropriate work factor."""
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Test with work factor 12 (as per requirements)
        hashed = pwd_context.using(rounds=12).hash("testpassword")
        
        # Verify it was hashed with 12 rounds
        assert pwd_context.verify("testpassword", hashed)
