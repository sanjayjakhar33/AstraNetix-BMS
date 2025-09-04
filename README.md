# AstraNetix AI Bandwidth Management System

A comprehensive AI-powered SaaS platform for ISP bandwidth management that surpasses PHPRadius through advanced automation, multi-tenant architecture, global payment integration, and superior user experience.

## 🚀 Features

### Multi-Tenant Architecture
- **Founder Portal**: System-wide management and ISP creation
- **ISP Portals**: White-labeled dashboards with custom branding
- **Branch Management**: Hierarchical sub-branch organization
- **User Self-Service**: Customer portals with real-time monitoring

### AI-Powered Intelligence
- Real-time bandwidth optimization using machine learning
- Predictive analytics for capacity planning and revenue forecasting
- Automated threat detection and network security monitoring
- Intelligent billing and payment processing automation
- Churn prediction and customer satisfaction optimization
- **AI-Based Audit System**: Intelligent audit analysis with anomaly detection and risk scoring

### NOC (Network Operations Center) Dashboard 📊
- Centralized view for network engineers with real-time topology maps
- Alert correlation and incident management with automated escalation
- SLA compliance monitoring with visual timelines and breach detection
- Network health scoring and performance metrics tracking

### Support & Ticketing Portal 🎫
- Integrated helpdesk with ticket creation in UI and email
- AI chatbot for first-level support and knowledgebase suggestions
- SLA-driven ticket priorities and automated reminders
- Escalation chains and KPI dashboards for support teams
- Customer satisfaction surveys and comprehensive reporting

### CRM & Marketing Automation 🤝
- Advanced subscriber segmentation by usage, location, and plan
- Automated email/SMS campaigns with AI-powered optimization
- Referral and loyalty program management with tracking
- Upsell/cross-sell recommendations via AI insights
- Integration ready for Mailchimp, HubSpot, and Twilio

### Advanced Reporting & Exports 📑
- Custom report builder with drag-and-drop field selection
- Scheduled report generation and delivery (CSV, PDF, XLSX)
- API endpoints for third-party BI tools (Tableau, Power BI)
- Compliance reports (GDPR, PCI, ISO) with automated checking
- Usage trend forecasting with AI-powered projections

### Multi-Language & Multi-Currency Support 🌐
- Localized UI support (English, Spanish, French, Arabic, Hindi)
- Dynamic date/time formatting per locale
- Multi-currency displays and billing with real-time conversion
- Local tax calculation rules and automated integration

### Backup & Disaster Recovery 🚨
- Automated nightly backups (database, configs, logs)
- Geo-distributed snapshots with configurable retention policies
- One-click restore to any point in time
- Disaster-recovery drills and automated failover systems

### Log Management & SIEM Integration 🔍
- Centralized log aggregation (syslog, SNMP traps, API logs)
- Real-time security event monitoring and alerting
- Integration ready for SIEMs (Splunk, ELK, QRadar)
- Threat intelligence feeds and automated blocking capabilities

### Training & Certification Portal 🎓
- Self-paced training modules for ISP staff development
- Virtual labs with sandbox network environments
- Certification exams and digital badges system
- Partner-branded learning portal with progress tracking

### Mobile App Templates 📱
- White-label iOS/Android app configuration
- Customer features: usage monitoring, bill payment, support tickets
- Push notifications for outages, promotions, and alerts
- In-app AI assistant for customer support

### REST API & Webhook Marketplace 🔌
- Comprehensive RESTful API for all platform features
- Real-time webhooks for event notifications
- Developer portal with API documentation and SDKs
- Plugin marketplace for community-built extensions

### SLA & Contract Management 📜
- Template-driven SLA documents linked to customer accounts
- Automated SLA breach detection and real-time reporting
- Penalty calculations and automated credit issuance workflows
- Compliance tracking and customer notifications

### Green Network & CSR Dashboard 🌱
- Energy consumption tracking per device and data center
- Carbon footprint calculation and offset purchase integration
- Sustainability scorecards for ISPs to share with customers
- Renewable energy tracking and efficiency optimization

