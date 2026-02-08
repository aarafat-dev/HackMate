"""
HackMate v2.0 - Engagement Schemas
Request and response models for engagements API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class EngagementStatus(str, Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"


class EngagementCreate(BaseModel):
    """Schema for creating a new engagement."""
    name: str = Field(..., min_length=1, max_length=200, description="Engagement name")
    target: str = Field(..., min_length=1, max_length=500, description="Target domain/IP")
    scope: Optional[str] = Field(None, description="Scope description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "ACME Corp Pentest Q1",
                "target": "acme.example.com",
                "scope": "All subdomains of acme.example.com"
            }
        }


class EngagementUpdate(BaseModel):
    """Schema for updating an engagement."""
    name: Optional[str] = Field(None, max_length=200)
    target: Optional[str] = Field(None, max_length=500)
    scope: Optional[str] = None
    status: Optional[EngagementStatus] = None


class EngagementResponse(BaseModel):
    """Schema for engagement response."""
    id: str
    name: str
    target: str
    scope: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    
    # Optional nested data
    phase_count: Optional[int] = None
    completed_phases: Optional[int] = None
    finding_count: Optional[int] = None
    critical_findings: Optional[int] = None
    
    class Config:
        from_attributes = True


class EngagementStats(BaseModel):
    """Dashboard statistics for engagements."""
    total_engagements: int
    active_engagements: int
    completed_engagements: int
    total_findings: int
    critical_findings: int
    high_findings: int
