from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Dict, Any
from datetime import datetime, timedelta
import numpy as np

from shared.database.connection import get_db
from shared.models.models import (
    NetworkAlert, SLADefinition, AuditLog, BandwidthUsage, 
    NetworkDevice, User, Branch, ISP
)
from auth.dependencies import get_current_user, get_current_isp
from .schemas import (
    NOCDashboardResponse, NetworkAlertCreate, NetworkAlertResponse,
    SLADefinitionCreate, SLADefinitionResponse, SLAComplianceReport,
    AuditAnomalyResponse, AIAuditAnalysisResponse
)

router = APIRouter()

@router.get("/{tenant_id}/dashboard", response_model=NOCDashboardResponse)
async def get_noc_dashboard(
    tenant_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    NOC Dashboard with centralized network monitoring
    - Real-time network topology map
    - Alert correlation and incident management
    - SLA compliance monitoring
    """
    try:
        # Get total alerts in last 24 hours
        yesterday = datetime.now() - timedelta(days=1)
        total_alerts = db.query(NetworkAlert).filter(
            NetworkAlert.tenant_id == tenant_id,
            NetworkAlert.created_at >= yesterday
        ).count()
        
        # Get critical alerts
        critical_alerts = db.query(NetworkAlert).filter(
            NetworkAlert.tenant_id == tenant_id,
            NetworkAlert.severity == 'critical',
            NetworkAlert.status == 'open'
        ).count()
        
        # Get recent alerts
        recent_alerts = db.query(NetworkAlert).filter(
            NetworkAlert.tenant_id == tenant_id
        ).order_by(desc(NetworkAlert.created_at)).limit(10).all()
        
        # Calculate network health score (simplified)
        network_health = max(0, 100 - (critical_alerts * 10) - (total_alerts * 2))
        
        # Get active devices count
        active_devices = db.query(NetworkDevice).filter(
            NetworkDevice.tenant_id == tenant_id,
            NetworkDevice.status == 'online'
        ).count()
        
        # Calculate bandwidth utilization (last hour average)
        hour_ago = datetime.now() - timedelta(hours=1)
        bandwidth_usage = db.query(BandwidthUsage).join(User).join(Branch).filter(
            Branch.isp_id == tenant_id,
            BandwidthUsage.created_at >= hour_ago
        ).all()
        
        total_usage = sum([usage.total_bytes for usage in bandwidth_usage])
        bandwidth_utilization = min(100, (total_usage / (1024**3)) * 100)  # GB to percentage
        
        # Calculate uptime percentage (simplified)
        uptime_percentage = max(95.0, 100.0 - (critical_alerts * 0.5))
        
        return NOCDashboardResponse(
            total_alerts=total_alerts,
            critical_alerts=critical_alerts,
            network_health=network_health,
            uptime_percentage=uptime_percentage,
            active_devices=active_devices,
            bandwidth_utilization=bandwidth_utilization,
            recent_alerts=[
                NetworkAlertResponse(
                    id=str(alert.id),
                    tenant_id=str(alert.tenant_id),
                    tenant_type=alert.tenant_type,
                    alert_type=alert.alert_type,
                    severity=alert.severity,
                    title=alert.title,
                    description=alert.description,
                    source=alert.source,
                    status=alert.status,
                    escalated=alert.escalated,
                    auto_resolved=alert.auto_resolved,
                    metadata=alert.metadata,
                    created_at=alert.created_at,
                    resolved_at=alert.resolved_at
                ) for alert in recent_alerts
            ],
            network_topology={
                "nodes": active_devices,
                "connections": active_devices * 2,  # Simplified
                "regions": 3
            },
            performance_metrics={
                "latency_ms": 25.5,
                "packet_loss": 0.02,
                "jitter_ms": 1.2,
                "throughput_mbps": 850.0
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching NOC dashboard: {str(e)}"
        )

@router.post("/{tenant_id}/alerts", response_model=NetworkAlertResponse)
async def create_network_alert(
    tenant_id: str,
    alert_data: NetworkAlertCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new network alert with automated escalation"""
    try:
        alert = NetworkAlert(
            tenant_id=tenant_id,
            tenant_type="isp",  # Could be dynamic based on context
            alert_type=alert_data.alert_type,
            severity=alert_data.severity,
            title=alert_data.title,
            description=alert_data.description,
            source=alert_data.source,
            metadata=alert_data.metadata
        )
        
        # Auto-escalate critical alerts
        if alert_data.severity == 'critical':
            alert.escalated = True
        
        db.add(alert)
        db.commit()
        db.refresh(alert)
        
        return NetworkAlertResponse(
            id=str(alert.id),
            tenant_id=str(alert.tenant_id),
            tenant_type=alert.tenant_type,
            alert_type=alert.alert_type,
            severity=alert.severity,
            title=alert.title,
            description=alert.description,
            source=alert.source,
            status=alert.status,
            escalated=alert.escalated,
            auto_resolved=alert.auto_resolved,
            metadata=alert.metadata,
            created_at=alert.created_at,
            resolved_at=alert.resolved_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating network alert: {str(e)}"
        )

@router.get("/{tenant_id}/ai-audit", response_model=AIAuditAnalysisResponse)
async def get_ai_audit_analysis(
    tenant_id: str,
    hours_back: int = 24,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI-based audit analysis with anomaly detection
    - Intelligent pattern recognition
    - Risk scoring and classification
    - Automated threat detection
    """
    try:
        # Get audit logs for analysis
        time_threshold = datetime.now() - timedelta(hours=hours_back)
        audit_logs = db.query(AuditLog).filter(
            AuditLog.tenant_id == tenant_id,
            AuditLog.created_at >= time_threshold
        ).all()
        
        total_logs = len(audit_logs)
        anomalies = []
        suspicious_patterns = []
        
        if total_logs > 0:
            # AI-based anomaly detection (simplified implementation)
            # In production, this would use more sophisticated ML models
            
            # Detect unusual activity patterns
            action_counts = {}
            user_activity = {}
            
            for log in audit_logs:
                # Count actions
                action_counts[log.action] = action_counts.get(log.action, 0) + 1
                
                # Count user activity
                if log.user_id:
                    user_id = str(log.user_id)
                    user_activity[user_id] = user_activity.get(user_id, 0) + 1
            
            # Calculate thresholds for anomaly detection
            if action_counts:
                action_values = list(action_counts.values())
                action_mean = np.mean(action_values)
                action_std = np.std(action_values)
                
                # Detect unusual actions (more than 2 standard deviations)
                for action, count in action_counts.items():
                    if action_std > 0 and abs(count - action_mean) > 2 * action_std:
                        suspicious_patterns.append({
                            "type": "unusual_action_frequency",
                            "action": action,
                            "count": count,
                            "expected_range": f"{action_mean:.1f} ± {action_std:.1f}",
                            "severity": "medium"
                        })
            
            # Detect hyperactive users
            if user_activity:
                activity_values = list(user_activity.values())
                activity_mean = np.mean(activity_values)
                activity_std = np.std(activity_values)
                
                for user_id, count in user_activity.items():
                    if activity_std > 0 and count > activity_mean + 2 * activity_std:
                        suspicious_patterns.append({
                            "type": "hyperactive_user",
                            "user_id": user_id,
                            "activity_count": count,
                            "threshold": f"{activity_mean + 2 * activity_std:.1f}",
                            "severity": "high"
                        })
            
            # Calculate AI risk scores for recent logs
            for log in audit_logs[-50:]:  # Analyze last 50 logs
                risk_score = calculate_risk_score(log, action_counts, user_activity)
                
                if risk_score > 0.7:  # High risk threshold
                    anomalies.append({
                        "log_id": str(log.id),
                        "action": log.action,
                        "risk_score": risk_score,
                        "user_id": str(log.user_id) if log.user_id else None,
                        "created_at": log.created_at.isoformat(),
                        "reason": "High risk activity detected"
                    })
        
        # Generate recommendations
        recommendations = []
        if len(suspicious_patterns) > 0:
            recommendations.append("Review user access patterns for potential security threats")
        if len(anomalies) > 5:
            recommendations.append("Implement additional monitoring for high-risk activities")
        recommendations.append("Regular audit log analysis helps maintain security posture")
        
        # Risk distribution
        risk_distribution = {
            "low": max(0, total_logs - len(anomalies) - len(suspicious_patterns)),
            "medium": len(suspicious_patterns),
            "high": len(anomalies)
        }
        
        return AIAuditAnalysisResponse(
            total_logs=total_logs,
            anomalies_detected=len(anomalies),
            high_risk_activities=len([a for a in anomalies if a.get("risk_score", 0) > 0.8]),
            suspicious_patterns=suspicious_patterns,
            recommendations=recommendations,
            risk_distribution=risk_distribution
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing AI audit analysis: {str(e)}"
        )

def calculate_risk_score(log: AuditLog, action_counts: Dict, user_activity: Dict) -> float:
    """Calculate AI-based risk score for audit log entry"""
    base_score = 0.1
    
    # High-risk actions
    high_risk_actions = ['delete', 'modify_critical', 'admin_access', 'password_change']
    if log.action in high_risk_actions:
        base_score += 0.4
    
    # Unusual time patterns (simplified - would use more sophisticated time analysis)
    hour = log.created_at.hour
    if hour < 6 or hour > 22:  # Outside business hours
        base_score += 0.2
    
    # Frequency-based risk
    if log.user_id and str(log.user_id) in user_activity:
        user_count = user_activity[str(log.user_id)]
        if user_count > 50:  # High activity user
            base_score += 0.3
    
    # IP-based risk (simplified)
    if log.ip_address and str(log.ip_address).startswith('10.'):  # Internal IP
        base_score -= 0.1  # Lower risk for internal IPs
    else:
        base_score += 0.2  # Higher risk for external IPs
    
    return min(1.0, base_score)

@router.get("/{isp_id}/sla", response_model=List[SLADefinitionResponse])
async def get_sla_definitions(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """Get SLA definitions for ISP"""
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        slas = db.query(SLADefinition).filter(
            SLADefinition.isp_id == current_isp.id,
            SLADefinition.is_active == True
        ).all()
        
        return [
            SLADefinitionResponse(
                id=str(sla.id),
                isp_id=str(sla.isp_id),
                name=sla.name,
                description=sla.description,
                uptime_target=float(sla.uptime_target),
                response_time_target=sla.response_time_target,
                resolution_time_target=sla.resolution_time_target,
                bandwidth_guarantee=sla.bandwidth_guarantee,
                penalties=sla.penalties,
                is_active=sla.is_active,
                created_at=sla.created_at
            ) for sla in slas
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching SLA definitions: {str(e)}"
        )

@router.post("/{isp_id}/sla", response_model=SLADefinitionResponse)
async def create_sla_definition(
    isp_id: str,
    sla_data: SLADefinitionCreate,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """Create new SLA definition"""
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        sla = SLADefinition(
            isp_id=current_isp.id,
            name=sla_data.name,
            description=sla_data.description,
            uptime_target=sla_data.uptime_target,
            response_time_target=sla_data.response_time_target,
            resolution_time_target=sla_data.resolution_time_target,
            bandwidth_guarantee=sla_data.bandwidth_guarantee,
            penalties=sla_data.penalties
        )
        
        db.add(sla)
        db.commit()
        db.refresh(sla)
        
        return SLADefinitionResponse(
            id=str(sla.id),
            isp_id=str(sla.isp_id),
            name=sla.name,
            description=sla.description,
            uptime_target=float(sla.uptime_target),
            response_time_target=sla.response_time_target,
            resolution_time_target=sla.resolution_time_target,
            bandwidth_guarantee=sla.bandwidth_guarantee,
            penalties=sla.penalties,
            is_active=sla.is_active,
            created_at=sla.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating SLA definition: {str(e)}"
        )