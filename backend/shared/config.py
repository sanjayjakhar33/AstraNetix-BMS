import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    app_name: str = "AstraNetix AI Bandwidth Management System"
    debug: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Database configuration
    database_url: str = os.getenv('DATABASE_URL', 'postgresql://astranetix_user:secure_password@localhost:5432/astranetix_bms')
    
    # Redis configuration
    redis_url: str = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # JWT configuration
    jwt_secret_key: str = os.getenv('JWT_SECRET_KEY', 'your-super-secure-secret-key-change-in-production')
    jwt_algorithm: str = os.getenv('JWT_ALGORITHM', 'HS256')
    access_token_expire_minutes: int = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    
    # AI/ML configuration
    openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
    google_gemini_api_key: str = os.getenv('GOOGLE_GEMINI_API_KEY', '')
    
    # Payment gateway configuration
    stripe_secret_key: str = os.getenv('STRIPE_SECRET_KEY', '')
    stripe_publishable_key: str = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
    paypal_client_id: str = os.getenv('PAYPAL_CLIENT_ID', '')
    paypal_client_secret: str = os.getenv('PAYPAL_CLIENT_SECRET', '')
    razorpay_key_id: str = os.getenv('RAZORPAY_KEY_ID', '')
    razorpay_key_secret: str = os.getenv('RAZORPAY_KEY_SECRET', '')
    
    # Network configuration
    radius_server_host: str = os.getenv('RADIUS_SERVER_HOST', 'localhost')
    radius_server_port: int = int(os.getenv('RADIUS_SERVER_PORT', '1812'))
    radius_secret: str = os.getenv('RADIUS_SECRET', 'your-radius-secret')
    
    # CORS configuration
    cors_origins: List[str] = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003').split(',')
    
    # Deployment configuration
    domain: str = os.getenv('DOMAIN', 'astranetix.com')
    ssl_enabled: bool = os.getenv('SSL_ENABLED', 'true').lower() == 'true'
    cdn_enabled: bool = os.getenv('CDN_ENABLED', 'true').lower() == 'true'
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()

# Legacy database configuration for backward compatibility
DB_HOST = settings.database_url.split('@')[1].split(':')[0] if '@' in settings.database_url else 'localhost'
DB_PORT = 5432
DB_USER = settings.database_url.split('://')[1].split(':')[0] if '://' in settings.database_url else 'user'
DB_PASSWORD = settings.database_url.split('://')[1].split(':')[1].split('@')[0] if '://' in settings.database_url and ':' in settings.database_url.split('://')[1] else 'password'
DB_NAME = settings.database_url.split('/')[-1] if '/' in settings.database_url else 'dbname'