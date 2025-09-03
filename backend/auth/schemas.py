from pydantic import BaseModel, EmailStr
from typing import Optional

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user_type: str  # founder, isp, user
    user_id: str
    name: str
    email: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    company_name: str
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    user_type: str
    is_active: bool