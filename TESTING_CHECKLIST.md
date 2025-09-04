# 🎯 AstraNetix BMS - Free Tier Testing Checklist

**Use this checklist to test your Render deployment efficiently!**

## ✅ Deployment Verification

### Phase 1: Deployment Status
- [ ] All 7 services show "✅ Live" in Render dashboard
- [ ] PostgreSQL database is running
- [ ] Redis cache is running  
- [ ] Backend API is running
- [ ] All 4 frontend portals are running

### Phase 2: Backend Testing
- [ ] Health check responds: `https://astranetix-backend-XXXX.onrender.com/health`
  - Should return: `{"status": "healthy", "database": "connected"}`
- [ ] API documentation loads: `https://astranetix-backend-XXXX.onrender.com/docs`
- [ ] Root endpoint works: `https://astranetix-backend-XXXX.onrender.com/`

### Phase 3: Frontend Testing
Test each portal loads without errors:
- [ ] **Founder Portal**: `https://astranetix-founder-portal-XXXX.onrender.com`
- [ ] **ISP Portal**: `https://astranetix-isp-portal-XXXX.onrender.com`
- [ ] **Branch Portal**: `https://astranetix-branch-portal-XXXX.onrender.com`
- [ ] **User Portal**: `https://astranetix-user-portal-XXXX.onrender.com`

### Phase 4: Core Functionality
- [ ] **Register**: Create test account on Founder Portal
- [ ] **Login**: Authenticate with test credentials
- [ ] **Dashboard**: Navigate to main dashboard
- [ ] **API Calls**: Check browser dev tools for successful API responses
- [ ] **Mobile View**: Test responsive design on mobile

### Phase 5: Performance Check
- [ ] **Initial Load**: All portals load within 60 seconds (first-time wake)
- [ ] **Subsequent Loads**: Pages load within 10 seconds when active
- [ ] **API Response**: Health check responds within 5 seconds when active

## 🐌 Free Tier Expectations

### Normal Behavior
- ✅ 30-60 second wake time after 15 minutes of inactivity
- ✅ Slower performance compared to paid tiers
- ✅ All features work, just with resource limitations

### Concerning Signs
- ❌ Services fail to wake up after 2 minutes
- ❌ Health check returns database errors
- ❌ Frontend shows white screen or 500 errors
- ❌ Build failures in deployment logs

## 🚀 Testing Scenarios

### Scenario A: ISP Owner Workflow (15 minutes)
1. **Register** on Founder Portal as ISP owner
2. **Create** ISP company profile  
3. **Switch** to ISP Portal
4. **Add** branch location
5. **Create** test user account

### Scenario B: Branch Manager Workflow (10 minutes)
1. **Login** to Branch Portal
2. **View** customer dashboard
3. **Generate** test report
4. **Update** customer plan (demo mode)

### Scenario C: End User Workflow (5 minutes)
1. **Login** to User Portal
2. **View** usage statistics
3. **Check** billing information
4. **Submit** test support ticket

## 🔧 Troubleshooting

### If Services Are Sleeping
```bash
# Wake up backend
curl https://astranetix-backend-XXXX.onrender.com/health

# Wait 30-60 seconds, then test frontends
```

### If Database Connection Fails
- Check Render dashboard for PostgreSQL service status
- Look for connection string in backend service logs
- Verify environment variables are set correctly

### If Frontend Shows Errors
- Check browser dev tools for API connection errors
- Verify REACT_APP_API_URL points to correct backend
- Clear browser cache and try again

## 📊 Success Metrics

### Minimum Viable Test
- [ ] Health check returns "healthy" status
- [ ] At least one portal loads and shows login page
- [ ] Can create and login with test account

### Full Feature Test  
- [ ] All 4 portals load successfully
- [ ] Can register, login, and navigate dashboards
- [ ] API endpoints respond correctly
- [ ] Mobile responsive design works

### Performance Benchmark
- [ ] Wake time: < 60 seconds
- [ ] Page load: < 10 seconds (when active)
- [ ] API response: < 5 seconds (when active)

## 🎉 Next Steps

### If Testing Goes Well
- [ ] Document which features you liked most
- [ ] Consider upgrading to Starter plan ($25-50/month)
- [ ] Plan production deployment with custom domain
- [ ] Review paid tier benefits (no sleeping, better performance)

### If Issues Found
- [ ] Check [troubleshooting guide](RENDER_TROUBLESHOOTING.md)
- [ ] Review deployment logs in Render dashboard
- [ ] Open issue on [GitHub](https://github.com/sanjayjakhar33/AstraNetix-BMS/issues)
- [ ] Ask for help in [Render community](https://community.render.com)

---

**🎯 Goal**: Evaluate all core features within free tier limitations  
**⏰ Time**: 30-45 minutes of active testing  
**💰 Cost**: $0 (completely free)  

**Happy testing! 🚀**