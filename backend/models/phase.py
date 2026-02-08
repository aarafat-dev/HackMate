"""
HackMate v2.0 - Phase Model
Represents PTES methodology phases (8 phases).
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
import enum


class PhaseStatus(str, enum.Enum):
    """Valid statuses for a phase."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# PTES Phase definitions
PTES_PHASES = [
    {
        "number": 1,
        "name": "Pre-Engagement Interactions",
        "description": "Define scope, rules of engagement, and establish communication channels.",
        "objectives": [
            "Define scope and boundaries",
            "Get written authorization",
            "Establish communication channels",
            "Create Statement of Work",
            "Define Rules of Engagement"
        ]
    },
    {
        "number": 2,
        "name": "Intelligence Gathering",
        "description": "Collect public information without direct target interaction (OSINT).",
        "objectives": [
            "Domain enumeration",
            "Email harvesting",
            "Employee discovery",
            "Technology fingerprinting",
            "Social media reconnaissance"
        ]
    },
    {
        "number": 3,
        "name": "Threat Modeling",
        "description": "Identify critical assets, map attack surface, prioritize targets.",
        "objectives": [
            "Identify critical assets",
            "Map attack surface",
            "Create attack trees",
            "Prioritize targets",
            "Align with MITRE ATT&CK"
        ]
    },
    {
        "number": 4,
        "name": "Vulnerability Analysis",
        "description": "Identify security weaknesses through scanning and enumeration.",
        "objectives": [
            "Port scanning",
            "Service enumeration",
            "Web application scanning",
            "Vulnerability scanning",
            "Configuration review"
        ]
    },
    {
        "number": 5,
        "name": "Exploitation",
        "description": "Validate vulnerabilities through controlled exploitation.",
        "objectives": [
            "Validate vulnerabilities",
            "Gain initial access",
            "Capture evidence",
            "Document exploitation steps",
            "Maintain operational security"
        ]
    },
    {
        "number": 6,
        "name": "Post Exploitation",
        "description": "Demonstrate impact through privilege escalation and lateral movement.",
        "objectives": [
            "Privilege escalation",
            "Lateral movement",
            "Data discovery",
            "Persistence mechanisms",
            "Impact assessment"
        ]
    },
    {
        "number": 7,
        "name": "Reporting",
        "description": "Document findings and provide actionable recommendations.",
        "objectives": [
            "Document all findings",
            "Write executive summary",
            "Create technical report",
            "Develop remediation roadmap",
            "Prepare presentation"
        ]
    },
    {
        "number": 8,
        "name": "Cleanup",
        "description": "Remove artifacts and restore systems to original state.",
        "objectives": [
            "Remove backdoors",
            "Delete uploaded tools",
            "Restore configurations",
            "Verify system functionality",
            "Final handoff"
        ]
    }
]


class Phase(Base):
    """
    Phase model - represents a PTES methodology phase.
    
    Each engagement has 8 phases that must be completed in order.
    """
    __tablename__ = "phases"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    engagement_id = Column(String(36), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False, index=True)
    phase_number = Column(Integer, nullable=False)  # 1-8
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default=PhaseStatus.NOT_STARTED.value)
    objectives = Column(JSON, nullable=True)  # List of objectives
    guidance = Column(Text, nullable=True)  # AI-generated guidance
    notes = Column(Text, nullable=True)  # User notes
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    engagement = relationship("Engagement", back_populates="phases")
    
    def __repr__(self):
        return f"<Phase(id={self.id}, number={self.phase_number}, name={self.name}, status={self.status})>"


def create_phases_for_engagement(engagement_id: str) -> list:
    """
    Create all 8 PTES phases for a new engagement.
    Returns list of Phase objects (not yet committed to DB).
    """
    phases = []
    for phase_def in PTES_PHASES:
        phase = Phase(
            engagement_id=engagement_id,
            phase_number=phase_def["number"],
            name=phase_def["name"],
            description=phase_def["description"],
            objectives=phase_def["objectives"],
            status=PhaseStatus.NOT_STARTED.value
        )
        phases.append(phase)
    return phases
