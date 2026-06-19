# National Makhana Board Portal Build Blueprint

## Purpose

This document converts the tender analysis into a future build reference for a National Makhana Board (NMB) portal. It is not just a summary of the RFP. It is a practical product and engineering blueprint for building the platform with the best balance of delivery speed, compliance readiness, scalability, and demo value.

## 1. What This Project Actually Is

The NMB portal is **not** just a public website.

It is a combined platform with three parallel responsibilities:

1. A public-facing government portal for schemes, notifications, updates, and transparency.
2. A workflow platform for beneficiary applications, Annual Action Plans (AAPs), inspections, approvals, and state-central coordination.
3. A decision-support system with dashboards, drill-down analytics, reports, and budget/progress monitoring.

The future build should always treat this as a **scheme management and monitoring system with a public portal attached**, not as a CMS-first website.

## 2. Core Outcome the System Must Deliver

The system should allow:

- Farmers/beneficiaries to register, apply, upload documents, and track status.
- States to submit AAPs, enter field data, review applications, manage clarifications, and recommend cases.
- NMB officials to review submissions, allocate budgets, approve/reject applications, monitor progress, and generate MIS reports.
- Central authorities to see national-level progress across states with drill-down visibility.
- Inspectors to conduct geo-tagged field verification with checklist-driven data capture.
- Administrators to maintain auditability, integration readiness, and operational reliability.

## 3. Product Vision

The ideal product should feel like an **official government operations portal**:

- Simple and trustworthy UI
- Strong role separation
- Clear workflow stages
- High traceability
- Location-aware data capture
- Dashboard-first monitoring
- Integration-ready architecture
- Easy O&M for at least 2 years

## 4. Strategic Interpretation of the Tender

The strongest reading of the tender is:

- The committee wants proof that we understand government workflow systems.
- The dashboard, workflow, and data model matter more than a flashy UI.
- Integration maturity matters, but live Aadhaar/Agristack connectivity is not expected in a PoC.
- Audit logs, security controls, and operational readiness materially increase trust.
- A working prototype with realistic flow coverage is more valuable than many half-built features.

## 5. Recommended Build Philosophy

For best long-term results, build the platform in this order:

1. Workflow backbone
2. Role-based access and permissions
3. Master data and location hierarchy
4. Beneficiary + AAP + inspection transaction modules
5. Dashboard aggregation layer
6. Notification and audit systems
7. External integration adapters
8. Reporting, monitoring, and O&M tooling

Reason:

- Workflows drive the product.
- Dashboards depend on clean transactional data.
- Integrations should plug into stable business flows, not define them.

## 6. Recommended Scope Breakdown

### 6.1 Public Portal

Must include:

- Home
- About NMB
- Schemes
- News / Notifications
- Tenders / Circulars
- Photo gallery
- Contact
- FAQ
- Related links
- Basic bilingual placeholder support

This should be built as a clean public information layer, but it must remain secondary to the transaction platform.

### 6.2 Internal Operational Modules

Core modules:

- Authentication and role-based dashboards
- Beneficiary registration
- Scheme application management
- Document management
- Geo-tagging
- Clarification workflow
- Inspection workflow
- AAP submission and review
- Field data entry
- Budget allocation and utilization
- Notification center
- Audit log
- MIS reports
- System health / admin operations panel

### 6.3 Dashboard Layer

Must support:

- National view
- State view
- District drill-down
- KPI cards
- Trend charts
- Pipeline/status charts
- Map-based views
- Budget and utilization analysis
- Export capability

## 7. Primary User Roles

Recommended baseline roles:

- Public Visitor
- Beneficiary / Farmer
- State Officer
- District Inspector
- NMB Admin
- Central Authority
- Helpdesk / Support
- Super Admin

Recommended rule:

- Keep permissions explicit and module-based.
- Never rely only on UI hiding; enforce RBAC at API/service level.

## 8. Core Workflows

### 8.1 Beneficiary Application Workflow

Recommended lifecycle:

