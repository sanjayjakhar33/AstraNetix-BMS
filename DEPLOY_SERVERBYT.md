# 🎯 AstraNetix BMS - Serverbyt.in Deployment Instructions

## 🚀 Quick Start Guide

Your AstraNetix AI Bandwidth Management System is now ready for deployment on **serverbyt.in** hosting platform!

### ⚡ 3-Step Deployment Process

#### Step 1: Setup Your Server
```bash
# Connect to your serverbyt.in server
ssh root@your-server-ip

# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

# Create user and setup project
adduser astranetix && usermod -aG docker,sudo astranetix
su - astranetix
git clone https://github.com/sanjayjakhar33/AstraNetix-BMS.git
cd AstraNetix-BMS
```

#### Step 2: Configure Environment
```bash
# Run the setup wizard
./scripts/setup-serverbyt.sh

# This will:
# - Create .env configuration file
# - Generate secure passwords
# - Set up domain configuration
```

#### Step 3: Deploy Application
```bash
# Deploy with one command
./scripts/deploy-serverbyt.sh

# This will:
# - Install all dependencies
# - Build and start all services
# - Run database migrations
# - Setup monitoring
```

### 🌐 Configure DNS Records

Before deployment, configure these DNS A records:
```
serverbyt.in         → Your Server IP
api.serverbyt.in     → Your Server IP
isp.serverbyt.in     → Your Server IP
branch.serverbyt.in  → Your Server IP
user.serverbyt.in    → Your Server IP
```

### 🔒 Setup SSL Certificates
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificates
sudo certbot certonly --standalone \
  -d serverbyt.in \
  -d api.serverbyt.in \
  -d isp.serverbyt.in \
  -d branch.serverbyt.in \
  -d user.serverbyt.in
```

### 🌐 Configure Nginx
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/astranetix-serverbyt

# Copy the configuration from SERVERBYT_DEPLOYMENT_GUIDE.md
# Then enable it:
sudo ln -s /etc/nginx/sites-available/astranetix-serverbyt /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

## 📱 Access Your Application

After successful deployment:

- **🏠 Main Portal**: https://serverbyt.in
- **🔗 API Documentation**: https://api.serverbyt.in/docs
- **🏢 ISP Management**: https://isp.serverbyt.in
- **🏪 Branch Portal**: https://branch.serverbyt.in
- **👤 User Portal**: https://user.serverbyt.in

## 🔧 Management Commands

### Check Application Status
```bash
docker compose -f docker-compose.serverbyt.yml ps
```

### View Logs
```bash
docker compose -f docker-compose.serverbyt.yml logs -f
```

### Restart Services
```bash
docker compose -f docker-compose.serverbyt.yml restart
```

### Update Application
```bash
git pull origin main
docker compose -f docker-compose.serverbyt.yml down
docker compose -f docker-compose.serverbyt.yml up -d --build
```

### Backup Data
```bash
./scripts/backup.sh
```

## 📚 Documentation Files

- **Complete Guide**: `SERVERBYT_DEPLOYMENT_GUIDE.md`
- **Quick Summary**: `SERVERBYT_SUMMARY.md`
- **Environment Template**: `.env.serverbyt`
- **Docker Configuration**: `docker-compose.serverbyt.yml`

## 🆘 Troubleshooting

### Common Issues

1. **Services not starting**
   ```bash
   docker compose -f docker-compose.serverbyt.yml logs
   ```

2. **Database connection errors**
   ```bash
   docker compose -f docker-compose.serverbyt.yml restart postgres
   ```

3. **SSL certificate issues**
   ```bash
   sudo certbot renew --dry-run
   ```

### Support
- GitHub Issues: https://github.com/sanjayjakhar33/AstraNetix-BMS/issues
- Check logs for detailed error messages
- Verify DNS configuration
- Ensure all environment variables are set

## 🎉 Success!

Once deployed, you'll have a fully functional multi-tenant ISP bandwidth management system running on your serverbyt.in hosting platform!

---

**Need help?** Check `SERVERBYT_DEPLOYMENT_GUIDE.md` for detailed instructions.