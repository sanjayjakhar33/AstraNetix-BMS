from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# Request schemas
class ISPCreateRequest(BaseModel):
    company_name: str
    email: EmailStr
    password: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    branding: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None

class GlobalPoliciesRequest(BaseModel):
    pricing_policies: Optional[Dict[str, Any]] = None
    bandwidth_rules: Optional[Dict[str, Any]] = None
    security_settings: Optional[Dict[str, Any]] = None
    payment_gateways: Optional[Dict[str, Any]] = None
    compliance_settings: Optional[Dict[str, Any]] = None

# Response schemas
class ISPCreateResponse(BaseModel):
    isp_id: str
    portal_url: str
    domain: str
    message: str

class ISPSummary(BaseModel):
    id: str
    company_name: str
    domain: str
    created_at: str
    is_active: bool

class FounderDashboardResponse(BaseModel):
    total_isps: int
    total_branches: int
    total_users: int
    monthly_revenue: float
    system_health: float
    recent_isps: List[ISPSummary]

class ISPListResponse(BaseModel):
    id: str
    company_name: str
    domain: str
    email: str
    contact_person: Optional[str]
    branches_count: int
    users_count: int
    monthly_revenue: float
    is_active: bool
    created_at: str
    portal_url: str

class RevenueAnalyticsResponse(BaseModel):
    historical_revenue: Dict[str, float]  # Month -> Revenue
    predicted_revenue: List[float]  # Next 3 months prediction
    total_revenue: float
    growth_rate: float
    confidence_score: float

class SystemAlert(BaseModel):
    type: str  # info, warning, error
    message: str
    timestamp: str

class SystemMonitoringResponse(BaseModel):
    system_health: float
    active_users: int
    total_bandwidth_gb: float
    avg_peak_usage_mbps: float
    alerts: List[SystemAlert]
    recommendations: List[str]