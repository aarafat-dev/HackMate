"""
HackMate v2.0 - Reports Router
Report generation endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.report import Report, ReportType, ReportFormat
from models.engagement import Engagement
from models.finding import Finding, Severity
from schemas.report import ReportRequest, ReportResponse
from services.ai_service import AIService

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/", response_model=List[ReportResponse])
async def list_all_reports(
    report_type: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List reports across all engagements."""
    query = db.query(Report)
    if report_type: query = query.filter(Report.report_type == report_type)
    
    reports = query.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
    return [ReportResponse(
        id=r.id, engagement_id=r.engagement_id, report_type=r.report_type,
        title=r.title, content=r.content, format=r.format,
        metadata=r.report_metadata, created_at=r.created_at
    ) for r in reports]


@router.post("/{engagement_id}", response_model=ReportResponse, status_code=201)
async def generate_report(
    engagement_id: str,
    data: ReportRequest,
    db: Session = Depends(get_db)
):
    """
    Generate a penetration testing report.
    
    Uses AI to create professional reports based on engagement findings.
    
    Report types:
    - executive: High-level summary for management
    - technical: Detailed technical findings for security teams
    - full: Complete report with both sections
    """
    # Verify engagement exists
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Get findings
    findings = db.query(Finding).filter(Finding.engagement_id == engagement_id).all()
    
    # Count by severity
    severity_counts = {
        "critical": len([f for f in findings if f.severity == Severity.CRITICAL.value]),
        "high": len([f for f in findings if f.severity == Severity.HIGH.value]),
        "medium": len([f for f in findings if f.severity == Severity.MEDIUM.value]),
        "low": len([f for f in findings if f.severity == Severity.LOW.value]),
        "info": len([f for f in findings if f.severity == Severity.INFO.value])
    }
    
    # Generate report using AI
    ai_service = AIService()
    content = await ai_service.generate_report(
        engagement_name=engagement.name,
        target=engagement.target,
        scope=engagement.scope,
        findings=findings,
        report_type=data.report_type.value,
        include_evidence=data.include_evidence,
        include_remediation=data.include_remediation
    )
    
    # Create report record
    report = Report(
        engagement_id=engagementId,
        report_type=data.report_type.value,
        title=f"{engagement.name} - {data.report_type.value.title()} Report",
        content=content,
        format=data.format.value,
        report_metadata={
            "findings_count": len(findings),
            "severity_counts": severity_counts
        }
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return ReportResponse(
        id=report.id,
        engagement_id=report.engagement_id,
        report_type=report.report_type,
        title=report.title,
        content=report.content,
        format=report.format,
        metadata=report.report_metadata,
        created_at=report.created_at
    )


@router.get("/engagement/{engagement_id}", response_model=List[ReportResponse])
async def list_reports(
    engagement_id: str,
    report_type: str = Query(None, description="Filter by type"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all reports for an engagement."""
    query = db.query(Report).filter(Report.engagement_id == engagement_id)
    
    if report_type:
        query = query.filter(Report.report_type == report_type)
    
    reports = query.order_by(Report.created_at.desc()).offset(skip).limit(limit).all()
    
    return [ReportResponse(
        id=r.id,
        engagement_id=r.engagement_id,
        report_type=r.report_type,
        title=r.title,
        content=r.content,
        format=r.format,
        metadata=r.report_metadata,
        created_at=r.created_at
    ) for r in reports]


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, db: Session = Depends(get_db)):
    """Get a single report by ID."""
    report = db.query(Report).filter(Report.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return ReportResponse(
        id=report.id,
        engagement_id=report.engagement_id,
        report_type=report.report_type,
        title=report.title,
        content=report.content,
        format=report.format,
        metadata=report.report_metadata,
        created_at=report.created_at
    )


@router.delete("/{report_id}", status_code=204)
async def delete_report(report_id: str, db: Session = Depends(get_db)):
    """Delete a report."""
    report = db.query(Report).filter(Report.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    
    return None
