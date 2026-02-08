"""
HackMate v2.0 - AI Router
AI assistant endpoints for chat and analysis.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.chat import ChatMessage, MessageRole
from models.engagement import Engagement
from models.phase import Phase
from models.finding import Finding
from schemas.chat import (
    ChatRequest,
    ChatResponse,
    MessageResponse,
    OutputAnalysisRequest,
    OutputAnalysisResponse
)
from services.ai_service import AIService

router = APIRouter(prefix="/api/ai", tags=["AI Assistant"])


@router.post("/chat/{engagement_id}", response_model=ChatResponse)
async def send_chat_message(
    engagement_id: str,
    data: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Send a message to the AI assistant.
    
    The AI provides contextual guidance based on:
    - Current engagement and target
    - Active phase
    - Previous findings
    - Recent chat history
    """
    # Verify engagement exists or handle default
    if engagement_id == "default":
        engagement = db.query(Engagement).filter(Engagement.id == "default").first()
        if not engagement:
            engagement = Engagement(
                id="default",
                name="General Assistant",
                target="General",
                status="active"
            )
            db.add(engagement)
            db.commit()
            db.refresh(engagement)
    else:
        engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
        if not engagement:
            raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Get current phase
    current_phase = db.query(Phase).filter(
        Phase.engagement_id == engagement_id,
        Phase.status == "in_progress"
    ).first()
    
    # Get findings count
    findings_count = db.query(Finding).filter(Finding.engagement_id == engagement_id).count()
    
    # Save user message
    user_message = ChatMessage(
        engagement_id=engagement_id,
        role=MessageRole.USER.value,
        content=data.message
    )
    db.add(user_message)
    
    # Get AI response
    ai_service = AIService()
    context = {
        "engagement_name": engagement.name,
        "target": engagement.target,
        "current_phase": current_phase.name if current_phase else "Unknown",
        "phase_number": current_phase.phase_number if current_phase else 0,
        "findings_count": findings_count,
        "additional_context": data.context
    }
    
    response = await ai_service.chat(data.message, context)
    
    # Save assistant message
    assistant_message = ChatMessage(
        engagement_id=engagement_id,
        role=MessageRole.ASSISTANT.value,
        content=response["message"]
    )
    db.add(assistant_message)
    db.commit()
    
    return ChatResponse(
        message=response["message"],
        suggestions=response.get("suggestions", [])
    )


@router.get("/chat/{engagement_id}", response_model=List[MessageResponse])
async def get_chat_history(
    engagement_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    """Get chat history for an engagement."""
    # Handle default engagement if needed
    if engagement_id == "default":
        engagement = db.query(Engagement).filter(Engagement.id == "default").first()
        if not engagement:
            engagement = Engagement(
                id="default",
                name="General Assistant",
                target="General",
                status="active"
            )
            db.add(engagement)
            db.commit()
            db.refresh(engagement)
    else:
        # Check if engagement exists for normal IDs
        engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
        if not engagement:
             # Just return empty list or 404? 
             # The defined behavior for get_chat_history is usually just returning history.
             # If engagement doesn't exist, returning 404 is correct.
             raise HTTPException(status_code=404, detail="Engagement not found")

    # Check if history is empty
    message_count = db.query(ChatMessage).filter(ChatMessage.engagement_id == engagement_id).count()
    
    if message_count == 0:
        # Generate initial welcome message
        ai_service = AIService()
        welcome_text = await ai_service.generate_welcome(engagement.target)
        
        welcome_msg = ChatMessage(
            engagement_id=engagement_id,
            role=MessageRole.ASSISTANT.value,
            content=welcome_text
        )
        db.add(welcome_msg)
        db.commit()

    messages = db.query(ChatMessage).filter(
        ChatMessage.engagement_id == engagement_id
    ).order_by(ChatMessage.created_at.asc()).offset(skip).limit(limit).all()
    
    return [MessageResponse(
        id=m.id,
        role=m.role,
        content=m.content,
        created_at=m.created_at
    ) for m in messages]


@router.post("/analyze-output/{engagement_id}", response_model=OutputAnalysisResponse)
async def analyze_output(
    engagement_id: str,
    data: OutputAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze tool output and extract findings.
    
    The AI parses scan output and identifies:
    - Key findings and vulnerabilities
    - Risk assessment
    - Recommended next steps
    """
    # Verify engagement exists
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Analyze using AI
    ai_service = AIService()
    analysis = await ai_service.analyze_output(
        tool=data.tool,
        output=data.output,
        target=engagement.target
    )
    
    return OutputAnalysisResponse(
        summary=analysis["summary"],
        findings=analysis["findings"],
        next_steps=analysis["next_steps"],
        risk_level=analysis["risk_level"]
    )


@router.post("/phase-guidance/{engagement_id}", response_model=dict)
async def get_phase_guidance(
    engagement_id: str,
    phase_number: Optional[int] = Query(None, ge=1, le=8),
    db: Session = Depends(get_db)
):
    """
    Get AI guidance for the current phase.
    
    Returns customized recommendations based on:
    - Target type and technology
    - Current phase objectives
    - Progress so far
    """
    # Verify engagement exists
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Get phase
    query = db.query(Phase).filter(Phase.engagement_id == engagement_id)
    
    if phase_number:
        current_phase = query.filter(Phase.phase_number == phase_number).first()
    else:
        current_phase = query.filter(Phase.status == "in_progress").first()
    
    if not current_phase:
        raise HTTPException(status_code=404, detail="No active phase found")
    
    # Generate guidance
    ai_service = AIService()
    guidance = await ai_service.generate_phase_guidance(
        phase_name=current_phase.name,
        phase_number=current_phase.phase_number,
        target=engagement.target,
        objectives=current_phase.objectives
    )
    
    return {
        "phase_number": current_phase.phase_number,
        "phase_name": current_phase.name,
        "guidance": guidance
    }


@router.post("/suggest-next-scan/{engagement_id}", response_model=dict)
async def suggest_next_scan(
    engagement_id: str,
    db: Session = Depends(get_db)
):
    """
    Get AI suggestion for the next scan to run.
    
    Based on current phase and previous scan results.
    """
    # Verify engagement exists
    engagement = db.query(Engagement).filter(Engagement.id == engagement_id).first()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engagement not found")
    
    # Get current phase
    current_phase = db.query(Phase).filter(
        Phase.engagement_id == engagement_id,
        Phase.status == "in_progress"
    ).first()
    
    # Generate suggestion
    ai_service = AIService()
    suggestion = await ai_service.suggest_next_scan(
        target=engagement.target,
        phase_number=current_phase.phase_number if current_phase else 4,
        phase_name=current_phase.name if current_phase else "Vulnerability Analysis"
    )
    
    return suggestion
