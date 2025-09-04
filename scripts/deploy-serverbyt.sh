#!/bin/bash

# AstraNetix BMS - Serverbyt.in Deployment Script
# This script automates the deployment process for serverbyt.in hosting

set -e

echo "🚀 AstraNetix BMS - Serverbyt.in Deployment"
echo "==========================================="
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo -e "${RED}❌ Please do not run this script as root. Run as astranetix user.${NC}"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "docker-compose.serverbyt.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.serverbyt.yml not found. Please run this script from the AstraNetix-BMS root directory.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found serverbyt.in configuration files${NC}"
echo

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${BLUE}🔍 Checking prerequisites...${NC}"

# Check Docker
if ! command_exists docker; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${NC}"
    echo "Run: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
    exit 1
fi
echo -e "${GREEN}✅ Docker found${NC}"

# Check Docker Compose
if ! command_exists docker-compose && ! docker compose version >/dev/null 2>&1; then
    echo -e "${RED}❌ Docker Compose not found. Please install Docker Compose first.${NC}"
    echo "Run: sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose"
    exit 1
fi
echo -e "${GREEN}✅ Docker Compose found${NC}"

# Check if user is in docker group
if ! groups $USER | grep &>/dev/null '\bdocker\b'; then
    echo -e "${YELLOW}⚠️  User not in docker group. Adding user to docker group...${NC}"
    sudo usermod -aG docker $USER
    echo -e "${YELLOW}⚠️  Please logout and login again for group changes to take effect.${NC}"
    echo "Then run this script again."
    exit 1
fi
echo -e "${GREEN}✅ User in docker group${NC}"

echo

# Check environment file
if [ ! -f ".env" ]; then
    if [ -f ".env.serverbyt" ]; then
        echo -e "${YELLOW}📄 Copying serverbyt.in environment template...${NC}"
        cp .env.serverbyt .env
        echo -e "${GREEN}✅ Environment file created${NC}"
    else
        echo -e "${RED}❌ No environment file found. Please create .env file from .env.serverbyt template.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Environment file found${NC}"
fi

# Check if environment variables are configured
echo -e "${BLUE}🔧 Checking environment configuration...${NC}"

# Source environment file
set -o allexport
source .env
set +o allexport

# Check critical variables
if [ "$POSTGRES_PASSWORD" = "your_secure_password" ]; then
    echo -e "${RED}❌ Please update POSTGRES_PASSWORD in .env file${NC}"
    exit 1
fi

if [ "$JWT_SECRET_KEY" = "your-super-secure-secret-key-change-in-production" ]; then
    echo -e "${YELLOW}⚠️  Generating new JWT secret key...${NC}"
    if command_exists openssl; then
        JWT_SECRET=$(openssl rand -hex 32)
        sed -i "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$JWT_SECRET/" .env
        echo -e "${GREEN}✅ JWT secret key generated${NC}"
    else
        echo -e "${RED}❌ Please update JWT_SECRET_KEY in .env file manually${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}✅ Environment configuration looks good${NC}"
echo

# Create necessary directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p backups/postgres backups/redis scripts
echo -e "${GREEN}✅ Directories created${NC}"

# Create backup script if it doesn't exist
if [ ! -f "scripts/backup.sh" ]; then
    echo -e "${BLUE}📝 Creating backup script...${NC}"
    cat > scripts/backup.sh << 'EOF'
#!/bin/bash
# Automated backup script for AstraNetix BMS

set -e

BACKUP_DIR="/home/astranetix/AstraNetix-BMS/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Use Docker Compose command based on what's available
COMPOSE_CMD="docker compose"
if command -v docker-compose >/dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
fi

echo "Starting backup process..."

# Database backup
echo "Backing up PostgreSQL database..."
$COMPOSE_CMD -f docker-compose.serverbyt.yml exec -T postgres pg_dump -U $POSTGRES_USER -d $POSTGRES_DB > $BACKUP_DIR/postgres/backup_$DATE.sql

# Redis backup  
echo "Backing up Redis data..."
$COMPOSE_CMD -f docker-compose.serverbyt.yml exec -T redis redis-cli --rdb $BACKUP_DIR/redis/dump_$DATE.rdb

# Cleanup old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.rdb" -mtime +30 -delete

echo "Backup completed successfully at $DATE"
EOF
    chmod +x scripts/backup.sh
    echo -e "${GREEN}✅ Backup script created${NC}"
fi

echo

# Use Docker Compose command based on what's available
COMPOSE_CMD="docker compose"
if command_exists docker-compose; then
    COMPOSE_CMD="docker-compose"
fi

# Pull latest images
echo -e "${BLUE}📦 Pulling latest Docker images...${NC}"
$COMPOSE_CMD -f docker-compose.serverbyt.yml pull

# Build and start services
echo -e "${BLUE}🚀 Building and starting services...${NC}"
$COMPOSE_CMD -f docker-compose.serverbyt.yml up -d --build

# Wait for services to be ready
echo -e "${BLUE}⏳ Waiting for services to start...${NC}"
sleep 30

# Check service health
echo -e "${BLUE}🔍 Checking service health...${NC}"
$COMPOSE_CMD -f docker-compose.serverbyt.yml ps

# Run database migrations
echo -e "${BLUE}🗄️  Running database migrations...${NC}"
if $COMPOSE_CMD -f docker-compose.serverbyt.yml exec -T backend python -m alembic upgrade head; then
    echo -e "${GREEN}✅ Database migrations completed${NC}"
else
    echo -e "${YELLOW}⚠️  Database migrations failed or no migrations to run${NC}"
fi

echo

# Show deployment status
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo
echo -e "${BLUE}📊 Service Status:${NC}"
$COMPOSE_CMD -f docker-compose.serverbyt.yml ps

echo
echo -e "${BLUE}🌐 Your application URLs:${NC}"
echo -e "Main Portal:    ${GREEN}https://serverbyt.in${NC}"
echo -e "API:           ${GREEN}https://api.serverbyt.in${NC}"
echo -e "ISP Portal:    ${GREEN}https://isp.serverbyt.in${NC}"
echo -e "Branch Portal: ${GREEN}https://branch.serverbyt.in${NC}"
echo -e "User Portal:   ${GREEN}https://user.serverbyt.in${NC}"

echo
echo -e "${BLUE}📝 Next Steps:${NC}"
echo "1. Configure SSL certificates with Let's Encrypt"
echo "2. Setup Nginx reverse proxy configuration"
echo "3. Create admin user account"
echo "4. Configure backup schedule"
echo
echo -e "${YELLOW}📚 See SERVERBYT_DEPLOYMENT_GUIDE.md for complete setup instructions${NC}"

echo
echo -e "${GREEN}✅ AstraNetix BMS is now running on Serverbyt.in! 🚀${NC}"