`Draft -> Submitted -> Under State Review -> Clarification Raised -> Resubmitted -> Inspection Assigned -> Inspection Completed -> Recommended by State -> Under NMB Review -> Approved / Rejected / Returned`

System expectations:

- Every transition is logged
- Every transition can trigger notification events
- Status history is visible to farmer and officials with role-appropriate detail

### 8.2 Annual Action Plan Workflow

Recommended lifecycle:

`Draft -> Submitted -> Under Review -> Query Raised -> Revised Submission -> Approved / Returned`

AAP should support:

- District-wise targets
- Cultivation targets
- Farmer coverage targets
- Infrastructure planning
- Training plans
- Budget request
- Supporting documents

### 8.3 Inspection Workflow

Recommended lifecycle:

`Assigned -> In Progress -> Completed -> Verified -> Accepted / Reopened`

Inspection data should capture:

- GPS coordinates
- Timestamp
- Inspector identity
- Checklist
- Photos
- Remarks
- Verification result

## 9. Recommended Architecture

### 9.1 Preferred Stack

Frontend:

- `Next.js` with React
- TypeScript
- Responsive UI

Backend:

- `Django + Django REST Framework`
- Service-layer-based modular apps

Database:

- `PostgreSQL`
- `PostGIS` for geo features

Dashboard / BI:

- `Apache Superset`
- Alternative: `Metabase` if the team already has strong experience there

Background jobs:

- `Celery + Redis`

Storage:

- `MinIO` for S3-compatible file storage

Deployment:

- `Docker + Docker Compose` for development/staging

### 9.2 Why This Stack Is Optimal

- Mature and government-suitable
- Easy to maintain during O&M
- Good support for forms, workflows, admin, reporting, and security
- Strong documentation and hiring availability
- Geospatial support without vendor lock-in
- Open-source and cost-controlled

### 9.3 Architectural Layers

Recommended layers:

1. Presentation layer
2. API layer
3. Authentication/authorization layer
4. Business service layer
5. Workflow/state-machine layer
6. Persistence layer
7. File/document storage layer
8. Notification layer
9. External integration layer
10. Analytics/BI layer
11. Monitoring and backup layer

### 9.4 Non-Negotiable Architecture Rules

- Keep business logic out of controllers/views.
- Use explicit service classes per module.
- Model workflows as state transitions, not ad hoc status strings in scattered code.
- Treat external integrations as adapters behind interfaces.
- Make all environment-specific values configurable.
- Build audit logging centrally, not module-by-module ad hoc.

## 10. Recommended Solution Structure

Suggested backend module boundaries:

- `users`
- `roles_permissions`
- `locations_lgd`
- `beneficiaries`
- `applications`
- `clarifications`
- `inspections`
- `annual_action_plans`
- `field_data`
- `budgets`
- `documents`
- `notifications`
- `audit`
- `reports`
- `dashboard`
- `integrations`
- `system_admin`

Suggested frontend areas:

- Public portal
- Farmer portal
- State operations portal
- NMB admin portal
- Inspector workspace
- Shared dashboard shell
- Admin / support console

## 11. Data Model Direction

### 11.1 High-Value Core Entities

At minimum, the future build should define:

- `users`
- `roles`
- `permissions`
- `states`
- `districts`
- `blocks`
- `villages`
- `beneficiaries`
- `applications`
- `application_status_history`
- `documents`
- `inspections`
- `geo_tags`
- `scheme_components`
- `annual_action_plans`
- `aap_status_history`
- `budget_allocations`
- `fund_utilization`
- `notifications`
- `audit_logs`
- `api_sync_logs`
- `field_data`
- `clarifications`

### 11.2 Data Modeling Principles

- Use normalized master data for geography.
- Use `JSONB` only for flexible scheme-specific sections, not for everything.
- Separate transaction data from dashboard aggregates.
- Keep status history as its own table.
- Do not store raw Aadhaar in plain text.
- Make uploaded files first-class records with metadata.

### 11.3 Dashboard Data Strategy

Do not run all dashboard queries directly from raw transactional tables in production.

Recommended approach:

