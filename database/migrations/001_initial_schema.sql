-- Multi-tenant architecture with logical isolation
-- AstraNetix BMS Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Founder level (system owners)
CREATE TABLE founders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ISP level (clients of founders)
CREATE TABLE isps (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    founder_id UUID REFERENCES founders(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    branding JSONB DEFAULT '{}', -- logo, colors, theme customization
    settings JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Branch level (sub-locations of ISPs)
CREATE TABLE branches (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    isp_id UUID REFERENCES isps(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    manager_name VARCHAR(255),
    contact_email VARCHAR(255),
    phone VARCHAR(20),
    address TEXT,
    settings JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- User level (end customers)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    branch_id UUID REFERENCES branches(id) ON DELETE CASCADE,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    subscription_plan VARCHAR(100),
    bandwidth_limit INTEGER, -- in Mbps
    data_limit INTEGER, -- in GB, null for unlimited
    connection_type VARCHAR(50) DEFAULT 'broadband',
    ip_address INET,
    mac_address VARCHAR(17),
    is_active BOOLEAN DEFAULT true,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Multi-tenant access control
CREATE TABLE tenant_access (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL,
    tenant_id UUID NOT NULL,
    tenant_type VARCHAR(20) NOT NULL CHECK (tenant_type IN ('founder', 'isp', 'branch', 'user')),
    role VARCHAR(100) NOT NULL,
    permissions JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Subscription plans
CREATE TABLE subscription_plans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    isp_id UUID REFERENCES isps(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    bandwidth_limit INTEGER NOT NULL, -- in Mbps
    data_limit INTEGER, -- in GB, null for unlimited
    price DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    billing_cycle VARCHAR(20) DEFAULT 'monthly', -- monthly, quarterly, yearly
    features JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Bandwidth usage tracking
CREATE TABLE bandwidth_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    upload_bytes BIGINT DEFAULT 0,
    download_bytes BIGINT DEFAULT 0,
    total_bytes BIGINT DEFAULT 0,
    peak_usage_mbps INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Payment transactions
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    gateway VARCHAR(50) NOT NULL, -- stripe, paypal, razorpay, crypto
    gateway_transaction_id VARCHAR(255),
    status VARCHAR(20) DEFAULT 'pending', -- pending, completed, failed, refunded
    billing_period_start DATE,
    billing_period_end DATE,
    invoice_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Support tickets
CREATE TABLE support_tickets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) DEFAULT 'general',
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, urgent
    status VARCHAR(20) DEFAULT 'open', -- open, in_progress, resolved, closed
    assigned_to UUID,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Network devices (Mikrotik, etc.)
CREATE TABLE network_devices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    branch_id UUID REFERENCES branches(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    device_type VARCHAR(50) NOT NULL, -- mikrotik, cisco, etc.
    ip_address INET NOT NULL,
    username VARCHAR(100),
    password_encrypted TEXT,
    snmp_community VARCHAR(100),
    radius_secret VARCHAR(255),
    settings JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT true,
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- AI analytics and insights
CREATE TABLE ai_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID NOT NULL,
    tenant_type VARCHAR(20) NOT NULL,
    insight_type VARCHAR(100) NOT NULL, -- bandwidth_optimization, churn_prediction, revenue_forecast
    data JSONB NOT NULL,
    confidence_score DECIMAL(5,4),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Audit logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    tenant_id UUID,
    tenant_type VARCHAR(20),
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(100),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_isps_founder_id ON isps(founder_id);
CREATE INDEX idx_branches_isp_id ON branches(isp_id);
CREATE INDEX idx_users_branch_id ON users(branch_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_bandwidth_usage_user_date ON bandwidth_usage(user_id, date);
CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_support_tickets_user_id ON support_tickets(user_id);
CREATE INDEX idx_network_devices_branch_id ON network_devices(branch_id);
CREATE INDEX idx_tenant_access_user_tenant ON tenant_access(user_id, tenant_id, tenant_type);
CREATE INDEX idx_audit_logs_tenant ON audit_logs(tenant_id, tenant_type);

-- Create update timestamp triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_founders_updated_at BEFORE UPDATE ON founders FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_isps_updated_at BEFORE UPDATE ON isps FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_branches_updated_at BEFORE UPDATE ON branches FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_payments_updated_at BEFORE UPDATE ON payments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_support_tickets_updated_at BEFORE UPDATE ON support_tickets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_network_devices_updated_at BEFORE UPDATE ON network_devices FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();