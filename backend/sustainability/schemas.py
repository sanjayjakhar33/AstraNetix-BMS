from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime, date

# Sustainability Metrics Schemas
class SustainabilityMetricCreate(BaseModel):
    metric_type: str  # energy_consumption, carbon_footprint, renewable_usage
    value: float
    unit: str  # kWh, kg_co2, percentage, etc.
    period_start: date
    period_end: date
    device_id: Optional[str] = None
    location: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class SustainabilityMetricResponse(BaseModel):
    id: str
    tenant_id: str
    tenant_type: str
    metric_type: str
    value: float
    unit: str
    period_start: date
    period_end: date
    device_id: Optional[str]
    location: Optional[str]
    metadata: Dict[str, Any]
    created_at: datetime

# Green Dashboard Schemas
class GreenDashboardResponse(BaseModel):
    total_energy_consumption: float  # kWh
    carbon_footprint: float  # kg CO2
    renewable_energy_percentage: float
    energy_efficiency_score: float
    cost_savings: float
    green_initiatives: List[Dict[str, Any]]
    sustainability_goals: Dict[str, Any]
    environmental_impact: Dict[str, float]

# Carbon Offset Schemas
class CarbonOffsetPurchase(BaseModel):
    amount_co2: float  # kg CO2
    price_per_kg: float
    provider: str
    certificate_id: Optional[str] = None
    project_details: Dict[str, Any]

class CarbonOffsetResponse(BaseModel):
    id: str
    tenant_id: str
    amount_co2: float
    total_cost: float
    provider: str
    certificate_id: Optional[str]
    project_details: Dict[str, Any]
    purchase_date: datetime
    status: str

# Sustainability Report Schemas
class SustainabilityReport(BaseModel):
    report_period: str
    energy_metrics: Dict[str, float]
    carbon_metrics: Dict[str, float]
    efficiency_improvements: List[Dict[str, Any]]
    cost_analysis: Dict[str, float]
    recommendations: List[str]
    compliance_status: Dict[str, Any]
    generated_at: datetime

# Green Initiative Schemas
class GreenInitiativeCreate(BaseModel):
    title: str
    description: str
    category: str  # energy_saving, renewable, efficiency, waste_reduction
    target_metrics: Dict[str, float]
    implementation_plan: Dict[str, Any]
    budget: Optional[float] = None
    timeline: Dict[str, str]

class GreenInitiativeResponse(BaseModel):
    id: str
    tenant_id: str
    title: str
    description: str
    category: str
    target_metrics: Dict[str, float]
    actual_metrics: Dict[str, float]
    implementation_plan: Dict[str, Any]
    budget: Optional[float]
    timeline: Dict[str, str]
    status: str
    roi: Optional[float]
    created_at: datetime