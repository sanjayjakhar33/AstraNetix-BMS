from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

# Request schemas
class BranchCreateRequest(BaseModel):
    name: str
    location: Optional[str] = None
    manager_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    settings: Optional[Dict[str, Any]] = None

# Response schemas
class BranchCreateResponse(BaseModel):
    branch_id: str
    name: str
    location: Optional[str]
    manager_name: Optional[str]
    contact_email: Optional[str]
    message: str

class TopUser(BaseModel):
    username: str
    full_name: str
    plan: str
    usage_gb: float

class BranchDashboardResponse(BaseModel):
    branch_id: str
    name: str
    location: Optional[str]
    manager_name: Optional[str]
    total_users: int
    monthly_revenue: float
    total_bandwidth_gb: float
    avg_peak_usage_mbps: float
    open_support_tickets: int
    network_health: float
    top_users: List[TopUser]

class BranchListResponse(BaseModel):
    id: str
    name: str
    location: Optional[str]
    manager_name: Optional[str]
    contact_email: Optional[str]
    phone: Optional[str]
    user_count: int
    monthly_revenue: float
    is_active: bool
    created_at: str

class BranchUserListResponse(BaseModel):
    id: str
    username: str
    full_name: str
    email: str
    subscription_plan: str
    bandwidth_limit: int
    is_active: bool
    recent_usage_gb: float
    last_payment_status: str
    last_payment_date: Optional[str]
    open_tickets: int
    created_at: str

class BranchAnalyticsResponse(BaseModel):
    branch_id: str
    branch_name: str
    total_users: int
    new_users_month: int
    user_growth_rate: float
    total_revenue_month: float
    avg_revenue_per_user: float
    peak_usage_hour: int
    customer_satisfaction_score: float
    support_tickets_month: int
    network_utilization: float
    recommendations: List[str]
    performance_score: float