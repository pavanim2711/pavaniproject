"""Security utilities for password hashing with bcrypt."""
import bcrypt


def hash_password(password: str) -> str:
    """Generate bcrypt hash of password.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        bcrypt hashed password string
    """
    # Bcrypt has a 72-byte limit
    password = password[:72]
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: bcrypt hashed password to check against
        
    Returns:
        True if password matches, False otherwise
    """
    # Bcrypt has a 72-byte limit
    plain_password = plain_password[:72]
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def is_password_hashed(password: str) -> bool:
    """Check if a password string is already hashed.
    
    Args:
        password: Password string to check
        
    Returns:
        True if password appears to be hashed, False otherwise
    """
    # Bcrypt hashes start with $2b$, $2a$, or $2y$
    return password.startswith("$2")

