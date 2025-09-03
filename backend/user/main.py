from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..shared.database.connection import get_db
from ..shared.models.models import User, BandwidthUsage, Payment, SupportTicket, SubscriptionPlan, Branch
from .schemas import (
    UserDashboardResponse, UsageResponse, PaymentHistoryResponse,
    SupportTicketCreateRequest, SupportTicketResponse, PlanUpgradeRequest
)
from ..auth.dependencies import get_current_end_user

router = APIRouter()

@router.get("/{user_id}/dashboard", response_model=UserDashboardResponse)
async def get_user_dashboard(
    user_id: str,
    current_user: User = Depends(get_current_end_user),
    db: Session = Depends(get_db)
):
    """
    User self-service dashboard
    - Real-time usage monitoring
    - Billing and payment history
    - Plan upgrade/downgrade options
    - Support ticket management
    """
    try:
        # Verify user access
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this user account"
            )
        
        # Get current month usage
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        current_usage = db.query(BandwidthUsage).filter(
            BandwidthUsage.user_id == current_user.id,
            BandwidthUsage.date >= current_month_start.date()
        ).all()
        
        total_usage_gb = sum([usage.total_bytes / (1024**3) for usage in current_usage])
        peak_usage_mbps = max([usage.peak_usage_mbps for usage in current_usage], default=0)
        
        # Calculate usage percentage
        data_limit = current_user.data_limit
        usage_percentage = (total_usage_gb / data_limit * 100) if data_limit else 0
        
        # Get latest payment
        latest_payment = db.query(Payment).filter(
            Payment.user_id == current_user.id
        ).order_by(Payment.created_at.desc()).first()
        
        # Get open support tickets
        open_tickets = db.query(SupportTicket).filter(
            SupportTicket.user_id == current_user.id,
            SupportTicket.status.in_(['open', 'in_progress'])
        ).count()
        
        # Calculate next billing date
        next_billing_date = datetime.now() + timedelta(days=30)  # Simplified
        
        return UserDashboardResponse(
            user_id=str(current_user.id),
            username=current_user.username,
            full_name=current_user.full_name,
            email=current_user.email,
            subscription_plan=current_user.subscription_plan,
            bandwidth_limit=current_user.bandwidth_limit,
            data_limit=current_user.data_limit,
            current_usage_gb=round(total_usage_gb, 2),
            usage_percentage=round(usage_percentage, 1),
            peak_usage_mbps=peak_usage_mbps,
            account_status="active" if current_user.is_active else "suspended",
            next_billing_date=next_billing_date.isoformat(),
            last_payment_amount=float(latest_payment.amount) if latest_payment else 0,
            last_payment_status=latest_payment.status if latest_payment else "no_payments",
            open_support_tickets=open_tickets,
            connection_status="online",  # This would be from network monitoring
            ip_address=str(current_user.ip_address) if current_user.ip_address else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching user dashboard: {str(e)}"
        )

@router.get("/{user_id}/usage/realtime", response_model=UsageResponse)
async def get_realtime_usage(
    user_id: str,
    days: int = 30,
    current_user: User = Depends(get_current_end_user),
    db: Session = Depends(get_db)
):
    """
    Real-time bandwidth usage monitoring
    - Current usage statistics
    - Historical usage trends
    - Usage alerts and notifications
    - Bandwidth optimization tips
    """
    try:
        # Verify user access
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this user account"
            )
        
        # Get usage data for specified period
        start_date = datetime.now() - timedelta(days=days)
        usage_data = db.query(BandwidthUsage).filter(
            BandwidthUsage.user_id == current_user.id,
            BandwidthUsage.date >= start_date.date()
        ).order_by(BandwidthUsage.date.desc()).all()
        
        # Calculate statistics
        total_usage_gb = sum([usage.total_bytes / (1024**3) for usage in usage_data])
        avg_daily_usage = total_usage_gb / days if days > 0 else 0
        peak_usage = max([usage.peak_usage_mbps for usage in usage_data], default=0)
        
        # Daily breakdown
        daily_usage = {}
        for usage in usage_data:
            date_key = usage.date.isoformat()
            daily_usage[date_key] = {
                "total_gb": round(usage.total_bytes / (1024**3), 2),
                "upload_gb": round(usage.upload_bytes / (1024**3), 2),
                "download_gb": round(usage.download_bytes / (1024**3), 2),
                "peak_mbps": usage.peak_usage_mbps
            }
        
        # Generate usage alerts
        alerts = []
        if current_user.data_limit:
            current_month_usage = sum([
                usage.total_bytes / (1024**3) for usage in usage_data 
                if usage.date.month == datetime.now().month
            ])
            usage_percentage = (current_month_usage / current_user.data_limit) * 100
            
            if usage_percentage > 90:
                alerts.append({
                    "type": "critical",
                    "message": f"You've used {usage_percentage:.1f}% of your monthly data limit"
                })
            elif usage_percentage > 75:
                alerts.append({
                    "type": "warning", 
                    "message": f"You've used {usage_percentage:.1f}% of your monthly data limit"
                })
        
        # Optimization tips
        optimization_tips = [
            "Stream videos in HD instead of 4K to save bandwidth",
            "Use WiFi when available to avoid mobile data usage",
            "Download large files during off-peak hours",
            "Enable data compression in your browser"
        ]
        
        return UsageResponse(
            user_id=str(current_user.id),
            period_days=days,
            total_usage_gb=round(total_usage_gb, 2),
            avg_daily_usage_gb=round(avg_daily_usage, 2),
            peak_usage_mbps=peak_usage,
            data_limit_gb=current_user.data_limit,
            bandwidth_limit_mbps=current_user.bandwidth_limit,
            daily_usage=daily_usage,
            alerts=alerts,
            optimization_tips=optimization_tips
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching usage data: {str(e)}"
        )

