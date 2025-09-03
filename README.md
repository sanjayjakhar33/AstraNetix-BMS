# AstraNetix BMS

AI-powered Bandwidth Management System for ISPs.

## Quickstart

1. Clone this repo
2. Copy `.env.example` to `.env` and fill in credentials
3. Run database migrations in `database/migrations/`
4. Build and start containers:
   ```bash
docker-compose up --build
   ```
5. Access FastAPI docs at `http://localhost:8000/docs`

## Stack

- Backend: FastAPI (Python)
- Frontend: React + TypeScript
- Database: PostgreSQL (multi-tenant)
- Caching: Redis
- AI/ML: OpenAI GPT-4, Google Gemini
- Payment: Stripe, PayPal, Razorpay, Crypto

## Production Deployment

- Deploy on Serverbyt.in cloud with unlimited SSD/bandwidth
- Configure SSL and domains for all tenants
- Enable CDN and backups, setup CI/CD

## License

MIT
