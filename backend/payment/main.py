from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def payment_engine_root():
    """Payment Engine API root endpoint"""
    return {"message": "Payment Engine API - Coming Soon"}

# Placeholder for payment processing endpoints
# This will be implemented in the next phase