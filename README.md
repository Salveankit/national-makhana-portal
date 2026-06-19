# National Makhana Board Portal

This repository is a working proof of concept for a Government of India-style National Makhana Board digital services portal. Treat this README as the central mental model for future work in this codebase.

The product combines public portal pages, beneficiary services, officer operations, planning, monitoring, notifications, and integration-readiness demonstrations in one FastAPI application with a static HTML/CSS/JavaScript frontend.

## Current Product State

The app is deployed on Vercel as a demo deployment and can also run locally with Uvicorn.

Current implementation:

- FastAPI backend in `backend/app`
- Static frontend pages in `frontend`
- Role-based login and bearer-token session storage in browser local storage
- SQLite-backed PoC persistence
- File-based document placeholder storage
- Seeded demo data for walkthroughs
- Government-style public portal and officer console UI
- Vercel configuration for serverless demo deployment
- Regression tests covering core workflows

Important deployment reality:

- Local mode stores SQLite and document placeholders under `backend/data`.
- Vercel mode stores SQLite and document placeholders under `/tmp/national-makhana-portal`.
- Vercel `/tmp` storage is not durable, so deployed demo data may reset between cold starts or deployments.
- Production-grade persistence still needs a hosted database and object storage.

## Product Mental Model

The portal has four primary user perspectives:

- Public visitor: views official pages, services, schemes, updates, and helpdesk information.
- Beneficiary/farmer: manages profile, verifies Aadhaar, submits applications, responds to clarifications, and tracks application status.
- State officer/inspector: reviews applications, raises clarifications, assigns or completes inspections, submits AAPs, updates field data, and reports budget utilization.
- NMB admin: monitors national/state dashboards, reviews AAPs, makes board decisions, runs batch decisions, views system health, and demonstrates integration readiness.

The codebase should be understood as a single-window agriculture service platform, not as separate apps. The FastAPI app serves both APIs and frontend pages.

## Main User Flows

Beneficiary flow:

- Login as farmer
- View or update profile
- Tokenize Aadhaar verification in mock mode
- Submit application with geo tag and document metadata
- Track status history
- Respond to clarification

Officer workflow:

- Login as state officer or inspector
- View assigned applications
- Raise clarification
- Assign field inspection
- Complete inspection with geo tag and photo metadata
- Recommend application to NMB

NMB admin workflow:

- Login as NMB admin
- View KPI dashboard and filtered monitoring data
- Review AAP submissions
- Create or review budget records
- Approve, reject, or return applications
- Run batch decisions
- View audit, notification, and integration logs

Integration demonstration flow:

- View service catalog
- Trigger SMS, email, or WhatsApp notification events
- Trigger Aadhaar KYC demonstration
- Trigger DBT disbursement demonstration
- Review integration event logs

## Demo Accounts

```text
nmb.admin@example.com      / Pass@123
bihar.officer@example.com  / Pass@123
inspector@example.com      / Pass@123
farmer@example.com         / Pass@123
```

## Architecture

```text
backend/
  app/
    main.py              FastAPI routes, page serving, workflow actions
    data.py              SQLite storage, seed data, persistence helpers
    models.py            Domain records
    schemas.py           Request/response models
    deps.py              Auth dependencies
    core/
      config.py          Environment settings
      rbac.py            Role permissions
      security.py        Password hashing and token helpers
  data/                  Local runtime SQLite/documents, ignored by Git

frontend/
  index.html             Public portal home
  login.html             Login page
  beneficiary.html       Beneficiary workspace
  dashboard.html         Officer/admin console
  services.html          Public services page
  schemes.html           Public schemes page
  updates.html           Public updates page
  helpdesk.html          Public helpdesk page
  assets/
    styles.css           Shared government portal styling
    app.js               Login/public frontend behavior
    beneficiary.js       Beneficiary workspace behavior
    dashboard.js         Officer console behavior
    images/              Portal illustrations and logo assets

scripts/
  reset_demo_data.py     Recreates seeded demo state locally

tests/
  test_workflows.py      Regression tests for core workflows
```

## Backend Capabilities

Major API areas:

- `/health`
- `/api/v1/auth/*`
- `/api/v1/locations/*`
- `/api/v1/beneficiary/*`
- `/api/v1/officer/*`
- `/api/v1/nmb/*`
- `/api/v1/aap`
- `/api/v1/field-data`
- `/api/v1/budgets`
- `/api/v1/dashboard/summary`
- `/api/v1/reports/overview`
- `/api/v1/notifications`
- `/api/v1/system/overview`
- `/api/v1/integrations/mock/*`

Key implementation notes:

