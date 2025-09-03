-- Seed data for AstraNetix BMS
-- This creates initial demo data for development and testing

-- Insert demo founder
INSERT INTO founders (id, email, password_hash, company_name, full_name, phone, address)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'founder@astranetix.com',
    '$2b$12$LQv3c1yqBwEHxkqx8kfPPeOC8ZYP7.c5QnV0L7YXQ5X5X5X5X5X5X', -- password: 'admin123'
    'AstraNetix Technologies',
    'John Founder',
    '+1-555-0100',
    '123 Tech Street, Silicon Valley, CA 94000'
);

-- Insert demo ISP
INSERT INTO isps (id, founder_id, company_name, domain, email, password_hash, contact_person, phone, address, branding)
VALUES (
    '550e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440000',
    'Demo ISP Solutions',
    'demo-isp',
    'admin@demo-isp.com',
    '$2b$12$LQv3c1yqBwEHxkqx8kfPPeOC8ZYP7.c5QnV0L7YXQ5X5X5X5X5X5X', -- password: 'admin123'
    'Jane ISP Manager',
    '+1-555-0200',
    '456 Network Ave, Tech City, CA 94001',
    '{"logo": "demo-logo.png", "primary_color": "#007bff", "secondary_color": "#6c757d", "theme": "modern"}'
);

-- Insert demo branches
INSERT INTO branches (id, isp_id, name, location, manager_name, contact_email, phone, address)
VALUES 
(
    '550e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440001',
    'Downtown Branch',
    'Downtown District',
    'Mike Branch Manager',
    'mike@demo-isp.com',
    '+1-555-0300',
    '789 Main Street, Downtown, CA 94002'
),
(
    '550e8400-e29b-41d4-a716-446655440003',
    '550e8400-e29b-41d4-a716-446655440001',
    'Suburban Branch',
    'Suburban Area',
    'Sarah Branch Manager',
    'sarah@demo-isp.com',
    '+1-555-0400',
    '321 Suburban Blvd, Suburbia, CA 94003'
);

-- Insert demo subscription plans
INSERT INTO subscription_plans (id, isp_id, name, description, bandwidth_limit, data_limit, price, currency, billing_cycle, features)
VALUES 
(
    '550e8400-e29b-41d4-a716-446655440010',
    '550e8400-e29b-41d4-a716-446655440001',
    'Basic Plan',
    'Perfect for home users with light internet usage',
    25, -- 25 Mbps
    500, -- 500 GB
    29.99,
    'USD',
    'monthly',
    '{"support": "email", "static_ip": false, "priority": "standard"}'
),
(
    '550e8400-e29b-41d4-a716-446655440011',
    '550e8400-e29b-41d4-a716-446655440001',
    'Premium Plan',
    'High-speed internet for families and small businesses',
    100, -- 100 Mbps
    null, -- unlimited
    59.99,
    'USD',
    'monthly',
    '{"support": "phone", "static_ip": true, "priority": "high"}'
),
(
    '550e8400-e29b-41d4-a716-446655440012',
    '550e8400-e29b-41d4-a716-446655440001',
    'Enterprise Plan',
    'Ultra-fast internet for businesses with high demands',
    500, -- 500 Mbps
    null, -- unlimited
    199.99,
    'USD',
    'monthly',
    '{"support": "24/7", "static_ip": true, "priority": "enterprise", "dedicated_line": true}'
);

-- Insert demo users
INSERT INTO users (id, branch_id, username, email, password_hash, full_name, phone, address, subscription_plan, bandwidth_limit, data_limit, ip_address, mac_address)
VALUES 
(
    '550e8400-e29b-41d4-a716-446655440004',
    '550e8400-e29b-41d4-a716-446655440002',
    'johndoe',
    'john.doe@email.com',
    '$2b$12$LQv3c1yqBwEHxkqx8kfPPeOC8ZYP7.c5QnV0L7YXQ5X5X5X5X5X5X', -- password: 'user123'
    'John Doe',
    '+1-555-0500',
    '123 Residential St, Downtown, CA 94002',
    'Basic Plan',
    25,
    500,
    '192.168.1.100',
    '00:11:22:33:44:55'
),
(
    '550e8400-e29b-41d4-a716-446655440005',
    '550e8400-e29b-41d4-a716-446655440002',
    'janesmith',
    'jane.smith@email.com',
    '$2b$12$LQv3c1yqBwEHxkqx8kfPPeOC8ZYP7.c5QnV0L7YXQ5X5X5X5X5X5X', -- password: 'user123'
    'Jane Smith',
    '+1-555-0600',
    '456 Family Ave, Downtown, CA 94002',
    'Premium Plan',
    100,
    null,
    '192.168.1.101',
    '00:11:22:33:44:66'
),
(
    '550e8400-e29b-41d4-a716-446655440006',
    '550e8400-e29b-41d4-a716-446655440003',
    'acmecorp',
    'admin@acmecorp.com',
    '$2b$12$LQv3c1yqBwEHxkqx8kfPPeOC8ZYP7.c5QnV0L7YXQ5X5X5X5X5X5X', -- password: 'user123'
    'ACME Corporation',
    '+1-555-0700',
    '789 Business Park, Suburbia, CA 94003',
    'Enterprise Plan',
    500,
    null,
    '192.168.2.100',
    '00:11:22:33:44:77'
);

