"""
HackMate v2.0 - Report Model
Stores generated penetration testing reports.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum


class ReportType(str, enum.Enum):
    """Types of reports that can be generated."""
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    FULL = "full"


class ReportFormat(str, enum.Enum):
    """Output formats for reports."""
    MARKDOWN = "markdown"
    PDF = "pdf"
    HTML = "html"


class Report(Base):
    """
    Report model - stores generated reports.
    
    Attributes:
        id: Unique identifier
        engagement_id: Parent engagement
        report_type: Type of report (executive, technical, full)
        content: The report content (Markdown)
        format: Output format
        report_metadata: Additional report info (JSON)
        created_at: When the report was generated
    """
    __tablename__ = "reports"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engagement_id = Column(String(36), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False, index=True)
    
    report_type = Column(String(20), nullable=False, index=True)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)
    format = Column(String(20), default=ReportFormat.MARKDOWN.value)
    
    report_metadata = Column(JSON, nullable=True)  # findings count, severity breakdown, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="reports")
    
    def __repr__(self):
        return f"<Report(id={self.id}, type={self.report_type})>"
