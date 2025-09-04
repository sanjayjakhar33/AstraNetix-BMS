# 🚀 AstraNetix AI BMS - Complete Deployment Guide for Render

This guide provides step-by-step instructions for deploying the AstraNetix AI Bandwidth Management System on Render cloud platform.

## 📋 Overview

AstraNetix BMS is a comprehensive multi-tenant ISP management system with:
- **Backend**: FastAPI with PostgreSQL and Redis
- **Frontend**: Multiple React portals (Founder, ISP, Branch, User)
- **Services**: 11+ microservices including AI, Payment, CRM, NOC, Reporting

## 🎯 Render Services Required

1. **Web Services** (4 services):
   - Backend API (FastAPI)
   - Founder Portal (React)
   - ISP Portal (React) 
   - Branch Portal (React)
   - User Portal (React)

2. **Databases** (2 services):
   - PostgreSQL Database
   - Redis Cache

## 📋 Prerequisites

### Requirements
- Render account (free tier available)
- GitHub repository access
- Domain name (optional, Render provides subdomains)
- Payment gateway API keys (Stripe, PayPal, Razorpay)
- AI API keys (OpenAI, Google Gemini)

### Cost Estimation (Monthly)
- **Free Tier**: $0 (limited resources, good for testing)
- **Starter Plan**: ~$25-50 (suitable for small deployments)
- **Professional Plan**: ~$100-200 (recommended for production)

## 🚀 Step 1: Prepare Your Repository

### 1.1 Fork/Clone the Repository
```bash
# Fork the repository on GitHub or clone it
git clone https://github.com/sanjayjakhar33/AstraNetix-BMS.git
cd AstraNetix-BMS
```

### 1.2 Create Render Configuration
Create `render.yaml` in the root directory:

```yaml
# render.yaml
services:
  # PostgreSQL Database
  - type: pserv
    name: astranetix-postgres
    env: python
    plan: starter
    databases:
      - name: astranetix_bms
        user: astranetix_user

  # Redis Cache
  - type: redis
    name: astranetix-redis
    plan: starter
    maxmemoryPolicy: allkeys-lru

  # Backend API
  - type: web
    name: astranetix-backend
    env: python
    plan: starter
    buildCommand: "pip install -r backend/requirements.txt"
    startCommand: "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: astranetix-postgres
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: astranetix-redis
          property: connectionString
      - key: DEBUG
        value: "false"
      - key: LOG_LEVEL
        value: "INFO"

  # Founder Portal
  - type: web
    name: astranetix-founder-portal
    env: node
    plan: starter
    buildCommand: "cd frontend/founder-portal && npm install && npm run build"
    staticPublishPath: frontend/founder-portal/build
    envVars:
      - key: REACT_APP_API_URL
        fromService:
          type: web
          name: astranetix-backend
          envVarKey: RENDER_EXTERNAL_URL

  # ISP Portal
  - type: web
    name: astranetix-isp-portal
    env: node
    plan: starter
    buildCommand: "cd frontend/isp-portal && npm install && npm run build"
    staticPublishPath: frontend/isp-portal/build
    envVars:
      - key: REACT_APP_API_URL
        fromService:
          type: web
          name: astranetix-backend
          envVarKey: RENDER_EXTERNAL_URL

  # Branch Portal
  - type: web
    name: astranetix-branch-portal
    env: node
    plan: starter
    buildCommand: "cd frontend/branch-portal && npm install && npm run build"
    staticPublishPath: frontend/branch-portal/build
    envVars:
      - key: REACT_APP_API_URL
        fromService:
          type: web
          name: astranetix-backend
          envVarKey: RENDER_EXTERNAL_URL

  # User Portal
  - type: web
    name: astranetix-user-portal
    env: node
    plan: starter
    buildCommand: "cd frontend/user-portal && npm install && npm run build"
    staticPublishPath: frontend/user-portal/build
    envVars:
      - key: REACT_APP_API_URL
        fromService:
          type: web
          name: astranetix-backend
          envVarKey: RENDER_EXTERNAL_URL
```

## 🚀 Step 2: Deploy Database Services

### 2.1 Create PostgreSQL Database

