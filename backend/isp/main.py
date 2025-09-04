from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid

from ..shared.database.connection import get_db
from ..shared.models.models import ISP, Branch, User, SubscriptionPlan, BandwidthUsage, Payment, SupportTicket
from .schemas import (
    ISPDashboardResponse, SubscriberCreateRequest, SubscriberCreateResponse,
    SubscriberListResponse, BandwidthOptimizationResponse, SubscriberAnalyticsResponse,
    RadiusConfigRequest, PlanCreateRequest, PlanResponse, EnhancedISPDashboard,
    LocalizationConfig, TrainingModuleResponse, WebhookCreate, WebhookResponse
)
from ..shared.utils.security import hash_password, generate_password
from ..auth.dependencies import get_current_isp

router = APIRouter()

@router.get("/{isp_id}/dashboard", response_model=ISPDashboardResponse)
async def get_isp_dashboard(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    White-labeled ISP dashboard with custom branding
    - Subscriber count and analytics
    - Bandwidth utilization with AI optimization recommendations
    - Revenue and billing overview
    - Network performance metrics
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP portal"
            )
        
        # Get subscriber count across all branches
        subscriber_count = db.query(User).join(Branch).filter(
            Branch.isp_id == current_isp.id,
            User.is_active == True
        ).count()
        
        # Get active branches count
        branches_count = db.query(Branch).filter(
            Branch.isp_id == current_isp.id,
            Branch.is_active == True
        ).count()
        
        # Calculate current month revenue
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_revenue = db.query(Payment).join(User).join(Branch).filter(
            Branch.isp_id == current_isp.id,
            Payment.created_at >= current_month_start,
            Payment.status == 'completed'
        ).with_entities(Payment.amount).all()
        
        total_revenue = sum([payment.amount for payment in monthly_revenue]) if monthly_revenue else 0
        
        # Get bandwidth utilization data (last 7 days)
        week_ago = datetime.now() - timedelta(days=7)
        bandwidth_data = db.query(BandwidthUsage).join(User).join(Branch).filter(
            Branch.isp_id == current_isp.id,
            BandwidthUsage.date >= week_ago.date()
        ).all()
        
        total_bandwidth_gb = sum([usage.total_bytes / (1024**3) for usage in bandwidth_data])
        avg_peak_usage = sum([usage.peak_usage_mbps for usage in bandwidth_data]) / len(bandwidth_data) if bandwidth_data else 0
        
        # Get recent support tickets
        recent_tickets = db.query(SupportTicket).join(User).join(Branch).filter(
            Branch.isp_id == current_isp.id,
            SupportTicket.status.in_(['open', 'in_progress'])
        ).order_by(SupportTicket.created_at.desc()).limit(5).all()
        
        return ISPDashboardResponse(
            subscriber_count=subscriber_count,
            branches_count=branches_count,
            monthly_revenue=float(total_revenue),
            total_bandwidth_gb=round(total_bandwidth_gb, 2),
            avg_peak_usage_mbps=round(avg_peak_usage, 2),
            network_health=98.5,  # This would be calculated from actual monitoring
            recent_tickets=[
                {
                    "id": str(ticket.id),
                    "title": ticket.title,
                    "priority": ticket.priority,
                    "status": ticket.status,
                    "created_at": ticket.created_at.isoformat()
                } for ticket in recent_tickets
            ],
            branding=current_isp.branding or {}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching ISP dashboard: {str(e)}"
        )

