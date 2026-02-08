"""
HackMate v2.0 - Chat Message Model
Stores AI chat conversation history.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import enum


class MessageRole(str, enum.Enum):
    """Chat message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(Base):
    """
    ChatMessage model - stores AI chat history.
    
    Attributes:
        id: Unique identifier
        engagement_id: Parent engagement
        role: Who sent the message (user, assistant, system)
        content: Message content
        created_at: When the message was sent
    """
    __tablename__ = "chat_messages"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engagement_id = Column(String(36), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False, index=True)
    
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="chat_messages")
    
    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role={self.role})>"
