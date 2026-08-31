# Wealth Conversational Finance Assistant

A full-stack reconstruction of a university finance-assistant project: secure accounts, financial profiles, explainable metrics, two conversational NLP modes, private history, and credential-free provider fallbacks.

> This repository is a reconstruction of the original university project from its project documentation because the original development repository was unavailable. It is not the exact original source code.

## What it does

- Registers and authenticates users with bcrypt password hashing and JWT access tokens.
- Stores user profiles, financial profiles, goals, conversations, notifications, and upload metadata in MongoDB.
- Calculates monthly surplus, savings rate, expense ratio, emergency-fund targets/gaps, goal progress, and transparent recommendations without an LLM.
- Offers an offline rule-based entity chatbot and an intent/entity AI provider abstraction.
- Runs without paid credentials using mock AI, email, and storage providers.
- Enforces user ownership on conversation list/detail/delete and tests cross-user access denial.
- Provides a responsive, finance-specific Next.js interface for landing, auth, dashboard, profile, chat, and history.

The assistant is educational. It does not execute transactions, store bank credentials, fabricate live market data, rank current securities, or promise returns.

## Architecture

| Layer | Technology | Responsibility |
|---|---|---|
| Web | Next.js 16, React 19, TypeScript | Responsive pages, authenticated workflows, dual-mode chat |
| API | FastAPI, Pydantic | Validation, authentication, authorization, business orchestration |
| Persistence | MongoDB / PyMongo | Users, profiles, conversations, messages, notifications, file metadata |
| NLP | Python rule engine + `AIProvider` | Intent/entity recognition and cautious educational responses |
| Providers | Mock/OpenAI-compatible, mock/SMTP, mock/Cloudinary | Swappable external integrations with safe fallback |

The code is a modular monolith. Report references to microservices, queues, and serverless functions are preserved as historical context, not copied into unnecessary infrastructure. See [Architecture](docs/ARCHITECTURE.md) and [Reconstruction assumptions](docs/RECONSTRUCTION_ASSUMPTIONS.md).

## Repository layout

```text
backend/       FastAPI application and tests
frontend/      Next.js application and tests
docs/          Reconstructed specification, schema, API, logs, and audit
evaluation/    Labeled chatbot query set
results/       Measured evaluation outputs
scripts/       Evaluation and live integration smoke scripts
```

## Quick start with Docker Compose

Requirements: Docker with Compose support.

```bash
cp .env.example .env
# Set a strong SECRET_KEY in .env before any non-local deployment.
docker compose up --build
```

Open `http://localhost:3000`. API documentation is at `http://localhost:8000/docs`.

Compose starts MongoDB, the FastAPI API on port 8000, and Next.js on port 3000. AI, email, and storage default to mock mode.

## Manual development setup

### Backend

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e 'backend[test]'
export SECRET_KEY='replace-with-a-local-random-value'
export MONGODB_URI='mongodb://localhost:27017'
uvicorn app.main:app --app-dir backend --reload
```

For a disposable demo without MongoDB, explicitly set `DATABASE_BACKEND=memory`. Production configuration rejects this mode.

### Frontend

```bash
cd frontend
npm ci
NEXT_PUBLIC_API_URL=http://localhost:8000/api npm run dev
```

## Environment variables

Copy `.env.example`; never commit `.env`.

| Variable | Required | Purpose |
|---|:---:|---|
| `SECRET_KEY` | production | JWT signing secret |
| `DATABASE_BACKEND` | no | `mongodb` (default) or disposable `memory` |
| `MONGODB_URI`, `MONGODB_DATABASE` | MongoDB mode | Database connection |
| `FRONTEND_URL` | no | CORS/reset-link frontend origin |
| `AI_PROVIDER` | no | `mock` or `openai` |
| `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_MODEL` | OpenAI mode | OpenAI-compatible provider |
| `EMAIL_PROVIDER` | no | `mock` or `smtp` |
| `SMTP_*` | SMTP mode | Deployment-owned email configuration |
| `STORAGE_PROVIDER` | no | `mock` or `cloudinary` |
| `CLOUDINARY_*` | Cloudinary mode | Deployment-owned storage configuration |
| `NEXT_PUBLIC_API_URL` | frontend build | Browser-visible API base URL |
| `NEXT_PUBLIC_SITE_URL` | frontend build | Canonical frontend origin for social-preview metadata |

If a non-mock provider is selected without complete credentials, startup selects the matching mock and reports the fallback in health/admin metadata. Credentials are never stored in MongoDB.

## Testing and validation

```bash
# Backend
.venv/bin/python -m pytest backend/tests --cov=backend/app --cov-report=term-missing
.venv/bin/python -m compileall -q backend/app
.venv/bin/python -m pip check

# Frontend
cd frontend
npm run lint
npm run typecheck
npm test
npm run build
npm audit --omit=dev
```

The live smoke script expects a running API:

```bash
.venv/bin/python scripts/integration_smoke.py
```

It exercises health, registration, login, profiles, recommendations, both chat modes, conversation history, mock upload, notification history, and logout without printing the JWT.

## Chatbot evaluation

```bash
.venv/bin/python scripts/evaluate_chatbots.py
```

This reads `evaluation/test_queries.json` and regenerates `results/evaluation.json` plus `results/evaluation.md`. Current AI results use `MockAIProvider`; they are not foundation-model benchmark claims. Metrics are exact intent accuracy, entity-type precision/recall, and fallback rate.

## Key limitations

- The code is reconstructed from an inconsistent report; the exact original implementation cannot be recovered.
- Social login, MFA, sentiment analysis, multilingual NLP, and authoritative live market data remain future work.
- The default AI comparison is a deterministic mock provider.
- Frontend JWT storage is suitable for this reconstruction; a production deployment should move to a same-site HttpOnly cookie/BFF design.
- Money movement, brokerage actions, bank credential storage, and guaranteed-return recommendations are intentionally excluded.
- No software license is granted by default; the project owners should choose one after confirming ownership requirements.

## Reconstruction evidence

- [Project specification](docs/PROJECT_SPEC.md)
- [Feature evidence matrix](docs/FEATURE_MATRIX.md)
- [Database schema](docs/DATABASE_SCHEMA.md)
- [API specification](docs/API_SPEC.md)
- [Implementation audit](docs/IMPLEMENTATION_AUDIT.md)
- [Development log](docs/DEVELOPMENT_LOG.md)
