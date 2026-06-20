# National Makhana Board Portal

This repository is a working Government of India-style portal PoC for the National Makhana Board. Use this README as the default mental model for future chats in this codebase.

The application is one FastAPI project that serves:

- public-facing portal pages
- beneficiary self-service workflows
- officer and inspector operations
- NMB admin monitoring and decisions
- mock integration demonstrations
- an embedded AI-assisted chatbot grounded in curated portal knowledge and runtime data

## Current Product State

The project is beyond a static demo site. It already behaves like a functional workflow PoC with seeded operational data.

Implemented today:

- FastAPI backend in `backend/app`
- static HTML/CSS/JS frontend in `frontend`
- role-based login with bearer-token auth stored in browser local storage
- SQLite-backed seeded PoC persistence
- placeholder document storage under local filesystem or `/tmp`
- beneficiary profile, Aadhaar mock verification, application filing, clarification response, and status tracking
- officer review, clarification, inspection, recommendation, AAP, field-data, and budget flows
- NMB admin dashboards, approvals, batch decisions, audit visibility, and system overview
- mock SMS, email, WhatsApp, Aadhaar KYC, and DBT integration logging
- floating chatbot UI on public pages plus beneficiary and dashboard views
- chatbot support for retrieval fallback, Azure OpenAI grounded responses, and streaming-style UI delivery
- curated knowledge base under `knowledge/`
- regression tests for workflows, knowledge loading, and chatbot behavior

Important deployment reality:

- local runtime data lives under `backend/data`
- Vercel runtime data lives under `/tmp/national-makhana-portal`
- Vercel `/tmp` storage is ephemeral
- this is still a PoC deployment model, not production persistence

## Product Mental Model

Treat the portal as a single-window digital service platform, not as a set of disconnected pages.

There are four main user perspectives:

- `public visitor`: understands the portal, finds the right service path, reads updates, and uses helpdesk guidance
- `beneficiary`: manages profile, verifies identity in mock mode, submits applications, responds to clarifications, and tracks status
- `state officer / inspector`: reviews cases, raises clarifications, assigns or completes inspections, submits planning data, and updates workflow records
- `nmb admin`: monitors national/state operations, reviews AAPs and budgets, issues final decisions, and checks system readiness

The chatbot should also be understood in this same model:

- on public pages it acts as a guided portal assistant
- on beneficiary pages it can answer from beneficiary runtime context plus static knowledge
- on dashboard pages it can answer from operations/runtime context plus static knowledge

## Core Surfaces

Public surfaces:

- `/`
- `/services`
- `/schemes`
- `/updates`
- `/helpdesk`
- `/login`

Protected/role-aware surfaces:

- `/beneficiary`
- `/dashboard`

Operational endpoints:

- `/health`
- `/api/v1/*`

## Chatbot Model

The chatbot is now a meaningful part of the PoC, not just placeholder scaffolding.

### What it does

- presents a floating assistant shell in the UI
- supports suggested prompts per page
- sends questions to backend chat endpoints
- shows a short artificial delay and streaming-style response reveal
- formats answers into readable chat content
- optionally shows source titles and guided next actions

### Backend answer modes

The chatbot currently has two broad answer paths:

1. `azure_grounded`
2. fallback retrieval modes

Fallback modes include:

- `retrieval_fallback`
- `beneficiary_runtime_fallback`
- `operations_runtime_fallback`

### Knowledge sources

The chatbot answers from:

- curated file-based knowledge in `knowledge/official`, `knowledge/faq`, and `knowledge/demo`
- runtime beneficiary data such as profile, applications, clarifications, and notifications
- runtime operations data such as queues, inspections, AAPs, budgets, field summaries, and service readiness

### Azure OpenAI reality

Azure OpenAI is only considered active when all of the following are true:

- `CHATBOT_ENABLED=true`
- `AZURE_OPENAI_ENDPOINT` is set
- `AZURE_OPENAI_API_KEY` is set
- `AZURE_OPENAI_DEPLOYMENT` is set

If any of those are missing, the chatbot still works, but it will answer through the local retrieval fallback path.

There is no separate startup handshake endpoint today. The model is attempted at request time.

### Main chat endpoints

- `POST /api/v1/chat/message`
- `POST /api/v1/chat/stream`
- `GET /api/v1/chat/history`
- `GET /api/v1/chat/analytics`