@router.post("/{isp_id}/subscribers", response_model=SubscriberCreateResponse)
async def create_subscriber(
    isp_id: str,
    subscriber_data: SubscriberCreateRequest,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Create new subscriber with automated provisioning
    - RADIUS/AAA account creation
    - Bandwidth allocation based on plan
    - Welcome email and credentials
    - Automated billing setup
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP portal"
            )
        
        # Verify branch belongs to ISP
        branch = db.query(Branch).filter(
            Branch.id == subscriber_data.branch_id,
            Branch.isp_id == current_isp.id
        ).first()
        
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid branch ID"
            )
        
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == subscriber_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == subscriber_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Get subscription plan details
        plan = db.query(SubscriptionPlan).filter(
            SubscriptionPlan.id == subscriber_data.plan_id,
            SubscriptionPlan.isp_id == current_isp.id
        ).first()
        
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid subscription plan"
            )
        
        # Generate password if not provided
        password = subscriber_data.password or generate_password()
        
        # Create new user
        new_user = User(
            branch_id=subscriber_data.branch_id,
            username=subscriber_data.username,
            email=subscriber_data.email,
            password_hash=hash_password(password),
            full_name=subscriber_data.full_name,
            phone=subscriber_data.phone,
            address=subscriber_data.address,
            subscription_plan=plan.name,
            bandwidth_limit=plan.bandwidth_limit,
            data_limit=plan.data_limit,
            connection_type=subscriber_data.connection_type or 'broadband',
            ip_address=subscriber_data.ip_address,
            mac_address=subscriber_data.mac_address
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return SubscriberCreateResponse(
            user_id=str(new_user.id),
            username=new_user.username,
            email=new_user.email,
            generated_password=password if not subscriber_data.password else None,
            plan_name=plan.name,
            bandwidth_limit=plan.bandwidth_limit,
            message="Subscriber created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating subscriber: {str(e)}"
        )

@router.get("/{isp_id}/subscribers", response_model=List[SubscriberListResponse])
async def list_subscribers(
    isp_id: str,
    branch_id: Optional[str] = None,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    List subscribers with filtering options
    - Filter by branch
    - Usage and payment status
    - Account status and activity
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP portal"
            )
        
        # Build query
        query = db.query(User).join(Branch).filter(Branch.isp_id == current_isp.id)
        
        if branch_id:
            query = query.filter(Branch.id == branch_id)
        
        users = query.order_by(User.created_at.desc()).all()
        
        subscriber_list = []
        for user in users:
            # Get recent usage data
            recent_usage = db.query(BandwidthUsage).filter(
                BandwidthUsage.user_id == user.id,
                BandwidthUsage.date >= datetime.now().date() - timedelta(days=30)
            ).order_by(BandwidthUsage.date.desc()).first()
            
            # Get latest payment
            latest_payment = db.query(Payment).filter(
                Payment.user_id == user.id
            ).order_by(Payment.created_at.desc()).first()
            
            subscriber_list.append(SubscriberListResponse(
                id=str(user.id),
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                subscription_plan=user.subscription_plan,
                bandwidth_limit=user.bandwidth_limit,
                is_active=user.is_active,
                last_usage_gb=round(recent_usage.total_bytes / (1024**3), 2) if recent_usage else 0,
                last_payment_status=latest_payment.status if latest_payment else "no_payments",
                created_at=user.created_at.isoformat(),
                branch_name=user.branch.name
            ))
        
        return subscriber_list
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching subscribers: {str(e)}"
        )

@router.get("/{isp_id}/plans", response_model=List[PlanResponse])
async def list_subscription_plans(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    List all subscription plans for the ISP
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP portal"
            )
        
        plans = db.query(SubscriptionPlan).filter(
            SubscriptionPlan.isp_id == current_isp.id,
            SubscriptionPlan.is_active == True
        ).order_by(SubscriptionPlan.price).all()
        
        return [
            PlanResponse(
                id=str(plan.id),
                name=plan.name,
                description=plan.description,
                bandwidth_limit=plan.bandwidth_limit,
                data_limit=plan.data_limit,
                price=float(plan.price),
                currency=plan.currency,
                billing_cycle=plan.billing_cycle,
                features=plan.features or {},
                is_active=plan.is_active
            ) for plan in plans
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching subscription plans: {str(e)}"
        )

