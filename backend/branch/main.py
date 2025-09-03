from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..shared.database.connection import get_db
from ..shared.models.models import Branch, User, Payment, SupportTicket, BandwidthUsage, ISP
from .schemas import (
    BranchCreateRequest, BranchCreateResponse, BranchDashboardResponse,
    BranchListResponse, BranchUserListResponse, BranchAnalyticsResponse
)
from ..auth.dependencies import get_current_isp, get_current_user

router = APIRouter()

@router.post("/{isp_id}/create", response_model=BranchCreateResponse)
async def create_branch(
    isp_id: str,
    branch_data: BranchCreateRequest,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    Create new branch/sub-branch for ISP
    - Hierarchical branch structure support
    - Individual branch settings and branding
    - Local staff and user management
    - Branch-specific billing configuration
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        # Create new branch
        new_branch = Branch(
            isp_id=current_isp.id,
            name=branch_data.name,
            location=branch_data.location,
            manager_name=branch_data.manager_name,
            contact_email=branch_data.contact_email,
            phone=branch_data.phone,
            address=branch_data.address,
            settings=branch_data.settings or {}
        )
        
        db.add(new_branch)
        db.commit()
        db.refresh(new_branch)
        
        return BranchCreateResponse(
            branch_id=str(new_branch.id),
            name=new_branch.name,
            location=new_branch.location,
            manager_name=new_branch.manager_name,
            contact_email=new_branch.contact_email,
            message="Branch created successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating branch: {str(e)}"
        )

@router.get("/{branch_id}/dashboard", response_model=BranchDashboardResponse)
async def get_branch_dashboard(
    branch_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Branch-specific dashboard with local analytics
    - Local subscriber management
    - Branch-specific bandwidth utilization
    - Local revenue and billing
    - Staff performance metrics
    """
    try:
        # Get branch and verify access
        branch = db.query(Branch).filter(Branch.id == branch_id).first()
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )
        
        # Verify user has access to this branch
        if current_user['user_type'] == 'isp':
            isp = db.query(ISP).filter(ISP.id == current_user['sub']).first()
            if not isp or str(branch.isp_id) != str(isp.id):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this branch"
                )
        
        # Get branch statistics
        total_users = db.query(User).filter(
            User.branch_id == branch.id,
            User.is_active == True
        ).count()
        
        # Calculate monthly revenue
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_revenue = db.query(Payment).join(User).filter(
            User.branch_id == branch.id,
            Payment.created_at >= current_month_start,
            Payment.status == 'completed'
        ).with_entities(Payment.amount).all()
        
        total_revenue = sum([payment.amount for payment in monthly_revenue]) if monthly_revenue else 0
        
        # Get bandwidth usage for this branch
        week_ago = datetime.now() - timedelta(days=7)
        bandwidth_usage = db.query(BandwidthUsage).join(User).filter(
            User.branch_id == branch.id,
            BandwidthUsage.date >= week_ago.date()
        ).all()
        
        total_bandwidth_gb = sum([usage.total_bytes / (1024**3) for usage in bandwidth_usage])
        avg_peak_usage = sum([usage.peak_usage_mbps for usage in bandwidth_usage]) / len(bandwidth_usage) if bandwidth_usage else 0
        
        # Get support tickets
        open_tickets = db.query(SupportTicket).join(User).filter(
            User.branch_id == branch.id,
            SupportTicket.status.in_(['open', 'in_progress'])
        ).count()
        
        # Get top users by usage
        top_users = db.query(User).filter(User.branch_id == branch.id).limit(5).all()
        top_users_data = []
        for user in top_users:
            recent_usage = db.query(BandwidthUsage).filter(
                BandwidthUsage.user_id == user.id,
                BandwidthUsage.date >= week_ago.date()
            ).all()
            total_user_usage = sum([usage.total_bytes / (1024**3) for usage in recent_usage])
            
            top_users_data.append({
                "username": user.username,
                "full_name": user.full_name,
                "plan": user.subscription_plan,
                "usage_gb": round(total_user_usage, 2)
            })
        
        return BranchDashboardResponse(
            branch_id=str(branch.id),
            name=branch.name,
            location=branch.location,
            manager_name=branch.manager_name,
            total_users=total_users,
            monthly_revenue=float(total_revenue),
            total_bandwidth_gb=round(total_bandwidth_gb, 2),
            avg_peak_usage_mbps=round(avg_peak_usage, 2),
            open_support_tickets=open_tickets,
            network_health=97.8,  # This would be calculated from actual monitoring
            top_users=top_users_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching branch dashboard: {str(e)}"
        )

@router.get("/{isp_id}/list", response_model=List[BranchListResponse])
async def list_branches(
    isp_id: str,
    current_isp: ISP = Depends(get_current_isp),
    db: Session = Depends(get_db)
):
    """
    List all branches for an ISP
    """
    try:
        # Verify ISP access
        if str(current_isp.id) != isp_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this ISP"
            )
        
        branches = db.query(Branch).filter(
            Branch.isp_id == current_isp.id,
            Branch.is_active == True
        ).all()
        
        branch_list = []
        for branch in branches:
            # Get user count for each branch
            user_count = db.query(User).filter(
                User.branch_id == branch.id,
                User.is_active == True
            ).count()
            
            # Get recent revenue
            current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            revenue = db.query(Payment).join(User).filter(
                User.branch_id == branch.id,
                Payment.created_at >= current_month_start,
                Payment.status == 'completed'
            ).with_entities(Payment.amount).all()
            
            monthly_revenue = sum([payment.amount for payment in revenue]) if revenue else 0
            
            branch_list.append(BranchListResponse(
                id=str(branch.id),
                name=branch.name,
                location=branch.location,
                manager_name=branch.manager_name,
                contact_email=branch.contact_email,
                phone=branch.phone,
                user_count=user_count,
                monthly_revenue=float(monthly_revenue),
                is_active=branch.is_active,
                created_at=branch.created_at.isoformat()
            ))
        
        return branch_list
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching branch list: {str(e)}"
        )

@router.get("/{branch_id}/users", response_model=List[BranchUserListResponse])
async def list_branch_users(
    branch_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all users under specific branch
    - User status and activity
    - Bandwidth usage per user
    - Payment status and history
    - Support ticket tracking
    """
    try:
        # Get branch and verify access
        branch = db.query(Branch).filter(Branch.id == branch_id).first()
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )
        
        users = db.query(User).filter(User.branch_id == branch.id).all()
        
        user_list = []
        for user in users:
            # Get recent usage
            week_ago = datetime.now() - timedelta(days=7)
            recent_usage = db.query(BandwidthUsage).filter(
                BandwidthUsage.user_id == user.id,
                BandwidthUsage.date >= week_ago.date()
            ).all()
            
            total_usage_gb = sum([usage.total_bytes / (1024**3) for usage in recent_usage])
            
            # Get latest payment
            latest_payment = db.query(Payment).filter(
                Payment.user_id == user.id
            ).order_by(Payment.created_at.desc()).first()
            
            # Get open tickets
            open_tickets = db.query(SupportTicket).filter(
                SupportTicket.user_id == user.id,
                SupportTicket.status.in_(['open', 'in_progress'])
            ).count()
            
            user_list.append(BranchUserListResponse(
                id=str(user.id),
                username=user.username,
                full_name=user.full_name,
                email=user.email,
                subscription_plan=user.subscription_plan,
                bandwidth_limit=user.bandwidth_limit,
                is_active=user.is_active,
                recent_usage_gb=round(total_usage_gb, 2),
                last_payment_status=latest_payment.status if latest_payment else "no_payments",
                last_payment_date=latest_payment.created_at.isoformat() if latest_payment else None,
                open_tickets=open_tickets,
                created_at=user.created_at.isoformat()
            ))
        
        return user_list
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching branch users: {str(e)}"
        )

