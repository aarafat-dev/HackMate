"""
HackMate v2.0 - Chat Schemas
Request and response models for AI chat API.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatRequest(BaseModel):
    """Schema for sending a chat message."""
    message: str = Field(..., min_length=1, max_length=5000)
    context: Optional[str] = Field(None, description="Additional context for AI")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What tools should I use for web application scanning?",
                "context": "Currently in phase 4 (Vulnerability Analysis)"
            }
        }


class ChatResponse(BaseModel):
    """Schema for AI chat response."""
    message: str
    suggestions: Optional[List[str]] = None
    
    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Schema for a single chat message."""
    id: str
    role: str
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class OutputAnalysisRequest(BaseModel):
    """Schema for analyzing tool output."""
    tool: str
    output: str = Field(..., min_length=1)
    
    class Config:
        json_schema_extra = {
            "example": {
                "tool": "nmap",
                "output": "PORT   STATE SERVICE VERSION\n22/tcp open  ssh     OpenSSH 7.4"
            }
        }


class OutputAnalysisResponse(BaseModel):
    """Schema for output analysis response."""
    summary: str
    findings: List[dict]
    next_steps: List[str]
    risk_level: str