### Payment & Billing
- Global payment gateway support (Stripe, PayPal, Razorpay, Crypto)
- Multi-currency support (140+ currencies)
- Automated invoice generation with usage-based billing
- AI-powered fraud detection and risk assessment
- Subscription plan management and upgrades

### Network Integration
- RADIUS/AAA authentication system integration
- Mikrotik and Cisco hardware support
- SNMP monitoring and device management
- Real-time network health monitoring
- Automated provisioning and configuration

## 🏗️ Technology Stack

**Backend**: Python FastAPI (microservices architecture)
- PostgreSQL with multi-tenant schema design
- Redis for session management and real-time data
- JWT-based authentication with role-based access control

**Frontend**: React + TypeScript + Material-UI
- Responsive, mobile-first design
- White-label branding support
- Real-time dashboards and analytics

**AI/ML**: Integration with OpenAI GPT-4, Google Gemini
- Scikit-learn for predictive analytics
- Pandas and NumPy for data processing

**Infrastructure**: Docker containers, automated CI/CD
- PostgreSQL, Redis, and microservices orchestration
- Scalable deployment with unlimited SSD and bandwidth

## 📋 System Requirements

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/sanjayjakhar33/AstraNetix-BMS.git
cd AstraNetix-BMS
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Database Setup
```bash
# Initialize PostgreSQL database
docker-compose up postgres -d

# Run migrations
docker-compose exec postgres psql -U astranetix_user -d astranetix_bms -f /docker-entrypoint-initdb.d/001_initial_schema.sql

# Seed demo data
docker-compose exec postgres psql -U astranetix_user -d astranetix_bms -f /docker-entrypoint-initdb.d/001_demo_data.sql
```

### 4. Start All Services
```bash
# Start all services
docker-compose up --build

# Or start individually
docker-compose up postgres redis backend -d
```

### 5. Access Applications

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Founder Portal**: http://localhost:3000
- **ISP Portal**: http://localhost:3001
- **Branch Portal**: http://localhost:3002
- **User Portal**: http://localhost:3003

## 🔧 Development Setup

### Backend Development
```bash
cd backend
pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend/founder-portal
npm install
npm start
```

## 📊 Core Hierarchy

