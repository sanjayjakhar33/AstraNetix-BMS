from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Request schemas
class TrafficAnalysisRequest(BaseModel):
    tenant_id: Optional[str] = None
    start_date: str  # ISO format
    end_date: str    # ISO format
    analysis_type: str = "comprehensive"  # comprehensive, peak_hours, congestion

# Response schemas
class TrafficAnalysisResponse(BaseModel):
    analysis_id: str
    predicted_bandwidth_gb: List[float]
    peak_hours: List[int]
    congestion_risk_score: float
    optimization_recommendations: List[str]
    confidence_score: float
    data_points_analyzed: int

class OptimizationRecommendation(BaseModel):
    user_id: str
    username: str
    current_plan: str
    priority_level: str  # high, standard, low
    recommended_bandwidth: int  # in Mbps
    traffic_shaping_rules: Dict[str, str]
    recommendations: List[str]

class QoSOptimizationResponse(BaseModel):
    optimization_id: str
    total_users_analyzed: int
    high_priority_users: int
    optimization_score: float
    user_recommendations: List[OptimizationRecommendation]
    global_recommendations: List[str]

class NetworkPredictionResponse(BaseModel):
    prediction_id: str
    days_ahead: int
    predicted_peak_usage_gb: float
    predicted_average_usage_gb: float
    growth_rate_percent: float
    confidence_score: float
    capacity_recommendations: List[str]
    risk_factors: List[str]

class NetworkAnomaly(BaseModel):
    type: str  # unusual_data_usage, bandwidth_spike, connection_failure, etc.
    severity: str  # low, medium, high, critical
    description: str
    timestamp: str
    user_id: Optional[str]
    z_score: float

class AnomalyDetectionResponse(BaseModel):
    detection_id: str
    time_period_hours: int
    anomalies_detected: int
    high_severity_count: int
    anomalies: List[NetworkAnomaly]
    baseline_metrics: Dict[str, float]
    recommendations: List[str]