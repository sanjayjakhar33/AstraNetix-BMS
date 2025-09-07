#!/bin/bash

# AstraNetix BMS - Serverbyt.in Quick Setup Script
# This script provides a quick setup wizard for serverbyt.in deployment

set -e

echo "🚀 AstraNetix BMS - Serverbyt.in Quick Setup Wizard"
echo "=================================================="
echo

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check if we're in the right directory
if [ ! -f ".env.serverbyt" ]; then
    echo -e "${RED}❌ Error: .env.serverbyt not found. Please run this script from the AstraNetix-BMS root directory.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ AstraNetix BMS repository found${NC}"
echo

# Function to generate secure password
generate_password() {
    openssl rand -base64 32 | tr -d "=+/" | cut -c1-25
}

# Function to generate JWT secret
generate_jwt_secret() {
    openssl rand -hex 32
}

echo -e "${BLUE}🔧 Setting up environment configuration for serverbyt.in...${NC}"
echo

# Copy template
cp .env.serverbyt .env

# Collect user inputs
echo -e "${YELLOW}📝 Please provide the following information:${NC}"
echo

# Database password
echo -n "Enter PostgreSQL password (or press Enter to generate): "
read db_password
if [ -z "$db_password" ]; then
    db_password=$(generate_password)
    echo -e "${GREEN}Generated password: $db_password${NC}"
fi

# JWT secret
jwt_secret=$(generate_jwt_secret)
echo -e "${GREEN}Generated JWT secret: ${jwt_secret:0:20}...${NC}"

# Optional API keys
echo
echo -e "${YELLOW}🔑 Optional API Keys (press Enter to skip):${NC}"

echo -n "OpenAI API Key: "
read openai_key

echo -n "Google Gemini API Key: "
read gemini_key

echo -n "Stripe Secret Key: "
read stripe_key

echo -n "Razorpay Key ID: "
read razorpay_key

echo

# Update .env file
echo -e "${BLUE}📝 Updating configuration file...${NC}"

# Update passwords and secrets
sed -i "s/POSTGRES_PASSWORD=your_secure_password/POSTGRES_PASSWORD=$db_password/" .env
sed -i "s/JWT_SECRET_KEY=your-super-secure-secret-key-change-in-production/JWT_SECRET_KEY=$jwt_secret/" .env

# Update optional API keys if provided
if [ ! -z "$openai_key" ]; then
    sed -i "s/OPENAI_API_KEY=your-openai-api-key/OPENAI_API_KEY=$openai_key/" .env
fi

if [ ! -z "$gemini_key" ]; then
    sed -i "s/GOOGLE_GEMINI_API_KEY=your-google-gemini-api-key/GOOGLE_GEMINI_API_KEY=$gemini_key/" .env
fi

if [ ! -z "$stripe_key" ]; then
    sed -i "s/STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key/STRIPE_SECRET_KEY=$stripe_key/" .env
fi

if [ ! -z "$razorpay_key" ]; then
    sed -i "s/RAZORPAY_KEY_ID=your-razorpay-key-id/RAZORPAY_KEY_ID=$razorpay_key/" .env
fi

echo -e "${GREEN}✅ Configuration file updated successfully${NC}"
echo

# Create deployment summary
echo -e "${BLUE}📋 Deployment Summary${NC}"
echo "===================="
echo
echo -e "${GREEN}Domain Configuration:${NC}"
echo "  Main Portal:    https://serverbyt.in"
echo "  API Endpoint:   https://api.serverbyt.in"
echo "  ISP Portal:     https://isp.serverbyt.in"
echo "  Branch Portal:  https://branch.serverbyt.in"
echo "  User Portal:    https://user.serverbyt.in"
echo
echo -e "${GREEN}Database Configuration:${NC}"
echo "  Database Name:  astranetix_bms"
echo "  Database User:  astranetix_user"
echo "  Database Pass:  [CONFIGURED]"
echo
echo -e "${GREEN}Security:${NC}"
echo "  JWT Secret:     [CONFIGURED]"
echo "  SSL Enabled:    true"
echo "  Debug Mode:     false"
echo

# Show next steps
echo -e "${YELLOW}📚 Next Steps:${NC}"
echo "1. Make sure your domain DNS is configured:"
echo "   - serverbyt.in → Your Server IP"
echo "   - api.serverbyt.in → Your Server IP"
echo "   - isp.serverbyt.in → Your Server IP"
echo "   - branch.serverbyt.in → Your Server IP"
echo "   - user.serverbyt.in → Your Server IP"
echo
echo "2. Run the deployment script:"
echo "   ./scripts/deploy-serverbyt.sh"
echo
echo "3. Configure SSL certificates:"
echo "   sudo certbot certonly --standalone -d serverbyt.in -d api.serverbyt.in -d isp.serverbyt.in -d branch.serverbyt.in -d user.serverbyt.in"
echo
echo "4. Setup Nginx configuration:"
echo "   Follow SERVERBYT_DEPLOYMENT_GUIDE.md Step 5"
echo
echo -e "${GREEN}🎉 Setup completed! Your configuration is ready for deployment.${NC}"
echo
echo -e "${BLUE}📖 For complete deployment instructions, see:${NC}"
echo "   SERVERBYT_DEPLOYMENT_GUIDE.md"