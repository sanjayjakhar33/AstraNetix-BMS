# 🚀 Deploy AstraNetix BMS to Render - Quick Start

Deploy your AstraNetix AI Bandwidth Management System to Render in minutes!

## 🆓 Free Tier Testing (Recommended for First-Time Users)

**Want to test AstraNetix BMS for free?** Perfect! Start here:

[![Test on Free Tier](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/sanjayjakhar33/AstraNetix-BMS&blueprint=render-free-tier.yaml)

📖 **[Complete Free Tier Testing Guide](RENDER_FREE_TIER_TESTING.md)** - Step-by-step instructions

⚠️ **Free Tier Notes**:
- Services sleep after 15 minutes (30-60s wake time)
- Perfect for evaluation and testing
- 512MB RAM, 0.1 CPU per service
- Upgrade to paid plans for production use

## 🎯 Full Production Deploy

Ready for production? Use the full configuration:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/sanjayjakhar33/AstraNetix-BMS)

## 📋 What You'll Get

- **🖥️ Backend API** - FastAPI with PostgreSQL & Redis
- **🌐 4 Frontend Portals** - Founder, ISP, Branch, User interfaces  
- **🔐 Secure Authentication** - JWT-based multi-tenant auth
- **📊 Real-time Analytics** - AI-powered bandwidth insights
- **💳 Payment Integration** - Stripe, PayPal, Razorpay support
- **🤖 AI Features** - OpenAI & Google Gemini integration

## ⚡ 5-Minute Setup

### 1. Prepare Repository
```bash
# Run the setup script
./scripts/setup-render.sh
```

### 2. Deploy to Render
1. **Sign up**: [render.com](https://render.com) (free tier available)
2. **Connect**: Link your GitHub repository  
3. **Import**: Use the `render.yaml` configuration
4. **Deploy**: Follow the [complete guide](RENDER_DEPLOYMENT_GUIDE.md)

### 3. Configure Environment
Copy values from `.env.render` to your Render services.

## 🔧 Manual Deployment

If you prefer step-by-step control:

1. **📖 Read the Guide**: [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)
2. **🗄️ Create Database**: PostgreSQL service on Render
3. **🔴 Add Cache**: Redis service on Render  
4. **🖥️ Deploy Backend**: FastAPI web service
5. **🌐 Deploy Frontends**: 4 React static sites

## 💰 Pricing

| Plan | Monthly Cost | Best For | Performance |
|------|-------------|----------|-------------|
| **Free** | $0 | Testing & Evaluation | Services sleep after 15min, 512MB RAM |
| **Starter** | ~$25-50 | Small ISPs, Always-on | 1GB RAM, no sleeping |
| **Professional** | ~$100-200 | Production, High traffic | 2GB+ RAM, SLA support |

**💡 Recommendation**: Start with **Free** for testing, upgrade to **Starter** for production.

## 🆘 Need Help?

- 📚 **Full Guide**: [RENDER_DEPLOYMENT_GUIDE.md](RENDER_DEPLOYMENT_GUIDE.md)
- 🔧 **Configuration**: [render.yaml](render.yaml)  
- ⚙️ **Environment**: [.env.render](.env.render)
- 🐛 **Issues**: [GitHub Issues](https://github.com/sanjayjakhar33/AstraNetix-BMS/issues)

## 🌐 Live Demo

After deployment, your services will be available at:

- **API**: `https://your-backend.onrender.com/docs`
- **Founder Portal**: `https://your-founder-portal.onrender.com`  
- **ISP Portal**: `https://your-isp-portal.onrender.com`
- **Branch Portal**: `https://your-branch-portal.onrender.com`
- **User Portal**: `https://your-user-portal.onrender.com`

## ✨ Features

- 🏢 **Multi-tenant** - Support unlimited ISPs
- 🤖 **AI-Powered** - Intelligent bandwidth optimization  
- 📱 **Mobile Ready** - Responsive design for all devices
- 🔒 **Enterprise Security** - Role-based access control
- 📈 **Real-time Analytics** - Live usage monitoring
- 💰 **Payment Ready** - Integrated billing system
- 🌍 **Global Ready** - Multi-language support
- 🔄 **Auto-scaling** - Handles traffic spikes

Start managing your ISP business with AI today! 🚀