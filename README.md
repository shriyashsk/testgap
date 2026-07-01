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

## AI-Assisted Test Generation & API Documentation

As part of this project, I used an AI code generator to scaffold missing tests and API documentation for a legacy codebase. 

### The Challenge
The backend had **0/59 functions covered (0.0% coverage)** and lacked a standard Postman collection for API exploration. Manually writing tests and documentation for the entire router and service layer would have been incredibly time-consuming.

### The Process
1. **Gap Analysis:** Ran a script to parse the AST (Abstract Syntax Tree) of the codebase, generating a `gap_report.json` to establish a baseline.
2. **AI Generation:** Fed the gap report and target files (`settlements.py`) to the AI, instructing it to generate a `pytest` file and a Postman collection.
3. **API Documentation:** Successfully imported the generated `settlements.postman_collection.json` into Postman, providing immediate, structured access to the `create_settlement` and `reverse_settlement` endpoints.
4. **Test Refinement (The Human in the Loop):**
   While the AI generated a strong foundation, the tests required manual engineering to execute correctly within the asynchronous environment:
   * **Scope Fixing:** Added `pytest.mark.asyncio` globally to handle standard async test execution.
   * **Mocking External Services:** Corrected the AI's patching paths. The AI attempted to mock functions at their source (`app.services...`), but I re-engineered the mocks to patch them where they were imported and used (`app.routers.settlements...`).
   * **SQLAlchemy Async Workarounds:** Fixed a nuanced bug where the AI mocked `db.execute().scalar_one_or_none()` as an `AsyncMock`. Because `scalar_one_or_none` evaluates synchronously on the awaited result, I restructured the fixture to use a standard `MagicMock` for the result object, resolving a `coroutine object has no attribute` error.
   * **Mock Class Attributes:** Updated the mock SQLAlchemy model to include class-level attributes so that query-building logic like `select(Settlement).where(Settlement.id == ...)` would evaluate properly.

### The Result
The `test_settlements.py` test suite now successfully passes all scenarios (success, not found, already deleted). This process proved that while AI is incredibly powerful for scaffolding bulk code and documentation, human engineering is still required to handle framework-specific nuances (like SQLAlchemy's async patterns).
