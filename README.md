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
- `POST /api/isp/{isp_id}/subscribers` - Create subscriber
- `GET /api/isp/{isp_id}/subscribers` - List subscribers
- `GET /api/isp/{isp_id}/bandwidth/optimize` - AI optimization
- `GET /api/isp/{isp_id}/analytics/subscribers` - Subscriber analytics

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

### Production Deployment on Serverbyt.in

1. **Server Setup**
   - Unlimited SSD storage for multi-tenant data
   - Unlimited bandwidth for global ISP traffic
   - SSL certificates for multi-domain security
   - CDN integration for global performance

2. **Environment Configuration**
   ```bash
   # Production environment variables
   DEBUG=false
   DATABASE_URL=postgresql://user:pass@prod-db:5432/astranetix_bms
   REDIS_URL=redis://prod-redis:6379/0
   DOMAIN=astranetix.com
   SSL_ENABLED=true
   CDN_ENABLED=true
   ```

3. **CI/CD Pipeline**
   - Automated testing and deployment
   - Docker container orchestration
   - Database migrations and backups
   - Performance monitoring and alerting

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
