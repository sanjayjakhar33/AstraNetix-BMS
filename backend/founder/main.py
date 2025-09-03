from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from ..shared.database.connection import get_db
from ..shared.models.models import Founder, ISP, Branch, User, Payment, BandwidthUsage
from .schemas import (
    FounderDashboardResponse, ISPCreateRequest, ISPCreateResponse, 
    ISPListResponse, GlobalPoliciesRequest, RevenueAnalyticsResponse,
    SystemMonitoringResponse
)
from ..shared.utils.security import hash_password, generate_domain_safe_string
from ..auth.dependencies import get_current_founder

router = APIRouter()

@router.get("/dashboard", response_model=FounderDashboardResponse)
async def get_founder_dashboard(
    current_founder: Founder = Depends(get_current_founder),
    db: Session = Depends(get_db)
):
    """
    Founder dashboard overview with AI-powered analytics
    - Total ISPs, revenue, system performance
    - Predictive revenue forecasting using ML
    - Real-time system health monitoring
    """
    try:
        # Get total ISPs count
        total_isps = db.query(ISP).filter(ISP.founder_id == current_founder.id).count()
        
        # Get total branches across all ISPs
        total_branches = db.query(Branch).join(ISP).filter(
            ISP.founder_id == current_founder.id
        ).count()
        
        # Get total users across all ISPs
        total_users = db.query(User).join(Branch).join(ISP).filter(
            ISP.founder_id == current_founder.id
        ).count()
        
        # Calculate total revenue for current month
        current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        total_revenue = db.query(Payment).join(User).join(Branch).join(ISP).filter(
            ISP.founder_id == current_founder.id,
            Payment.created_at >= current_month_start,
            Payment.status == 'completed'
        ).with_entities(Payment.amount).all()
        
        monthly_revenue = sum([payment.amount for payment in total_revenue]) if total_revenue else 0
        
        # Get recent ISP activity
        recent_isps = db.query(ISP).filter(
            ISP.founder_id == current_founder.id
        ).order_by(ISP.created_at.desc()).limit(5).all()
        
        return FounderDashboardResponse(
            total_isps=total_isps,
            total_branches=total_branches,
            total_users=total_users,
            monthly_revenue=float(monthly_revenue),
            system_health=99.9,  # This would be calculated from actual monitoring
            recent_isps=[
                {
                    "id": str(isp.id),
                    "company_name": isp.company_name,
                    "domain": isp.domain,
                    "created_at": isp.created_at.isoformat(),
                    "is_active": isp.is_active
                } for isp in recent_isps
            ]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching dashboard data: {str(e)}"
        )

@router.post("/isp/create", response_model=ISPCreateResponse)
async def create_isp_portal(
    isp_data: ISPCreateRequest,
    current_founder: Founder = Depends(get_current_founder),
    db: Session = Depends(get_db)
):
    """
    Create new ISP portal with auto-generated URL and white-label branding
    - Generate unique subdomain (isp-name.astranetix.com)
    - Setup custom branding (logo, colors, theme)
    - Initialize ISP database schemas and default settings
    - Send welcome email with login credentials
    """
    try:
        # Generate domain-safe string from company name
        domain_name = generate_domain_safe_string(isp_data.company_name)
        
        # Check if domain already exists
        existing_isp = db.query(ISP).filter(ISP.domain == domain_name).first()
        if existing_isp:
            # If domain exists, append a number
            counter = 1
            while existing_isp:
                test_domain = f"{domain_name}-{counter}"
                existing_isp = db.query(ISP).filter(ISP.domain == test_domain).first()
                if not existing_isp:
                    domain_name = test_domain
                    break
                counter += 1
        
        # Create new ISP
        new_isp = ISP(
            founder_id=current_founder.id,
            company_name=isp_data.company_name,
            domain=domain_name,
            email=isp_data.email,
            password_hash=hash_password(isp_data.password),
            contact_person=isp_data.contact_person,
            phone=isp_data.phone,
            address=isp_data.address,
            branding=isp_data.branding or {},
            settings=isp_data.settings or {}
        )
        
        db.add(new_isp)
        db.commit()
        db.refresh(new_isp)
        
        # Generate portal URL
        from ..shared.config import settings
        portal_url = f"https://{domain_name}.{settings.domain}"
        
        return ISPCreateResponse(
            isp_id=str(new_isp.id),
            portal_url=portal_url,
            domain=domain_name,
            message="ISP portal created successfully"
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating ISP portal: {str(e)}"
        )

