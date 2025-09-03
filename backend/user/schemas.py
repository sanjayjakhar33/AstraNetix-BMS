from pydantic import BaseModel
from typing import Optional, List, Dict, Any

# Request schemas
class SupportTicketCreateRequest(BaseModel):
    title: str
    description: str
    category: Optional[str] = "general"  # technical, billing, general
    priority: Optional[str] = "medium"   # low, medium, high, urgent

class PlanUpgradeRequest(BaseModel):
    new_plan_id: str
    effective_date: Optional[str] = None  # ISO format, default to immediate

# Response schemas
class UserDashboardResponse(BaseModel):
    user_id: str
    username: str
    full_name: str
    email: str
    subscription_plan: str
    bandwidth_limit: int
    data_limit: Optional[int]
    current_usage_gb: float
    usage_percentage: float
    peak_usage_mbps: int
    account_status: str  # active, suspended, expired
    next_billing_date: str
    last_payment_amount: float
    last_payment_status: str
    open_support_tickets: int
    connection_status: str  # online, offline
    ip_address: Optional[str]

class UsageAlert(BaseModel):
    type: str  # info, warning, critical
    message: str

class UsageResponse(BaseModel):
    user_id: str
    period_days: int
    total_usage_gb: float
    avg_daily_usage_gb: float
    peak_usage_mbps: int
    data_limit_gb: Optional[int]
    bandwidth_limit_mbps: int
    daily_usage: Dict[str, Dict[str, float]]  # date -> usage details
    alerts: List[UsageAlert]
    optimization_tips: List[str]

class PaymentInfo(BaseModel):
    id: str
    amount: float
    currency: str
    status: str
    gateway: str
    billing_period_start: Optional[str]
    billing_period_end: Optional[str]
    created_at: str

class PaymentHistoryResponse(BaseModel):
    user_id: str
    total_payments: int
    total_amount_paid: float
    payments: List[PaymentInfo]

class SupportTicketResponse(BaseModel):
    ticket_id: str
    title: str
    status: str
    category: str
    priority: str
    created_at: str
    auto_suggestions: List[str]
    estimated_resolution: str