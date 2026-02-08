"""
HackMate v2.0 - Terminal Schemas
Request and response models for terminal API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CommandRequest(BaseModel):
    """Schema for executing a command."""
    command: str = Field(..., min_length=1, max_length=2000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "command": "nmap -sV example.com"
            }
        }


class CommandResponse(BaseModel):
    """Schema for command execution response."""
    id: str
    command: str
    output: str
    exit_code: int
    execution_time: float
    executed_at: datetime
    
    class Config:
        from_attributes = True


class HistoryResponse(BaseModel):
    """Schema for terminal history response."""
    id: str
    command: str
    output: Optional[str]
    exit_code: Optional[int]
    execution_time: Optional[float]
    executed_at: datetime
    
    class Config:
        from_attributes = True


class CommandSuggestion(BaseModel):
    """AI-suggested command."""
    command: str
    description: str
    category: str
