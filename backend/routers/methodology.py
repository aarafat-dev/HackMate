"""
HackMate v2.0 - Methodology Router
PTES phases management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.phase import Phase, PhaseStatus
from models.engagement import Engagement, EngagementStatus
from schemas.phase import PhaseResponse, PhaseUpdate, PhaseComplete
from services.ai_service import AIService

router = APIRouter(prefix="/api/methodology", tags=["Methodology"])


@router.get("/phases/{engagement_id}", response_model=List[PhaseResponse])
async def get_phases(engagement_id: str, db: Session = Depends(get_db)):
    """
    Get all 8 PTES phases for an engagement.
    
    Returns phases in order (1-8) with status and objectives.
    """
    # Verify engagement exists
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    phases = db.query(Phase).filter(
        Phase.engagement_id == engagement_id
    ).order_by(Phase.phase_number).all()
    
    return [PhaseResponse(
        id=p.id,
        engagement_id=p.engagement_id,
        phase_number=p.phase_number,
        name=p.name,
        description=p.description,
        status=p.status,
        objectives=p.objectives,
        guidance=p.guidance,
        notes=p.notes,
        completed_at=p.completed_at,
        created_at=p.created_at
    ) for p in phases]


@router.get("/phases/{engagement_id}/current", response_model=PhaseResponse)
async def get_current_phase(engagement_id: str, db: Session = Depends(get_db)):
    """
    Get the current active phase for an engagement.
    
    Returns the first phase that is 'in_progress', or the first
    'not_started' phase if none are in progress.
    """
    # Check for in_progress phase
    phase = db.query(Phase).filter(
        Phase.engagement_id == engagement_id,
        Phase.status == PhaseStatus.IN_PROGRESS.value
    ).first()
    
    if not phase:
        # Get first not_started phase
        phase = db.query(Phase).filter(
            Phase.engagement_id == engagement_id,
            Phase.status == PhaseStatus.NOT_STARTED.value
        ).order_by(Phase.phase_number).first()
    
    if not phase:
        raise HTTPException(status_code=404, detail="No active phase found")
    
    return PhaseResponse(
        id=phase.id,
        engagement_id=phase.engagement_id,
        phase_number=phase.phase_number,
        name=phase.name,
        description=phase.description,
        status=phase.status,
        objectives=phase.objectives,
        guidance=phase.guidance,
        notes=phase.notes,
        completed_at=phase.completed_at,
        created_at=phase.created_at
    )


@router.put("/phases/{phase_id}", response_model=PhaseResponse)
async def update_phase(
    phase_id: str,
    data: PhaseUpdate,
    db: Session = Depends(get_db)
):
    """Update a phase's status or notes."""
    phase = db.query(Phase).filter(Phase.id == phase_id).first()
    
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    
    if data.status is not None:
        phase.status = data.status.value
        if data.status == PhaseStatus.COMPLETED:
            phase.completed_at = datetime.utcnow()
    
    if data.notes is not None:
        phase.notes = data.notes
    
    if data.guidance is not None:
        phase.guidance = data.guidance
    
    db.commit()
    db.refresh(phase)
    
    return PhaseResponse(
        id=phase.id,
        engagement_id=phase.engagement_id,
        phase_number=phase.phase_number,
        name=phase.name,
        description=phase.description,
        status=phase.status,
        objectives=phase.objectives,
        guidance=phase.guidance,
        notes=phase.notes,
        completed_at=phase.completed_at,
        created_at=phase.created_at
    )


@router.post("/phases/{phase_id}/complete", response_model=PhaseResponse)
async def complete_phase(
    phase_id: str,
    data: PhaseComplete = None,
    db: Session = Depends(get_db)
):
    """
    Mark a phase as complete and activate the next phase.
    
    When Phase 8 is completed, the engagement status is set to 'completed'.
    """
    phase = db.query(Phase).filter(Phase.id == phase_id).first()
    
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    
    # Mark current phase as completed
    phase.status = PhaseStatus.COMPLETED.value
    phase.completed_at = datetime.utcnow()
    
    if data and data.notes:
        phase.notes = data.notes
    
    # Check if this is the final phase
    if phase.phase_number == 8:
        # Complete the engagement
        engagement = db.query(Engagement).filter(Engagement.id == phase.engagement_id).first()
        if engagement:
            engagement.status = EngagementStatus.COMPLETED.value
    else:
        # Activate next phase
        next_phase = db.query(Phase).filter(
            Phase.engagement_id == phase.engagement_id,
            Phase.phase_number == phase.phase_number + 1
        ).first()
        
        if next_phase:
            next_phase.status = PhaseStatus.IN_PROGRESS.value
            
            # Set engagement to active if it was planning
            engagement = db.query(Engagement).filter(Engagement.id == phase.engagement_id).first()
            if engagement and engagement.status == EngagementStatus.PLANNING.value:
                engagement.status = EngagementStatus.ACTIVE.value
    
    db.commit()
    db.refresh(phase)
    
    return PhaseResponse(
        id=phase.id,
        engagement_id=phase.engagement_id,
        phase_number=phase.phase_number,
        name=phase.name,
        description=phase.description,
        status=phase.status,
        objectives=phase.objectives,
        guidance=phase.guidance,
        notes=phase.notes,
        completed_at=phase.completed_at,
        created_at=phase.created_at
    )


@router.post("/phases/{phase_id}/guidance", response_model=dict)
async def generate_phase_guidance(
    phase_id: str,
    db: Session = Depends(get_db)
):
    """
    Generate AI guidance for a specific phase.
    
    Uses Google Gemini to provide contextual recommendations
    based on the engagement target and current phase.
    """
    phase = db.query(Phase).filter(Phase.id == phase_id).first()
    
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")
    
    engagement = db.query(Engagement).filter(Engagement.id == phase.engagement_id).first()
    
    # Generate guidance using AI service
    ai_service = AIService()
    guidance = await ai_service.generate_phase_guidance(
        phase_name=phase.name,
        phase_number=phase.phase_number,
        target=engagement.target,
        objectives=phase.objectives
    )
    
    # Save guidance to phase
    phase.guidance = guidance
    db.commit()
    
    return {"guidance": guidance}