## Main User Flows

Beneficiary flow:

1. login as `farmer@example.com`
2. open beneficiary workspace
3. update profile
4. run mock Aadhaar verification
5. submit application with metadata and geotag
6. track status history
7. respond to open clarification

Officer flow:

1. login as state officer or inspector
2. review assigned applications
3. raise clarification if needed
4. assign inspection
5. complete inspection with remarks and geotag metadata
6. recommend case onward

NMB admin flow:

1. login as `nmb.admin@example.com`
2. review dashboard KPIs and filters
3. inspect planning, workflow, and system overview sections
4. review AAP and budget states
5. approve, reject, or return applications
6. run batch decision actions

Integration-readiness flow:

1. open dashboard system/integration areas
2. trigger mock notification events
3. trigger mock Aadhaar KYC
4. trigger mock DBT disbursement
5. inspect recorded integration logs

Chatbot demo flow:

1. open any public page, `/beneficiary`, or `/dashboard`
2. open the floating assistant
3. ask a public workflow question or use a suggested prompt
4. validate formatted response quality
5. if logged in, test beneficiary or dashboard runtime questions

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
    main.py                FastAPI routes, page serving, chat streaming, workflow actions
    chatbot.py             Retrieval, runtime context assembly, Azure OpenAI call path
    knowledge.py           Knowledge document/chunk loading and summary helpers
    data.py                SQLite storage, seed data, persistence helpers
    models.py              Domain records
    schemas.py             Request/response models
    deps.py                Auth dependencies
    core/
      config.py            Environment loading and settings
      rbac.py              Role permissions
      security.py          Password hashing and token helpers
  data/                    Local runtime SQLite/documents, ignored by Git

frontend/
  index.html               Public home
  services.html            Public services
  schemes.html             Public schemes
  updates.html             Public updates
  helpdesk.html            Public helpdesk
  login.html               Secure login
  beneficiary.html         Beneficiary workspace
  dashboard.html           Officer/admin console
  assets/
    app.js                 Login and page-specific frontend wiring
    beneficiary.js         Beneficiary workspace logic
    dashboard.js           Dashboard workspace logic
    site.js                Shared public UI, translations, chatbot shell/streaming behavior
    styles.css             Shared visual system and chatbot styles
    images/                Portal images and identity assets

knowledge/
  official/                Curated official/project guidance
  faq/                     Structured portal and support Q&A
  demo/                    PoC-specific seeded knowledge
  manifest.json            Knowledge manifest used by tooling/reference
  README.md                Knowledge base notes

scripts/
  reset_demo_data.py       Rebuilds local seeded runtime state
  build_knowledge_manifest.py
                           Rebuilds knowledge manifest from curated content

tests/
  test_workflows.py        End-to-end workflow regression coverage
  test_knowledge_base.py   Knowledge loading and summary checks
  test_chatbot.py          Chat response, runtime context, and stream tests
