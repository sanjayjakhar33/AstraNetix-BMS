# 🚀 Quick Testing Reference - Render Free Tier

**Print this page or keep it open while testing AstraNetix BMS!**

## 🆓 One-Click Deploy (Free Tier)

1. **Fork this repo** → [github.com/sanjayjakhar33/AstraNetix-BMS](https://github.com/sanjayjakhar33/AstraNetix-BMS) → Click "Fork"
2. **Deploy to Render** → [![Deploy](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/YOUR_USERNAME/AstraNetix-BMS&blueprint=render-free-tier.yaml)
3. **Wait 15 minutes** → All services will auto-deploy
4. **Test URLs** → Check your Render dashboard for live URLs

## ⚡ Quick Test Checklist

### URLs to Test (Replace XXXX with your Render service ID)
- [ ] **API Health**: `https://astranetix-backend-XXXX.onrender.com/health`
- [ ] **API Docs**: `https://astranetix-backend-XXXX.onrender.com/docs`
- [ ] **Founder Portal**: `https://astranetix-founder-portal-XXXX.onrender.com`
- [ ] **ISP Portal**: `https://astranetix-isp-portal-XXXX.onrender.com`
- [ ] **Branch Portal**: `https://astranetix-branch-portal-XXXX.onrender.com`
- [ ] **User Portal**: `https://astranetix-user-portal-XXXX.onrender.com`

### Core Features to Test
- [ ] **Registration** → Create test account on Founder Portal
- [ ] **Login/Logout** → Test authentication
- [ ] **Dashboard Navigation** → Browse all 4 portals
- [ ] **Data Entry** → Add test ISP, branch, user
- [ ] **API Calls** → Check network tab for successful API responses
- [ ] **Mobile View** → Test responsive design

## 🐌 Free Tier Expectations

| Aspect | What to Expect |
|--------|----------------|
| **First Load** | 30-60 seconds (services waking up) |
| **Normal Load** | 1-3 seconds after warm-up |
| **Service Sleep** | After 15 minutes of inactivity |
| **Wake Time** | 30-60 seconds when accessed again |
| **Performance** | Slower than production, but functional |
| **Concurrent Users** | Best with 1-2 users for testing |

## 🛠️ Common Issues & Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| **"Service Unavailable"** | Wait 60 seconds, refresh page |
| **Slow Loading** | Normal on free tier, wait for warm-up |
| **Build Failed** | Check Render dashboard logs, retry deployment |
| **404 Error** | Service might be sleeping, access any URL to wake |

## 📱 Test Scenarios

### Scenario 1: ISP Owner Workflow
1. Register on **Founder Portal** as ISP owner
2. Create ISP company profile
3. Switch to **ISP Portal** 
4. Add branch locations
5. Create user accounts

### Scenario 2: Branch Manager Workflow  
1. Login to **Branch Portal** 
2. View assigned customers
3. Generate bandwidth reports
4. Update customer plans

### Scenario 3: End User Workflow
1. Login to **User Portal**
2. View usage statistics
3. Pay bills (demo mode)
4. Submit support tickets

## 💡 Pro Testing Tips

- **Keep tabs open** → Prevents services from sleeping
- **Test sequentially** → One portal at a time for best performance  
- **Use demo data** → Don't enter real personal information
- **Take screenshots** → Document features you like
- **Note response times** → Compare with paid tier expectations

## 🚀 Ready for Production?

If testing goes well, upgrade to **Starter Plan** ($25-50/month) for:
- ✅ No service sleeping (always-on)
- ✅ 2x faster performance (1GB RAM, 0.5 CPU)
- ✅ Production stability
- ✅ Custom domain support

## 📞 Need Help?

- 🐛 **Issues**: [GitHub Issues](https://github.com/sanjayjakhar33/AstraNetix-BMS/issues)
- 📚 **Full Guide**: [RENDER_FREE_TIER_TESTING.md](RENDER_FREE_TIER_TESTING.md)
- 💬 **Community**: [Render Community](https://community.render.com)

---
**🎯 Goal**: Test all features in 30 minutes or less!  
**⏰ Setup**: 15 minutes | **💰 Cost**: $0 | **🔄 Upgrade**: Anytime