# 🚀 AstraNetix AI BMS - Complete Deployment Guide for Serverbyt.in

This guide provides step-by-step instructions for deploying the AstraNetix AI Bandwidth Management System on Serverbyt.in hosting platform.

## 📋 Prerequisites

### System Requirements
- **Server**: VPS or Dedicated Server on Serverbyt.in
- **OS**: Ubuntu 20.04 LTS or higher
- **RAM**: Minimum 8GB, Recommended 16GB+
- **Storage**: Minimum 100GB SSD
- **CPU**: Minimum 4 cores, Recommended 8 cores+
- **Network**: Unlimited bandwidth (essential for ISP management)

### Software Requirements
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Redis 6+
- Nginx
- Docker & Docker Compose
- SSL Certificate (Let's Encrypt)

## 🔧 Step 1: Server Setup on Serverbyt.in

### 1.1 Purchase and Configure Server
```bash
# Log into Serverbyt.in dashboard
# Choose VPS or Dedicated Server plan
# Select Ubuntu 20.04 LTS
# Configure DNS to point to your server IP
```

### 1.2 Initial Server Setup
```bash
# Connect to your server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install essential packages
apt install -y curl wget git ufw fail2ban

# Configure firewall
ufw allow OpenSSH
ufw allow 80
ufw allow 443
ufw enable

# Create deployment user
adduser astranetix
usermod -aG sudo astranetix
su - astranetix
```

## 🐳 Step 2: Docker Installation

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again for group changes to take effect
exit
ssh astranetix@your-server-ip
```

## 📥 Step 3: Clone and Setup Application

```bash
# Clone the repository
git clone https://github.com/sanjayjakhar33/AstraNetix-BMS.git
cd AstraNetix-BMS

# Create production environment file
cp .env.example .env.production

# Edit environment variables
nano .env.production
```

### 3.1 Production Environment Configuration

```bash
# .env.production
# Database Configuration
POSTGRES_DB=astranetix_bms_prod
POSTGRES_USER=astranetix_prod
POSTGRES_PASSWORD=your_ultra_secure_password_here

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO
JWT_SECRET_KEY=your_super_secure_jwt_secret_key_change_this

# Domain Configuration
DOMAIN=your-domain.com
SSL_ENABLED=true
CDN_ENABLED=true

# Database URLs
DATABASE_URL=postgresql://astranetix_prod:your_ultra_secure_password_here@postgres:5432/astranetix_bms_prod
REDIS_URL=redis://redis:6379/0

# Payment Gateway Configuration (Production Keys)
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
PAYPAL_CLIENT_ID=your_paypal_production_client_id
PAYPAL_CLIENT_SECRET=your_paypal_production_secret
RAZORPAY_KEY_ID=rzp_live_your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

# AI/ML Configuration
OPENAI_API_KEY=your_openai_api_key
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key

# CORS Origins (Add your domain)
CORS_ORIGINS=https://your-domain.com,https://app.your-domain.com,https://isp.your-domain.com

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@domain.com
SMTP_PASSWORD=your-app-password

# Backup Configuration
BACKUP_ENABLED=true
BACKUP_RETENTION_DAYS=30
BACKUP_ENCRYPTION_KEY=your_backup_encryption_key
```

## 🔧 Step 4: SSL Certificate Setup

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Generate SSL certificate
sudo certbot certonly --standalone -d your-domain.com -d app.your-domain.com -d isp.your-domain.com -d api.your-domain.com

# Setup auto-renewal
sudo crontab -e
# Add this line:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

## 🌐 Step 5: Nginx Configuration

```bash
# Install Nginx
sudo apt install nginx -y

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/astranetix
```

### 5.1 Nginx Configuration File

```nginx
# /etc/nginx/sites-available/astranetix
server {
    listen 80;
    server_name your-domain.com app.your-domain.com isp.your-domain.com api.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# API Backend
server {
    listen 443 ssl http2;
    server_name api.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}

# Founder Portal
server {
    listen 443 ssl http2;
    server_name your-domain.com app.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# ISP Portal
server {
    listen 443 ssl http2;
    server_name isp.your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/astranetix /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🚀 Step 6: Deploy Application

### 6.1 Create Production Docker Compose

```bash
# Create production docker-compose file
nano docker-compose.prod.yml
```

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/migrations:/docker-entrypoint-initdb.d
      - ./backups/postgres:/backups
    ports:
      - "127.0.0.1:5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 30s
      timeout: 10s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
      - ./backups/redis:/backups
    ports:
      - "127.0.0.1:6379:6379"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: ../docker/Dockerfile.backend.prod
    ports:
      - "127.0.0.1:8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - DEBUG=false
      - JWT_SECRET_KEY=${JWT_SECRET_KEY}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
      - PAYPAL_CLIENT_ID=${PAYPAL_CLIENT_ID}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
      - ./uploads:/app/uploads
      - ./reports:/app/reports
    restart: unless-stopped

  founder-portal:
    build:
      context: ./frontend/founder-portal
      dockerfile: ../../docker/Dockerfile.frontend.prod
    ports:
      - "127.0.0.1:3000:80"
    environment:
      - REACT_APP_API_URL=https://api.your-domain.com/api
    restart: unless-stopped

  isp-portal:
    build:
      context: ./frontend/isp-portal
      dockerfile: ../../docker/Dockerfile.frontend.prod
    ports:
      - "127.0.0.1:3001:80"
    environment:
      - REACT_APP_API_URL=https://api.your-domain.com/api
    restart: unless-stopped

  # Backup Service
  backup:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - ./backups:/backups
      - ./scripts/backup.sh:/backup.sh
    entrypoint: ["/backup.sh"]
    depends_on:
      - postgres
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  default:
    name: astranetix_production
```

### 6.2 Create Production Dockerfiles

```bash
# Create production backend Dockerfile
mkdir -p docker
nano docker/Dockerfile.backend.prod
```

```dockerfile
# docker/Dockerfile.backend.prod
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 astranetix && chown -R astranetix:astranetix /app
USER astranetix

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

```bash
# Create production frontend Dockerfile
nano docker/Dockerfile.frontend.prod
```

```dockerfile
# docker/Dockerfile.frontend.prod
# Build stage
FROM node:18-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 6.3 Deploy the Application

```bash
# Build and start the application
docker-compose -f docker-compose.prod.yml up -d --build

# Check if services are running
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔄 Step 7: Database Migration and Setup

```bash
# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend python -m alembic upgrade head

# Create initial admin user
docker-compose -f docker-compose.prod.yml exec backend python scripts/create_admin.py
```

## 📊 Step 8: Monitoring and Backup Setup

### 8.1 Setup Automated Backups

```bash
# Create backup script
mkdir -p scripts backups/postgres backups/redis
nano scripts/backup.sh
```

```bash
#!/bin/bash
# scripts/backup.sh

set -e

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
echo "Starting database backup..."
pg_dump -h postgres -U $POSTGRES_USER -d $POSTGRES_DB > $BACKUP_DIR/postgres/backup_$DATE.sql

# Redis backup
echo "Starting Redis backup..."
redis-cli -h redis --rdb $BACKUP_DIR/redis/dump_$DATE.rdb

# Cleanup old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.rdb" -mtime +30 -delete

echo "Backup completed successfully!"
```

```bash
chmod +x scripts/backup.sh

# Setup cron job for automated backups
crontab -e
# Add this line for daily backups at 2 AM:
# 0 2 * * * cd /home/astranetix/AstraNetix-BMS && docker-compose -f docker-compose.prod.yml run --rm backup
```

### 8.2 Setup Monitoring

```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Create monitoring script
nano scripts/monitor.sh
```

```bash
#!/bin/bash
# scripts/monitor.sh

echo "=== System Resource Usage ==="
free -h
echo ""
df -h
echo ""
echo "=== Docker Container Status ==="
docker-compose -f docker-compose.prod.yml ps
echo ""
echo "=== Application Health Check ==="
curl -s https://api.your-domain.com/health | jq .
```

## 🔐 Step 9: Security Hardening

### 9.1 Configure Fail2ban

```bash
# Configure fail2ban for additional security
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
action = iptables-multiport[name=ReqLimit, port="http,https", protocol=tcp]
logpath = /var/log/nginx/error.log
maxretry = 10
findtime = 600
bantime = 7200
```

```bash
sudo systemctl restart fail2ban
```

### 9.2 Setup Firewall Rules

```bash
# Additional firewall configuration
sudo ufw deny 5432  # PostgreSQL
sudo ufw deny 6379  # Redis
sudo ufw allow from 127.0.0.1 to any port 5432
sudo ufw allow from 127.0.0.1 to any port 6379
sudo ufw reload
```

## 📈 Step 10: Performance Optimization

### 10.1 Database Optimization

```sql
-- Connect to PostgreSQL and run these optimizations
-- docker-compose -f docker-compose.prod.yml exec postgres psql -U astranetix_prod -d astranetix_bms_prod

-- Create indexes for better performance
CREATE INDEX CONCURRENTLY idx_bandwidth_usage_created_at ON bandwidth_usage(created_at);
CREATE INDEX CONCURRENTLY idx_audit_logs_tenant_id ON audit_logs(tenant_id);
CREATE INDEX CONCURRENTLY idx_users_isp_branch ON users(is_active, branch_id);

-- Optimize PostgreSQL settings
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET work_mem = '4MB';
SELECT pg_reload_conf();
```

### 10.2 Redis Optimization

```bash
# Optimize Redis configuration
docker-compose -f docker-compose.prod.yml exec redis redis-cli CONFIG SET maxmemory 512mb
docker-compose -f docker-compose.prod.yml exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

## 🚀 Step 11: Go Live Checklist

### Pre-Launch Checklist
- [ ] SSL certificates installed and working
- [ ] All environment variables configured for production
- [ ] Database migrations completed
- [ ] Payment gateways tested in production mode
- [ ] Email configuration tested
- [ ] Backup system tested
- [ ] Monitoring setup and alerts configured
- [ ] DNS properly configured
- [ ] Firewall rules applied
- [ ] Load testing completed

### Post-Launch Monitoring
```bash
# Daily health checks
curl -s https://api.your-domain.com/health
curl -s https://your-domain.com
curl -s https://isp.your-domain.com

# Monitor logs
docker-compose -f docker-compose.prod.yml logs --tail=100 -f backend

# Check resource usage
docker stats

# Monitor database performance
docker-compose -f docker-compose.prod.yml exec postgres psql -U astranetix_prod -d astranetix_bms_prod -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"
```

## 🆘 Troubleshooting

### Common Issues and Solutions

1. **502 Bad Gateway**
   ```bash
   # Check if backend is running
   docker-compose -f docker-compose.prod.yml logs backend
   # Restart backend service
   docker-compose -f docker-compose.prod.yml restart backend
   ```

2. **Database Connection Issues**
   ```bash
   # Check PostgreSQL logs
   docker-compose -f docker-compose.prod.yml logs postgres
   # Verify connection
   docker-compose -f docker-compose.prod.yml exec postgres psql -U astranetix_prod -d astranetix_bms_prod -c "SELECT 1;"
   ```

3. **High Memory Usage**
   ```bash
   # Monitor memory usage
   docker stats
   # Restart services if needed
   docker-compose -f docker-compose.prod.yml restart
   ```

## 📞 Support and Maintenance

### Regular Maintenance Tasks

1. **Weekly**
   - Check application logs for errors
   - Monitor resource usage
   - Verify backup integrity

2. **Monthly**
   - Update SSL certificates (automatic with certbot)
   - Review security logs
   - Performance optimization review

3. **Quarterly**
   - Security audit
   - Dependency updates
   - Disaster recovery testing

### Getting Help

- **Documentation**: Check the comprehensive API documentation at `/docs`
- **Logs**: All application logs are stored in `./logs` directory
- **Monitoring**: Use the built-in health endpoints for monitoring
- **Support**: Contact Serverbyt.in support for infrastructure issues

## 🎉 Conclusion

Your AstraNetix AI BMS is now successfully deployed on Serverbyt.in! The platform provides:

- ✅ Scalable multi-tenant architecture
- ✅ AI-powered bandwidth optimization
- ✅ Comprehensive ISP management tools
- ✅ Advanced reporting and analytics
- ✅ Green network monitoring
- ✅ Enterprise-grade security
- ✅ 24/7 monitoring and backups

Your ISP clients can now access their white-labeled portals and enjoy the full power of AI-driven bandwidth management.