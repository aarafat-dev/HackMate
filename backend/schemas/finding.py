"""
HackMate v2.0 - Finding Schemas
Request and response models for findings API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class FindingStatus(str, Enum):
    OPEN = "open"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    REMEDIATED = "remediated"


class FindingCreate(BaseModel):
    """Schema for creating a new finding."""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    severity: Severity = Severity.INFO
    affected_component: Optional[str] = Field(None, max_length=500)
    evidence: Optional[str] = None
    remediation: Optional[str] = None
    cvss_score: Optional[float] = Field(None, ge=0, le=10)
    cve_id: Optional[str] = Field(None, max_length=50)
    phase_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "SQL Injection in Login Form",
                "description": "The login form is vulnerable to SQL injection...",
                "severity": "critical",
                "affected_component": "/login.php",
                "remediation": "Use parameterized queries",
                "cvss_score": 9.8,
                "cve_id": "CVE-2024-12345"
            }
        }


class FindingUpdate(BaseModel):
    """Schema for updating a finding."""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    severity: Optional[Severity] = None
    status: Optional[FindingStatus] = None
    affected_component: Optional[str] = None
    evidence: Optional[str] = None
    remediation: Optional[str] = None
    cvss_score: Optional[float] = Field(None, ge=0, le=10)
    cve_id: Optional[str] = None


class FindingResponse(BaseModel):
    """Schema for finding response."""
    id: str
    engagement_id: str
    phase_id: Optional[str]
    title: str
    description: Optional[str]
    severity: str
    status: str
    affected_component: Optional[str]
    evidence: Optional[str]
    remediation: Optional[str]
    cvss_score: Optional[float]
    cve_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BulkStatusUpdate(BaseModel):
    """Schema for bulk status update."""
    finding_ids: List[str]
    status: FindingStatus