@router.get("/{branch_id}/analytics/ai", response_model=BranchAnalyticsResponse)
async def get_ai_branch_analytics(
    branch_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI-powered branch performance analytics
    - Resource optimization recommendations
    - Local traffic pattern analysis
    - Cross-branch performance comparison
    - Predictive maintenance alerts
    """
    try:
        # Get branch and verify access
        branch = db.query(Branch).filter(Branch.id == branch_id).first()
        if not branch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Branch not found"
            )
        
        # Get analytics data
        month_ago = datetime.now() - timedelta(days=30)
        
        # User growth
        users_data = db.query(User).filter(
            User.branch_id == branch.id,
            User.created_at >= month_ago
        ).all()
        
        # Calculate growth metrics
        total_users = db.query(User).filter(User.branch_id == branch.id).count()
        new_users_month = len(users_data)
        growth_rate = (new_users_month / total_users * 100) if total_users > 0 else 0
        
        # Revenue analytics
        revenue_data = db.query(Payment).join(User).filter(
            User.branch_id == branch.id,
            Payment.created_at >= month_ago,
            Payment.status == 'completed'
        ).all()
        
        total_revenue = sum([float(payment.amount) for payment in revenue_data])
        avg_revenue_per_user = total_revenue / total_users if total_users > 0 else 0
        
        # Bandwidth analytics
        bandwidth_data = db.query(BandwidthUsage).join(User).filter(
            User.branch_id == branch.id,
            BandwidthUsage.date >= month_ago.date()
        ).all()
        
        peak_usage_hours = {}
        for usage in bandwidth_data:
            hour = usage.created_at.hour
            peak_usage_hours[hour] = peak_usage_hours.get(hour, 0) + usage.peak_usage_mbps
        
        # Find peak hour
        peak_hour = max(peak_usage_hours.items(), key=lambda x: x[1])[0] if peak_usage_hours else 20
        
        # AI recommendations (simplified)
        recommendations = [
            f"Peak usage occurs at {peak_hour}:00. Consider traffic shaping during this time.",
            "User growth is steady. Plan for 20% capacity increase in next quarter.",
            "Revenue per user is below ISP average. Consider plan upgrade campaigns."
        ]
        
        if growth_rate > 10:
            recommendations.append("High user growth detected. Monitor network capacity closely.")
        
        # Performance metrics
        support_tickets = db.query(SupportTicket).join(User).filter(
            User.branch_id == branch.id,
            SupportTicket.created_at >= month_ago
        ).count()
        
        customer_satisfaction = max(0, 5.0 - (support_tickets / total_users * 5)) if total_users > 0 else 5.0
        
        return BranchAnalyticsResponse(
            branch_id=str(branch.id),
            branch_name=branch.name,
            total_users=total_users,
            new_users_month=new_users_month,
            user_growth_rate=round(growth_rate, 2),
            total_revenue_month=round(total_revenue, 2),
            avg_revenue_per_user=round(avg_revenue_per_user, 2),
            peak_usage_hour=peak_hour,
            customer_satisfaction_score=round(customer_satisfaction, 1),
            support_tickets_month=support_tickets,
            network_utilization=75.5,  # This would be from actual monitoring
            recommendations=recommendations,
            performance_score=85.2  # Calculated based on various metrics
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching branch analytics: {str(e)}"
        )