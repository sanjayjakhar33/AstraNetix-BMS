# 🆓 AstraNetix BMS - Free Tier Testing Guide

**Quick testing guide for Render's free tier - Perfect for evaluating AstraNetix BMS before committing to paid plans!**

## 🎯 What You'll Get (Free Tier)

✅ **Full System Demo** - All features work, just with limitations  
✅ **1 Backend API** - Core functionality  
✅ **4 Frontend Portals** - All user interfaces  
✅ **PostgreSQL Database** - 1GB storage  
✅ **Redis Cache** - 25MB memory  
✅ **SSL Certificates** - Automatic HTTPS  

⚠️ **Free Tier Limitations**:
- Services sleep after 15 minutes of inactivity (30-60 second wake time)
- Limited resources (512MB RAM, 0.1 CPU per service)
- 750 hours/month total across all services
- Slower performance compared to paid tiers

## ⏱️ Quick Start (15 minutes)

### Step 1: Prepare Your GitHub Repository

1. **Fork the repository**: Go to [AstraNetix-BMS](https://github.com/sanjayjakhar33/AstraNetix-BMS) and click "Fork"
2. **No local setup needed** - We'll deploy directly from GitHub

### Step 2: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)
4. Connect your GitHub account

### Step 3: Deploy with One Click

1. **Use the free tier blueprint**: Click the button below
   
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/AstraNetix-BMS&blueprint=render-free-tier.yaml)

2. **Configure the deployment**:
   - Repository: Select your forked `AstraNetix-BMS`
   - Branch: `main`
   - Blueprint: Will auto-select `render-free-tier.yaml`

3. **Set required environment variables**:
   ```
   JWT_SECRET_KEY: [Click "Generate" - Render will create a secure key]
   ```

4. **Click "Create Services"** - This will create all 6 services automatically

### Step 4: Wait for Deployment (10-15 minutes)

Render will deploy services in this order:
1. ✅ PostgreSQL Database (2-3 min)
2. ✅ Redis Cache (2-3 min)  
3. ✅ Backend API (5-7 min)
4. ✅ Frontend Portals (3-5 min each)

**Monitor progress**: Go to your Render dashboard to watch the deployment

### Step 5: Test Your Deployment

Once all services show "✅ Live", test these URLs:

1. **Backend API Health Check**:
   ```
   https://astranetix-backend-XXXX.onrender.com/health
   ```
   Should return: `{"status": "healthy", "database": "connected"}`

2. **API Documentation**:
   ```
   https://astranetix-backend-XXXX.onrender.com/docs
   ```

3. **Frontend Portals**:
   ```
   Founder Portal: https://astranetix-founder-portal-XXXX.onrender.com
   ISP Portal:     https://astranetix-isp-portal-XXXX.onrender.com
   Branch Portal:  https://astranetix-branch-portal-XXXX.onrender.com
   User Portal:    https://astranetix-user-portal-XXXX.onrender.com
   ```

### Step 6: Create Test Account

1. Open the **Founder Portal**
2. Click "Register" to create a test account
3. Use any email (verification disabled in test mode)
4. Login and explore the dashboard

## 🧪 What to Test

### Core Features (Available on Free Tier)
- ✅ **User Authentication** - Register, login, logout
- ✅ **Dashboard Navigation** - All 4 portals
- ✅ **Database Operations** - CRUD operations work
- ✅ **Real-time Data** - Live updates and stats
- ✅ **API Endpoints** - All REST APIs functional
- ✅ **Responsive Design** - Mobile and desktop views

### Limited Features (Due to Free Tier)
- ⚠️ **AI Features** - Slower response (requires API keys)
- ⚠️ **Payment Processing** - Demo mode only (requires paid gateways)
- ⚠️ **Email Notifications** - Limited (requires SMTP config)
- ⚠️ **File Uploads** - Basic only (limited storage)

### Performance Expectations
- 🐌 **First Load**: 30-60 seconds (services waking up)
- ⚡ **Subsequent Loads**: 1-3 seconds
- 😴 **Auto-sleep**: After 15 minutes of inactivity
- 🔄 **Auto-wake**: 30-60 seconds when accessed

## 🔧 Free Tier Optimization Tips

### Keep Services Awake
```bash
# Set up a simple ping service (optional)
curl https://astranetix-backend-XXXX.onrender.com/health
```

### Monitor Resource Usage
- Check Render dashboard for memory/CPU usage
- Free tier: 512MB RAM, 0.1 CPU per service
- If hitting limits, some features may be slower

### Test During Low Traffic
- Free tier performs best with 1-2 concurrent users
- For load testing, upgrade to Starter plan ($7/month)

## 🚀 When to Upgrade to Paid Plans

Upgrade to **Starter Plan** ($25-50/month) when you need:
- ✅ No service sleeping (always-on)
- ✅ Better performance (1GB RAM, 0.5 CPU)
- ✅ Production-ready stability
- ✅ Custom domain support
- ✅ Priority support

Upgrade to **Professional Plan** ($100-200/month) for:
- ✅ High-traffic support (2GB+ RAM, 1+ CPU)
- ✅ Multiple ISP deployments
- ✅ Advanced monitoring
- ✅ SLA guarantees

## 🛠️ Troubleshooting Free Tier Issues

### Service Not Responding
**Problem**: Service shows "404" or timeout
**Solution**: Wait 60 seconds for auto-wake, then refresh

### Slow Performance
**Problem**: Pages load slowly
**Solution**: This is normal on free tier. Wait for services to warm up

### Build Failures
**Problem**: Deployment failed during build
**Solutions**:
1. Check if you exceeded free tier build minutes
2. Retry deployment (temporary resource issue)
3. Check logs in Render dashboard

### Database Connection Errors
**Problem**: Backend can't connect to database
**Solution**: Database might be sleeping. Wake it by accessing any API endpoint

## 📊 Free Tier Resource Limits

| Resource | Free Tier Limit | Usage Tips |
|----------|-----------------|------------|
| **Build Minutes** | 500/month | Builds typically take 5-10 minutes each |
| **Runtime Hours** | 750/month total | ~125 hours per service if you have 6 services |
| **RAM** | 512MB per service | Sufficient for testing, not for production |
| **Storage** | 1GB PostgreSQL | Good for 10,000+ test records |
| **Bandwidth** | 100GB/month | More than enough for testing |

## 🎉 Next Steps After Testing

### If You Like What You See:
1. **Upgrade to Starter Plan** for better performance
2. **Add your payment gateway credentials** for real transactions
3. **Configure custom domain** for professional URLs
4. **Set up monitoring** for production use
5. **Add AI API keys** for intelligent features

### If You Need Help:
- 📚 **Full Documentation**: [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)
- 🐛 **Issues**: [GitHub Issues](https://github.com/sanjayjakhar33/AstraNetix-BMS/issues)
- 💬 **Community**: [Render Community](https://community.render.com)

## 💡 Pro Tips for Free Tier Testing

1. **Test during your local work hours** to minimize wake-up delays
2. **Keep one tab open** to each portal to prevent sleeping
3. **Focus on core functionality** rather than performance testing
4. **Document what you want to test** before starting
5. **Take screenshots** of features you like
6. **Invite colleagues** to test different user roles

---

**🎯 Goal**: Evaluate AstraNetix BMS features and functionality without any upfront cost!

**⏰ Time Commitment**: 15 minutes setup + unlimited testing time

**💰 Cost**: $0 (completely free for testing)

**🚀 Ready to test?** Click the deploy button above and start exploring!