1. **Log into Render Dashboard**
   - Go to [render.com](https://render.com)
   - Sign in or create account
   - Click "New +" → "PostgreSQL"

2. **Configure Database**
   ```
   Name: astranetix-postgres
   Database: astranetix_bms
   User: astranetix_user
   Region: Choose closest to your users
   Plan: Starter ($7/month) or Free (limited)
   ```

3. **Save Database Credentials**
   ```
   Host: [provided by Render]
   Port: 5432
   Database: astranetix_bms
   Username: astranetix_user
   Password: [auto-generated]
   Connection String: [copy this for backend]
   ```

### 2.2 Create Redis Cache

1. **Create Redis Service**
   - Click "New +" → "Redis"
   
2. **Configure Redis**
   ```
   Name: astranetix-redis
   Plan: Starter ($7/month) or Free (limited)
   Max Memory Policy: allkeys-lru
   ```

3. **Save Redis URL**
   ```
   Redis URL: [copy this for backend]
   ```

## 🚀 Step 3: Deploy Backend API

### 3.1 Create Web Service for Backend

1. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository: `AstraNetix-BMS`

2. **Configure Backend Service**
   ```
   Name: astranetix-backend
   Environment: Python 3
   Region: Same as database
   Branch: main
   Root Directory: . (leave empty)
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2
   Plan: Starter ($7/month)
   ```

### 3.2 Set Environment Variables

Add these environment variables in Render dashboard:

```bash
# Database Configuration
DATABASE_URL=[Your PostgreSQL connection string from Step 2.1]
POSTGRES_DB=astranetix_bms
POSTGRES_USER=astranetix_user
POSTGRES_PASSWORD=[Auto-generated password]

# Redis Configuration
REDIS_URL=[Your Redis connection string from Step 2.2]

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO
JWT_SECRET_KEY=[Generate strong secret: openssl rand -hex 32]
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration (Update with your Render URLs)
CORS_ORIGINS=https://astranetix-founder-portal.onrender.com,https://astranetix-isp-portal.onrender.com,https://astranetix-branch-portal.onrender.com,https://astranetix-user-portal.onrender.com

# AI/ML Configuration (Optional)
OPENAI_API_KEY=your-openai-api-key
GOOGLE_GEMINI_API_KEY=your-google-gemini-api-key

# Payment Gateway Configuration (Optional)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# Domain Configuration
DOMAIN=your-custom-domain.com
SSL_ENABLED=true
CDN_ENABLED=true
```

### 3.3 Deploy Backend

1. Click "Create Web Service"
2. Wait for build and deployment (5-10 minutes)
3. Check logs for any errors
4. Test API endpoint: `https://astranetix-backend.onrender.com/docs`

## 🚀 Step 4: Deploy Frontend Applications

### 4.1 Founder Portal

1. **Create Static Site**
   - Click "New +" → "Static Site"
   - Connect same GitHub repository
   
2. **Configure Founder Portal**
   ```
   Name: astranetix-founder-portal
   Branch: main
   Root Directory: frontend/founder-portal
   Build Command: npm install && npm run build
   Publish Directory: build
   ```

3. **Set Environment Variables**
   ```
   REACT_APP_API_URL=https://astranetix-backend.onrender.com/api
   ```

### 4.2 ISP Portal

1. **Create Static Site**
   - Click "New +" → "Static Site"
   
2. **Configure ISP Portal**
   ```
   Name: astranetix-isp-portal
   Branch: main
   Root Directory: frontend/isp-portal
   Build Command: npm install && npm run build
   Publish Directory: build
   ```

3. **Set Environment Variables**
   ```
   REACT_APP_API_URL=https://astranetix-backend.onrender.com/api
   ```

### 4.3 Branch Portal

1. **Create Static Site**
   ```
   Name: astranetix-branch-portal
   Root Directory: frontend/branch-portal
   Build Command: npm install && npm run build
   Publish Directory: build
   ```

2. **Set Environment Variables**
   ```
   REACT_APP_API_URL=https://astranetix-backend.onrender.com/api
   ```

### 4.4 User Portal

1. **Create Static Site**
   ```
   Name: astranetix-user-portal
   Root Directory: frontend/user-portal
   Build Command: npm install && npm run build
   Publish Directory: build
   ```

2. **Set Environment Variables**
   ```
   REACT_APP_API_URL=https://astranetix-backend.onrender.com/api
   ```

## 🚀 Step 5: Database Setup and Migrations

### 5.1 Access Backend Service Shell

1. Go to backend service in Render dashboard
2. Click "Shell" tab
3. Run database migrations:

```bash
# Install alembic if not already installed
pip install alembic

# Run database migrations
cd /opt/render/project/src/backend
python -m alembic upgrade head

# Create initial admin user (optional)
python scripts/create_admin.py
```

### 5.2 Initialize Database Schema

If migrations don't exist, initialize manually:

```bash
# Connect to PostgreSQL (use connection details from Render)
psql $DATABASE_URL

# Create initial tables (run the SQL from database/migrations)
\i database/migrations/001_initial_schema.sql
\i database/migrations/002_demo_data.sql
```

## 🚀 Step 6: Custom Domain Setup (Optional)

### 6.1 Configure Custom Domain

1. **For Each Service**:
   - Go to service settings
   - Click "Custom Domains"
   - Add your domain/subdomain

2. **DNS Configuration**:
   ```
   # Main API
   api.yourdomain.com → CNAME → astranetix-backend.onrender.com
   
   # Founder Portal
   founder.yourdomain.com → CNAME → astranetix-founder-portal.onrender.com
   
   # ISP Portal
   isp.yourdomain.com → CNAME → astranetix-isp-portal.onrender.com
   
   # Branch Portal
   branch.yourdomain.com → CNAME → astranetix-branch-portal.onrender.com
   
   # User Portal
   portal.yourdomain.com → CNAME → astranetix-user-portal.onrender.com
   ```

3. **Update CORS Origins**:
   Update backend environment variables with new domains.

## 🚀 Step 7: Testing and Verification

### 7.1 Test All Services

1. **Backend API**:
   ```
   https://astranetix-backend.onrender.com/docs
   https://astranetix-backend.onrender.com/health
   ```

2. **Frontend Applications**:
   ```
   https://astranetix-founder-portal.onrender.com
   https://astranetix-isp-portal.onrender.com
   https://astranetix-branch-portal.onrender.com
   https://astranetix-user-portal.onrender.com
   ```

### 7.2 Health Checks

1. **Database Connection**: Check backend logs for database connectivity
2. **Redis Connection**: Verify caching is working
3. **API Endpoints**: Test authentication and basic operations
4. **Frontend-Backend Communication**: Verify API calls work

## 🔧 Step 8: Performance Optimization

### 8.1 Database Optimization

1. **Upgrade Plan**: Consider upgrading to higher tier for production
2. **Connection Pooling**: Already handled by SQLAlchemy
3. **Indexing**: Run optimization queries:

```sql
-- Connect to database and run these
CREATE INDEX CONCURRENTLY idx_bandwidth_usage_created_at ON bandwidth_usage(created_at);
CREATE INDEX CONCURRENTLY idx_audit_logs_tenant_id ON audit_logs(tenant_id);
CREATE INDEX CONCURRENTLY idx_users_isp_branch ON users(is_active, branch_id);
```

### 8.2 Backend Optimization

1. **Scale Workers**: Update start command to use more workers:
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT --workers 4
   ```

2. **Memory Settings**: Upgrade to higher plan if needed

### 8.3 Frontend Optimization

1. **CDN**: Render automatically provides CDN for static sites
2. **Caching**: Configure appropriate cache headers
3. **Compression**: Enabled by default on Render

## 📊 Step 9: Monitoring and Maintenance

### 9.1 Set Up Monitoring

1. **Render Dashboard**: Monitor service health, metrics, and logs
2. **Custom Monitoring**: Consider integrating external monitoring
3. **Alerts**: Set up alerts for service downtime

### 9.2 Backup Strategy

1. **Database Backups**: Render provides automatic backups
2. **Additional Backups**: Consider setting up additional backup jobs
3. **Code Backups**: Ensure Git repository is properly backed up

### 9.3 Regular Maintenance

1. **Dependencies**: Regularly update Python and Node.js dependencies
2. **Security**: Monitor for security updates
3. **Performance**: Regular performance reviews and optimizations

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Build Failures

**Problem**: Frontend build fails
```bash
# Solution: Check package.json and ensure all dependencies are correct
npm install
npm run build
```

**Problem**: Backend dependencies fail
```bash
# Solution: Check requirements.txt and Python version
pip install -r backend/requirements.txt
```

#### 2. Database Connection Issues

**Problem**: Cannot connect to database
```bash
# Check environment variables
echo $DATABASE_URL

# Test connection manually
psql $DATABASE_URL
```

#### 3. CORS Issues

**Problem**: Frontend cannot connect to backend
- Update CORS_ORIGINS environment variable with correct Render URLs
- Ensure protocol (https/http) matches

#### 4. Service Won't Start

**Problem**: Service crashes on startup
1. Check logs in Render dashboard
2. Verify environment variables
3. Test locally with same configuration

#### 5. Memory Issues

**Problem**: Service runs out of memory
- Upgrade to higher plan
- Optimize code for memory usage
- Reduce worker count if necessary

### Getting Help

1. **Render Documentation**: [render.com/docs](https://render.com/docs)
2. **Render Support**: Available through dashboard
3. **Community Forums**: GitHub discussions and Stack Overflow
4. **AstraNetix Support**: Create issues in the GitHub repository

## 🎉 Congratulations!

Your AstraNetix AI BMS is now deployed on Render! You should have:

✅ **Backend API** running with full functionality  
✅ **PostgreSQL Database** with proper schema  
✅ **Redis Cache** for session management  
✅ **4 Frontend Applications** (Founder, ISP, Branch, User portals)  
✅ **SSL Certificates** automatically managed  
✅ **Monitoring and Logging** through Render dashboard  

### Next Steps

1. **Configure Your Business**: Set up ISPs, branches, and users
2. **Payment Integration**: Configure payment gateways
3. **AI Features**: Set up OpenAI and Google Gemini APIs
4. **Custom Branding**: Customize the frontend for your brand
5. **Scale**: Upgrade plans as your business grows

### Support

For deployment issues, create an issue in the GitHub repository with:
- Service logs from Render dashboard
- Environment variable configuration (without sensitive data)
- Detailed error description

Happy managing your ISP business with AstraNetix! 🚀