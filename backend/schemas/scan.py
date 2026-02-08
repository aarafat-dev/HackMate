"""
HackMate v2.0 - Scan Schemas
Request and response models for scans API.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ScanTool(str, Enum):
    NMAP = "nmap"
    NIKTO = "nikto"
    GOBUSTER = "gobuster"
    NUCLEI = "nuclei"
    CUSTOM = "custom"


class ScanStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ScanCreate(BaseModel):
    """Schema for creating a new scan."""
    tool: ScanTool
    target: str = Field(..., min_length=1, max_length=500)
    options: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "tool": "nmap",
                "target": "example.com",
                "options": "-sV -sC"
            }
        }


class ScanResponse(BaseModel):
    """Schema for scan response."""
    id: str
    engagement_id: str
    tool: str
    target: str
    command: str
    options: Optional[str]
    status: str
    output: Optional[str]
    parsed_results: Optional[Dict[str, Any]]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True
