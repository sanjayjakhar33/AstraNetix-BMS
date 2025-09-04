# 🚀 AstraNetix BMS - Step-by-Step Render Deployment Guide

**Quick deployment guide to get AstraNetix BMS running on Render's free tier in under 15 minutes!**

## 🎯 What You're About to Deploy

- **Backend API** (Python FastAPI)
- **4 Frontend Portals** (React apps)
- **PostgreSQL Database** (Free 1GB)
- **Redis Cache** (Free 25MB)

All completely **FREE** for testing and evaluation!

## 📋 Step-by-Step Instructions

### Step 1: Prepare Your GitHub Account
1. **Fork this repository** to your GitHub account
   - Go to: https://github.com/sanjayjakhar33/AstraNetix-BMS
   - Click the "Fork" button in the top right
   - Wait for the fork to complete

### Step 2: Deploy to Render (One-Click)
1. **Open Render Deploy**
   - Go to: https://render.com/deploy
   - Or click this button: [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

2. **Connect Your Repository**
   - Repository URL: `https://github.com/YOUR_USERNAME/AstraNetix-BMS`
   - Replace `YOUR_USERNAME` with your actual GitHub username
   - Blueprint: `render-free-tier.yaml` (should auto-select)

3. **Configure Environment**
   - Service Group Name: `astranetix-bms-test` (or any name you prefer)
   - Only required setting: **JWT_SECRET_KEY**
   - Click "Generate" next to JWT_SECRET_KEY (Render will create a secure key)

4. **Start Deployment**
   - Click "Create Services"
   - Wait 10-15 minutes for deployment to complete

### Step 3: Monitor Deployment Progress
Watch your Render dashboard as services deploy in this order:
1. ✅ PostgreSQL Database (2-3 minutes)
2. ✅ Redis Cache (2-3 minutes)
3. ✅ Backend API (5-7 minutes)
4. ✅ Frontend Portals (3-5 minutes each)

### Step 4: Test Your Deployment
Once all services show "✅ Live", test these URLs:

1. **Backend Health Check**:
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

*Replace XXXX with your actual Render service ID*

### Step 5: Create Test Account
1. Open the **Founder Portal**
2. Click "Register" to create a test account
3. Use any email (verification disabled in test mode)
4. Login and explore the dashboard

## 🔧 Free Tier Optimizations Applied

Your deployment includes these free tier optimizations:
- ✅ Single worker processes for all services
- ✅ Reduced database connection pools
- ✅ Optimized cache settings
- ✅ Disabled source maps for faster builds
- ✅ Production-optimized React builds

## ⚠️ Free Tier Limitations

- **Services sleep** after 15 minutes of inactivity (30-60s wake time)
- **Limited resources**: 512MB RAM, 0.1 CPU per service
- **750 hours/month** total across all services
- **Slower performance** compared to paid tiers

## 💡 Pro Tips for Testing

1. **Keep tabs open** → Prevents services from sleeping
2. **Test sequentially** → One portal at a time for best performance
3. **Use demo data** → Don't enter real personal information
4. **Take screenshots** → Document features you like

## 🚀 Ready for Production?

If you like what you see, upgrade to **Starter Plan** ($25-50/month) for:
- ✅ Always-on services (no sleeping)
- ✅ Better performance (1GB RAM, 0.5 CPU)
- ✅ Custom domains
- ✅ Priority support

## 🆘 Need Help?

- 🐛 **Issues**: [GitHub Issues](https://github.com/sanjayjakhar33/AstraNetix-BMS/issues)
- 📚 **Full Guide**: [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)
- 💬 **Community**: [Render Community](https://community.render.com)

---

**🎯 Total Time**: ~15 minutes setup + unlimited testing  
**💰 Cost**: $0 (completely free)  
**🎉 Result**: Fully functional ISP management system for testing!