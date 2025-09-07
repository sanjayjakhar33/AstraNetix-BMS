# 🚀 AstraNetix AI BMS - Serverbyt.in Production Deployment Guide

Complete step-by-step guide to deploy AstraNetix AI Bandwidth Management System on Serverbyt.in hosting platform with your custom domain.

## 📋 Prerequisites

### Serverbyt.in Account Setup
- **Hosting Account**: Active Serverbyt.in hosting account
- **Domain**: Your custom domain pointed to serverbyt.in nameservers
- **Server**: VPS or Dedicated Server with root access
- **DNS**: Configure A records for your subdomains

### System Requirements
- **OS**: Ubuntu 20.04 LTS or higher
- **RAM**: Minimum 8GB, Recommended 16GB+
- **Storage**: Minimum 100GB SSD
- **CPU**: Minimum 4 cores, Recommended 8 cores+
- **Network**: Unlimited bandwidth

### Required Subdomains
Configure these A records in your domain DNS:
```
serverbyt.in          → Your Server IP
api.serverbyt.in      → Your Server IP
app.serverbyt.in      → Your Server IP
isp.serverbyt.in      → Your Server IP
branch.serverbyt.in   → Your Server IP
user.serverbyt.in     → Your Server IP
```

## 🔧 Step 1: Server Setup on Serverbyt.in

### 1.1 Connect to Your Server
```bash
# Connect to your serverbyt.in server
ssh root@your-server-ip

# Update system
apt update && apt upgrade -y

# Install essential packages
apt install -y curl wget git ufw fail2ban nginx

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

## 🐳 Step 2: Install Docker & Docker Compose

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
exit
ssh astranetix@your-server-ip
```

## 📥 Step 3: Clone and Setup Application

```bash
# Clone the repository
git clone https://github.com/sanjayjakhar33/AstraNetix-BMS.git
cd AstraNetix-BMS

# Copy serverbyt.in environment configuration
cp .env.serverbyt .env

# Edit configuration file with your details
nano .env
```

### 3.1 Update Environment Variables

Edit `.env` file and update these critical values:

```bash
# Replace with your secure passwords
POSTGRES_PASSWORD=your_super_secure_db_password
JWT_SECRET_KEY=your_generated_jwt_secret_32_chars

# Update with your API keys (optional)
OPENAI_API_KEY=your-openai-api-key
GOOGLE_GEMINI_API_KEY=your-google-gemini-api-key

# Payment gateways (optional)
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
RAZORPAY_KEY_ID=your-razorpay-key-id
```

**Generate JWT Secret:**
```bash
openssl rand -hex 32
```

## 🔐 Step 4: SSL Certificate Setup with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Stop nginx temporarily if running
sudo systemctl stop nginx

# Get SSL certificates for all serverbyt.in domains
sudo certbot certonly --standalone \
  -d serverbyt.in \
  -d api.serverbyt.in \
  -d app.serverbyt.in \
  -d isp.serverbyt.in \
  -d branch.serverbyt.in \
  -d user.serverbyt.in \
  --agree-tos \
  --email your-email@serverbyt.in
```

### 4.1 SSL Auto-Renewal Setup

```bash
# Add SSL certificate auto-renewal to crontab
echo "0 12 * * * /usr/bin/certbot renew --quiet && systemctl reload nginx" | sudo crontab -

# Test renewal
sudo certbot renew --dry-run
```

## 🌐 Step 5: Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/astranetix-serverbyt
```

### 5.1 Nginx Configuration File

```nginx
# /etc/nginx/sites-available/astranetix-serverbyt

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name serverbyt.in api.serverbyt.in app.serverbyt.in isp.serverbyt.in branch.serverbyt.in user.serverbyt.in;
    return 301 https://$server_name$request_uri;
}

# API Backend
server {
    listen 443 ssl http2;
    server_name api.serverbyt.in;

    ssl_certificate /etc/letsencrypt/live/serverbyt.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/serverbyt.in/privkey.pem;
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

# Main Portal (Founder)
server {
    listen 443 ssl http2;
    server_name serverbyt.in app.serverbyt.in;

    ssl_certificate /etc/letsencrypt/live/serverbyt.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/serverbyt.in/privkey.pem;
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
    server_name isp.serverbyt.in;

    ssl_certificate /etc/letsencrypt/live/serverbyt.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/serverbyt.in/privkey.pem;
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

# Branch Portal
server {
    listen 443 ssl http2;
    server_name branch.serverbyt.in;

    ssl_certificate /etc/letsencrypt/live/serverbyt.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/serverbyt.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# User Portal
server {
    listen 443 ssl http2;
    server_name user.serverbyt.in;

    ssl_certificate /etc/letsencrypt/live/serverbyt.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/serverbyt.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://localhost:3003;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5.2 Enable Nginx Configuration

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/astranetix-serverbyt /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl start nginx
sudo systemctl enable nginx
```

