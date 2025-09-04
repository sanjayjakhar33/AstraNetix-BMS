#!/bin/bash

# 🚀 AstraNetix BMS - One-Click Render Deployment Assistant
# This script helps you deploy AstraNetix BMS to Render's free tier

set -e  # Exit on any error

echo "🚀 AstraNetix BMS - Render Deployment Assistant"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're in the right directory
if [ ! -f "render-free-tier.yaml" ]; then
    print_error "This script must be run from the AstraNetix-BMS root directory"
    print_info "Please cd to the directory containing render-free-tier.yaml"
    exit 1
fi

print_status "Found render-free-tier.yaml configuration"

# Validate YAML syntax
if command -v python3 &> /dev/null; then
    python3 -c "import yaml; yaml.safe_load(open('render-free-tier.yaml'))" 2>/dev/null
    if [ $? -eq 0 ]; then
        print_status "YAML configuration is valid"
    else
        print_error "YAML configuration has syntax errors"
        exit 1
    fi
fi

# Check if this is a forked repository
if git remote -v | grep -q "sanjayjakhar33/AstraNetix-BMS"; then
    if git remote -v | grep origin | grep -q "sanjayjakhar33/AstraNetix-BMS"; then
        print_warning "You're using the original repository"
        print_info "For deployment, you should fork this repository to your GitHub account"
        print_info "Go to: https://github.com/sanjayjakhar33/AstraNetix-BMS and click 'Fork'"
        echo ""
    fi
fi

echo "📋 Deployment Checklist:"
echo "========================"
echo ""
echo "1. 🍴 Fork Repository (if not done already)"
echo "   └── Go to: https://github.com/sanjayjakhar33/AstraNetix-BMS"
echo "   └── Click 'Fork' button"
echo ""
echo "2. 🌐 Deploy to Render"
echo "   └── Go to: https://render.com/deploy"
echo "   └── Repository URL: https://github.com/YOUR_USERNAME/AstraNetix-BMS"
echo "   └── Blueprint: render-free-tier.yaml"
echo ""
echo "3. ⚙️  Configure Environment"
echo "   └── JWT_SECRET_KEY: Click 'Generate' (Render will create it)"
echo "   └── Click 'Create Services'"
echo ""
echo "4. ⏳ Wait for Deployment (10-15 minutes)"
echo "   └── Monitor progress in Render dashboard"
echo ""
echo "5. 🧪 Test Your Deployment"
echo "   └── Backend health: https://astranetix-backend-XXXX.onrender.com/health"
echo "   └── API docs: https://astranetix-backend-XXXX.onrender.com/docs"
echo "   └── Founder portal: https://astranetix-founder-portal-XXXX.onrender.com"
echo ""

print_info "Ready to deploy? Here are your next steps:"
echo ""
echo "🔗 Quick Deploy Links:"
echo "   • Render Deploy: https://render.com/deploy"
echo "   • Render Dashboard: https://dashboard.render.com"
echo ""

# Create a simple deployment info file
cat > deployment-info.txt << EOF
AstraNetix BMS - Render Deployment Information
Generated: $(date)

Repository: https://github.com/sanjayjakhar33/AstraNetix-BMS
Blueprint: render-free-tier.yaml

Services to be deployed:
- astranetix-postgres (Database)
- astranetix-redis (Cache)
- astranetix-backend (API)
- astranetix-founder-portal (Frontend)
- astranetix-isp-portal (Frontend)
- astranetix-branch-portal (Frontend)
- astranetix-user-portal (Frontend)

Free Tier Limitations:
- Services sleep after 15 minutes
- 512MB RAM, 0.1 CPU per service
- 750 hours/month total

Testing URLs (replace XXXX with your service ID):
- Health Check: https://astranetix-backend-XXXX.onrender.com/health
- API Docs: https://astranetix-backend-XXXX.onrender.com/docs
- Founder Portal: https://astranetix-founder-portal-XXXX.onrender.com
- ISP Portal: https://astranetix-isp-portal-XXXX.onrender.com
- Branch Portal: https://astranetix-branch-portal-XXXX.onrender.com
- User Portal: https://astranetix-user-portal-XXXX.onrender.com

For help: https://github.com/sanjayjakhar33/AstraNetix-BMS/issues
EOF

print_status "Created deployment-info.txt with all the details"

echo ""
print_status "Deployment assistant completed!"
print_info "Next: Visit https://render.com/deploy to start your deployment"
print_info "Need help? Check RENDER_DEPLOYMENT_STEPS.md for detailed instructions"