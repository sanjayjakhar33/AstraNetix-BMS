from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..shared.database.connection import get_db
from ..shared.models.models import Founder, ISP, User
from .main import get_current_user

async def get_current_founder(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Founder:
    """
    Get current authenticated founder
    """
    if current_user["user_type"] != "founder":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Founder role required."
        )
    
    founder = db.query(Founder).filter(Founder.id == current_user["sub"]).first()
    if not founder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Founder not found"
        )
    
    return founder

async def get_current_isp(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ISP:
    """
    Get current authenticated ISP
    """
    if current_user["user_type"] != "isp":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. ISP role required."
        )
    
    isp = db.query(ISP).filter(ISP.id == current_user["sub"]).first()
    if not isp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ISP not found"
        )
    
    return isp

async def get_current_end_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated end user
    """
    if current_user["user_type"] != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. User role required."
        )
    
    user = db.query(User).filter(User.id == current_user["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user