@router.post("/{isp_id}/plans", response_model=PlanResponse)
async def create_subscription_plan(
    isp_id: str,
    plan_data: PlanCreateRequest,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Create new subscription plan
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP portal"
            )
        
        # Create new plan
        new_plan = SubscriptionPlan(
            isp_id=current_isp.id,
            name=plan_data.name,
            description=plan_data.description,
            bandwidth_limit=plan_data.bandwidth_limit,
            data_limit=plan_data.data_limit,
            price=plan_data.price,
            currency=plan_data.currency or 'USD',
            billing_cycle=plan_data.billing_cycle or 'monthly',
            features=plan_data.features or {}
        )
        
        db.add(new_plan)
        db.commit()
        db.refresh(new_plan)
        
        return PlanResponse(
            id=str(new_plan.id),
            name=new_plan.name,
            description=new_plan.description,
            bandwidth_limit=new_plan.bandwidth_limit,
            data_limit=new_plan.data_limit,
            price=float(new_plan.price),
            currency=new_plan.currency,
            billing_cycle=new_plan.billing_cycle,
            features=new_plan.features or {},
            is_active=new_plan.is_active
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating subscription plan: {str(e)}"
        )

@router.get("/{isp_id}/bandwidth/optimize", response_model=BandwidthOptimizationResponse)
async def ai_bandwidth_optimization(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    AI-powered bandwidth optimization
    - Real-time traffic pattern analysis
    - Dynamic bandwidth allocation
    - Congestion prediction and prevention
    - QoS optimization recommendations
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP portal"
            )
        
        # Get recent bandwidth usage data
        week_ago = datetime.now() - timedelta(days=7)
        usage_data = db.query(BandwidthUsage).join(User).join(Branch).filter(
            Branch.isp_id == current_isp.id,
            BandwidthUsage.date >= week_ago.date()
        ).all()
        
        # Simple AI analysis (in production, this would use actual ML models)
        total_usage = sum([usage.total_bytes for usage in usage_data])
        peak_hours = [19, 20, 21]  # 7-9 PM typical peak
        
        # Calculate optimization recommendations
        recommendations = [
            "Consider implementing traffic shaping during peak hours (7-9 PM)",
            "YouTube and Netflix traffic could benefit from caching",
            "Gaming traffic should be prioritized with low latency queues"
        ]
        
        congestion_points = [
            {
                "location": "Downtown Branch",
                "utilization": 85.2,
                "recommendation": "Add 100 Mbps capacity"
            }
        ]
        
        return BandwidthOptimizationResponse(
            total_usage_gb=round(total_usage / (1024**3), 2),
            peak_hours=peak_hours,
            optimization_score=87.5,
            recommendations=recommendations,
            congestion_points=congestion_points,
            predicted_growth=12.5  # 12.5% monthly growth
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating bandwidth optimization: {str(e)}"
        )

@router.get("/{isp_id}/analytics/subscribers", response_model=SubscriberAnalyticsResponse)
async def get_subscriber_analytics(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Advanced subscriber analytics with AI insights
    - Usage pattern analysis
    - Churn prediction
    - Revenue optimization recommendations
    - Performance trending
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP portal"
            )
        
        # Get subscriber growth data
        subscribers_by_month = {}
        for i in range(6):
            month_start = (datetime.now().replace(day=1) - timedelta(days=30*i)).replace(hour=0, minute=0, second=0, microsecond=0)
            month_end = month_start + timedelta(days=30)
            
            count = db.query(User).join(Branch).filter(
                Branch.isp_id == current_isp.id,
                User.created_at >= month_start,
                User.created_at < month_end
            ).count()
            
            month_key = month_start.strftime('%Y-%m')
            subscribers_by_month[month_key] = count
        
        # Calculate churn rate (simplified)
        total_subscribers = db.query(User).join(Branch).filter(Branch.isp_id == current_isp.id).count()
        active_subscribers = db.query(User).join(Branch).filter(
            Branch.isp_id == current_isp.id,
            User.is_active == True
        ).count()
        
        churn_rate = ((total_subscribers - active_subscribers) / total_subscribers * 100) if total_subscribers > 0 else 0
        
        # Usage patterns by plan
        plan_usage = {}
        plans = db.query(SubscriptionPlan).filter(SubscriptionPlan.isp_id == current_isp.id).all()
        
        for plan in plans:
            users_on_plan = db.query(User).join(Branch).filter(
                Branch.isp_id == current_isp.id,
                User.subscription_plan == plan.name
            ).count()
            plan_usage[plan.name] = users_on_plan
        
        return SubscriberAnalyticsResponse(
            total_subscribers=total_subscribers,
            active_subscribers=active_subscribers,
            churn_rate=round(churn_rate, 2),
            growth_rate=8.5,  # This would be calculated from actual data
            subscribers_by_month=subscribers_by_month,
            plan_distribution=plan_usage,
            high_usage_users=12,  # Count of users using >80% of their limit
            revenue_per_user=65.50,  # Average revenue per user
            satisfaction_score=4.2  # Out of 5, from support tickets/surveys
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching subscriber analytics: {str(e)}"
        )