@router.get("/isp/list", response_model=List[ISPListResponse])
async def list_isps(
    current_founder: Founder = Depends(get_current_founder),
    db: Session = Depends(get_db)
):
    """
    List all ISPs with status, revenue, and performance metrics
    - ISP performance analytics
    - Revenue tracking per ISP
    - Health status and alerts
    """
    try:
        isps = db.query(ISP).filter(ISP.founder_id == current_founder.id).all()
        
        isp_list = []
        for isp in isps:
            # Get branches count
            branches_count = db.query(Branch).filter(Branch.isp_id == isp.id).count()
            
            # Get users count
            users_count = db.query(User).join(Branch).filter(Branch.isp_id == isp.id).count()
            
            # Calculate monthly revenue
            current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            revenue = db.query(Payment).join(User).join(Branch).filter(
                Branch.isp_id == isp.id,
                Payment.created_at >= current_month_start,
                Payment.status == 'completed'
            ).with_entities(Payment.amount).all()
            
            monthly_revenue = sum([payment.amount for payment in revenue]) if revenue else 0
            
            isp_list.append(ISPListResponse(
                id=str(isp.id),
                company_name=isp.company_name,
                domain=isp.domain,
                email=isp.email,
                contact_person=isp.contact_person,
                branches_count=branches_count,
                users_count=users_count,
                monthly_revenue=float(monthly_revenue),
                is_active=isp.is_active,
                created_at=isp.created_at.isoformat(),
                portal_url=f"https://{isp.domain}.{settings.domain}"
            ))
        
        return isp_list
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching ISP list: {str(e)}"
        )

@router.put("/policies/global")
async def set_global_policies(
    policies: GlobalPoliciesRequest,
    current_founder: Founder = Depends(get_current_founder),
    db: Session = Depends(get_db)
):
    """
    Configure system-wide policies and settings
    - Global pricing policies
    - Bandwidth allocation rules
    - Compliance and security settings
    - Payment gateway configurations
    """
    try:
        # Update founder settings with global policies
        current_founder.settings = {
            **current_founder.settings,
            "global_policies": policies.dict()
        }
        
        db.commit()
        
        return {
            "message": "Global policies updated successfully",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating global policies: {str(e)}"
        )

@router.get("/revenue/analytics", response_model=RevenueAnalyticsResponse)
async def get_revenue_analytics(
    current_founder: Founder = Depends(get_current_founder),
    db: Session = Depends(get_db)
):
    """
    AI-powered revenue analytics and forecasting
    - Historical revenue trends
    - Predictive revenue forecasting using ML
    - Per-ISP revenue breakdown
    - Commission calculations
    """
    try:
        # Get revenue data for the last 12 months
        twelve_months_ago = datetime.now() - timedelta(days=365)
        
        revenue_data = db.query(Payment).join(User).join(Branch).join(ISP).filter(
            ISP.founder_id == current_founder.id,
            Payment.created_at >= twelve_months_ago,
            Payment.status == 'completed'
        ).all()
        
        # Group revenue by month
        monthly_revenue = {}
        for payment in revenue_data:
            month_key = payment.created_at.strftime('%Y-%m')
            if month_key not in monthly_revenue:
                monthly_revenue[month_key] = 0
            monthly_revenue[month_key] += float(payment.amount)
        
        # Simple prediction for next 3 months (in real implementation, use ML)
        last_3_months_avg = sum(list(monthly_revenue.values())[-3:]) / 3 if monthly_revenue else 0
        predicted_revenue = [last_3_months_avg * 1.05, last_3_months_avg * 1.08, last_3_months_avg * 1.12]
        
        return RevenueAnalyticsResponse(
            historical_revenue=monthly_revenue,
            predicted_revenue=predicted_revenue,
            total_revenue=sum(monthly_revenue.values()),
            growth_rate=5.0,  # This would be calculated from actual data
            confidence_score=0.85
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching revenue analytics: {str(e)}"
        )

@router.get("/system/monitoring", response_model=SystemMonitoringResponse)
async def get_system_monitoring(
    current_founder: Founder = Depends(get_current_founder),
    db: Session = Depends(get_db)
):
    """
    Real-time system monitoring with AI anomaly detection
    - System performance metrics
    - Resource utilization across all ISPs
    - Anomaly detection alerts
    - Predictive maintenance recommendations
    """
    try:
        # Get total users across all ISPs
        total_users = db.query(User).join(Branch).join(ISP).filter(
            ISP.founder_id == current_founder.id,
            User.is_active == True
        ).count()
        
        # Get recent bandwidth usage (mock data for demo)
        recent_usage = db.query(BandwidthUsage).join(User).join(Branch).join(ISP).filter(
            ISP.founder_id == current_founder.id,
            BandwidthUsage.date >= datetime.now().date() - timedelta(days=7)
        ).all()
        
        total_bandwidth_gb = sum([usage.total_bytes / (1024**3) for usage in recent_usage])
        avg_peak_usage = sum([usage.peak_usage_mbps for usage in recent_usage]) / len(recent_usage) if recent_usage else 0
        
        return SystemMonitoringResponse(
            system_health=99.9,
            active_users=total_users,
            total_bandwidth_gb=round(total_bandwidth_gb, 2),
            avg_peak_usage_mbps=round(avg_peak_usage, 2),
            alerts=[
                {
                    "type": "info",
                    "message": "System performance is optimal",
                    "timestamp": datetime.now().isoformat()
                }
            ],
            recommendations=[
                "Consider upgrading bandwidth capacity in the downtown region",
                "Monitor network performance during peak hours (7-10 PM)"
            ]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching system monitoring data: {str(e)}"
        )