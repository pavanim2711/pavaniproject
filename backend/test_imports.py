"""Quick test of backend imports."""
import sys
sys.path.insert(0, '.')

try:
    from app.core.config import settings
    from app.db.session import engine, SessionLocal
    from app.models.user import User
    from app.core.security import hash_password
    from app.core.jwt import create_access_token
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
