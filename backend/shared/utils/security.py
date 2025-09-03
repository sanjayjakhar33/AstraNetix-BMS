from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import secrets
import string

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def generate_password(length: int = 12) -> str:
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

# JWT token management
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, secret_key: str = None, algorithm: str = "HS256"):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    
    if not secret_key:
        from ..config import settings
        secret_key = settings.jwt_secret_key
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

def verify_access_token(token: str, secret_key: str = None, algorithm: str = "HS256") -> Optional[dict]:
    """Verify and decode a JWT access token"""
    try:
        if not secret_key:
            from ..config import settings
            secret_key = settings.jwt_secret_key
            
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return None

def generate_api_key(length: int = 32) -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(length)

def generate_domain_safe_string(text: str) -> str:
    """Generate a domain-safe string from text"""
    # Convert to lowercase and replace spaces with hyphens
    domain_safe = text.lower().replace(' ', '-')
    
    # Keep only alphanumeric characters and hyphens
    domain_safe = ''.join(c for c in domain_safe if c.isalnum() or c == '-')
    
    # Remove multiple consecutive hyphens
    while '--' in domain_safe:
        domain_safe = domain_safe.replace('--', '-')
    
    # Remove leading/trailing hyphens
    domain_safe = domain_safe.strip('-')
    
    return domain_safe

def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Mask sensitive data showing only the last few characters"""
    if len(data) <= visible_chars:
        return '*' * len(data)
    return '*' * (len(data) - visible_chars) + data[-visible_chars:]