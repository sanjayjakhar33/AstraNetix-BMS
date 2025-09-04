#!/bin/bash

# AstraNetix BMS - Render Deployment Setup Script
# This script helps prepare your repository for Render deployment

set -e

echo "🚀 AstraNetix BMS - Render Deployment Setup"
echo "============================================="
echo

# Check if we're in the right directory
if [ ! -f "render.yaml" ]; then
    echo "❌ Error: render.yaml not found. Please run this script from the AstraNetix-BMS root directory."
    exit 1
fi

echo "✅ Found render.yaml configuration file"

# Check for required files
echo "🔍 Checking required files..."

# Check backend files
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: backend/main.py not found"
    exit 1
fi
echo "✅ Backend main.py found"

if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Error: backend/requirements.txt not found"
    exit 1
fi
echo "✅ Backend requirements.txt found"

# Check frontend directories
FRONTEND_DIRS=("founder-portal" "isp-portal" "branch-portal" "user-portal")
for dir in "${FRONTEND_DIRS[@]}"; do
    if [ ! -d "frontend/$dir" ]; then
        echo "❌ Error: frontend/$dir directory not found"
        exit 1
    fi
    
    if [ ! -f "frontend/$dir/package.json" ]; then
        echo "❌ Error: frontend/$dir/package.json not found"
        exit 1
    fi
    
    echo "✅ Frontend $dir configuration found"
done

echo
echo "🔧 Setup Tasks:"

# Generate JWT secret if needed
if [ ! -f ".env.render" ]; then
    echo "❌ Error: .env.render template not found"
    exit 1
fi

echo "✅ Environment template found (.env.render)"

# Check if user has OpenSSL for JWT key generation
if command -v openssl &> /dev/null; then
    JWT_SECRET=$(openssl rand -hex 32)
    echo "✅ Generated JWT secret key"
    echo "   Add this to your Render environment variables:"
    echo "   JWT_SECRET_KEY=$JWT_SECRET"
    echo
else
    echo "⚠️  OpenSSL not found. Please generate a secure JWT secret key manually."
    echo "   You can use an online generator or Python:"
    echo "   python3 -c \"import secrets; print(secrets.token_hex(32))\""
    echo
fi

echo "📋 Next Steps:"
echo "   🆓 For FREE TIER TESTING:"
echo "   1. 📖 Read: RENDER_FREE_TIER_TESTING.md"
echo "   2. 🚀 Deploy: Use render-free-tier.yaml blueprint"
echo "   3. ⏱️  Time: 15 minutes setup, \$0 cost"
echo "   4. 🎯 Perfect for: Evaluation and testing"
echo
echo "   🏢 For PRODUCTION DEPLOYMENT:"
echo "1. 🔐 Sign up/login to Render: https://render.com"
echo "2. 🔗 Connect your GitHub repository to Render"
echo "3. 📚 Follow the RENDER_DEPLOYMENT_GUIDE.md step by step"
echo "4. 🗄️  Create PostgreSQL database first"
echo "5. 🔴 Create Redis cache second" 
echo "6. 🖥️  Deploy backend API third"
echo "7. 🌐 Deploy frontend applications last"
echo "8. ⚙️  Configure environment variables from .env.render"
echo

echo "📖 Quick Links:"
echo "   🆓 Free Tier Testing: RENDER_FREE_TIER_TESTING.md"
echo "   📘 Full Production Guide: RENDER_DEPLOYMENT_GUIDE.md"
echo "   🔧 Deployment Validation: scripts/validate-deployment.py"
echo "   🛠️  Fix Summary: DEPLOYMENT_FIXES.md"
echo "   ⚙️  Environment Variables: .env.render" 
echo "   🔧 Production Config: render.yaml"
echo "   🧪 Free Tier Config: render-free-tier.yaml"
echo

echo "🎯 Estimated Times:"
echo "   🆓 Free Tier Testing: 15 minutes, \$0/month"
echo "   🏢 Production Deployment: 30 minutes, \$25-50/month"
echo

echo "✨ Setup complete! Choose your deployment path:"
echo "   🔍 First, validate: python scripts/validate-deployment.py"
echo "   📖 For testing: Open RENDER_FREE_TIER_TESTING.md"
echo "   📖 For production: Open RENDER_DEPLOYMENT_GUIDE.md"