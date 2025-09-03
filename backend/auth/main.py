from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import timedelta

from ..shared.database.connection import get_db
from ..shared.models.models import Founder, ISP, User
from ..shared.utils.security import verify_password, create_access_token, hash_password
from ..shared.config import settings
from .schemas import LoginRequest, LoginResponse, RegisterRequest, UserResponse

router = APIRouter()
security = HTTPBearer()

@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token
    Supports login for Founder, ISP, and User roles
    """
    try:
        user = None
        user_type = None
        
        # Try to find user in founders table
        founder = db.query(Founder).filter(Founder.email == credentials.email).first()
        if founder and verify_password(credentials.password, founder.password_hash):
            user = founder
            user_type = "founder"
        
        # Try to find user in ISPs table
        if not user:
            isp = db.query(ISP).filter(ISP.email == credentials.email).first()
            if isp and verify_password(credentials.password, isp.password_hash):
                user = isp
                user_type = "isp"
        
        # Try to find user in users table
        if not user:
            end_user = db.query(User).filter(User.email == credentials.email).first()
            if end_user and verify_password(credentials.password, end_user.password_hash):
                user = end_user
                user_type = "user"
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "user_type": user_type,
                "name": getattr(user, 'full_name', getattr(user, 'company_name', 'Unknown'))
            },
            expires_delta=access_token_expires
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user_type=user_type,
            user_id=str(user.id),
            name=getattr(user, 'full_name', getattr(user, 'company_name', 'Unknown')),
            email=user.email
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )

@router.post("/register/founder", response_model=UserResponse)
async def register_founder(
    user_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new founder (system admin)
    """
    try:
        # Check if email already exists
        existing_founder = db.query(Founder).filter(Founder.email == user_data.email).first()
        if existing_founder:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new founder
        new_founder = Founder(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            company_name=user_data.company_name,
            full_name=user_data.full_name,
            phone=user_data.phone,
            address=user_data.address
        )
        
        db.add(new_founder)
        db.commit()
        db.refresh(new_founder)
        
        return UserResponse(
            id=str(new_founder.id),
            email=new_founder.email,
            name=new_founder.full_name,
            user_type="founder",
            is_active=new_founder.is_active
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user)
):
    """
    Get current authenticated user information
    """
    return UserResponse(
        id=current_user["sub"],
        email=current_user["email"],
        name=current_user["name"],
        user_type=current_user["user_type"],
        is_active=True
    )

@router.post("/logout")
async def logout():
    """
    Logout endpoint (client-side token removal)
    """
    return {"message": "Logged out successfully"}

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Verify JWT token and return current user data
    """
    from ..shared.utils.security import verify_access_token
    
    try:
        token = credentials.credentials
        payload = verify_access_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return payload
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )