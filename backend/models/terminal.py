"""
HackMate v2.0 - Terminal History Model
Stores command execution history.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class TerminalHistory(Base):
    """
    TerminalHistory model - stores executed commands and their output.
    
    Attributes:
        id: Unique identifier
        engagement_id: Parent engagement
        command: The command that was executed
        output: Command output (stdout + stderr)
        exit_code: Process exit code
        execution_time: How long the command took (seconds)
        executed_at: When the command was run
    """
    __tablename__ = "terminal_history"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engagement_id = Column(String(36), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False, index=True)
    
    command = Column(Text, nullable=False)
    output = Column(Text, nullable=True)
    exit_code = Column(Integer, nullable=True)
    execution_time = Column(Float, nullable=True)  # seconds
    
    executed_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="terminal_history")
    
    def __repr__(self):
        return f"<TerminalHistory(id={self.id}, command={self.command[:50]}...)>"
