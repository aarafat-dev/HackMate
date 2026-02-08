"""
HackMate v2.0 - FastAPI Application
Main entry point for the backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import get_settings
from database import init_db

# Import routers
from routers.engagements import router as engagements_router
from routers.methodology import router as methodology_router
from routers.terminal import router as terminal_router
from routers.findings import router as findings_router
from routers.scans import router as scans_router
from routers.reports import router as reports_router
from routers.ai import router as ai_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    
    Handles startup and shutdown events.
    """
    # Startup
    print("=" * 60)
    print(f"  {settings.app_name} Starting...")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    print(f"  ✓ Database initialized")
    print(f"  ✓ API documentation at /docs")
    print("=" * 60)
    
    yield
    
    # Shutdown
    print("\n[SHUTDOWN] HackMate API shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="""
## HackMate v2.0 API

Professional penetration testing platform with AI assistance.

### Features
- **Engagements**: Manage penetration testing projects
- **PTES Methodology**: 8-phase structured approach
- **Terminal**: Execute security tools safely
- **Findings**: Track discovered vulnerabilities
- **Scans**: Run automated security scans
- **Reports**: Generate professional reports
- **AI Assistant**: Get intelligent guidance

### Documentation
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
    """,
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(engagements_router)
app.include_router(methodology_router)
app.include_router(terminal_router)
app.include_router(findings_router)
app.include_router(scans_router)
app.include_router(reports_router)
app.include_router(ai_router)


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - returns API info.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs"
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "available"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