- The app seeds demo data automatically when the SQLite database is empty.
- Auth is a lightweight PoC bearer token implementation, not production OAuth.
- Audit logs are written for major workflow actions.
- Notifications and integrations are logged as events, not sent through live providers.
- SMS/WhatsApp notification demo recipients must be 10 digit mobile numbers.
- Email notification demo recipients must be valid email addresses.
- Uploaded documents are placeholder records/files, not a full secure upload pipeline.

## Frontend Model

The frontend is static HTML/CSS/JS served by FastAPI.

The visual direction is a restrained Indian government portal style:

- Noto Sans typography
- Government identity bar, masthead, green navigation
- Compact officer dashboard with sidebar workspaces
- Minimal but useful illustrations
- Dense forms and monitoring cards
- Channel-aware notification form
- Historical/current FY filters, not future-year defaults

Officer console sections:

- Dashboard Overview
- Planning Workspace
- Workflow Desk
- System Overview
- Service Readiness

Avoid adding duplicate navigation controls inside content when the sidebar already owns workspace navigation.

## Local Development

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run locally:

```powershell
python -m uvicorn backend.app.main:app --reload --app-dir .
```

Open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/login
http://127.0.0.1:8000/dashboard
http://127.0.0.1:8000/health
```

Reset local demo data:

```powershell
python scripts/reset_demo_data.py
```

Run tests:

```powershell
python -m unittest tests.test_workflows
```

## Vercel Deployment

This repo is prepared for Vercel:

- `requirements.txt` defines Python dependencies.
- `pyproject.toml` exposes `backend.app.main:app` as the app entry.
- `vercel.json` sets PoC runtime storage paths under `/tmp`.
- `.vercelignore` excludes tests, caches, local data, and development artifacts.

Deployment model:

- Push changes to GitHub.
- Vercel imports the GitHub repo.
- Future pushes to the connected production branch trigger deployments.

Use Vercel deployment for demos only until persistence is moved off local SQLite.

## Docker

Docker files exist for local/container demos:

- `backend/Dockerfile` runs FastAPI on port `8000`
- `frontend/Dockerfile` serves static files through Nginx on port `3000`
- `docker-compose.yml` starts API, frontend, Postgres, Redis, and MinIO

Current app persistence still uses SQLite by default. Postgres, Redis, and MinIO are infrastructure placeholders unless explicitly integrated later.

## Environment Variables

The app reads:

```text
APP_ENV
APP_SECRET
APP_DATA_DIR
SQLITE_PATH
DOCUMENT_ROOT
SMS_GATEWAY_ENABLED
EMAIL_GATEWAY_ENABLED
WHATSAPP_GATEWAY_ENABLED
AADHAAR_VAULT_ENABLED
```

Defaults:

- `EMAIL_GATEWAY_ENABLED=true`
- `SMS_GATEWAY_ENABLED=false`
- `WHATSAPP_GATEWAY_ENABLED=false`
- `AADHAAR_VAULT_ENABLED=false`

## Current Limitations

Do not mistake the PoC for a production system.

Known limitations:

- SQLite is local/serverless-temp storage.
- Vercel data is ephemeral.
- Auth is simplified.
- No real Aadhaar, SMS, WhatsApp, email, or DBT integration is active.
- Document handling is placeholder-based.
- No production-grade file upload, virus scanning, or object storage.
- No database migrations.
- No admin user management UI.
- No real observability pipeline beyond health and logs.

## Future Development Priorities

Highest value next steps:

- Replace SQLite with hosted Postgres.
- Move document placeholders/files to object storage.
- Add migration tooling.
- Replace mock integrations with provider adapters.
- Add stronger auth and session management.
- Add role/user administration.
- Add deployment smoke tests.
- Add Playwright UI checks for key pages.
- Split public static assets to a CDN/static hosting path if needed.

## Rules for Future Chats

When continuing work in this repo:

- Preserve the Government of India portal tone.
- Keep admin/officer screens compact, dense, and task-focused.
- Avoid duplicate navigation; sidebar owns officer-console workspaces.
- Do not introduce future financial years unless explicitly requested.
- Treat Vercel deployment as demo infrastructure until durable storage is added.
- Keep local runtime data out of Git.
- Run `python -m unittest tests.test_workflows` after backend or workflow changes.
- Prefer small, directly useful UI changes over decorative redesigns.
- Update this README when the product model, deployment model, or persistence model changes.

## Quick Smoke Test

After deployment or a major change:

1. Open `/health`.
2. Open `/login`.
3. Login as `nmb.admin@example.com`.
4. Open `/dashboard`.
5. Check dashboard filters and service readiness tab.
6. Trigger one notification demo with SMS mobile number `9876543210`.
7. Confirm `/api/v1/reports/overview?format=csv` still exports.

## Demo Script

Use [DEMO_SCRIPT.md](DEMO_SCRIPT.md) for the curated walkthrough order and seeded scenario list.
