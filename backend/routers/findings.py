"""
HackMate v2.0 - Findings Router
CRUD endpoints for vulnerability findings.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.finding import Finding, Severity, FindingStatus
from models.engagement import Engagement
from schemas.finding import FindingCreate, FindingUpdate, FindingResponse, BulkStatusUpdate

router = APIRouter(prefix="/api/findings", tags=["Findings"])


@router.get("/", response_model=List[FindingResponse])
async def list_all_findings(
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List findings across all engagements."""
    query = db.query(Finding)
    if severity: query = query.filter(Finding.severity == severity)
    if status: query = query.filter(Finding.status == status)
    if search: query = query.filter(Finding.title.ilike(f"%{search}%"))
    
    findings = query.order_by(Finding.created_at.desc()).offset(skip).limit(limit).all()
    return [FindingResponse(
        id=f.id, engagement_id=f.engagement_id, phase_id=f.phase_id,
        title=f.title, description=f.description, severity=f.severity,
        status=f.status, affected_component=f.affected_component,
        evidence=f.evidence, remediation=f.remediation,
        cvss_score=f.cvss_score, cve_id=f.cve_id,
        created_at=f.created_at, updated_at=f.updated_at
    ) for f in findings]


@router.post("/{engagement_id}", response_model=FindingResponse, status_code=201)
async def create_finding(
    engagement_id: str,
    data: FindingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new finding for an engagement.
    
    Findings track discovered vulnerabilities with severity levels,
    evidence, and remediation recommendations.
    """
    # Verify engagement exists
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    finding = Finding(
        engagement_id=engagement_id,
        phase_id=data.phase_id,
        title=data.title,
        description=data.description,
        severity=data.severity.value,
        affected_component=data.affected_component,
        evidence=data.evidence,
        remediation=data.remediation,
        cvss_score=data.cvss_score,
        cve_id=data.cve_id
    )
    
    db.add(finding)
    db.commit()
    db.refresh(finding)
    
    return FindingResponse(
        id=finding.id,
        engagement_id=finding.engagement_id,
        phase_id=finding.phase_id,
        title=finding.title,
        description=finding.description,
        severity=finding.severity,
        status=finding.status,
        affected_component=finding.affected_component,
        evidence=finding.evidence,
        remediation=finding.remediation,
        cvss_score=finding.cvss_score,
        cve_id=finding.cve_id,
        created_at=finding.created_at,
        updated_at=finding.updated_at
    )


@router.get("/engagement/{engagement_id}", response_model=List[FindingResponse])
async def list_findings(
    engagement_id: str,
    severity: Optional[str] = Query(None, description="Filter by severity"),
    status: Optional[str] = Query(None, description="Filter by status"),
    search: Optional[str] = Query(None, description="Search by title"),
    sort_by: str = Query("severity", description="Sort by: severity, created_at, title"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List findings for an engagement with filtering and sorting.
    
    Supports filtering by severity, status, and search.
    Default sort is by severity (critical first).
    """
    query = db.query(Finding).filter(Finding.engagement_id == engagement_id)
    
    if severity:
        query = query.filter(Finding.severity == severity)
    
    if status:
        query = query.filter(Finding.status == status)
    
    if search:
        query = query.filter(Finding.title.ilike(f"%{search}%"))
    
    # Sorting
    if sort_by == "severity":
        # Custom severity order
        severity_order = {
            Severity.CRITICAL.value: 1,
            Severity.HIGH.value: 2,
            Severity.MEDIUM.value: 3,
            Severity.LOW.value: 4,
            Severity.INFO.value: 5
        }
        # For SQLite, use CASE
        from sqlalchemy import case
        query = query.order_by(
            case(severity_order, value=Finding.severity)
        )
    elif sort_by == "created_at":
        query = query.order_by(Finding.created_at.desc())
    elif sort_by == "title":
        query = query.order_by(Finding.title)
    
    findings = query.offset(skip).limit(limit).all()
    
    return [FindingResponse(
        id=f.id,
        engagement_id=f.engagement_id,
        phase_id=f.phase_id,
        title=f.title,
        description=f.description,
        severity=f.severity,
        status=f.status,
        affected_component=f.affected_component,
        evidence=f.evidence,
        remediation=f.remediation,
        cvss_score=f.cvss_score,
        cve_id=f.cve_id,
        created_at=f.created_at,
        updated_at=f.updated_at
    ) for f in findings]


@router.get("/{finding_id}", response_model=FindingResponse)
async def get_finding(finding_id: str, db: Session = Depends(get_db)):
    """Get a single finding by ID."""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    return FindingResponse(
        id=finding.id,
        engagement_id=finding.engagement_id,
        phase_id=finding.phase_id,
        title=finding.title,
        description=finding.description,
        severity=finding.severity,
        status=finding.status,
        affected_component=finding.affected_component,
        evidence=finding.evidence,
        remediation=finding.remediation,
        cvss_score=finding.cvss_score,
        cve_id=finding.cve_id,
        created_at=finding.created_at,
        updated_at=finding.updated_at
    )


@router.put("/{finding_id}", response_model=FindingResponse)
async def update_finding(
    finding_id: str,
    data: FindingUpdate,
    db: Session = Depends(get_db)
):
    """Update a finding."""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    # Update fields
    if data.title is not None:
        finding.title = data.title
    if data.description is not None:
        finding.description = data.description
    if data.severity is not None:
        finding.severity = data.severity.value
    if data.status is not None:
        finding.status = data.status.value
    if data.affected_component is not None:
        finding.affected_component = data.affected_component
    if data.evidence is not None:
        finding.evidence = data.evidence
    if data.remediation is not None:
        finding.remediation = data.remediation
    if data.cvss_score is not None:
        finding.cvss_score = data.cvss_score
    if data.cve_id is not None:
        finding.cve_id = data.cve_id
    
    db.commit()
    db.refresh(finding)
    
    return FindingResponse(
        id=finding.id,
        engagement_id=finding.engagement_id,
        phase_id=finding.phase_id,
        title=finding.title,
        description=finding.description,
        severity=finding.severity,
        status=finding.status,
        affected_component=finding.affected_component,
        evidence=finding.evidence,
        remediation=finding.remediation,
        cvss_score=finding.cvss_score,
        cve_id=finding.cve_id,
        created_at=finding.created_at,
        updated_at=finding.updated_at
    )


@router.delete("/{finding_id}", status_code=204)
async def delete_finding(finding_id: str, db: Session = Depends(get_db)):
    """Delete a finding."""
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    
    db.delete(finding)
    db.commit()
    
    return None


@router.post("/bulk-update", response_model=dict)
async def bulk_update_findings(
    data: BulkStatusUpdate,
    db: Session = Depends(get_db)
):
    """
    Update status for multiple findings at once.
    
    Useful for marking multiple findings as confirmed or false positive.
    """
    updated = 0
    for finding_id in data.finding_ids:
        finding = db.query(Finding).filter(Finding.id == finding_id).first()
        if finding:
            finding.status = data.status.value
            updated += 1
    
    db.commit()
    
    return {"updated": updated, "total": len(data.finding_ids)}