- Transaction tables for operational workflows
- Materialized views / summary tables for KPI aggregation
- Scheduled refresh jobs
- Filter-friendly indexed aggregates

## 12. Integration Strategy

### 12.1 Integrations Expected by the Tender

- LGD
- SMS gateway
- Email gateway
- WhatsApp gateway
- Aadhaar Vault
- Agristack
- Geospatial APIs / map services
- Possibly Krishi Mapper or other government ecosystem integrations

### 12.2 Correct Future Approach

Build all integrations through a configurable adapter pattern:

- `adapter interface`
- `provider implementation`
- `request/response logging`
- `retry + failure handling`
- `mock provider for demo/staging`

### 12.3 What Should Be Live vs Mocked

Safe for early implementation:

- LGD data ingestion / lookup
- Email integration
- Internal notification log
- Map display with browser geolocation

Usually mocked until approvals exist:

- Aadhaar authentication
- Aadhaar Vault production connectivity
- Agristack APIs
- Real WhatsApp Business API
- Department-provisioned SMS gateway

## 13. Security and Compliance Direction

### 13.1 Minimum Security Baseline

- HTTPS everywhere
- Password hashing with `argon2` or `bcrypt`
- RBAC at API and service levels
- Sensitive field masking
- Session timeout
- CSRF protection where applicable
- Input validation
- Output encoding
- Security headers
- File type and size validation
- Virus scanning for uploads
- Immutable audit logging

### 13.2 Sensitive Data Handling

Recommended treatment:

- Aadhaar stored only as token/reference through vault model
- Bank details encrypted at rest
- PII access restricted by role and purpose
- Audit every privileged read/update

### 13.3 Compliance Readiness

The platform should be built so that later it can align with:

- Aadhaar compliance requirements
- DPDP obligations
- CERT-In good practices
- VA/PT expectations
- Government hosting and audit expectations

## 14. Auditability Requirements

The future system should assume that every important action may be reviewed later.

Audit logs should capture:

- user
- role
- action
- module
- entity
- old value
- new value
- IP address
- user agent
- session
- timestamp

Recommended principle:

- No silent status changes
- No privileged actions without trace
- No deletion of audit records

## 15. Notification Design

Recommended channels:

- In-app
- SMS
- Email
- WhatsApp

Recommended event triggers:

- Registration completed
- Application submitted
- Clarification raised
- Clarification responded
- Inspection assigned
- Inspection completed
- State recommendation completed
- NMB approval/rejection/return
- AAP submitted
- AAP queried
- AAP approved/returned

Recommended structure:

- Template library
- Channel abstraction
- Delivery log
- Retry policy
- Language-ready template variables

## 16. Geo and Location Design

Geo support should not be treated as a cosmetic feature.

It directly supports:

- inspection authenticity
- implementation tracking
- map dashboards
- future geo-fencing

Recommended build decisions:

- Use LGD-based location hierarchy
- Capture lat/long with accuracy metadata
- Store inspection photos with geo context
- Support map plotting for applications and inspections

## 17. Dashboard Design Guidance

Recommended national KPIs:

- Registered farmers
- Applications submitted
- Applications approved
- Applications pending
- Area under cultivation
- Production in MT
- Yield
- Processing units
- Budget allocated
- Budget released
- Budget utilized

Recommended visual blocks:

- State-wise comparison bar chart
- Status pipeline chart
- Time trend line
- Scheme component distribution
- India/state map overlays
- District drill-down table

Recommended dashboard filters:

- financial year
- state
- district
- component
- status
- time period

## 18. Reporting Strategy

Do not try to build a huge reporting engine first.

Start with a small but credible MIS package:

- state summary report
- application status report
- budget utilization report
- inspection completion report
- AAP progress report

Export targets:

- PDF
- Excel

## 19. O&M Readiness

The tender heavily values post-go-live stability. The future build should therefore include an operations mindset from the start.

Recommended O&M capabilities:

- API health checks
- job monitoring
- error log viewer
- backup visibility
- storage usage monitoring
- performance metrics
- admin issue triage support

Recommended operational stack:

