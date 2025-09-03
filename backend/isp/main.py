from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def isp_portal_root():
    """ISP Portal API root endpoint"""
    return {"message": "ISP Portal API - Coming Soon"}

# Placeholder for ISP portal endpoints
# This will be implemented in the next phase