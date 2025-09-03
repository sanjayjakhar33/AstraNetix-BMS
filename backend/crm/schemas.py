from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

# Customer Segmentation Schemas
class CustomerSegmentCreate(BaseModel):
    name: str
    criteria: Dict[str, Any]
    description: Optional[str] = None
    auto_update: bool = True

class CustomerSegmentResponse(BaseModel):
    id: str
    isp_id: str
    name: str
    criteria: Dict[str, Any]
    description: Optional[str]
    auto_update: bool
    subscriber_count: int
    created_at: datetime

# Marketing Campaign Schemas
class MarketingCampaignCreate(BaseModel):
    name: str
    campaign_type: str  # email, sms, push
    target_segments: List[str]
    content: Dict[str, Any]
    scheduled_at: Optional[datetime] = None

class MarketingCampaignResponse(BaseModel):
    id: str
    isp_id: str
    name: str
    campaign_type: str
    status: str
    target_segments: List[str]
    content: Dict[str, Any]
    scheduled_at: Optional[datetime]
    metrics: Dict[str, Any]
    created_at: datetime

class CampaignMetrics(BaseModel):
    sent: int
    delivered: int
    opened: int
    clicked: int
    unsubscribed: int
    bounced: int
    delivery_rate: float
    open_rate: float
    click_rate: float

# Customer Analytics
class CustomerAnalytics(BaseModel):
    total_subscribers: int
    active_subscribers: int
    churn_rate: float
    average_revenue: float
    segments: List[Dict[str, Any]]
    growth_trends: List[Dict[str, Any]]
    geographic_distribution: Dict[str, int]

# Loyalty & Referral Schemas
class LoyaltyProgramCreate(BaseModel):
    name: str
    description: str
    points_per_dollar: float
    redemption_rules: Dict[str, Any]
    tier_benefits: Dict[str, Any]

class ReferralProgramCreate(BaseModel):
    name: str
    description: str
    referrer_reward: Dict[str, Any]
    referee_reward: Dict[str, Any]
    conditions: Dict[str, Any]