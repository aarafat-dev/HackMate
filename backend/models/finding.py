"""
HackMate v2.0 - Finding Model
Represents discovered vulnerabilities.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum


class Severity(str, enum.Enum):
    """Vulnerability severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(str, enum.Enum):
    """Finding status values."""
    OPEN = "open"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    REMEDIATED = "remediated"


class Finding(Base):
    """
    Finding model - represents a discovered vulnerability.
    
    Attributes:
        id: Unique identifier
        engagement_id: Parent engagement
        phase_id: Phase where discovered (optional)
        title: Short title for the finding
        description: Detailed description
        severity: Risk level (critical, high, medium, low, info)
        status: Current status
        affected_component: What's affected (URL, service, etc.)
        evidence: Proof/screenshots/output
        remediation: Fix recommendations
        cvss_score: CVSS score if applicable (0-10)
        cve_id: CVE identifier if applicable
    """
    __tablename__ = "findings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engagement_id = Column(String(36), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False, index=True)
    phase_id = Column(String(36), ForeignKey("phases.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(20), default=Severity.INFO.value, index=True)
    status = Column(String(20), default=FindingStatus.OPEN.value, index=True)
    
    affected_component = Column(String(500), nullable=True)
    evidence = Column(Text, nullable=True)
    remediation = Column(Text, nullable=True)
    
    cvss_score = Column(Float, nullable=True)
    cve_id = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="findings")
    
    def __repr__(self):
        return f"<Finding(id={self.id}, title={self.title}, severity={self.severity})>"
