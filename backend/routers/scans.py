"""
HackMate v2.0 - Scans Router
Security scan management endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models.scan import Scan, ScanStatus, ScanTool
from models.engagement import Engagement
from schemas.scan import ScanCreate, ScanResponse
from services.terminal_service import TerminalService

router = APIRouter(prefix="/api/scans", tags=["Scans"])


@router.get("/", response_model=List[ScanResponse])
async def list_all_scans(
    tool: str = Query(None),
    status: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List scans across all engagements."""
    query = db.query(Scan)
    if tool: query = query.filter(Scan.tool == tool)
    if status: query = query.filter(Scan.status == status)
    
    scans = query.order_by(Scan.created_at.desc()).offset(skip).limit(limit).all()
    return [ScanResponse(
        id=s.id, engagement_id=s.engagement_id, tool=s.tool,
        target=s.target, command=s.command, options=s.options,
        status=s.status, output=s.output, parsed_results=s.parsed_results,
        started_at=s.started_at, completed_at=s.completed_at, created_at=s.created_at
    ) for s in scans]


def build_scan_command(tool: str, target: str, options: str = None) -> str:
    """Build the full command for a scan tool."""
    commands = {
        "nmap": f"nmap {options or '-sV -sC'} {target}",
        "nikto": f"nikto -h {target} {options or ''}",
        "gobuster": f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt {options or ''}",
        "nuclei": f"nuclei -u {target} {options or ''}",
        "custom": f"{options or 'echo No command specified'}"
    }
    return commands.get(tool, f"echo Unknown tool: {tool}")


async def run_scan_background(scan_id: str, command: str, db_url: str):
    """Background task to run a scan."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    
    try:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if not scan:
            return
        
        # Update status to running
        scan.status = ScanStatus.RUNNING.value
        scan.started_at = datetime.utcnow()
        db.commit()
        
        # Execute command
        terminal_service = TerminalService()
        result = await terminal_service.execute_command(command, scan.engagement_id)
        
        # Update scan with results
        scan.status = ScanStatus.COMPLETED.value if result["exit_code"] == 0 else ScanStatus.FAILED.value
        scan.output = result["stdout"] + ("\n" + result["stderr"] if result["stderr"] else "")
        scan.completed_at = datetime.utcnow()
        
        db.commit()
        
    except Exception as e:
        scan = db.query(Scan).filter(Scan.id == scan_id).first()
        if scan:
            scan.status = ScanStatus.FAILED.value
            scan.output = f"Error: {str(e)}"
            scan.completed_at = datetime.utcnow()
            db.commit()
    finally:
        db.close()


@router.post("/{engagement_id}", response_model=ScanResponse, status_code=201)
async def create_scan(
    engagement_id: str,
    data: ScanCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create and start a new security scan.
    
    The scan runs in the background and updates status as it progresses.
    Check the scan status endpoint to monitor progress.
    """
    # Verify engagement exists
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Build command
    command = build_scan_command(data.tool.value, data.target, data.options)
    
    # Create scan record
    scan = Scan(
        engagement_id=engagement_id,
        tool=data.tool.value,
        target=data.target,
        command=command,
        options=data.options,
        status=ScanStatus.PENDING.value
    )
    
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    # Queue background task
    from config import get_settings
    settings = get_settings()
    background_tasks.add_task(
        run_scan_background,
        scan.id,
        command,
        settings.database_url
    )
    
    return ScanResponse(
        id=scan.id,
        engagement_id=scan.engagement_id,
        tool=scan.tool,
        target=scan.target,
        command=scan.command,
        options=scan.options,
        status=scan.status,
        output=scan.output,
        parsed_results=scan.parsed_results,
        started_at=scan.started_at,
        completed_at=scan.completed_at,
        created_at=scan.created_at
    )


@router.get("/engagement/{engagement_id}", response_model=List[ScanResponse])
async def list_scans(
    engagement_id: str,
    tool: str = Query(None, description="Filter by tool"),
    status: str = Query(None, description="Filter by status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all scans for an engagement."""
    query = db.query(Scan).filter(Scan.engagement_id == engagement_id)
    
    if tool:
        query = query.filter(Scan.tool == tool)
    
    if status:
        query = query.filter(Scan.status == status)
    
    scans = query.order_by(Scan.created_at.desc()).offset(skip).limit(limit).all()
    
    return [ScanResponse(
        id=s.id,
        engagement_id=s.engagement_id,
        tool=s.tool,
        target=s.target,
        command=s.command,
        options=s.options,
        status=s.status,
        output=s.output,
        parsed_results=s.parsed_results,
        started_at=s.started_at,
        completed_at=s.completed_at,
        created_at=s.created_at
    ) for s in scans]


@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan(scan_id: str, db: Session = Depends(get_db)):
    """Get a single scan by ID."""
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return ScanResponse(
        id=scan.id,
        engagement_id=scan.engagement_id,
        tool=scan.tool,
        target=scan.target,
        command=scan.command,
        options=scan.options,
        status=scan.status,
        output=scan.output,
        parsed_results=scan.parsed_results,
        started_at=scan.started_at,
        completed_at=scan.completed_at,
        created_at=scan.created_at
    )


@router.delete("/{scan_id}", status_code=204)
async def cancel_scan(scan_id: str, db: Session = Depends(get_db)):
    """
    Cancel a running scan or delete a completed scan.
    
    Note: Actual process cancellation is not implemented in this scaffold.
    """
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    if scan.status == ScanStatus.RUNNING.value:
        scan.status = ScanStatus.CANCELLED.value
        scan.completed_at = datetime.utcnow()
        db.commit()
    else:
        db.delete(scan)
        db.commit()
    
    return None