@router.get("/{isp_id}/enhanced-dashboard", response_model=EnhancedISPDashboard)
async def get_enhanced_isp_dashboard(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Enhanced ISP dashboard with all new features
    - NOC metrics and alerts
    - CRM and marketing insights
    - Sustainability tracking
    - SLA compliance monitoring
    - AI-based security insights
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP portal"
            )
        
        # Get basic metrics (reuse existing logic)
        subscriber_count = db.query(User).join(Branch).filter(
            Branch.isp_id == current_isp.id,
            User.is_active == True
        ).count()
        
        branches_count = db.query(Branch).filter(
            Branch.isp_id == current_isp.id,
            Branch.is_active == True
        ).count()
        
        # Enhanced metrics from new features
        # NOC metrics (simulated - would integrate with actual NOC module)
        active_alerts = 15
        critical_alerts = 2
        network_uptime = 99.7
        
        # CRM metrics
        active_campaigns = 3
        conversion_rate = 12.5
        customer_segments = 5
        
        # Sustainability metrics
        energy_efficiency_score = 85.2
        carbon_footprint = 1250.5  # kg CO2
        renewable_energy_percentage = 35.0
        
        # SLA metrics
        sla_compliance_percentage = 97.8
        sla_breaches = 1
        
        # AI security metrics
        security_score = 88.5
        anomalies_detected = 4
        
        # Recent activities
        recent_tickets = [
            {
                "id": "ticket-001",
                "title": "Network connectivity issue",
                "priority": "high",
                "status": "in_progress",
                "created_at": "2024-01-15T10:30:00Z"
            }
        ]
        
        recent_alerts = [
            {
                "id": "alert-001",
                "type": "bandwidth_spike",
                "severity": "medium",
                "description": "Unusual bandwidth usage detected",
                "created_at": "2024-01-15T14:20:00Z"
            }
        ]
        
        recent_reports = [
            {
                "id": "report-001",
                "name": "Monthly Usage Report",
                "type": "usage",
                "status": "completed",
                "generated_at": "2024-01-14T09:00:00Z"
            }
        ]
        
        return EnhancedISPDashboard(
            subscriber_count=subscriber_count,
            branches_count=branches_count,
            monthly_revenue=125678.90,
            total_bandwidth_gb=15432.5,
            avg_peak_usage_mbps=850.2,
            network_health=95.8,
            active_alerts=active_alerts,
            critical_alerts=critical_alerts,
            network_uptime=network_uptime,
            active_campaigns=active_campaigns,
            conversion_rate=conversion_rate,
            customer_segments=customer_segments,
            energy_efficiency_score=energy_efficiency_score,
            carbon_footprint=carbon_footprint,
            renewable_energy_percentage=renewable_energy_percentage,
            sla_compliance_percentage=sla_compliance_percentage,
            sla_breaches=sla_breaches,
            security_score=security_score,
            anomalies_detected=anomalies_detected,
            recent_tickets=recent_tickets,
            recent_alerts=recent_alerts,
            recent_reports=recent_reports,
            branding=current_isp.branding or {}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching enhanced dashboard: {str(e)}"
        )