```
Founder Portal (CEO/System Owner)
  ↓ Creates & Manages
ISP Portals (Auto-generated URLs with white-label branding)
  ↓ Creates & Manages  
Sub-Branch Management (Hierarchical ISP branches)
  ↓ Serves
End User Management (Self-service portals)
```

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/login` - User authentication
- `POST /api/auth/register/founder` - Founder registration
- `GET /api/auth/me` - Current user info

### Founder Portal
- `GET /api/founder/dashboard` - System overview
- `POST /api/founder/isp/create` - Create ISP portal
- `GET /api/founder/isp/list` - List all ISPs
- `GET /api/founder/revenue/analytics` - Revenue analytics
- `GET /api/founder/system/monitoring` - System monitoring

### ISP Portal
- `GET /api/isp/{isp_id}/dashboard` - ISP dashboard
- `GET /api/isp/{isp_id}/enhanced-dashboard` - Enhanced dashboard with all new features
- `POST /api/isp/{isp_id}/subscribers` - Create subscriber
- `GET /api/isp/{isp_id}/subscribers` - List subscribers
- `GET /api/isp/{isp_id}/bandwidth/optimize` - AI optimization
- `GET /api/isp/{isp_id}/analytics/subscribers` - Subscriber analytics
- `POST /api/isp/{isp_id}/localization` - Configure multi-language support
- `POST /api/isp/{isp_id}/mobile-app` - Configure mobile app templates
- `GET /api/isp/{isp_id}/training-modules` - Training modules for staff
- `POST /api/isp/{isp_id}/webhooks` - Create webhook endpoints

### NOC Dashboard
- `GET /api/noc/{tenant_id}/dashboard` - NOC dashboard with real-time metrics
- `POST /api/noc/{tenant_id}/alerts` - Create network alerts
- `GET /api/noc/{tenant_id}/ai-audit` - AI-based audit analysis
- `GET /api/noc/{isp_id}/sla` - SLA definitions and compliance
- `POST /api/noc/{isp_id}/sla` - Create SLA definitions

### CRM & Marketing
- `GET /api/crm/{isp_id}/analytics` - Customer analytics and insights
- `POST /api/crm/{isp_id}/segments` - Create customer segments
- `GET /api/crm/{isp_id}/segments` - List customer segments
- `POST /api/crm/{isp_id}/campaigns` - Create marketing campaigns
- `GET /api/crm/{isp_id}/campaigns` - List marketing campaigns
- `GET /api/crm/{isp_id}/campaigns/{campaign_id}/metrics` - Campaign metrics

### Advanced Reporting
- `GET /api/reporting/{isp_id}/templates` - Report templates
- `POST /api/reporting/{isp_id}/templates` - Create custom report templates
- `POST /api/reporting/{isp_id}/generate` - Generate reports (PDF, CSV, XLSX)
- `POST /api/reporting/{isp_id}/custom-report` - Custom report builder
- `GET /api/reporting/{isp_id}/compliance/{report_type}` - Compliance reports
- `GET /api/reporting/{isp_id}/bi-endpoints` - BI integration endpoints

### Support & Ticketing
- `POST /api/support/{tenant_id}/tickets` - Create support tickets with SLA tracking
- `GET /api/support/{tenant_id}/tickets` - List support tickets with filtering
- `POST /api/support/{tenant_id}/chatbot` - AI chatbot for first-level support
- `GET /api/support/{tenant_id}/analytics` - Support analytics and KPI dashboard
- `GET /api/support/{tenant_id}/knowledge-base` - Knowledge base articles

### Advanced Reporting
- `GET /api/reporting/{isp_id}/templates` - Report templates
- `POST /api/reporting/{isp_id}/templates` - Create custom report templates
- `POST /api/reporting/{isp_id}/generate` - Generate reports (PDF, CSV, XLSX)
- `POST /api/reporting/{isp_id}/custom-report` - Custom report builder
- `GET /api/reporting/{isp_id}/compliance/{report_type}` - Compliance reports
- `GET /api/reporting/{isp_id}/bi-endpoints` - BI integration endpoints

### Green Network & CSR
- `GET /api/sustainability/{tenant_id}/dashboard` - Sustainability dashboard
- `POST /api/sustainability/{tenant_id}/metrics` - Create sustainability metrics
- `GET /api/sustainability/{tenant_id}/metrics` - Get sustainability metrics
- `POST /api/sustainability/{tenant_id}/carbon-offset` - Purchase carbon offsets
- `GET /api/sustainability/{tenant_id}/report` - Sustainability reports

### AI Manager
- `POST /api/ai/analyze/traffic` - Traffic pattern analysis
- `POST /api/ai/optimize/qos` - QoS optimization
- `GET /api/ai/predict/network/{tenant_id}` - Network predictions
- `GET /api/ai/detect/anomalies/{tenant_id}` - Anomaly detection

### Payment Engine
- `POST /api/payment/process` - Process payments
- `POST /api/payment/invoice/generate` - Generate invoices
- `GET /api/payment/analytics/{tenant_id}` - Billing analytics
- `GET /api/payment/methods` - Available payment methods

### User Portal
- `GET /api/user/{user_id}/dashboard` - User dashboard
- `GET /api/user/{user_id}/usage/realtime` - Usage monitoring
- `GET /api/user/{user_id}/payments` - Payment history
- `POST /api/user/{user_id}/support/ticket` - Create support ticket

### Branch Management
- `POST /api/branch/{isp_id}/create` - Create branch
- `GET /api/branch/{branch_id}/dashboard` - Branch dashboard
- `GET /api/branch/{branch_id}/users` - List branch users
- `GET /api/branch/{branch_id}/analytics/ai` - Branch analytics

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Run Frontend Tests
```bash
cd frontend/founder-portal
npm test
```

## 📈 Database Schema

The system uses a multi-tenant PostgreSQL schema with the following key tables:

- **founders**: System owners and administrators
- **isps**: Internet Service Providers
- **branches**: ISP branch locations
- **users**: End customers
- **subscription_plans**: Service plans and pricing
- **bandwidth_usage**: Usage tracking and analytics
- **payments**: Payment transactions and history
- **support_tickets**: Customer support system
- **network_devices**: Hardware management
- **ai_insights**: AI analytics and recommendations

## 🛡️ Security Features

- JWT-based authentication with role-based access control
- Multi-factor authentication support
- PCI DSS compliant payment processing
- Data encryption at rest and in transit
- Comprehensive audit logging
- GDPR compliance with data retention policies

## 🌐 Deployment

### 🚀 Deploy to Render (Recommended)

**Quick 5-minute deployment to Render cloud:**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/sanjayjakhar33/AstraNetix-BMS)

```bash
# Quick setup
./scripts/setup-render.sh

