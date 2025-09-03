from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, DECIMAL, Date, BigInteger, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class Founder(Base):
    __tablename__ = "founders"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    is_active = Column(Boolean, default=True)
    settings = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    isps = relationship("ISP", back_populates="founder")

class ISP(Base):
    __tablename__ = "isps"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    founder_id = Column(UUID(as_uuid=True), ForeignKey("founders.id", ondelete="CASCADE"))
    company_name = Column(String(255), nullable=False)
    domain = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    contact_person = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    branding = Column(JSONB, default={})
    settings = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    founder = relationship("Founder", back_populates="isps")
    branches = relationship("Branch", back_populates="isp")
    subscription_plans = relationship("SubscriptionPlan", back_populates="isp")

class Branch(Base):
    __tablename__ = "branches"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isp_id = Column(UUID(as_uuid=True), ForeignKey("isps.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    location = Column(String(255))
    manager_name = Column(String(255))
    contact_email = Column(String(255))
    phone = Column(String(20))
    address = Column(Text)
    settings = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    isp = relationship("ISP", back_populates="branches")
    users = relationship("User", back_populates="branch")
    network_devices = relationship("NetworkDevice", back_populates="branch")

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    branch_id = Column(UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"))
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20))
    address = Column(Text)
    subscription_plan = Column(String(100))
    bandwidth_limit = Column(Integer)  # in Mbps
    data_limit = Column(Integer)  # in GB, null for unlimited
    connection_type = Column(String(50), default='broadband')
    ip_address = Column(INET)
    mac_address = Column(String(17))
    is_active = Column(Boolean, default=True)
    settings = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    branch = relationship("Branch", back_populates="users")
    bandwidth_usage = relationship("BandwidthUsage", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    support_tickets = relationship("SupportTicket", back_populates="user")

class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isp_id = Column(UUID(as_uuid=True), ForeignKey("isps.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    description = Column(Text)
    bandwidth_limit = Column(Integer, nullable=False)  # in Mbps
    data_limit = Column(Integer)  # in GB, null for unlimited
    price = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default='USD')
    billing_cycle = Column(String(20), default='monthly')
    features = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    isp = relationship("ISP", back_populates="subscription_plans")

class BandwidthUsage(Base):
    __tablename__ = "bandwidth_usage"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    date = Column(Date, nullable=False)
    upload_bytes = Column(BigInteger, default=0)
    download_bytes = Column(BigInteger, default=0)
    total_bytes = Column(BigInteger, default=0)
    peak_usage_mbps = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bandwidth_usage")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default='USD')
    gateway = Column(String(50), nullable=False)
    gateway_transaction_id = Column(String(255))
    status = Column(String(20), default='pending')
    billing_period_start = Column(Date)
    billing_period_end = Column(Date)
    invoice_data = Column(JSONB)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="payments")

class SupportTicket(Base):
    __tablename__ = "support_tickets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), default='general')
    priority = Column(String(20), default='medium')
    status = Column(String(20), default='open')
    assigned_to = Column(UUID(as_uuid=True))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="support_tickets")

class NetworkDevice(Base):
    __tablename__ = "network_devices"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    branch_id = Column(UUID(as_uuid=True), ForeignKey("branches.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    device_type = Column(String(50), nullable=False)
    ip_address = Column(INET, nullable=False)
    username = Column(String(100))
    password_encrypted = Column(Text)
    snmp_community = Column(String(100))
    radius_secret = Column(String(255))
    settings = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    branch = relationship("Branch", back_populates="network_devices")

class TenantAccess(Base):
    __tablename__ = "tenant_access"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_type = Column(String(20), nullable=False)
    role = Column(String(100), nullable=False)
    permissions = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AIInsight(Base):
    __tablename__ = "ai_insights"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_type = Column(String(20), nullable=False)
    insight_type = Column(String(100), nullable=False)
    data = Column(JSONB, nullable=False)
    confidence_score = Column(DECIMAL(5, 4))
    created_at = Column(DateTime, default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True))
    tenant_id = Column(UUID(as_uuid=True))
    tenant_type = Column(String(20))
    action = Column(String(100), nullable=False)
    resource = Column(String(100))
    old_values = Column(JSONB)
    new_values = Column(JSONB)
    ip_address = Column(INET)
    user_agent = Column(Text)
    ai_risk_score = Column(Float)  # AI-based risk assessment
    created_at = Column(DateTime, default=func.now())

# NOC Dashboard Models
class NetworkAlert(Base):
    __tablename__ = "network_alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_type = Column(String(20), nullable=False)
    alert_type = Column(String(50), nullable=False)  # bandwidth, latency, device_down, security
    severity = Column(String(20), nullable=False)  # critical, high, medium, low
    title = Column(String(255), nullable=False)
    description = Column(Text)
    source = Column(String(100))  # device_id, network_segment, etc.
    status = Column(String(20), default='open')  # open, acknowledged, resolved
    escalated = Column(Boolean, default=False)
    auto_resolved = Column(Boolean, default=False)
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime)

class SLADefinition(Base):
    __tablename__ = "sla_definitions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isp_id = Column(UUID(as_uuid=True), ForeignKey("isps.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    uptime_target = Column(DECIMAL(5, 4), default=0.999)  # 99.9%
    response_time_target = Column(Integer)  # milliseconds
    resolution_time_target = Column(Integer)  # hours
    bandwidth_guarantee = Column(Integer)  # Mbps
    penalties = Column(JSONB, default={})
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

# CRM & Marketing Models
class CustomerSegment(Base):
    __tablename__ = "customer_segments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isp_id = Column(UUID(as_uuid=True), ForeignKey("isps.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    criteria = Column(JSONB, nullable=False)  # usage, location, plan, etc.
    description = Column(Text)
    auto_update = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class MarketingCampaign(Base):
    __tablename__ = "marketing_campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isp_id = Column(UUID(as_uuid=True), ForeignKey("isps.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    campaign_type = Column(String(50), nullable=False)  # email, sms, push
    status = Column(String(20), default='draft')  # draft, scheduled, running, completed
    target_segments = Column(JSONB, default=[])
    content = Column(JSONB, nullable=False)
    scheduled_at = Column(DateTime)
    metrics = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())

