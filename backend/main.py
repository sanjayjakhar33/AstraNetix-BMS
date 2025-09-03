from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import uvicorn
import os

# Import microservice routers
from founder.main import router as founder_router
from isp.main import router as isp_router
from branch.main import router as branch_router
from user.main import router as user_router
from payment.main import router as payment_router
from ai_manager.main import router as ai_router
from auth.main import router as auth_router

from shared.config import settings
from shared.database.connection import init_db

# Create FastAPI application
app = FastAPI(
    title="AstraNetix AI Bandwidth Management System",
    description="Complete AI-powered SaaS platform for ISP bandwidth management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include microservice routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(founder_router, prefix="/api/founder", tags=["Founder Portal"])
app.include_router(isp_router, prefix="/api/isp", tags=["ISP Portal"])
app.include_router(branch_router, prefix="/api/branch", tags=["Branch Management"])
app.include_router(user_router, prefix="/api/user", tags=["User Portal"])
app.include_router(payment_router, prefix="/api/payment", tags=["Payment Engine"])
app.include_router(ai_router, prefix="/api/ai", tags=["AI Manager"])

@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "message": "AstraNetix AI Bandwidth Management System",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }

if __name__ == '__main__':
    print('AstraNetix BMS Backend service is running...')
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )