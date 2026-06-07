# SplitEasy Backend

REST API for SplitEasy — a Splitwise-inspired expense splitting app built in 2 days as a Spreetail internship assignment.

## AI Tool Used
**Claude (claude.ai) — Claude Sonnet 4.6**
Claude was used as the primary development collaborator throughout the entire project. The AI was instructed to ask detailed product and engineering questions before building, and to maintain AI_CONTEXT.md as the living source of truth for all decisions.

## Live URLs
- **Backend API:** https://spliteasy-backend-production.up.railway.app
- **Swagger Docs:** https://spliteasy-backend-production.up.railway.app/docs
- **Frontend:** https://spliteasy-frontend.vercel.app

## Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python 3.11 + FastAPI |
| Database | PostgreSQL (Railway) |
| ORM | SQLAlchemy async + Alembic |
| Auth | Server-side sessions + Google OAuth |
| Real-time | python-socketio (WebSocket) |
| Email | SendGrid |
| Deploy | Railway |

## Local Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15+

### Steps
```bash
git clone https://github.com/shriyashsk/spliteasy-backend
cd spliteasy-backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env            # Fill in all values
alembic upgrade head            # Run migrations
uvicorn app.main:socket_app --reload --port 8000
```

### Environment Variables
- DATABASE_URL=postgresql+asyncpg://...
- SESSION_SECRET=...
- GOOGLE_CLIENT_ID=...
- GOOGLE_CLIENT_SECRET=...
- SENDGRID_API_KEY=...
- FROM_EMAIL=...
- EXCHANGE_RATE_API_KEY=...
- FRONTEND_URL=...
- BACKEND_URL=...
- CORS_ORIGINS=...

## Key Files
- `AI_CONTEXT.md` — Full product + engineering context used to build the app
- `BUILD_PLAN.md` — Product research, architecture, AI collaboration process, tradeoffs
- `app/routers/` — All API endpoints
- `app/services/` — Business logic (split calculation, balance updates, auth)
- `app/models/models.py` — All 11 SQLAlchemy models
- `alembic/versions/` — Database migration history
