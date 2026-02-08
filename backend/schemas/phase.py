"""
HackMate v2.0 - Phase Schemas
Request and response models for PTES phases API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PhaseStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class PhaseResponse(BaseModel):
    """Schema for phase response."""
    id: str
    engagement_id: str
    phase_number: int
    name: str
    description: Optional[str]
    status: str
    objectives: Optional[List[str]]
    guidance: Optional[str]
    notes: Optional[str]
    completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class PhaseUpdate(BaseModel):
    """Schema for updating a phase."""
    status: Optional[PhaseStatus] = None
    notes: Optional[str] = None
    guidance: Optional[str] = None


class PhaseComplete(BaseModel):
    """Schema for completing a phase."""
    notes: Optional[str] = Field(None, description="Completion notes")
