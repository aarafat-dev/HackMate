"""
HackMate v2.0 - Engagement Model
Represents a penetration testing engagement/project.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class EngagementStatus(str, enum.Enum):
    """Valid statuses for an engagement."""
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class Engagement(Base):
    """
    Engagement model - represents a penetration testing project.
    
    Attributes:
        id: Unique UUID identifier
        name: Name of the engagement (e.g., "ACME Corp Q1 Assessment")
        target: Primary target (domain, IP, or range)
        scope: Description of what's in-scope
        status: Current engagement status
        created_at: When the engagement was created
        updated_at: Last modification timestamp
    """
    __tablename__ = "engagements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False, index=True)
    target = Column(String(500), nullable=False)
    scope = Column(Text, nullable=True)
    status = Column(
        String(20),
        default=EngagementStatus.PLANNING.value,
        index=True
    )
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    phases = relationship("Phase", back_populates="engagement", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="engagement", cascade="all, delete-orphan")
    scans = relationship("Scan", back_populates="engagement", cascade="all, delete-orphan")
    terminal_history = relationship("TerminalHistory", back_populates="engagement", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="engagement", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="engagement", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Engagement(id={self.id}, name={self.name}, status={self.status})>"