@router.get("/{user_id}/payments", response_model=PaymentHistoryResponse)
async def get_payment_history(
    user_id: str,
    limit: int = 10,
    current_user: User = Depends(get_current_end_user),
    db: Session = Depends(get_db)
):
    """
    Get payment history for user
    """
    try:
        # Verify user access
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this user account"
            )
        
        payments = db.query(Payment).filter(
            Payment.user_id == current_user.id
        ).order_by(Payment.created_at.desc()).limit(limit).all()
        
        payment_list = []
        for payment in payments:
            payment_list.append({
                "id": str(payment.id),
                "amount": float(payment.amount),
                "currency": payment.currency,
                "status": payment.status,
                "gateway": payment.gateway,
                "billing_period_start": payment.billing_period_start.isoformat() if payment.billing_period_start else None,
                "billing_period_end": payment.billing_period_end.isoformat() if payment.billing_period_end else None,
                "created_at": payment.created_at.isoformat()
            })
        
        # Calculate total paid
        total_paid = sum([float(p.amount) for p in payments if p.status == 'completed'])
        
        return PaymentHistoryResponse(
            user_id=str(current_user.id),
            total_payments=len(payments),
            total_amount_paid=total_paid,
            payments=payment_list
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching payment history: {str(e)}"
        )

@router.post("/{user_id}/support/ticket", response_model=SupportTicketResponse)
async def create_support_ticket(
    user_id: str,
    ticket_data: SupportTicketCreateRequest,
    current_user: User = Depends(get_current_end_user),
    db: Session = Depends(get_db)
):
    """
    AI-powered support ticket system
    - Automated issue categorization
    - Smart troubleshooting suggestions
    - Intelligent ticket routing
    - Real-time status updates
    """
    try:
        # Verify user access
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this user account"
            )
        
        # Create support ticket
        new_ticket = SupportTicket(
            user_id=current_user.id,
            title=ticket_data.title,
            description=ticket_data.description,
            category=ticket_data.category or 'general',
            priority=ticket_data.priority or 'medium'
        )
        
        db.add(new_ticket)
        db.commit()
        db.refresh(new_ticket)
        
        # AI-powered automatic suggestions (simplified)
        auto_suggestions = []
        if 'slow' in ticket_data.description.lower() or 'speed' in ticket_data.description.lower():
            auto_suggestions = [
                "Try restarting your router/modem",
                "Check if other devices are using bandwidth",
                "Run a speed test at different times",
                "Contact us if speeds are consistently below your plan"
            ]
        elif 'connection' in ticket_data.description.lower() or 'internet' in ticket_data.description.lower():
            auto_suggestions = [
                "Check all cable connections",
                "Restart your router and modem",
                "Try connecting directly with ethernet cable",
                "Check if there are any service outages in your area"
            ]
        else:
            auto_suggestions = [
                "Please provide more details about the issue",
                "Include any error messages you're seeing",
                "Let us know when the issue started"
            ]
        
        return SupportTicketResponse(
            ticket_id=str(new_ticket.id),
            title=new_ticket.title,
            status=new_ticket.status,
            category=new_ticket.category,
            priority=new_ticket.priority,
            created_at=new_ticket.created_at.isoformat(),
            auto_suggestions=auto_suggestions,
            estimated_resolution="2-4 hours" if new_ticket.priority == 'high' else "24-48 hours"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating support ticket: {str(e)}"
        )

@router.get("/{user_id}/plans/available", response_model=List[dict])
async def get_available_plans(
    user_id: str,
    current_user: User = Depends(get_current_end_user),
    db: Session = Depends(get_db)
):
    """
    Get available subscription plans for upgrade/downgrade
    """
    try:
        # Verify user access
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this user account"
            )
        
        # Get available plans for this ISP
        plans = db.query(SubscriptionPlan).join(Branch).filter(
            Branch.id == current_user.branch_id,
            SubscriptionPlan.is_active == True
        ).all()
        
        plan_list = []
        for plan in plans:
            is_current = plan.name == current_user.subscription_plan
            
            plan_list.append({
                "id": str(plan.id),
                "name": plan.name,
                "description": plan.description,
                "bandwidth_limit": plan.bandwidth_limit,
                "data_limit": plan.data_limit,
                "price": float(plan.price),
                "currency": plan.currency,
                "billing_cycle": plan.billing_cycle,
                "features": plan.features or {},
                "is_current_plan": is_current,
                "upgrade_available": plan.price > next((p.price for p in plans if p.name == current_user.subscription_plan), 0),
                "downgrade_available": plan.price < next((p.price for p in plans if p.name == current_user.subscription_plan), float('inf'))
            })
        
        return plan_list
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching available plans: {str(e)}"
        )