from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random

from shared.database.connection import get_db
from shared.models.models import SupportTicket, User, ISP
from auth.dependencies import get_current_user, get_current_isp
from .schemas import (
    SupportTicketCreate, SupportTicketResponse, ChatbotQuery, ChatbotResponse,
    KnowledgeBaseArticle, KnowledgeBaseResponse, SLAConfiguration, SupportAnalytics
)

router = APIRouter()

@router.post("/{tenant_id}/tickets", response_model=SupportTicketResponse)
async def create_support_ticket(
    tenant_id: str,
    ticket_data: SupportTicketCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create support ticket with SLA-driven priorities
    - Automated priority assignment
    - SLA deadline calculation
    - Notification triggers
    """
    try:
        # Calculate SLA deadline based on priority
        sla_hours = {
            "critical": 2,
            "high": 8, 
            "medium": 24,
            "low": 72
        }
        
        sla_deadline = datetime.now() + timedelta(hours=sla_hours.get(ticket_data.priority, 24))
        
        ticket = SupportTicket(
            title=ticket_data.title,
            description=ticket_data.description,
            priority=ticket_data.priority,
            category=ticket_data.category,
            user_id=ticket_data.user_id,
            tenant_id=tenant_id,
            status='open'
        )
        
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        
        return SupportTicketResponse(
            id=str(ticket.id),
            title=ticket.title,
            description=ticket.description,
            priority=ticket.priority,
            category=ticket.category,
            status=ticket.status,
            user_id=str(ticket.user_id) if ticket.user_id else None,
            assigned_to=None,
            sla_deadline=sla_deadline,
            resolution_time=None,
            satisfaction_rating=None,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating support ticket: {str(e)}"
        )

@router.post("/{tenant_id}/chatbot", response_model=ChatbotResponse)
async def chatbot_query(
    tenant_id: str,
    query: ChatbotQuery,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    AI chatbot for first-level support
    - Natural language processing
    - Knowledge base integration
    - Escalation detection
    """
    try:
        # Simulate AI chatbot response (in production, integrate with OpenAI/Gemini)
        message = query.message.lower()
        
        # Simple keyword-based responses for demo
        if "password" in message or "login" in message:
            response = "I can help you with password reset. Please click on 'Forgot Password' on the login page or contact your administrator."
            confidence = 0.9
            suggested_actions = ["Reset Password", "Contact Admin"]
            escalate = False
            kb_articles = [
                {"title": "How to Reset Your Password", "url": "/kb/password-reset"},
                {"title": "Login Troubleshooting", "url": "/kb/login-issues"}
            ]
        elif "billing" in message or "payment" in message:
            response = "For billing inquiries, I can help you view your current balance and payment history. Would you like me to show your account details?"
            confidence = 0.85
            suggested_actions = ["View Balance", "Payment History", "Update Payment Method"]
            escalate = False
            kb_articles = [
                {"title": "Understanding Your Bill", "url": "/kb/billing-explained"},
                {"title": "Payment Methods", "url": "/kb/payment-options"}
            ]
        elif "slow" in message or "speed" in message or "internet" in message:
            response = "I understand you're experiencing speed issues. Let me help you troubleshoot. First, please try restarting your modem and router."
            confidence = 0.8
            suggested_actions = ["Speed Test", "Restart Equipment", "Check Network Status"]
            escalate = False
            kb_articles = [
                {"title": "Troubleshooting Slow Internet", "url": "/kb/slow-internet"},
                {"title": "Optimizing Your Connection", "url": "/kb/optimize-connection"}
            ]
        else:
            response = "I'm here to help! Could you please provide more details about your issue? You can ask about billing, technical problems, or account management."
            confidence = 0.6
            suggested_actions = ["Contact Human Agent", "Browse Help Topics"]
            escalate = True
            kb_articles = [
                {"title": "Getting Started Guide", "url": "/kb/getting-started"},
                {"title": "Frequently Asked Questions", "url": "/kb/faq"}
            ]
        
        return ChatbotResponse(
            response=response,
            confidence=confidence,
            suggested_actions=suggested_actions,
            escalate_to_human=escalate,
            knowledge_base_articles=kb_articles
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chatbot query: {str(e)}"
        )

@router.get("/{tenant_id}/analytics", response_model=SupportAnalytics)
async def get_support_analytics(
    tenant_id: str,
    days_back: int = 30,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Support analytics and KPI dashboard
    - Ticket volume and trends
    - Agent performance metrics
    - SLA compliance tracking
    - Customer satisfaction scores
    """
    try:
        start_date = datetime.now() - timedelta(days=days_back)
        
        # Get ticket statistics
        total_tickets = db.query(SupportTicket).filter(
            SupportTicket.tenant_id == tenant_id,
            SupportTicket.created_at >= start_date
        ).count()
        
        open_tickets = db.query(SupportTicket).filter(
            SupportTicket.tenant_id == tenant_id,
            SupportTicket.status.in_(['open', 'in_progress'])
        ).count()
        
        resolved_tickets = db.query(SupportTicket).filter(
            SupportTicket.tenant_id == tenant_id,
            SupportTicket.status == 'resolved',
            SupportTicket.created_at >= start_date
        ).count()
        
        # Calculate average resolution time (simulated)
        avg_resolution_time = 18.5  # hours
        
        # Calculate SLA compliance (simulated)
        sla_compliance_rate = 94.2  # percentage
        
        # Customer satisfaction (simulated)
        customer_satisfaction = 4.3  # out of 5
        
        # Top categories
        top_categories = [
            {"category": "Technical Issues", "count": 45, "percentage": 35.7},
            {"category": "Billing Inquiries", "count": 32, "count": 25.4},
            {"category": "Account Management", "count": 28, "percentage": 22.2},
            {"category": "General Questions", "count": 21, "percentage": 16.7}
        ]
        
        # Agent performance (simulated)
        agent_performance = [
            {
                "agent_name": "John Smith",
                "tickets_resolved": 23,
                "avg_resolution_time": 16.2,
                "satisfaction_rating": 4.5
            },
            {
                "agent_name": "Sarah Johnson", 
                "tickets_resolved": 19,
                "avg_resolution_time": 14.8,
                "satisfaction_rating": 4.7
            }
        ]
        
        # Ticket trends
        ticket_trends = []
        for i in range(7):  # Last 7 days
            day = datetime.now() - timedelta(days=i)
            count = random.randint(8, 25)  # Simulated daily ticket count
            ticket_trends.append({
                "date": day.strftime("%Y-%m-%d"),
                "ticket_count": count,
                "resolved_count": random.randint(6, count)
            })
        
        return SupportAnalytics(
            total_tickets=total_tickets,
            open_tickets=open_tickets,
            resolved_tickets=resolved_tickets,
            average_resolution_time=avg_resolution_time,
            sla_compliance_rate=sla_compliance_rate,
            customer_satisfaction=customer_satisfaction,
            top_categories=top_categories,
            agent_performance=agent_performance,
            ticket_trends=ticket_trends
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching support analytics: {str(e)}"
        )

@router.get("/{tenant_id}/tickets", response_model=List[SupportTicketResponse])
async def get_support_tickets(
    tenant_id: str,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = 50,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get support tickets with filtering options"""
    try:
        query = db.query(SupportTicket).filter(SupportTicket.tenant_id == tenant_id)
        
        if status:
            query = query.filter(SupportTicket.status == status)
            
        if priority:
            query = query.filter(SupportTicket.priority == priority)
        
        tickets = query.order_by(desc(SupportTicket.created_at)).limit(limit).all()
        
        return [
            SupportTicketResponse(
                id=str(ticket.id),
                title=ticket.title,
                description=ticket.description,
                priority=ticket.priority,
                category=ticket.category,
                status=ticket.status,
                user_id=str(ticket.user_id) if ticket.user_id else None,
                assigned_to=None,  # Would come from assigned agent relationship
                sla_deadline=None,  # Would be calculated from SLA rules
                resolution_time=None,  # Would be calculated from created/resolved times
                satisfaction_rating=None,  # Would come from satisfaction surveys
                created_at=ticket.created_at,
                updated_at=ticket.updated_at
            ) for ticket in tickets
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching support tickets: {str(e)}"
        )

@router.get("/{tenant_id}/knowledge-base", response_model=List[KnowledgeBaseResponse])
async def get_knowledge_base_articles(
    tenant_id: str,
    category: Optional[str] = None,
    language: str = "en",
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get knowledge base articles
    - Categorized help content
    - Multi-language support
    - Usage analytics
    """
    try:
        # Sample knowledge base articles (in production, these would be in database)
        articles = [
            {
                "id": "kb-001",
                "title": "Getting Started with Your Internet Service",
                "content": "Welcome to your new internet service! This guide will help you...",
                "category": "getting_started",
                "tags": ["setup", "basics", "new_customer"],
                "views": 1247,
                "helpful_votes": 89,
                "is_public": True,
                "language": "en",
                "created_at": datetime.now() - timedelta(days=30),
                "updated_at": datetime.now() - timedelta(days=5)
            },
            {
                "id": "kb-002",
                "title": "Troubleshooting Connection Issues",
                "content": "If you're experiencing connectivity problems, try these steps...",
                "category": "technical",
                "tags": ["troubleshooting", "connection", "technical"],
                "views": 892,
                "helpful_votes": 67,
                "is_public": True,
                "language": "en",
                "created_at": datetime.now() - timedelta(days=25),
                "updated_at": datetime.now() - timedelta(days=3)
            },
            {
                "id": "kb-003",
                "title": "Understanding Your Monthly Bill",
                "content": "Your monthly bill includes several components...",
                "category": "billing",
                "tags": ["billing", "charges", "explanation"],
                "views": 654,
                "helpful_votes": 45,
                "is_public": True,
                "language": "en",
                "created_at": datetime.now() - timedelta(days=20),
                "updated_at": datetime.now() - timedelta(days=1)
            }
        ]
        
        # Filter by category if specified
        if category:
            articles = [article for article in articles if article["category"] == category]
        
        return [KnowledgeBaseResponse(**article) for article in articles]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching knowledge base articles: {str(e)}"
        )