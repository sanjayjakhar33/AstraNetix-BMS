from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from decimal import Decimal

# Request schemas
class SubscriberCreateRequest(BaseModel):
    branch_id: str
    plan_id: str
    username: str
    email: EmailStr
    password: Optional[str] = None  # If not provided, will be auto-generated
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    connection_type: Optional[str] = "broadband"
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None

class PlanCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    bandwidth_limit: int  # in Mbps
    data_limit: Optional[int] = None  # in GB, null for unlimited
    price: Decimal
    currency: Optional[str] = "USD"
    billing_cycle: Optional[str] = "monthly"
    features: Optional[Dict[str, Any]] = None

class RadiusConfigRequest(BaseModel):
    server_host: str
    server_port: int = 1812
    secret: str
    nas_identifier: str
    auth_port: Optional[int] = 1812
    acct_port: Optional[int] = 1813

# Response schemas
class TicketSummary(BaseModel):
    id: str
    title: str
    priority: str
    status: str
    created_at: str

class ISPDashboardResponse(BaseModel):
    subscriber_count: int
    branches_count: int
    monthly_revenue: float
    total_bandwidth_gb: float
    avg_peak_usage_mbps: float
    network_health: float
    recent_tickets: List[TicketSummary]
    branding: Dict[str, Any]
    # Enhanced with new features
    noc_alerts: int
    sustainability_score: float
    sla_compliance: float
    active_campaigns: int

class EnhancedISPDashboard(BaseModel):
    # Core metrics
    subscriber_count: int
    branches_count: int
    monthly_revenue: float
    total_bandwidth_gb: float
    avg_peak_usage_mbps: float
    network_health: float
    
    # NOC Dashboard metrics
    active_alerts: int
    critical_alerts: int
    network_uptime: float
    
    # CRM & Marketing metrics
    active_campaigns: int
    conversion_rate: float
    customer_segments: int
    
    # Sustainability metrics
    energy_efficiency_score: float
    carbon_footprint: float
    renewable_energy_percentage: float
    
    # SLA metrics
    sla_compliance_percentage: float
    sla_breaches: int
    
    # AI Audit insights
    security_score: float
    anomalies_detected: int
    
    # Recent activities
    recent_tickets: List[TicketSummary]
    recent_alerts: List[Dict[str, Any]]
    recent_reports: List[Dict[str, Any]]
    
    branding: Dict[str, Any]

# Multi-language support schemas
class LocalizationConfig(BaseModel):
    language: str  # en, es, fr, ar, hi
    currency: str  # USD, EUR, INR, etc.
    date_format: str
    number_format: str
    timezone: str

class MultiLanguageContent(BaseModel):
    en: str
    es: Optional[str] = None
    fr: Optional[str] = None
    ar: Optional[str] = None
    hi: Optional[str] = None

# Mobile app configuration
class MobileAppFeatures(BaseModel):
    usage_monitoring: bool
    bill_payment: bool
    support_tickets: bool
    notifications: bool
    speedtest: bool
    plan_upgrade: bool

class MobileAppBranding(BaseModel):
    app_name: str
    primary_color: str
    secondary_color: str
    logo_url: str
    splash_screen_url: str
    icon_url: str

# Training module schemas
class TrainingModuleResponse(BaseModel):
    id: str
    title: str
    description: str
    difficulty_level: str
    estimated_duration: int
    completion_rate: float
    is_active: bool

# Webhook configuration
class WebhookCreate(BaseModel):
    url: str
    events: List[str]
    secret_key: Optional[str] = None
    is_active: bool = True

class WebhookResponse(BaseModel):
    id: str
    url: str
    events: List[str]
    is_active: bool
    last_delivery: Optional[datetime]
    created_at: datetime

class SubscriberCreateResponse(BaseModel):
    user_id: str
    username: str
    email: str
    generated_password: Optional[str] = None
    plan_name: str
    bandwidth_limit: int
    message: str

class SubscriberListResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    subscription_plan: str
    bandwidth_limit: int
    is_active: bool
    last_usage_gb: float
    last_payment_status: str
    created_at: str
    branch_name: str

class PlanResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    bandwidth_limit: int
    data_limit: Optional[int]
    price: float
    currency: str
    billing_cycle: str
    features: Dict[str, Any]
    is_active: bool

class CongestionPoint(BaseModel):
    location: str
    utilization: float
    recommendation: str

class BandwidthOptimizationResponse(BaseModel):
    total_usage_gb: float
    peak_hours: List[int]
    optimization_score: float
    recommendations: List[str]
    congestion_points: List[CongestionPoint]
    predicted_growth: float

class SubscriberAnalyticsResponse(BaseModel):
    total_subscribers: int
    active_subscribers: int
    churn_rate: float
    growth_rate: float
    subscribers_by_month: Dict[str, int]
    plan_distribution: Dict[str, int]
    high_usage_users: int
    revenue_per_user: float
    satisfaction_score: float