-- Insert demo network device
INSERT INTO network_devices (id, branch_id, name, device_type, ip_address, username, radius_secret, settings)
VALUES 
(
    '550e8400-e29b-41d4-a716-446655440020',
    '550e8400-e29b-41d4-a716-446655440002',
    'Main Router',
    'mikrotik',
    '192.168.1.1',
    'admin',
    'radius-secret-key',
    '{"model": "RB4011iGS+", "firmware": "7.6", "snmp_enabled": true}'
);

-- Insert tenant access permissions
INSERT INTO tenant_access (user_id, tenant_id, tenant_type, role, permissions)
VALUES 
-- Founder access
('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440000', 'founder', 'admin', '{"create_isp": true, "manage_system": true, "view_analytics": true}'),

-- ISP access
('550e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'isp', 'admin', '{"create_branch": true, "manage_users": true, "view_analytics": true, "billing": true}'),

-- Branch managers access
('550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440002', 'branch', 'manager', '{"manage_users": true, "view_analytics": true, "support": true}'),
('550e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440003', 'branch', 'manager', '{"manage_users": true, "view_analytics": true, "support": true}'),

-- User access
('550e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440004', 'user', 'customer', '{"view_usage": true, "manage_account": true, "create_tickets": true}'),
('550e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440005', 'user', 'customer', '{"view_usage": true, "manage_account": true, "create_tickets": true}'),
('550e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440006', 'user', 'customer', '{"view_usage": true, "manage_account": true, "create_tickets": true}');

-- Insert some demo bandwidth usage data
INSERT INTO bandwidth_usage (user_id, date, upload_bytes, download_bytes, total_bytes, peak_usage_mbps)
VALUES 
-- John Doe usage for last 7 days
('550e8400-e29b-41d4-a716-446655440004', CURRENT_DATE - INTERVAL '6 days', 1073741824, 5368709120, 6442450944, 18), -- 1GB up, 5GB down
('550e8400-e29b-41d4-a716-446655440004', CURRENT_DATE - INTERVAL '5 days', 1258291200, 6442450944, 7700742144, 22),
('550e8400-e29b-41d4-a716-446655440004', CURRENT_DATE - INTERVAL '4 days', 805306368, 4294967296, 5100273664, 15),
('550e8400-e29b-41d4-a716-446655440004', CURRENT_DATE - INTERVAL '3 days', 1610612736, 8589934592, 10200547328, 24),
('550e8400-e29b-41d4-a716-446655440004', CURRENT_DATE - INTERVAL '2 days', 1342177280, 7516192768, 8858370048, 20),
('550e8400-e29b-41d4-a716-446655440004', CURRENT_DATE - INTERVAL '1 day', 1073741824, 5368709120, 6442450944, 19),
('550e8400-e29b-41d4-a716-446655440004', CURRENT_DATE, 536870912, 3221225472, 3758096384, 16),

-- Jane Smith usage for last 7 days (Premium plan user)
('550e8400-e29b-41d4-a716-446655440005', CURRENT_DATE - INTERVAL '6 days', 2147483648, 17179869184, 19327352832, 85),
('550e8400-e29b-41d4-a716-446655440005', CURRENT_DATE - INTERVAL '5 days', 2684354560, 21474836480, 24159191040, 95),
('550e8400-e29b-41d4-a716-446655440005', CURRENT_DATE - INTERVAL '4 days', 1879048192, 15032385536, 16911433728, 78),
('550e8400-e29b-41d4-a716-446655440005', CURRENT_DATE - INTERVAL '3 days', 3221225472, 25769803776, 28991029248, 99),
('550e8400-e29b-41d4-a716-446655440005', CURRENT_DATE - INTERVAL '2 days', 2415919104, 19327352832, 21743271936, 88),
('550e8400-e29b-41d4-a716-446655440005', CURRENT_DATE - INTERVAL '1 day', 2147483648, 17179869184, 19327352832, 92),
('550e8400-e29b-41d4-a716-446655440005', CURRENT_DATE, 1610612736, 12884901888, 14495514624, 76);

-- Insert demo support ticket
INSERT INTO support_tickets (id, user_id, title, description, category, priority, status)
VALUES (
    '550e8400-e29b-41d4-a716-446655440030',
    '550e8400-e29b-41d4-a716-446655440004',
    'Slow internet speed during evening hours',
    'I am experiencing significantly slower internet speeds between 7 PM and 10 PM. During the day, I get close to my plan speed of 25 Mbps, but in the evening it drops to around 5-8 Mbps. This has been happening for the past week.',
    'technical',
    'medium',
    'open'
);