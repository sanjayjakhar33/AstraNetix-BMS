from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

# NOC Dashboard Schemas
class NetworkAlertCreate(BaseModel):
    alert_type: str
    severity: str
    title: str
    description: Optional[str] = None
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class NetworkAlertResponse(BaseModel):
    id: str
    tenant_id: str
    tenant_type: str
    alert_type: str
    severity: str
    title: str
    description: Optional[str]
    source: Optional[str]
    status: str
    escalated: bool
    auto_resolved: bool
    metadata: Dict[str, Any]
    created_at: datetime
    resolved_at: Optional[datetime]

class NOCDashboardResponse(BaseModel):
    total_alerts: int
    critical_alerts: int
    network_health: float
    uptime_percentage: float
    active_devices: int
    bandwidth_utilization: float
    recent_alerts: List[NetworkAlertResponse]
    network_topology: Dict[str, Any]
    performance_metrics: Dict[str, float]

# SLA Management Schemas
class SLADefinitionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    uptime_target: float = 0.999
    response_time_target: Optional[int] = None
    resolution_time_target: Optional[int] = None
    bandwidth_guarantee: Optional[int] = None
    penalties: Optional[Dict[str, Any]] = {}

class SLADefinitionResponse(BaseModel):
    id: str
    isp_id: str
    name: str
    description: Optional[str]
    uptime_target: float
    response_time_target: Optional[int]
    resolution_time_target: Optional[int]
    bandwidth_guarantee: Optional[int]
    penalties: Dict[str, Any]
    is_active: bool
    created_at: datetime

class SLAComplianceReport(BaseModel):
    sla_id: str
    period_start: datetime
    period_end: datetime
    uptime_achieved: float
    avg_response_time: float
    avg_resolution_time: float
    compliance_percentage: float
    breaches: List[Dict[str, Any]]
    penalties_incurred: float

# AI Audit Schemas
class AuditAnomalyResponse(BaseModel):
    id: str
    user_id: Optional[str]
    tenant_id: Optional[str]
    action: str
    resource: Optional[str]
    ai_risk_score: Optional[float]
    anomaly_type: str
    description: str
    confidence: float
    created_at: datetime

class AIAuditAnalysisResponse(BaseModel):
    total_logs: int
    anomalies_detected: int
    high_risk_activities: int
    suspicious_patterns: List[Dict[str, Any]]
    recommendations: List[str]
    risk_distribution: Dict[str, int]