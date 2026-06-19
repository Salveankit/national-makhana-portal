# National Makhana Board Portal PoC

This repository contains a working proof of concept for the National Makhana Board portal. The current project state is a FastAPI application with seeded SQLite persistence, file-based document placeholders, and a static government-style frontend for public pages, beneficiary services, officer workflows, and dashboard views.

## Current implementation

- FastAPI backend in `backend/app`
- SQLite database at `backend/data/makhana.db`
- Placeholder document storage under `backend/data/documents`
- Static frontend pages in `frontend`
- Seeded demo dataset for beneficiary, inspector, state officer, and NMB admin journeys
- Automated workflow regression tests in `tests/test_workflows.py`

## Main functional areas

- Public portal pages: `/`, `/services`, `/schemes`, `/updates`, `/helpdesk`
- Authentication and role-based access
- Beneficiary profile management and Aadhaar verification flow
- Application submission, clarification handling, inspection assignment, recommendation, and board decision flow
- AAP submission and review
- Budget allocation and utilization updates
- Field-data capture and dashboard summary reporting
- Notification logging and mock integration event logs
- CSV export from the reporting endpoint

## Tech stack

- Python 3.11+
- FastAPI
- Uvicorn
- SQLite
- Static HTML, CSS, and JavaScript frontend
- Optional Docker and Docker Compose setup

## Project structure

```text
backend/
  app/                    FastAPI app, models, storage, auth, and routes
  data/                   SQLite database and seeded document placeholders
frontend/                 Static public pages and dashboard/beneficiary views
scripts/reset_demo_data.py
tests/test_workflows.py
docker-compose.yml
DEMO_SCRIPT.md
```

## Local run

Install the runtime dependencies in your environment, then start the API:

```powershell
pip install fastapi uvicorn
python -m uvicorn backend.app.main:app --reload --app-dir .
```

Open:

- Public portal: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login`
- Health check: `http://127.0.0.1:8000/health`

In local mode, the FastAPI app serves both the API and the static frontend pages.

## Demo reset

Reset the seeded dataset before a walkthrough:

```powershell
python scripts/reset_demo_data.py
```

The reset recreates:

- demo users
- seeded beneficiary profile
- five sample applications across different statuses
- inspections, clarifications, AAPs, budgets, notifications, and mock integration events

See [DEMO_SCRIPT.md](/abs/path/c:/Users/hp5pr/national%20makhana%20poc/DEMO_SCRIPT.md) for the recommended walkthrough order and seeded scenario details.

## Demo accounts

- `nmb.admin@example.com` / `Pass@123`
- `bihar.officer@example.com` / `Pass@123`
- `inspector@example.com` / `Pass@123`
- `farmer@example.com` / `Pass@123`

## Tests

Run the regression suite with:

```powershell
python -m unittest tests.test_workflows
```

The current suite covers health checks, the main end-to-end workflow, reporting, notifications, mock integrations, batch decisions, and a few validation guards.

## Docker

The repository also includes Dockerfiles and a `docker-compose.yml`:

- `backend/Dockerfile` runs the FastAPI app on port `8000`
- `frontend/Dockerfile` serves the static frontend through Nginx on port `3000`
- `docker-compose.yml` also starts Postgres, Redis, and MinIO containers

Start the stack with:

```powershell
docker compose up --build
```

Important: the current application persistence still uses SQLite and local document storage by default. Postgres, Redis, and MinIO are present in Compose as infrastructure placeholders and health/config visibility, not as the active backing services for the PoC.

## Vercel deployment

This repo includes Vercel configuration for the FastAPI app:

- `pyproject.toml` exposes `backend.app.main:app` through `[project.scripts]`
- `requirements.txt` lists the Python runtime dependencies
- `vercel.json` points PoC data storage to `/tmp` for serverless execution

Deploy from a Vercel-connected Git repository, or use the Vercel CLI:

```powershell
vercel
vercel --prod
```

Important: Vercel serverless storage is not durable. The current SQLite database and document placeholders are suitable for a demo deployment only. For production, move persistence to a hosted database and object storage.

## Environment variables

The app reads these settings if provided:

- `APP_ENV`
- `APP_SECRET`
- `APP_DATA_DIR`
- `SQLITE_PATH`
- `DOCUMENT_ROOT`
- `SMS_GATEWAY_ENABLED`
- `EMAIL_GATEWAY_ENABLED`
- `WHATSAPP_GATEWAY_ENABLED`
- `AADHAAR_VAULT_ENABLED`

Default behavior today:

- email gateway flag is enabled by default
- SMS, WhatsApp, and Aadhaar vault integrations remain mock/off unless explicitly enabled

## Notes on current state

- The database file in `backend/data/makhana.db` is part of the active PoC state.
- Uploaded documents are represented as placeholder files, not a full upload pipeline.
- Mock integration endpoints exist for notification, Aadhaar KYC, and DBT disbursement demonstrations.
- `/health` reports SQLite and document storage as active services; Postgres, Redis, and MinIO currently appear as configured rather than live application dependencies.