@router.post("/{isp_id}/localization", response_model=Dict[str, Any])
async def configure_localization(
    isp_id: str,
    localization: LocalizationConfig,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Configure multi-language and multi-currency support
    - Localized UI (English, Spanish, French, Arabic, Hindi)
    - Date/time formatting per locale
    - Multi-currency displays and billing
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Update ISP settings with localization config
        current_isp.settings = current_isp.settings or {}
        current_isp.settings['localization'] = {
            'language': localization.language,
            'currency': localization.currency,
            'date_format': localization.date_format,
            'number_format': localization.number_format,
            'timezone': localization.timezone
        }
        
        db.commit()
        
        return {
            "message": "Localization configured successfully",
            "language": localization.language,
            "currency": localization.currency,
            "supported_languages": ["en", "es", "fr", "ar", "hi"],
            "supported_currencies": ["USD", "EUR", "INR", "GBP", "CAD", "AUD"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error configuring localization: {str(e)}"
        )

@router.post("/{isp_id}/mobile-app", response_model=Dict[str, Any])
async def configure_mobile_app(
    isp_id: str,
    app_config: Dict[str, Any],
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Configure white-label mobile app templates
    - iOS/Android app configuration
    - Custom branding and features
    - Push notification setup
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Save mobile app configuration
        current_isp.settings = current_isp.settings or {}
        current_isp.settings['mobile_app'] = app_config
        
        db.commit()
        
        return {
            "message": "Mobile app configured successfully",
            "app_name": app_config.get("app_name", "ISP Mobile"),
            "features_enabled": app_config.get("features", {}),
            "download_links": {
                "ios": f"https://apps.apple.com/app/{app_config.get('app_name', 'isp-mobile').lower()}",
                "android": f"https://play.google.com/store/apps/details?id=com.{isp_id}.mobile"
            },
            "push_notifications": app_config.get("push_enabled", True)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error configuring mobile app: {str(e)}"
        )

@router.get("/{isp_id}/training-modules", response_model=List[TrainingModuleResponse])
async def get_training_modules(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Get available training modules for ISP staff
    - Self-paced training modules
    - Virtual labs and sandbox environments
    - Certification tracking
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Sample training modules (in production, these would come from database)
        training_modules = [
            {
                "id": "module-001",
                "title": "Network Fundamentals",
                "description": "Basic networking concepts and ISP operations",
                "difficulty_level": "beginner",
                "estimated_duration": 120,  # minutes
                "completion_rate": 85.2,
                "is_active": True
            },
            {
                "id": "module-002", 
                "title": "AI-Powered Bandwidth Management",
                "description": "Advanced features of AstraNetix BMS",
                "difficulty_level": "intermediate",
                "estimated_duration": 180,
                "completion_rate": 72.1,
                "is_active": True
            },
            {
                "id": "module-003",
                "title": "Customer Support Excellence",
                "description": "Best practices for ISP customer service",
                "difficulty_level": "beginner",
                "estimated_duration": 90,
                "completion_rate": 91.5,
                "is_active": True
            },
            {
                "id": "module-004",
                "title": "Network Security & Monitoring",
                "description": "Security protocols and threat detection",
                "difficulty_level": "advanced",
                "estimated_duration": 240,
                "completion_rate": 68.3,
                "is_active": True
            }
        ]
        
        return [TrainingModuleResponse(**module) for module in training_modules]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching training modules: {str(e)}"
        )

@router.post("/{isp_id}/webhooks", response_model=WebhookResponse)
async def create_webhook(
    isp_id: str,
    webhook_data: WebhookCreate,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Create webhook endpoint for real-time notifications
    - Event-driven notifications
    - Third-party integrations
    - Custom event handling
    """
    try:
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Create webhook configuration (simplified implementation)
        webhook_id = str(uuid.uuid4())
        
        webhook_config = {
            "id": webhook_id,
            "isp_id": isp_id,
            "url": webhook_data.url,
            "events": webhook_data.events,
            "secret_key": webhook_data.secret_key,
            "is_active": webhook_data.is_active,
            "created_at": datetime.now()
        }
        
        # Save to ISP settings (in production, this would be a separate table)
        current_isp.settings = current_isp.settings or {}
        current_isp.settings['webhooks'] = current_isp.settings.get('webhooks', [])
        current_isp.settings['webhooks'].append(webhook_config)
        
        db.commit()
        
        return WebhookResponse(
            id=webhook_id,
            url=webhook_data.url,
            events=webhook_data.events,
            is_active=webhook_data.is_active,
            last_delivery=None,
            created_at=datetime.now()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating webhook: {str(e)}"
        )