- `Prometheus`
- `Grafana`
- structured logs
- periodic backup verification

## 20. Recommended Delivery Phases

### Phase 1: Foundation

- repo setup
- environment configuration
- auth and RBAC
- LGD master data structure
- shared layout and design system
- core database schema
- audit infrastructure

### Phase 2: Core Transactions

- beneficiary registration
- application flow
- document upload
- clarification workflow
- inspection assignment and completion
- AAP flow
- field data entry

### Phase 3: Monitoring and Decision Support

- KPI aggregation
- dashboards
- reports
- budget allocation/utilization
- notification center

### Phase 4: Integration and Hardening

- gateway adapters
- staging-grade configs
- security hardening
- performance improvements
- admin operations pages

### Phase 5: Go-Live Readiness

- UAT
- training materials
- SOPs
- backup/restore rehearsal
- cutover checklist

## 21. Recommended PoC Scope for Maximum Value

If building a PoC first, the best value sequence is:

1. Public homepage
2. RBAC login and dashboards
3. Beneficiary registration + application
4. State officer review queue
5. Clarification flow
6. Inspection workflow with geo-tagging
7. NMB approval flow
8. National/state dashboard
9. AAP submission
10. Audit log + notification log

This proves:

- domain understanding
- workflow understanding
- architecture maturity
- dashboard capability
- compliance thinking

## 22. Recommended 4-Week PoC Plan

### Week 1

- project setup
- base schema
- auth
- RBAC
- public pages

### Week 2

- beneficiary registration
- application forms
- LGD cascading selection
- document upload
- geo capture

### Week 3

- state review workflow
- clarification flow
- inspection module
- NMB approval
- status history

### Week 4

- dashboards
- audit log
- notifications
- sample MIS reports
- demo data
- presentation readiness

## 23. What Not to Build Early

To keep the project optimal, avoid early scope waste.

Do not prioritize:

- native mobile app
- AI/ML analytics
- chatbot features
- real Aadhaar integration before approvals
- full Agristack production integration before access
- payment/DBT flows unless explicitly added to scope
- oversized custom reporting engine
- over-engineered microservices

## 24. Major Risks and How the Design Should Absorb Them

### API dependency risk

Mitigation:

- adapter pattern
- mock providers
- feature flags

### state data quality risk

Mitigation:

- validation rules
- LGD standardization
- status checks
- data quality dashboards

### adoption risk

Mitigation:

- simple UX
- guided steps
- training materials
- support role/admin tools

### security risk

Mitigation:

- encryption
- masking
- RBAC
- audit
- hardened uploads

### delivery risk

Mitigation:

- phase-based build
- workflow-first delivery
- PoC-first proofing
- integration decoupling

## 25. Suggested Repository Starting Structure

```text
national-makhana-portal/
  docs/
    product/
    architecture/
    api/
    operations/
  frontend/
  backend/
  infra/
  demo-data/
  scripts/
```

Recommended docs to create early:

- product requirements document
- workflow specification
- ERD and schema notes
- API conventions
- integration matrix
- security approach
- deployment guide
- demo script

## 26. Best Next Build Artifacts

If this project is taken forward, the next most useful documents to create are:

1. `PRODUCT_REQUIREMENTS.md`
2. `WORKFLOW_SPECIFICATION.md`
3. `ERD_AND_DATA_MODEL.md`
4. `API_CONTRACTS.md`
5. `INTEGRATION_MATRIX.md`
6. `POC_EXECUTION_PLAN.md`
7. `DEMO_SCRIPT.md`

## 27. Final Build Recommendation

For best optimal results, the future implementation should be built as:

- a workflow-first government platform
- backed by clean RBAC and auditability
- powered by PostgreSQL/PostGIS and Django APIs
- surfaced through a Next.js frontend
- supported by a BI layer for dashboards
- prepared for integrations through adapters
- designed for maintainability from day one

If there is only one principle to preserve from this tender analysis, it is this:

**Build the system around operational workflows and trustworthy reporting, not around pages.**

That is the interpretation most likely to produce a strong PoC, a credible bid, and a maintainable production system.
