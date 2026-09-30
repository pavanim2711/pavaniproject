"""ai Model - MVP placeholder."""

from datetime import datetime
from sqlalchemy import Column, String, DateTime
import uuid

from app.db.session import Base


class Ai(Base):
    """Ai model - MVP placeholder."""
    __tablename__ = "ais"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<Ai(id={self.id})>"