# Follow the complete guide
open RENDER_DEPLOYMENT_GUIDE.md
```

**Features:**
- ✅ **One-click deployment** with render.yaml
- ✅ **Auto-scaling** backend and frontends  
- ✅ **Managed databases** (PostgreSQL + Redis)
- ✅ **SSL certificates** automatically managed
- ✅ **Global CDN** for frontend assets
- ✅ **Cost-effective** starting at $25/month

📚 **[Complete Render Guide →](RENDER_DEPLOYMENT_GUIDE.md)**

### 🏢 Production Deployment on Serverbyt.in

**Deploy to your own Serverbyt.in hosting server:**

```bash
# Quick deployment script
./scripts/deploy-serverbyt.sh

# Follow the complete guide
open SERVERBYT_DEPLOYMENT_GUIDE.md
```

**Features:**
- ✅ **Custom domain support** (serverbyt.in)
- ✅ **Full server control** with root access
- ✅ **Multi-subdomain setup** (api.serverbyt.in, isp.serverbyt.in, etc.)
- ✅ **SSL certificates** with Let's Encrypt
- ✅ **Docker containerization** for easy management
- ✅ **Automated backups** and monitoring
- ✅ **Cost-effective** dedicated hosting

📚 **[Complete Serverbyt.in Guide →](SERVERBYT_DEPLOYMENT_GUIDE.md)**

**Quick Access URLs:**
- **Main Portal**: https://serverbyt.in
- **API Docs**: https://api.serverbyt.in/docs
- **ISP Portal**: https://isp.serverbyt.in
- **Branch Portal**: https://branch.serverbyt.in
- **User Portal**: https://user.serverbyt.in

## 📝 Demo Data

The system includes comprehensive demo data:

- **Demo Founder**: founder@astranetix.com (admin123)
- **Demo ISP**: admin@demo-isp.com (admin123)
- **Demo Users**: john.doe@email.com, jane.smith@email.com (user123)

## 🤖 AI Features

### Bandwidth Optimization
- Real-time traffic pattern analysis
- Dynamic bandwidth allocation
- Congestion prediction and prevention
- QoS optimization recommendations

### Predictive Analytics
- Revenue forecasting with ML models
- Customer churn prediction
- Network capacity planning
- Usage trend analysis

### Fraud Detection
- AI-powered payment fraud detection
- Anomaly detection in network usage
- Suspicious activity monitoring
- Risk scoring and alerts

## 🔮 Roadmap

- [ ] Advanced ML models for traffic prediction
- [ ] Mobile applications for iOS and Android
- [ ] Advanced network hardware integrations
- [ ] Blockchain-based billing and payments
- [ ] IoT device management and monitoring
- [ ] Advanced security and threat detection
- [ ] Multi-language support and localization
- [ ] Enterprise SSO integration

## 📞 Support

For technical support and inquiries:
- Documentation: Available at `/docs` endpoint
- Issues: GitHub Issues
- Email: support@astranetix.com

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**AstraNetix BMS** - Revolutionizing ISP bandwidth management with AI-powered intelligence and superior user experience.
