from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from datetime import datetime

# Enhanced Support Ticket Schemas
class SupportTicketCreate(BaseModel):
    title: str
    description: str
    priority: str  # low, medium, high, critical
    category: str  # technical, billing, general
    user_id: Optional[str] = None
    attachments: Optional[List[str]] = []

class SupportTicketResponse(BaseModel):
    id: str
    title: str
    description: str
    priority: str
    category: str
    status: str  # open, in_progress, resolved, closed
    user_id: Optional[str]
    assigned_to: Optional[str]
    sla_deadline: Optional[datetime]
    resolution_time: Optional[int]  # minutes
    satisfaction_rating: Optional[int]  # 1-5
    created_at: datetime
    updated_at: datetime

# AI Chatbot Schemas
class ChatbotQuery(BaseModel):
    message: str
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = {}

class ChatbotResponse(BaseModel):
    response: str
    confidence: float
    suggested_actions: List[str]
    escalate_to_human: bool
    knowledge_base_articles: List[Dict[str, str]]

# Knowledge Base Schemas
class KnowledgeBaseArticle(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]
    is_public: bool = True
    language: str = "en"

class KnowledgeBaseResponse(BaseModel):
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    views: int
    helpful_votes: int
    is_public: bool
    language: str
    created_at: datetime
    updated_at: datetime

# SLA Configuration
class SLAConfiguration(BaseModel):
    priority_response_times: Dict[str, int]  # priority -> minutes
    escalation_rules: List[Dict[str, Any]]
    business_hours: Dict[str, str]
    notification_settings: Dict[str, Any]

# Support Analytics
class SupportAnalytics(BaseModel):
    total_tickets: int
    open_tickets: int
    resolved_tickets: int
    average_resolution_time: float  # hours
    sla_compliance_rate: float  # percentage
    customer_satisfaction: float  # average rating
    top_categories: List[Dict[str, Any]]
    agent_performance: List[Dict[str, Any]]
    ticket_trends: List[Dict[str, Any]]