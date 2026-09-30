"""JWT token generation and verification utilities."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import jwt, JWTError

from app.core.config import settings


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Create a new JWT access token.
    
    Args:
        data: Dictionary containing token payload data (sub, role, permissions)
        expires_delta: Optional token expiration time (default: 24 hours)
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT access token.
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Decoded token payload dictionary, or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None


def get_token_expiration(token: str) -> Optional[datetime]:
    """Get the expiration time of a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Expiration datetime, or None if invalid
    """
    payload = verify_access_token(token)
    if payload:
        exp = payload.get("exp")
        if exp:
            return datetime.utcfromtimestamp(exp)
    return None


def is_token_expired(token: str) -> bool:
    """Check if a JWT token has expired.
    
    Args:
        token: JWT token string
        
    Returns:
        True if token is expired, False otherwise
    """
    return verify_access_token(token) is None


def decode_token(token: str) -> Dict[str, Any]:
    """Decode a JWT token without verification.
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload dictionary
        
    Raises:
        JWTError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise
