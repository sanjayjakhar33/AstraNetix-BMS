from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from ..shared.database.connection import get_db
from ..shared.models.models import BandwidthUsage, User, Branch, ISP, AIInsight
from .schemas import (
    TrafficAnalysisRequest, TrafficAnalysisResponse, 
    QoSOptimizationResponse, NetworkPredictionResponse,
    AnomalyDetectionResponse, OptimizationRecommendation
)
from ..auth.dependencies import get_current_user

router = APIRouter()

class AIBandwidthOptimizer:
    """AI-powered bandwidth optimization engine"""
    
    def __init__(self):
        # In production, these would be pre-trained ML models
        self.traffic_patterns = {}
        self.congestion_thresholds = {
            'low': 60,
            'medium': 80,
            'high': 95
        }
    
    async def analyze_traffic_patterns(self, network_data: List[Dict]) -> Dict:
        """
        Real-time traffic pattern analysis using machine learning
        - Identify peak usage periods
        - Detect anomalous traffic behavior
        - Predict bandwidth requirements
        """
        if not network_data:
            return {
                'predicted_bandwidth': [],
                'congestion_risk': [],
                'optimization_recommendations': []
            }
        
        # Convert to pandas DataFrame for analysis
        df = pd.DataFrame(network_data)
        
        # Extract time-based features
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        
        # Calculate moving averages
        df['bandwidth_ma_7'] = df['total_bytes'].rolling(window=7, min_periods=1).mean()
        df['bandwidth_std_7'] = df['total_bytes'].rolling(window=7, min_periods=1).std()
        
        # Identify peak hours
        hourly_avg = df.groupby('hour')['total_bytes'].mean()
        peak_hours = hourly_avg.nlargest(3).index.tolist()
        
        # Simple bandwidth prediction (in production, use LSTM/Prophet)
        recent_trend = df['total_bytes'].tail(7).mean()
        predicted_bandwidth = [recent_trend * 1.1, recent_trend * 1.05, recent_trend * 1.15]
        
        # Congestion risk calculation
        current_utilization = df['peak_usage_mbps'].tail(1).iloc[0] if len(df) > 0 else 0
        congestion_risk = min(current_utilization / 100, 1.0)
        
        # Generate recommendations
        recommendations = self._generate_traffic_recommendations(df, peak_hours, congestion_risk)
        
        return {
            'predicted_bandwidth': predicted_bandwidth,
            'congestion_risk': [congestion_risk],
            'optimization_recommendations': recommendations,
            'peak_hours': peak_hours,
            'current_utilization': current_utilization
        }
    
    async def dynamic_qos_optimization(self, subscriber_data: List[Dict]) -> Dict:
        """
        AI-powered Quality of Service optimization
        - Application-specific traffic prioritization
        - Dynamic queue management
        - Latency optimization
        """
        qos_recommendations = {}
        
        for subscriber in subscriber_data:
            user_id = subscriber['id']
            usage_patterns = subscriber.get('usage_history', [])
            bandwidth_limit = subscriber.get('bandwidth_limit', 100)
            
            # Analyze usage patterns
            if usage_patterns:
                avg_usage = sum(usage_patterns) / len(usage_patterns)
                usage_variance = np.var(usage_patterns)
                
                # Generate QoS rules based on patterns
                qos_rules = {
                    'priority_level': 'high' if avg_usage > bandwidth_limit * 0.8 else 'standard',
                    'burst_allowance': min(bandwidth_limit * 1.2, bandwidth_limit + 50),
                    'rate_limiting': {
                        'download': bandwidth_limit * 1024,  # Convert to Kbps
                        'upload': bandwidth_limit * 1024 * 0.1,  # 10% of download
                    },
                    'traffic_shaping': {
                        'video_streaming': 'priority',
                        'gaming': 'low_latency',
                        'file_download': 'background'
                    },
                    'recommendations': self._generate_qos_recommendations(avg_usage, bandwidth_limit, usage_variance)
                }
                
                qos_recommendations[user_id] = qos_rules
        
        return qos_recommendations
    
    def _generate_traffic_recommendations(self, df: pd.DataFrame, peak_hours: List[int], congestion_risk: float) -> List[str]:
        """Generate traffic optimization recommendations"""
        recommendations = []
        
        if congestion_risk > 0.8:
            recommendations.append("Critical: Network congestion detected. Consider upgrading bandwidth capacity.")
            recommendations.append("Implement traffic shaping for non-essential applications during peak hours.")
        
        if peak_hours:
            peak_str = ", ".join([f"{h}:00-{h+1}:00" for h in peak_hours])
            recommendations.append(f"Peak usage detected during: {peak_str}. Consider implementing peak-hour pricing.")
        
        # Analyze data patterns
        if len(df) > 7:
            recent_growth = (df['total_bytes'].tail(3).mean() - df['total_bytes'].head(3).mean()) / df['total_bytes'].head(3).mean()
            if recent_growth > 0.2:
                recommendations.append("Rapid usage growth detected. Plan for 30% capacity increase within 3 months.")
        
        recommendations.append("Enable content caching for popular streaming services to reduce backbone usage.")
        recommendations.append("Implement gaming traffic prioritization to improve customer satisfaction.")
        
        return recommendations
    
    def _generate_qos_recommendations(self, avg_usage: float, bandwidth_limit: int, usage_variance: float) -> List[str]:
        """Generate QoS recommendations for individual users"""
        recommendations = []
        
        utilization = avg_usage / bandwidth_limit if bandwidth_limit > 0 else 0
        
        if utilization > 0.9:
            recommendations.append("User consistently near bandwidth limit. Consider plan upgrade.")
            recommendations.append("Implement fair usage policy to prevent service degradation.")
        elif utilization < 0.3:
            recommendations.append("User under-utilizing plan. Consider plan downgrade to optimize revenue.")
        
        if usage_variance > avg_usage * 0.5:
            recommendations.append("Highly variable usage pattern. Implement burst allowance for better experience.")
        
        return recommendations

