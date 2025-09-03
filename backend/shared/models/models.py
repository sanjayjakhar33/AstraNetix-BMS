from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, DECIMAL, Date, BigInteger, ForeignKey
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
    created_at = Column(DateTime, default=func.now())