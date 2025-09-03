from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def branch_portal_root():
    """Branch Management API root endpoint"""
    return {"message": "Branch Management API - Coming Soon"}

# Placeholder for branch management endpoints
# This will be implemented in the next phase