# Initialize AI optimizer
ai_optimizer = AIBandwidthOptimizer()

@router.post("/analyze/traffic", response_model=TrafficAnalysisResponse)
async def analyze_traffic_patterns(
    request: TrafficAnalysisRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze traffic patterns using AI for bandwidth optimization
    """
    try:
        # Get traffic data based on request parameters
        start_date = datetime.fromisoformat(request.start_date.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(request.end_date.replace('Z', '+00:00'))
        
        # Query bandwidth usage data
        query = db.query(BandwidthUsage).filter(
            BandwidthUsage.date >= start_date.date(),
            BandwidthUsage.date <= end_date.date()
        )
        
        # Filter by tenant if specified
        if request.tenant_id:
            if current_user['user_type'] == 'isp':
                # ISP can only see their own data
                query = query.join(User).join(Branch).join(ISP).filter(ISP.id == request.tenant_id)
            elif current_user['user_type'] == 'founder':
                # Founder can see any ISP's data
                query = query.join(User).join(Branch).join(ISP).filter(ISP.id == request.tenant_id)
        
        usage_data = query.all()
        
        # Convert to format for AI analysis
        network_data = [
            {
                'timestamp': usage.created_at.isoformat(),
                'total_bytes': usage.total_bytes,
                'upload_bytes': usage.upload_bytes,
                'download_bytes': usage.download_bytes,
                'peak_usage_mbps': usage.peak_usage_mbps
            }
            for usage in usage_data
        ]
        
        # Perform AI analysis
        analysis_result = await ai_optimizer.analyze_traffic_patterns(network_data)
        
        # Store insights in database
        if request.tenant_id:
            insight = AIInsight(
                tenant_id=request.tenant_id,
                tenant_type=current_user['user_type'],
                insight_type='traffic_analysis',
                data=analysis_result,
                confidence_score=0.85
            )
            db.add(insight)
            db.commit()
        
        return TrafficAnalysisResponse(
            analysis_id=str(insight.id) if request.tenant_id else "demo",
            predicted_bandwidth_gb=analysis_result['predicted_bandwidth'],
            peak_hours=analysis_result['peak_hours'],
            congestion_risk_score=analysis_result['congestion_risk'][0] if analysis_result['congestion_risk'] else 0,
            optimization_recommendations=analysis_result['optimization_recommendations'],
            confidence_score=0.85,
            data_points_analyzed=len(network_data)
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing traffic patterns: {str(e)}"
        )

@router.post("/optimize/qos", response_model=QoSOptimizationResponse)
async def optimize_qos(
    tenant_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate QoS optimization recommendations for all subscribers
    """
    try:
        # Get subscriber data
        query = db.query(User).join(Branch)
        
        if current_user['user_type'] == 'isp':
            query = query.join(ISP).filter(ISP.id == tenant_id)
        elif current_user['user_type'] == 'founder':
            query = query.join(ISP).filter(ISP.id == tenant_id)
        
        users = query.all()
        
        # Prepare data for AI analysis
        subscriber_data = []
        for user in users:
            # Get recent usage history
            usage_history = db.query(BandwidthUsage).filter(
                BandwidthUsage.user_id == user.id,
                BandwidthUsage.date >= datetime.now().date() - timedelta(days=30)
            ).all()
            
            usage_values = [usage.total_bytes / (1024**3) for usage in usage_history]  # Convert to GB
            
            subscriber_data.append({
                'id': str(user.id),
                'username': user.username,
                'bandwidth_limit': user.bandwidth_limit,
                'usage_history': usage_values,
                'subscription_plan': user.subscription_plan
            })
        
        # Generate QoS recommendations
        qos_recommendations = await ai_optimizer.dynamic_qos_optimization(subscriber_data)
        
        # Format response
        user_recommendations = []
        for user_id, qos_rules in qos_recommendations.items():
            user = next((u for u in users if str(u.id) == user_id), None)
            if user:
                user_recommendations.append(OptimizationRecommendation(
                    user_id=user_id,
                    username=user.username,
                    current_plan=user.subscription_plan,
                    priority_level=qos_rules['priority_level'],
                    recommended_bandwidth=qos_rules['rate_limiting']['download'] // 1024,  # Convert back to Mbps
                    traffic_shaping_rules=qos_rules['traffic_shaping'],
                    recommendations=qos_rules['recommendations']
                ))
        
        return QoSOptimizationResponse(
            optimization_id=f"qos_{tenant_id}_{int(datetime.now().timestamp())}",
            total_users_analyzed=len(users),
            high_priority_users=len([r for r in user_recommendations if r.priority_level == 'high']),
            optimization_score=87.5,  # This would be calculated based on actual metrics
            user_recommendations=user_recommendations,
            global_recommendations=[
                "Implement content delivery network (CDN) for popular streaming services",
                "Configure gaming traffic prioritization during peak hours",
                "Enable fair usage policies for heavy users",
                "Consider bandwidth pooling for enterprise customers"
            ]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error optimizing QoS: {str(e)}"
        )

@router.get("/predict/network/{tenant_id}", response_model=NetworkPredictionResponse)
async def predict_network_requirements(
    tenant_id: str,
    days_ahead: int = 30,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Predict future network requirements using AI
    """
    try:
        # Get historical data
        start_date = datetime.now() - timedelta(days=90)
        
        usage_data = db.query(BandwidthUsage).join(User).join(Branch).join(ISP).filter(
            ISP.id == tenant_id,
            BandwidthUsage.date >= start_date.date()
        ).all()
        
        if not usage_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No usage data found for prediction"
            )
        
        # Simple trend analysis (in production, use advanced time series models)
        daily_totals = {}
        for usage in usage_data:
            date_key = usage.date.isoformat()
            if date_key not in daily_totals:
                daily_totals[date_key] = 0
            daily_totals[date_key] += usage.total_bytes
        
        # Calculate growth trend
        dates = sorted(daily_totals.keys())
        values = [daily_totals[date] for date in dates]
        
        if len(values) >= 7:
            # Simple linear trend
            recent_avg = sum(values[-7:]) / 7
            older_avg = sum(values[:7]) / 7
            growth_rate = (recent_avg - older_avg) / older_avg if older_avg > 0 else 0
        else:
            growth_rate = 0.1  # Default 10% growth
        
        # Predict future values
        current_usage = values[-1] if values else 0
        predictions = []
        for day in range(1, days_ahead + 1):
            predicted_usage = current_usage * (1 + growth_rate * day / 30)
            predictions.append(predicted_usage)
        
        # Capacity recommendations
        peak_predicted = max(predictions)
        current_capacity = current_usage * 1.5  # Assume 50% headroom
        
        capacity_recommendations = []
        if peak_predicted > current_capacity * 0.8:
            capacity_recommendations.append("Upgrade network capacity within 30 days")
            capacity_recommendations.append(f"Recommended capacity: {peak_predicted / (1024**3):.1f} GB/day")
        
        return NetworkPredictionResponse(
            prediction_id=f"pred_{tenant_id}_{int(datetime.now().timestamp())}",
            days_ahead=days_ahead,
            predicted_peak_usage_gb=peak_predicted / (1024**3),
            predicted_average_usage_gb=sum(predictions) / len(predictions) / (1024**3),
            growth_rate_percent=growth_rate * 100,
            confidence_score=0.75,
            capacity_recommendations=capacity_recommendations,
            risk_factors=[
                "Seasonal traffic variations not accounted for",
                "New subscriber growth may exceed predictions",
                "Streaming service popularity changes"
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error predicting network requirements: {str(e)}"
        )

@router.get("/detect/anomalies/{tenant_id}", response_model=AnomalyDetectionResponse)
async def detect_network_anomalies(
    tenant_id: str,
    hours_back: int = 24,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Detect network anomalies using AI
    """
    try:
        # Get recent usage data
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        usage_data = db.query(BandwidthUsage).join(User).join(Branch).join(ISP).filter(
            ISP.id == tenant_id,
            BandwidthUsage.created_at >= cutoff_time
        ).all()
        
        anomalies = []
        
        if usage_data:
            # Calculate baseline statistics
            total_bytes = [usage.total_bytes for usage in usage_data]
            peak_usage = [usage.peak_usage_mbps for usage in usage_data]
            
            avg_bytes = np.mean(total_bytes)
            std_bytes = np.std(total_bytes)
            avg_peak = np.mean(peak_usage)
            std_peak = np.std(peak_usage)
            
            # Detect anomalies (simple statistical approach)
            for usage in usage_data:
                z_score_bytes = abs(usage.total_bytes - avg_bytes) / std_bytes if std_bytes > 0 else 0
                z_score_peak = abs(usage.peak_usage_mbps - avg_peak) / std_peak if std_peak > 0 else 0
                
                if z_score_bytes > 2.5:  # More than 2.5 standard deviations
                    anomalies.append({
                        "type": "unusual_data_usage",
                        "severity": "high" if z_score_bytes > 3 else "medium",
                        "description": f"Unusual data usage: {usage.total_bytes / (1024**3):.2f} GB",
                        "timestamp": usage.created_at.isoformat(),
                        "user_id": str(usage.user_id),
                        "z_score": round(z_score_bytes, 2)
                    })
                
                if z_score_peak > 2.5:
                    anomalies.append({
                        "type": "bandwidth_spike",
                        "severity": "high" if z_score_peak > 3 else "medium",
                        "description": f"Bandwidth spike: {usage.peak_usage_mbps} Mbps",
                        "timestamp": usage.created_at.isoformat(),
                        "user_id": str(usage.user_id),
                        "z_score": round(z_score_peak, 2)
                    })
        
        # Add some common anomaly patterns
        if not anomalies:
            anomalies.append({
                "type": "info",
                "severity": "low",
                "description": "No significant anomalies detected in the specified time period",
                "timestamp": datetime.now().isoformat(),
                "user_id": None,
                "z_score": 0
            })
        
        return AnomalyDetectionResponse(
            detection_id=f"anom_{tenant_id}_{int(datetime.now().timestamp())}",
            time_period_hours=hours_back,
            anomalies_detected=len([a for a in anomalies if a['type'] != 'info']),
            high_severity_count=len([a for a in anomalies if a['severity'] == 'high']),
            anomalies=anomalies,
            baseline_metrics={
                "avg_daily_usage_gb": avg_bytes / (1024**3) if usage_data else 0,
                "avg_peak_usage_mbps": avg_peak if usage_data else 0,
                "data_points_analyzed": len(usage_data)
            },
            recommendations=[
                "Monitor high-usage users for potential policy violations",
                "Investigate bandwidth spikes for security threats",
                "Consider implementing automated alerting for anomalies"
            ]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error detecting anomalies: {str(e)}"
        )