# Training & Certification Models
class TrainingModule(Base):
    __tablename__ = "training_modules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isp_id = Column(UUID(as_uuid=True), ForeignKey("isps.id", ondelete="CASCADE"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content = Column(JSONB, nullable=False)  # lessons, videos, documents
    difficulty_level = Column(String(20), default='beginner')
    estimated_duration = Column(Integer)  # minutes
    prerequisites = Column(JSONB, default=[])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class UserTrainingProgress(Base):
    __tablename__ = "user_training_progress"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    module_id = Column(UUID(as_uuid=True), ForeignKey("training_modules.id", ondelete="CASCADE"))
    progress_percentage = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    score = Column(Integer)
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)

# Backup & Disaster Recovery Models
class BackupSchedule(Base):
    __tablename__ = "backup_schedules"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_type = Column(String(20), nullable=False)
    backup_type = Column(String(50), nullable=False)  # database, configs, logs
    frequency = Column(String(20), nullable=False)  # daily, weekly, monthly
    retention_days = Column(Integer, default=30)
    geo_replication = Column(Boolean, default=True)
    encryption_enabled = Column(Boolean, default=True)
    last_backup = Column(DateTime)
    status = Column(String(20), default='active')
    settings = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())

class BackupRecord(Base):
    __tablename__ = "backup_records"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schedule_id = Column(UUID(as_uuid=True), ForeignKey("backup_schedules.id", ondelete="CASCADE"))
    backup_path = Column(String(500), nullable=False)
    file_size = Column(BigInteger)  # bytes
    status = Column(String(20), nullable=False)  # success, failed, in_progress
    error_message = Column(Text)
    checksum = Column(String(255))
    started_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)

# Log Management & SIEM Models
class SecurityEvent(Base):
    __tablename__ = "security_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    event_type = Column(String(50), nullable=False)  # intrusion, ddos, bruteforce, etc.
    severity = Column(String(20), nullable=False)
    source_ip = Column(INET)
    target_ip = Column(INET)
    description = Column(Text)
    raw_log = Column(Text)
    threat_score = Column(Integer)  # 1-100
    auto_blocked = Column(Boolean, default=False)
    investigated = Column(Boolean, default=False)
    false_positive = Column(Boolean, default=False)
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())

# Mobile App Configuration
class MobileAppConfig(Base):
    __tablename__ = "mobile_app_configs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isp_id = Column(UUID(as_uuid=True), ForeignKey("isps.id", ondelete="CASCADE"))
    app_name = Column(String(255), nullable=False)
    package_name = Column(String(255), nullable=False)
    version = Column(String(20), default='1.0.0')
    branding = Column(JSONB, default={})  # colors, logos, themes
    features = Column(JSONB, default={})  # enabled features
    push_config = Column(JSONB, default={})
    store_config = Column(JSONB, default={})  # app store details
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())

# Advanced Reporting Models
class ReportTemplate(Base):
    __tablename__ = "report_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    isp_id = Column(UUID(as_uuid=True), ForeignKey("isps.id", ondelete="CASCADE"))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    report_type = Column(String(50), nullable=False)  # usage, billing, network, compliance
    config = Column(JSONB, nullable=False)  # fields, filters, formatting
    schedule = Column(JSONB)  # auto-generation schedule
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())

class ReportGeneration(Base):
    __tablename__ = "report_generations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("report_templates.id", ondelete="CASCADE"))
    generated_by = Column(UUID(as_uuid=True))
    file_path = Column(String(500))
    file_format = Column(String(10))  # pdf, csv, xlsx
    status = Column(String(20), default='generating')
    parameters = Column(JSONB, default={})
    error_message = Column(Text)
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)

# Green Network & CSR Models
class SustainabilityMetric(Base):
    __tablename__ = "sustainability_metrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_type = Column(String(20), nullable=False)
    metric_type = Column(String(50), nullable=False)  # energy_consumption, carbon_footprint
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)  # kWh, kg_co2, etc.
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    device_id = Column(String(100))
    location = Column(String(255))
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime, default=func.now())

# Webhook System
class WebhookEndpoint(Base):
    __tablename__ = "webhook_endpoints"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    tenant_type = Column(String(20), nullable=False)
    url = Column(String(500), nullable=False)
    events = Column(JSONB, nullable=False)  # list of event types to subscribe to
    secret_key = Column(String(255))  # for signature verification
    is_active = Column(Boolean, default=True)
    retry_count = Column(Integer, default=3)
    timeout_seconds = Column(Integer, default=30)
    last_delivery = Column(DateTime)
    created_at = Column(DateTime, default=func.now())