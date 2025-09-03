from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def user_portal_root():
    """User Portal API root endpoint"""
    return {"message": "User Portal API - Coming Soon"}

# Placeholder for user portal endpoints
# This will be implemented in the next phase