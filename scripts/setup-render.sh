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
echo "   📘 Full Guide: RENDER_DEPLOYMENT_GUIDE.md"
echo "   ⚙️  Environment Variables: .env.render" 
echo "   🔧 Render Config: render.yaml"
echo

echo "🎯 Estimated Deployment Time: 15-30 minutes"
echo "💰 Estimated Monthly Cost: $25-50 (Starter plan)"
echo

echo "✨ Setup complete! Follow the deployment guide to continue."
echo "   Open RENDER_DEPLOYMENT_GUIDE.md for detailed instructions."