```

## Backend Capability Map

Major API areas:

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
- `/api/v1/chat/*`

Key implementation notes:

- the database seeds automatically when empty
- auth is lightweight bearer-token PoC auth, not production identity
- audit records are written for major actions
- integration actions are logged, not connected to live providers
- document handling is placeholder-level, not a hardened upload pipeline
- chat history and analytics are stored with answer mode and source titles

## Frontend Mental Model

The frontend is still static HTML/CSS/JS served by FastAPI, but it now behaves like a cohesive portal rather than isolated pages.

Visual direction:

- Indian government portal tone
- green agriculture-aligned palette
- compact operational views
- Noto Sans-based typography
- dense cards, filters, and work panels
- minimal decorative motion
- readable floating chat assistant instead of a generic chatbot widget

Important frontend rules:

- public pages must stay formal and government-facing
- officer/dashboard screens stay compact and dense
- beneficiary/dashboard navigation should not be duplicated unnecessarily
- chatbot should feel like a portal assistant, not a consumer-chat gimmick

## Local Development

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run locally:

```powershell
python -m uvicorn backend.app.main:app --reload --app-dir .
```

Useful URLs:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/login
http://127.0.0.1:8000/beneficiary
http://127.0.0.1:8000/dashboard
http://127.0.0.1:8000/health
```

Reset local demo data:

```powershell
python scripts/reset_demo_data.py
```

Rebuild knowledge manifest if needed:

```powershell
python scripts/build_knowledge_manifest.py
```

## Testing

Fastest useful regression commands:

```powershell
python -m unittest tests.test_workflows
python -m unittest tests.test_chatbot
python -m unittest tests.test_knowledge_base
```

Full current regression set:

```powershell
python -m unittest tests.test_workflows tests.test_chatbot tests.test_knowledge_base
```

## Vercel Deployment

This repo is configured for Vercel demo deployment.

Important constraints:

- runtime persistence is still temp-storage based on `/tmp`
- seeded data may reset across deployments or cold starts
- suitable for demos, evaluations, and bid walkthroughs
- not suitable yet for durable production operations

## Docker

Container files exist for local/container demos:

- `backend/Dockerfile`
- `frontend/Dockerfile`
- `docker-compose.yml`

Treat Docker infra as supportive demo tooling. The application still defaults to SQLite unless deliberately refactored to external infrastructure.

## Environment Variables

Core app and storage:

```text
APP_ENV
APP_SECRET
APP_DATA_DIR
SQLITE_PATH
DOCUMENT_ROOT
```

Chatbot and knowledge:

```text
CHATBOT_ENABLED
CHATBOT_PROVIDER
CHATBOT_DEFAULT_LANGUAGE
KNOWLEDGE_BASE_DIR
KNOWLEDGE_CHUNK_SIZE
KNOWLEDGE_CHUNK_OVERLAP
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_KEY
AZURE_OPENAI_DEPLOYMENT
AZURE_OPENAI_API_VERSION
```

Mock integration flags:

```text
SMS_GATEWAY_ENABLED
EMAIL_GATEWAY_ENABLED
WHATSAPP_GATEWAY_ENABLED
AADHAAR_VAULT_ENABLED
```

Important default behavior:

- `CHATBOT_ENABLED` defaults to `false`
- `EMAIL_GATEWAY_ENABLED` defaults to `true`
- most other integration flags default to `false`

## Current Limitations

This remains a PoC and bid/demo platform.

Known limitations:

- SQLite is still the main persistence layer
- Vercel storage is ephemeral
- auth is simplified
- no production OAuth, SSO, or hardened session management
- no live Aadhaar, DBT, SMS, WhatsApp, or email integrations
- no production-grade object storage or secure file pipeline
- no migrations framework
- no dedicated admin user-management interface
- chatbot quality still depends on curated knowledge and prompt discipline
- chatbot can fall back silently to retrieval if Azure is disabled or unavailable

## Immediate Priorities

Highest-value next steps from the current state:

- add durable Postgres persistence
- move documents to object storage
- add migration tooling
- improve chat diagnostics so active mode is more transparent
- harden off-topic chat behavior
- add UI smoke coverage for public, beneficiary, dashboard, and chat flows
- replace mock integrations with adapter-based live providers when needed
- strengthen auth/session model

## Rules For Future Chats

When continuing work in this repo:

- preserve the Government of India portal tone
- keep officer/admin screens compact and operational
- keep public wording formal and non-startup
- do not reintroduce obvious `PoC`, `demo`, or internal-delivery wording into public UI unless the user explicitly wants it
- treat the chatbot as a serious product surface, not a novelty
- do not assume Azure OpenAI is active unless `CHATBOT_ENABLED=true` and deployment variables are configured
- keep local runtime data out of Git
- run relevant unittests after workflow, chatbot, or knowledge changes
- update this README when architecture, deployment model, or product mental model changes

## Quick Smoke Test

After a major change:

1. open `/health`
2. open `/login`
3. login as `nmb.admin@example.com`
4. open `/dashboard`
5. verify dashboard summary loads
6. open chatbot on dashboard and ask `Summarize the AAP and budget situation.`
7. login as `farmer@example.com` and ask `Do I have any open clarification?`
8. trigger one notification demo with mobile `9876543210`
9. confirm `/api/v1/reports/overview?format=csv` still exports

## Related Docs

- [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
- [knowledge/README.md](knowledge/README.md)
- [NMB_PORTAL_BUILD_BLUEPRINT.md](NMB_PORTAL_BUILD_BLUEPRINT.md)
