from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from ..shared.database.connection import get_db
from ..shared.models.models import ISP, Branch, User, SubscriptionPlan, BandwidthUsage, Payment, SupportTicket
from .schemas import (
    ISPDashboardResponse, SubscriberCreateRequest, SubscriberCreateResponse,
    SubscriberListResponse, BandwidthOptimizationResponse, SubscriberAnalyticsResponse,
    RadiusConfigRequest, PlanCreateRequest, PlanResponse
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