## 🚀 Step 6: Deploy Application

```bash
# Create production directories
mkdir -p backups/postgres backups/redis scripts

# Build and start services
docker-compose -f docker-compose.serverbyt.yml up -d --build

# Check service status
docker-compose -f docker-compose.serverbyt.yml ps
```

## 🔄 Step 7: Database Setup & Migration

```bash
# Wait for database to be ready
sleep 30

# Run database migrations
docker-compose -f docker-compose.serverbyt.yml exec backend python -m alembic upgrade head

# Create initial admin user
docker-compose -f docker-compose.serverbyt.yml exec backend python scripts/create_admin.py
```

## 📊 Step 8: Setup Monitoring & Backups

### 8.1 Create Backup Script

```bash
# Create backup script
nano scripts/backup.sh
```

```bash
#!/bin/bash
# scripts/backup.sh

set -e

BACKUP_DIR="/home/astranetix/AstraNetix-BMS/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Database backup
echo "Starting database backup..."
docker-compose -f docker-compose.serverbyt.yml exec -T postgres pg_dump -U $POSTGRES_USER -d $POSTGRES_DB > $BACKUP_DIR/postgres/backup_$DATE.sql

# Redis backup
echo "Starting Redis backup..."
docker-compose -f docker-compose.serverbyt.yml exec -T redis redis-cli --rdb $BACKUP_DIR/redis/dump_$DATE.rdb

# Cleanup old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.rdb" -mtime +30 -delete

echo "Backup completed successfully!"
```

```bash
# Make script executable
chmod +x scripts/backup.sh

# Setup daily backup cron job
echo "0 2 * * * /home/astranetix/AstraNetix-BMS/scripts/backup.sh" | crontab -
```

### 8.2 Setup SSL Auto-Renewal

```bash
# Add SSL renewal to crontab
echo "0 12 * * * /usr/bin/certbot renew --quiet && systemctl reload nginx" | sudo crontab -
```

## 🔐 Step 9: Security Hardening

```bash
# Configure fail2ban
sudo nano /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true

[nginx-http-auth]
enabled = true

[nginx-limit-req]
enabled = true
```

```bash
# Start fail2ban
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

## 🚀 Step 10: Final Testing & Go Live

### 10.1 Test All Services

```bash
# Check all services are running
docker-compose -f docker-compose.serverbyt.yml ps

# Test API endpoint
curl -k https://api.serverbyt.in/health

# Check logs
docker-compose -f docker-compose.serverbyt.yml logs --tail=50
```

### 10.2 Access Your Applications

- **Main Portal**: https://serverbyt.in
- **API Documentation**: https://api.serverbyt.in/docs
- **ISP Portal**: https://isp.serverbyt.in
- **Branch Portal**: https://branch.serverbyt.in
- **User Portal**: https://user.serverbyt.in

## 🎯 Quick Deployment Commands

For future deployments:

```bash
# Navigate to project directory
cd /home/astranetix/AstraNetix-BMS

# Pull latest changes
git pull origin main

# Rebuild and restart services
docker-compose -f docker-compose.serverbyt.yml down
docker-compose -f docker-compose.serverbyt.yml up -d --build

# Run migrations if needed
docker-compose -f docker-compose.serverbyt.yml exec backend python -m alembic upgrade head
```

## 🆘 Troubleshooting

### Common Issues:

1. **SSL Certificate Issues**
   ```bash
   sudo certbot renew --dry-run
   sudo systemctl reload nginx
   ```

2. **Database Connection Issues**
   ```bash
   docker-compose -f docker-compose.serverbyt.yml logs postgres
   docker-compose -f docker-compose.serverbyt.yml restart postgres
   ```

3. **Service Not Starting**
   ```bash
   docker-compose -f docker-compose.serverbyt.yml logs [service-name]
   docker system prune -f
   ```

## 📞 Support

For technical support:
- **GitHub Issues**: https://github.com/sanjayjakhar33/AstraNetix-BMS/issues
- **Documentation**: Check the DEPLOYMENT_GUIDE.md for additional details

## 🎉 Congratulations!

Your AstraNetix AI Bandwidth Management System is now successfully deployed on Serverbyt.in hosting platform with your custom domain! 🚀