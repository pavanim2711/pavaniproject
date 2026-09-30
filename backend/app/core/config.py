"""Core configuration module."""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings."""
    
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    DATABASE_URL: str = "sqlite:///./quicktym.db"
    
    SECRET_KEY: str = "quick-tym-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    
    PAYMENT_MOCK_MODE: bool = True
    
    LOG_LEVEL: str = "INFO"
    
    # Email Configuration
    EMAIL_BACKEND: str = "console"  # Options: console, smtp
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: str = "noreply@quicktym.com"
    SMTP_USE_TLS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()