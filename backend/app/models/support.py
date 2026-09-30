"""Support ticket system models."""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from app.db.base import Base


class TicketStatus(str, enum.Enum):
    """Ticket status enum."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, enum.Enum):
    """Ticket priority enum."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketCategory(str, enum.Enum):
    """Ticket category enum."""
    RENTAL_ISSUE = "rental_issue"
    PAYMENT_ISSUE = "payment_issue"
    DELIVERY_ISSUE = "delivery_issue"
    PRODUCT_ISSUE = "product_issue"
    REFUND_REQUEST = "refund_request"
    ACCOUNT_ISSUE = "account_issue"
    OTHER = "other"


class SupportTicket(Base):
    """Support ticket model."""
    __tablename__ = "support_tickets"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    rental_id = Column(String(36), ForeignKey("rental_sessions.id"), nullable=True)
    
    # Ticket details
    ticket_number = Column(String(20), unique=True, nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(Enum(TicketCategory), default=TicketCategory.OTHER)
    priority = Column(Enum(TicketPriority), default=TicketPriority.MEDIUM)
    status = Column(Enum(TicketStatus), default=TicketStatus.OPEN)
    
    # Assignment
    assigned_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    assigned_at = Column(DateTime, nullable=True)
    
    # Resolution
    resolution = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id], backref="support_tickets")
    rental = relationship("RentalSession", foreign_keys=[rental_id])
    messages = relationship("TicketMessage", back_populates="ticket", cascade="all, delete-orphan")
    assignee = relationship("User", foreign_keys=[assigned_to])
    resolver = relationship("User", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<SupportTicket {self.ticket_number}>"
    
    @property
    def is_open(self) -> bool:
        """Check if ticket is still open."""
        return self.status not in [TicketStatus.RESOLVED, TicketStatus.CLOSED]


class TicketMessage(Base):
    """Ticket message model for conversations."""
    __tablename__ = "ticket_messages"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String(36), ForeignKey("support_tickets.id"), nullable=False)
    sender_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    message = Column(Text, nullable=False)
    attachments = Column(String(500), nullable=True)  # JSON string of file URLs
    
    is_internal = Column(Integer, default=0)  # 1 for internal notes (staff only)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    ticket = relationship("SupportTicket", back_populates="messages")
    sender = relationship("User", backref="ticket_messages")
    
    def __repr__(self):
        return f"<TicketMessage {self.id}>"


class TicketAttachment(Base):
    """Ticket attachment model."""
    __tablename__ = "ticket_attachments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String(36), ForeignKey("support_tickets.id"), nullable=False)
    message_id = Column(String(36), ForeignKey("ticket_messages.id"), nullable=True)
    
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(50), nullable=True)
    file_size = Column(Integer, nullable=True)
    
    uploaded_by = Column(String(36), ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ticket = relationship("SupportTicket", backref="attachments")
    message = relationship("TicketMessage", backref="attachment_files")
    uploader = relationship("User", backref="uploaded_attachments")
    
    def __repr__(self):
        return f"<TicketAttachment {self.file_name}>"


class TicketEscalation(Base):
    """Ticket escalation tracking."""
    __tablename__ = "ticket_escalations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ticket_id = Column(String(36), ForeignKey("support_tickets.id"), nullable=False)
    
    escalated_from = Column(String(36), ForeignKey("users.id"), nullable=True)
    escalated_to = Column(String(36), ForeignKey("users.id"), nullable=True)
    reason = Column(Text, nullable=True)
    
    escalated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    ticket = relationship("SupportTicket", backref="escalations")
    from_user = relationship("User", foreign_keys=[escalated_from])
    to_user = relationship("User", foreign_keys=[escalated_to])
    
    def __repr__(self):
        return f"<TicketEscalation {self.ticket_id}>"
