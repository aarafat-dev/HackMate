"""
HackMate v2.0 - Engagements Router
CRUD endpoints for penetration testing engagements.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from database import get_db
from models.engagement import Engagement, EngagementStatus
from models.phase import Phase, create_phases_for_engagement, PhaseStatus
from models.finding import Finding, Severity
from schemas.engagement import (
    EngagementCreate,
    EngagementUpdate,
    EngagementResponse,
    EngagementStats
)

router = APIRouter(prefix="/api/engagements", tags=["Engagements"])


@router.post("", response_model=EngagementResponse, status_code=201)
async def create_engagement(
    data: EngagementCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new engagement.
    
    This also creates all 8 PTES phases for the engagement.
    The first phase will be set to 'in_progress' status.
    """
    # Create engagement
    engagement = Engagement(
        name=data.name,
        target=data.target,
        scope=data.scope,
        status=EngagementStatus.PLANNING.value
    )
    db.add(engagement)
    db.flush()  # Get the ID
    
    # Create all 8 phases
    phases = create_phases_for_engagement(engagement.id)
    for phase in phases:
        db.add(phase)
    
    # Set first phase to in_progress
    phases[0].status = PhaseStatus.IN_PROGRESS.value
    
    db.commit()
    db.refresh(engagement)
    
    return EngagementResponse(
        id=engagement.id,
        name=engagement.name,
        target=engagement.target,
        scope=engagement.scope,
        status=engagement.status,
        created_at=engagement.created_at,
        updated_at=engagement.updated_at,
        phase_count=8,
        completed_phases=0,
        finding_count=0,
        critical_findings=0
    )


@router.get("", response_model=List[EngagementResponse])
async def list_engagements(
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by name or target"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List all engagements with optional filtering.
    
    Supports:
    - Status filter (planning, active, completed, on_hold)
    - Search by name or target
    - Pagination
    """
    query = db.query(Engagement)
    
    if status:
        query = query.filter(Engagement.status == status)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Engagement.name.ilike(search_term)) |
            (Engagement.target.ilike(search_term))
        )
    
    engagements = query.order_by(Engagement.created_at.desc()).offset(skip).limit(limit).all()
    
    results = []
    for eng in engagements:
        # Get phase stats
        completed_phases = db.query(Phase).filter(
            Phase.engagement_id == eng.id,
            Phase.status == PhaseStatus.COMPLETED.value
        ).count()
        
        # Get finding stats
        finding_count = db.query(Finding).filter(Finding.engagement_id == eng.id).count()
        critical_findings = db.query(Finding).filter(
            Finding.engagement_id == eng.id,
            Finding.severity == Severity.CRITICAL.value
        ).count()
        
        results.append(EngagementResponse(
            id=eng.id,
            name=eng.name,
            target=eng.target,
            scope=eng.scope,
            status=eng.status,
            created_at=eng.created_at,
            updated_at=eng.updated_at,
            phase_count=8,
            completed_phases=completed_phases,
            finding_count=finding_count,
            critical_findings=critical_findings
        ))
    
    return results


@router.get("/stats", response_model=EngagementStats)
async def get_engagement_stats(db: Session = Depends(get_db)):
    """
    Get dashboard statistics.
    
    Returns counts for engagements and findings.
    """
    total = db.query(Engagement).count()
    active = db.query(Engagement).filter(Engagement.status == EngagementStatus.ACTIVE.value).count()
    completed = db.query(Engagement).filter(Engagement.status == EngagementStatus.COMPLETED.value).count()
    
    total_findings = db.query(Finding).count()
    critical_findings = db.query(Finding).filter(Finding.severity == Severity.CRITICAL.value).count()
    high_findings = db.query(Finding).filter(Finding.severity == Severity.HIGH.value).count()
    
    return EngagementStats(
        total_engagements=total,
        active_engagements=active,
        completed_engagements=completed,
        total_findings=total_findings,
        critical_findings=critical_findings,
        high_findings=high_findings
    )


@router.get("/{engagement_id}", response_model=EngagementResponse)
async def get_engagement(engagement_id: str, db: Session = Depends(get_db)):
    """Get a single engagement by ID."""
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Get stats
    completed_phases = db.query(Phase).filter(
        Phase.engagement_id == engagement.id,
        Phase.status == PhaseStatus.COMPLETED.value
    ).count()
    
    finding_count = db.query(Finding).filter(Finding.engagement_id == engagement.id).count()
    critical_findings = db.query(Finding).filter(
        Finding.engagement_id == engagement.id,
        Finding.severity == Severity.CRITICAL.value
    ).count()
    
    return EngagementResponse(
        id=engagement.id,
        name=engagement.name,
        target=engagement.target,
        scope=engagement.scope,
        status=engagement.status,
        created_at=engagement.created_at,
        updated_at=engagement.updated_at,
        phase_count=8,
        completed_phases=completed_phases,
        finding_count=finding_count,
        critical_findings=critical_findings
    )


@router.put("/{engagement_id}", response_model=EngagementResponse)
async def update_engagement(
    engagement_id: str,
    data: EngagementUpdate,
    db: Session = Depends(get_db)
):
    """Update an engagement."""
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Update fields
    if data.name is not None:
        engagement.name = data.name
    if data.target is not None:
        engagement.target = data.target
    if data.scope is not None:
        engagement.scope = data.scope
    if data.status is not None:
        engagement.status = data.status.value
    
    db.commit()
    db.refresh(engagement)
    
    return EngagementResponse(
        id=engagement.id,
        name=engagement.name,
        target=engagement.target,
        scope=engagement.scope,
        status=engagement.status,
        created_at=engagement.created_at,
        updated_at=engagement.updated_at
    )


@router.delete("/{engagement_id}", status_code=204)
async def delete_engagement(engagement_id: str, db: Session = Depends(get_db)):
    """
    Delete an engagement and all related data.
    
    This cascades to delete phases, findings, scans, etc.
    """
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    db.delete(engagement)
    db.commit()
    
    return None
