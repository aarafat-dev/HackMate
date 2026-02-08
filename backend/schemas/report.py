"""
HackMate v2.0 - Report Schemas
Request and response models for reports API.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ReportType(str, Enum):
    EXECUTIVE = "executive"
    TECHNICAL = "technical"
    FULL = "full"


class ReportFormat(str, Enum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    HTML = "html"


class ReportRequest(BaseModel):
    """Schema for generating a report."""
    report_type: ReportType = ReportType.EXECUTIVE
    format: ReportFormat = ReportFormat.MARKDOWN
    include_evidence: bool = True
    include_remediation: bool = True
    
    class Config:
        json_schema_extra = {
            "example": {
                "report_type": "executive",
                "format": "markdown",
                "include_evidence": False,
                "include_remediation": True
            }
        }


class ReportResponse(BaseModel):
    """Schema for report response."""
    id: str
    engagement_id: str
    report_type: str
    title: Optional[str]
    content: str
    format: str
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True
