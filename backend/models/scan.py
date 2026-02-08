"""
HackMate v2.0 - Scan Model
Represents security scans (nmap, nikto, gobuster, nuclei).
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum


class ScanTool(str, enum.Enum):
    """Supported scanning tools."""
    NMAP = "nmap"
    NIKTO = "nikto"
    GOBUSTER = "gobuster"
    NUCLEI = "nuclei"
    CUSTOM = "custom"


class ScanStatus(str, enum.Enum):
    """Scan execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Scan(Base):
    """
    Scan model - represents a security scan execution.
    
    Attributes:
        id: Unique identifier
        engagement_id: Parent engagement
        tool: Which tool was used (nmap, nikto, etc.)
        target: What was scanned
        command: Full command that was executed
        options: Tool-specific options
        status: Execution status
        output: Raw output from the tool
        parsed_results: Structured results (JSON)
        started_at: When scan began
        completed_at: When scan finished
    """
    __tablename__ = "scans"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engagement_id = Column(String(36), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False, index=True)
    
    tool = Column(String(20), nullable=False, index=True)
    target = Column(String(500), nullable=False)
    command = Column(Text, nullable=False)
    options = Column(Text, nullable=True)
    
    status = Column(String(20), default=ScanStatus.PENDING.value, index=True)
    output = Column(Text, nullable=True)
    parsed_results = Column(JSON, nullable=True)
    
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="scans")
    
    def __repr__(self):
        return f"<Scan(id={self.id}, tool={self.tool}, status={self.status})>"
