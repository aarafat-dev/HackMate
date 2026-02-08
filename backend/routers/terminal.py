"""
HackMate v2.0 - Terminal Router
Command execution and history endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.terminal import TerminalHistory
from models.engagement import Engagement
from schemas.terminal import CommandRequest, CommandResponse, HistoryResponse, CommandSuggestion
from services.terminal_service import TerminalService

router = APIRouter(prefix="/api/terminal", tags=["Terminal"])


@router.post("/execute/{engagement_id}", response_model=CommandResponse)
async def execute_command(
    engagement_id: str,
    data: CommandRequest,
    db: Session = Depends(get_db)
):
    """
    Execute a command in the terminal.
    
    The command is validated against a whitelist of allowed commands
    and executed in a controlled environment.
    
    Supported commands include:
    - Network: nmap, ping, traceroute, dig, whois, host, nslookup
    - Web: nikto, gobuster, curl, wget
    - Scanning: nuclei, sqlmap
    - Utilities: grep, awk, sed, cat, less, head, tail
    """
    # Verify engagement exists
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Execute command
    terminal_service = TerminalService()
    
    try:
        result = await terminal_service.execute_command(
            command=data.command,
            engagement_id=engagement_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Command execution failed: {str(e)}")
    
    # Save to history
    history_entry = TerminalHistory(
        engagement_id=engagement_id,
        command=data.command,
        output=result["stdout"] + ("\n" + result["stderr"] if result["stderr"] else ""),
        exit_code=result["exit_code"],
        execution_time=result["execution_time"]
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    
    return CommandResponse(
        id=history_entry.id,
        command=history_entry.command,
        output=history_entry.output,
        exit_code=history_entry.exit_code,
        execution_time=history_entry.execution_time,
        executed_at=history_entry.executed_at
    )


@router.get("/history/{engagement_id}", response_model=List[HistoryResponse])
async def get_command_history(
    engagement_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """
    Get command history for an engagement.
    
    Returns commands in reverse chronological order (newest first).
    """
    history = db.query(TerminalHistory).filter(
        TerminalHistory.engagement_id == engagement_id
    ).order_by(TerminalHistory.executed_at.desc()).offset(skip).limit(limit).all()
    
    return [HistoryResponse(
        id=h.id,
        command=h.command,
        output=h.output,
        exit_code=h.exit_code,
        execution_time=h.execution_time,
        executed_at=h.executed_at
    ) for h in history]


@router.get("/suggestions/{engagement_id}", response_model=List[CommandSuggestion])
async def get_command_suggestions(
    engagement_id: str,
    phase: int = Query(None, ge=1, le=8, description="Current phase number"),
    db: Session = Depends(get_db)
):
    """
    Get AI-powered command suggestions based on current phase.
    
    Returns relevant commands for the current testing phase.
    """
    # Phase-based suggestions
    suggestions_by_phase = {
        1: [],  # Pre-engagement - no commands
        2: [  # Intelligence Gathering
            CommandSuggestion(command="whois {target}", description="Get domain registration info", category="OSINT"),
            CommandSuggestion(command="dig {target} ANY +noall +answer", description="DNS enumeration", category="OSINT"),
            CommandSuggestion(command="nslookup {target}", description="Name server lookup", category="OSINT"),
            CommandSuggestion(command="host -a {target}", description="Full DNS lookup", category="OSINT"),
        ],
        3: [  # Threat Modeling
            CommandSuggestion(command="nmap -sn {target}/24", description="Network discovery", category="Recon"),
        ],
        4: [  # Vulnerability Analysis
            CommandSuggestion(command="nmap -sV -sC {target}", description="Service version scan", category="Scanning"),
            CommandSuggestion(command="nmap -p- {target}", description="Full port scan", category="Scanning"),
            CommandSuggestion(command="nikto -h {target}", description="Web server scan", category="Web"),
            CommandSuggestion(command="gobuster dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt", description="Directory brute-force", category="Web"),
            CommandSuggestion(command="nuclei -u {target}", description="Vulnerability scan", category="Scanning"),
        ],
        5: [  # Exploitation
            CommandSuggestion(command="nmap --script=exploit {target}", description="Nmap exploit scripts", category="Exploit"),
        ],
        6: [  # Post Exploitation
            CommandSuggestion(command="nmap -sV --script=auth {target}", description="Authentication checks", category="Post-Exploit"),
        ],
        7: [],  # Reporting - no commands
        8: [],  # Cleanup - no commands
    }
    
    return suggestions_by_phase.get(phase, [])


@router.delete("/history/{entry_id}", status_code=204)
async def delete_history_entry(entry_id: str, db: Session = Depends(get_db)):
    """Delete a specific history entry."""
    entry = db.query(TerminalHistory).filter(TerminalHistory.id == entry_id).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="History entry not found")
    
    db.delete(entry)
    db.commit()
    
    return None
