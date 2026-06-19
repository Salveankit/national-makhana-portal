# Sprint Plan - National Makhana Board Portal
**Generated:** June 18, 2026
**Sprint Duration:** 2 weeks
**Total Estimated Points:** 151 SP
**Team Size (assumed):** 4 devs

## Project Summary

This plan covers the delivery of a workflow-first National Makhana Board portal that combines a public information website, state and board operational workflows, beneficiary-facing application journeys, and drill-down monitoring dashboards. The primary goal is to ship a government-grade platform that proves domain understanding, workflow correctness, integration readiness, and operational reliability. The primary success metric is a working end-to-end system where a beneficiary application, AAP workflow, inspection flow, and national dashboard all operate with role-based visibility and auditable status transitions.

## Assumptions & Constraints

- Assumed stack: `Next.js + TypeScript` frontend, `Django + DRF` backend, `PostgreSQL + PostGIS`, `Redis + Celery`, `MinIO`, `Apache Superset`.
- Assumed delivery shape: MVP-to-PoC-first execution, then hardening toward production readiness.
- Assumed sprint capacity: `30-32 SP` per sprint for a 4-person cross-functional team.
- Assumed team roles: `1 FE`, `2 BE/full-stack`, `1 QA/supporting full-stack`; PM/BA input is external.
- LGD integration is feasible early through master data ingestion or lookup integration.
- Aadhaar, Agristack, department SMS gateway, and WhatsApp production integrations are not available during early sprints and must remain adapter-based.
- Security, auditability, and government usability are first-order requirements, not later polish.
- The plan prioritizes vertical slices and visible demos over layer-by-layer technical completion.

## Definition of Done

- Code reviewed and merged to `main` or `develop`
- Unit tests written with at least `80%` coverage on new code
- Feature flag or rollback plan documented
- Acceptance criteria verified by QA or the author
- Docs or README updated if the change is user-facing or operationally relevant

---
## Sprint 1 - Foundation and Access Control (Dates: Week 1 - Week 2)
**Goal:** Ship the platform foundation with deployable environments, role-based login, location master data, and a public-facing portal shell.
**Capacity:** 31 SP

### Epic 1 - Establish Core Platform Foundation

#### 1.1 - Stand up containerized platform foundation
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | None |

**User Story:**
> As a delivery team, I want a reproducible local and staging-ready platform setup so that every future module is built on a stable base.

**Acceptance Criteria:**
- [ ] AC1 - Frontend, backend, database, Redis, and object storage services boot through a single documented local startup flow.
- [ ] AC2 - Environment variable templates exist for local, staging, and production-style settings.
- [ ] AC3 - Health endpoints confirm app and dependency availability.

**Subtasks:**
##### 1.1.1 - Create project skeleton for frontend, backend, and infra
- Estimated: 6h
- Notes: Establish repo layout, service naming, baseline environment files, and shared docs structure.

##### 1.1.2 - Configure Docker Compose for core services
- Estimated: 8h
- Notes: Include frontend, backend, PostgreSQL, Redis, MinIO, and network wiring.

##### 1.1.3 - Add health checks and startup documentation
- Estimated: 4h
- Notes: Add `/health` endpoints and a short runbook for local bring-up.

#### 1.2 - Implement authentication and RBAC baseline
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 8 SP |
| **Owner** | BE |
| **Dependencies** | Story 1.1 |

**User Story:**
> As an NMB platform user, I want secure login and role-based access so that each user only sees the data and actions relevant to their authority.

**Acceptance Criteria:**
- [ ] AC1 - Users can sign in with seeded demo accounts for NMB Admin, State Officer, Inspector, and Beneficiary.
- [ ] AC2 - JWT or session-based auth protects all private APIs.
- [ ] AC3 - RBAC rules restrict endpoints by role and geography scope.
- [ ] AC4 - Session timeout and password hashing are enforced.

**Subtasks:**
##### 1.2.1 - Create user, role, and permission schema
- Estimated: 8h
- Notes: Include role-to-module and geographic scope mapping.

##### 1.2.2 - Implement login, token/session handling, and password security
- Estimated: 10h
- Notes: Use hashed credentials and configurable session expiry.

##### 1.2.3 - Add API-level permission middleware or service guards
- Estimated: 8h
- Notes: Enforce role checks server-side, not only in UI.

#### 1.3 - Load LGD-based location hierarchy
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | BE |
| **Dependencies** | Story 1.1 |

**User Story:**
> As a farmer or officer, I want standardized location data so that every record maps correctly to state, district, block, and village.

**Acceptance Criteria:**
- [ ] AC1 - State, district, block, and village master tables exist and are queryable through API.
- [ ] AC2 - Cascading location APIs support state-to-village drill-down.
- [ ] AC3 - Bihar demo data is fully loaded and other states have at least seed coverage.

**Subtasks:**
##### 1.3.1 - Define LGD master tables and import scripts
- Estimated: 8h
- Notes: Prioritize the 10 target states and Bihar completeness.

##### 1.3.2 - Build cascading location APIs
- Estimated: 6h
- Notes: Optimize for dropdown-driven access patterns.

##### 1.3.3 - Seed demo geography data
- Estimated: 4h
- Notes: Include sample district hierarchy for demo flows.

#### 1.4 - Ship public portal shell and content framework
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | FE |
| **Dependencies** | Story 1.1 |

**User Story:**
> As a public visitor, I want a clean official portal homepage and content pages so that the platform immediately feels government-ready and credible.

**Acceptance Criteria:**
- [ ] AC1 - Home, About, Schemes, News, Contact, and FAQ pages render responsively.
- [ ] AC2 - Layout supports bilingual placeholder treatment and accessible navigation.
- [ ] AC3 - Branding, footer, and information layout feel like a formal government portal, not a startup site.

**Subtasks:**
##### 1.4.1 - Create public portal layout and navigation shell
- Estimated: 8h
- Notes: Build responsive navbar, content grid, and footer.

##### 1.4.2 - Implement core content pages with placeholder CMS-ready structure
- Estimated: 6h
- Notes: Keep content editable later without redesign.

##### 1.4.3 - Add accessibility and responsive validation
- Estimated: 4h
- Notes: Focus on contrast, keyboard flow, and mobile rendering.

#### 1.5 - Add audit framework and initial admin observability
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 8 SP |
| **Owner** | BE |
| **Dependencies** | Story 1.2 |

**User Story:**
> As an administrator, I want audit events recorded centrally so that the system is reviewable and compliant from the first workflow onward.

**Acceptance Criteria:**
- [ ] AC1 - Login, logout, and privileged actions write audit entries with actor, role, timestamp, and IP.
- [ ] AC2 - Audit records are immutable through application logic.
- [ ] AC3 - Admin users can inspect recent audit entries through a basic internal view or API.

**Subtasks:**
##### 1.5.1 - Create audit schema and event contract
- Estimated: 6h
- Notes: Standardize old/new values, module, entity type, and session metadata.

##### 1.5.2 - Instrument auth events and privileged API hooks
- Estimated: 8h
- Notes: Cover login, failed login, permission denial, and admin actions.

##### 1.5.3 - Expose basic audit inspection endpoint or admin screen
- Estimated: 4h
- Notes: Keep the view simple but filterable.

---
## Sprint 2 - Beneficiary Journey and Document Flow (Dates: Week 3 - Week 4)
**Goal:** Ship a working farmer-facing registration and application flow with location selection, document handling, geo capture, and status visibility.
**Capacity:** 31 SP

### Epic 2 - Deliver Beneficiary Registration and Application

#### 2.1 - Create beneficiary registration profile flow
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | Stories 1.2, 1.3 |

**User Story:**
> As a farmer, I want to register my profile in the portal so that I can apply for scheme benefits and track my history.

**Acceptance Criteria:**
- [ ] AC1 - A beneficiary can create and update a profile with personal, cultivation, and banking fields.
- [ ] AC2 - Aadhaar is captured through a masked placeholder/tokenized field pattern, not as plain text display.
- [ ] AC3 - Location selection uses LGD cascading data.

**Subtasks:**
##### 2.1.1 - Define beneficiary schema and validation rules
- Estimated: 6h
- Notes: Include cultivation type, land details, and FPO/SHG membership fields.

##### 2.1.2 - Build registration UI with LGD-driven selectors
- Estimated: 8h
- Notes: Ensure helpful error messaging for low-tech users.

##### 2.1.3 - Create beneficiary profile APIs and edit flow
- Estimated: 6h
- Notes: Add save/update/retrieve endpoints and masking behavior.

#### 2.2 - Implement application submission workflow
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 8 SP |
| **Owner** | Full-stack |
| **Dependencies** | Story 2.1 |

**User Story:**
> As a farmer, I want to submit a scheme application with supporting details so that my request enters the official review process.

**Acceptance Criteria:**
- [ ] AC1 - A beneficiary can select a scheme component and submit a complete application.
- [ ] AC2 - Each application receives a unique application ID and initial status history entry.
- [ ] AC3 - Submitted applications become visible in officer review queues.

**Subtasks:**
##### 2.2.1 - Create application schema, scheme component master, and status model
- Estimated: 8h
- Notes: Use a formal workflow status table/history pattern.

##### 2.2.2 - Build application form and submission confirmation flow
- Estimated: 10h
- Notes: Include step-based sections and save/submit semantics.

##### 2.2.3 - Write application creation services and queue exposure APIs
- Estimated: 8h
- Notes: Ensure submitted records appear in state officer worklists.

#### 2.3 - Add document upload and secure file handling
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | Stories 1.1, 2.2 |

**User Story:**
> As a farmer, I want to upload my required documents safely so that my application can be reviewed without offline follow-up.

**Acceptance Criteria:**
- [ ] AC1 - Beneficiaries can upload required file types with preview and validation.
- [ ] AC2 - Files are stored through object storage with metadata persisted in the database.
- [ ] AC3 - Invalid file type or oversize uploads are rejected with clear messages.

**Subtasks:**
##### 2.3.1 - Configure MinIO buckets and upload service
- Estimated: 6h
- Notes: Separate document paths by entity type and ID.

##### 2.3.2 - Add file validation, metadata persistence, and preview support
- Estimated: 8h
- Notes: Prepare for later virus scanning hook.

##### 2.3.3 - Implement beneficiary document upload UI
- Estimated: 4h
- Notes: Include progress state and uploaded-file list.

#### 2.4 - Capture geo-tagging at application stage
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | FE |
| **Dependencies** | Story 2.2 |

**User Story:**
> As a farmer, I want to capture the location of my cultivation or infrastructure site so that implementation can later be verified spatially.

**Acceptance Criteria:**
- [ ] AC1 - Browser-based location capture stores latitude, longitude, and accuracy.
- [ ] AC2 - Manual fallback is available when geolocation fails.
- [ ] AC3 - Saved coordinates are visible in the application detail screen.

**Subtasks:**
##### 2.4.1 - Add geolocation capture component with permission handling
- Estimated: 6h
- Notes: Handle deny/fail cases cleanly.

##### 2.4.2 - Persist geo-tag records and link them to applications
- Estimated: 4h
- Notes: Include device and capture timestamp metadata.

##### 2.4.3 - Show captured location in reviewable UI
- Estimated: 4h
- Notes: Basic map or coordinate presentation is sufficient in this sprint.

#### 2.5 - Build application status tracker and beneficiary dashboard
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 8 SP |
| **Owner** | Full-stack |
| **Dependencies** | Stories 2.2, 1.2 |

**User Story:**
> As a farmer, I want to see my application timeline and current status so that I know what has happened and what is pending.

**Acceptance Criteria:**
- [ ] AC1 - Beneficiaries can view all their submitted applications.
- [ ] AC2 - Each application shows status history as a timeline.
- [ ] AC3 - Clarification-required states are clearly visible with next-step messaging.

**Subtasks:**
##### 2.5.1 - Build beneficiary dashboard shell with application list
- Estimated: 8h
- Notes: Include status badges and quick actions.

##### 2.5.2 - Expose status history and timeline APIs
- Estimated: 6h
- Notes: Use ordered, readable transition records.

##### 2.5.3 - Implement timeline UI and empty/error states
- Estimated: 8h
- Notes: Optimize for clarity, not decorative complexity.

---
## Sprint 3 - Officer Review, Clarifications, and Inspections (Dates: Week 5 - Week 6)
**Goal:** Ship the state and board operational workflow from review through clarification, inspection, recommendation, and final decisioning.
**Capacity:** 31 SP

### Epic 3 - Deliver Multi-Level Government Review Workflow

#### 3.1 - Build state officer application queue and detail review
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | Story 2.2 |

**User Story:**
> As a state officer, I want a filtered application queue so that I can review incoming applications efficiently.

**Acceptance Criteria:**
- [ ] AC1 - State officers only see applications within their state scope.
- [ ] AC2 - Queue supports filters for status, district, component, and submission date.
- [ ] AC3 - Officers can open full application details and attached documents.

**Subtasks:**
##### 3.1.1 - Create scoped queue query services and filters
- Estimated: 8h
- Notes: Index for state/district/status access patterns.

##### 3.1.2 - Build officer queue UI and detail screen
- Estimated: 8h
- Notes: Prioritize clarity and table filters over visual complexity.

##### 3.1.3 - Add document/detail read permissions and audit hooks
- Estimated: 4h
- Notes: Log privileged views if required by policy.

#### 3.2 - Implement clarification raise and respond workflow
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | Story 3.1 |

**User Story:**
> As a state officer, I want to raise clarifications and receive responses so that incomplete applications can continue without offline tracking.

**Acceptance Criteria:**
- [ ] AC1 - Officers can raise a clarification linked to a specific application.
- [ ] AC2 - Beneficiaries can view and respond to open clarifications.
- [ ] AC3 - Clarification actions update status history and audit logs.

**Subtasks:**
##### 3.2.1 - Define clarification entity and status model
- Estimated: 4h
- Notes: Support open, responded, and closed states.

##### 3.2.2 - Build officer clarification creation flow
- Estimated: 6h
- Notes: Link message content and due-state to the application.

##### 3.2.3 - Build beneficiary response flow and status transition logic
- Estimated: 8h
- Notes: Ensure timeline reflects the clarification loop.

#### 3.3 - Deliver inspection assignment and field capture
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 8 SP |
| **Owner** | Full-stack |
| **Dependencies** | Story 3.1 |

**User Story:**
> As a state officer or inspector, I want to assign and complete field inspections so that site verification is part of the official approval chain.

**Acceptance Criteria:**
- [ ] AC1 - State officers can assign an application to an inspector.
- [ ] AC2 - Inspectors can complete a checklist with geo-tagged photos and remarks.
- [ ] AC3 - Completed inspections feed back into the officer review and board decision flow.

**Subtasks:**
##### 3.3.1 - Create inspection schema, checklist payload, and assignment flow
- Estimated: 8h
- Notes: Support assignment metadata and verification status.

##### 3.3.2 - Build inspector workspace and checklist form
- Estimated: 10h
- Notes: Include geo capture, photo upload, and remarks.

##### 3.3.3 - Wire inspection completion into application status lifecycle
- Estimated: 6h
- Notes: Add history entries, notification events, and queue updates.

#### 3.4 - Implement state recommendation and NMB decision workflow
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 8 SP |
| **Owner** | BE |
| **Dependencies** | Stories 3.2, 3.3 |

**User Story:**
> As a state officer or NMB admin, I want to recommend and decide on applications so that the workflow reaches a complete official outcome.

**Acceptance Criteria:**
- [ ] AC1 - State officers can recommend or return eligible applications.
- [ ] AC2 - NMB admins can approve, reject, or return state-recommended applications.
- [ ] AC3 - All decisions create audit events, status history, and beneficiary-visible outcomes.

**Subtasks:**
##### 3.4.1 - Model state recommendation and board decision transitions
- Estimated: 6h
- Notes: Keep business rules centralized in workflow services.

##### 3.4.2 - Build NMB approval queue and decision endpoints
- Estimated: 8h
- Notes: Support remarks and optional batch actions later.

##### 3.4.3 - Add beneficiary-visible decision states and messaging hooks
- Estimated: 6h
- Notes: Show approved, rejected, returned, and next steps clearly.

#### 3.5 - Expand audit logging across workflow transitions
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | BE |
| **Dependencies** | Stories 3.2, 3.3, 3.4 |

**User Story:**
> As an auditor or administrator, I want every review-stage action captured so that workflow decisions are fully traceable.

**Acceptance Criteria:**
- [ ] AC1 - Clarification, inspection, recommendation, and decision events all produce audit records.
- [ ] AC2 - Status history and audit logs remain internally consistent for the same transaction.
- [ ] AC3 - An admin can filter audit records by module and entity.

**Subtasks:**
##### 3.5.1 - Add centralized workflow event emitters for audit capture
- Estimated: 6h
- Notes: Avoid per-screen ad hoc logging.

##### 3.5.2 - Add audit filters by module, entity, and actor
- Estimated: 4h
- Notes: Keep support operations usable.

##### 3.5.3 - Validate history-to-audit consistency with tests
- Estimated: 4h
- Notes: Focus on transition integrity.

---
## Sprint 4 - AAP, Field Data, Budgeting, and Dashboards (Dates: Week 7 - Week 8)
**Goal:** Ship the state planning workflow and the first credible national/state dashboard backed by real platform transactions and field data.
**Capacity:** 30 SP

### Epic 4 - Deliver Planning and Monitoring Capabilities

#### 4.1 - Implement Annual Action Plan submission and review
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 8 SP |
| **Owner** | Full-stack |
| **Dependencies** | Stories 1.2, 1.3 |

**User Story:**
> As a state officer, I want to submit a structured Annual Action Plan so that the Board can review state targets, budgets, and implementation proposals.

**Acceptance Criteria:**
- [ ] AC1 - States can create and submit multi-section AAPs with district-wise targets and documents.
- [ ] AC2 - NMB reviewers can raise queries, return, or approve AAPs.
- [ ] AC3 - AAP status history is preserved and visible.

**Subtasks:**
##### 4.1.1 - Define AAP schema and workflow model
- Estimated: 8h
- Notes: Use JSONB selectively for flexible plan sections.

##### 4.1.2 - Build AAP multi-step UI and submission flow
- Estimated: 10h
- Notes: Include save draft, submit, and document attachment support.

##### 4.1.3 - Implement review/query/approval actions and history
- Estimated: 8h
- Notes: Mirror application workflow discipline.

#### 4.2 - Add field data entry and aggregation-ready capture
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | BE |
| **Dependencies** | Stories 1.3, 1.2 |

**User Story:**
> As a state officer, I want to enter cultivation and production metrics so that the Board dashboard reflects current sector performance.

**Acceptance Criteria:**
- [ ] AC1 - Field data supports area, production, yield, farmer count, and infrastructure counts.
- [ ] AC2 - Entry is scoped by geography and time period.
- [ ] AC3 - Data is retrievable for dashboard aggregation.

**Subtasks:**
##### 4.2.1 - Create field data schema and validation rules
- Estimated: 6h
- Notes: Support quarter and financial-year filters.

##### 4.2.2 - Build state data entry forms and APIs
- Estimated: 8h
- Notes: Optimize for repetitive entry with clear validation.

##### 4.2.3 - Add aggregation-ready query layer
- Estimated: 4h
- Notes: Prepare summary views for BI consumption.

#### 4.3 - Implement budget allocation and utilization tracking
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | Story 4.1 |

**User Story:**
> As an NMB admin, I want to allocate and monitor budgets by state and component so that financial progress is visible alongside program progress.

**Acceptance Criteria:**
- [ ] AC1 - NMB admins can record allocations by state, quarter, and component.
- [ ] AC2 - States can report utilization against allocations.
- [ ] AC3 - Utilization summaries are available for dashboard display.

**Subtasks:**
##### 4.3.1 - Create budget allocation and utilization entities
- Estimated: 5h
- Notes: Include quarter and financial-year dimensions.

##### 4.3.2 - Build allocation and utilization entry screens
- Estimated: 8h
- Notes: Separate NMB allocation from state utilization actions.

##### 4.3.3 - Add summary APIs for financial KPIs
- Estimated: 4h
- Notes: Optimize for allocated vs released vs utilized comparisons.

#### 4.4 - Ship national and state dashboards with drill-down
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 8 SP |
| **Owner** | FE |
| **Dependencies** | Stories 4.2, 4.3, 3.4 |

**User Story:**
> As a central authority or NMB admin, I want dashboard visibility from national to district level so that I can monitor progress and identify exceptions quickly.

**Acceptance Criteria:**
- [ ] AC1 - Dashboard shows KPI cards for applications, approvals, area, production, and budget metrics.
- [ ] AC2 - Users can drill from national to state and district views.
- [ ] AC3 - Charts and tables reflect live platform data or refreshed summary views.

**Subtasks:**
##### 4.4.1 - Create dashboard summary tables or materialized views
- Estimated: 8h
- Notes: Separate operational queries from analytics reads.

##### 4.4.2 - Build dashboard UI with KPI cards, charts, and drill-down routes
- Estimated: 10h
- Notes: Include filters for state, district, component, and period.

##### 4.4.3 - Add map and export placeholders or first-pass support
- Estimated: 5h
- Notes: Prioritize trust-building visuals over advanced cartography.

#### 4.5 - Build first MIS exports
| Field | Value |
|-------|-------|
| **Priority** | Medium |
| **Story Points** | 4 SP |
| **Owner** | BE |
| **Dependencies** | Stories 4.2, 4.3, 4.4 |

**User Story:**
> As an official, I want downloadable reports so that I can share and review progress outside the live dashboard.

**Acceptance Criteria:**
- [ ] AC1 - At least two reports export successfully as PDF or Excel.
- [ ] AC2 - Report values match dashboard or transactional data.
- [ ] AC3 - Export events are auditable.

**Subtasks:**
##### 4.5.1 - Build state summary report export
- Estimated: 5h
- Notes: Favor Excel first if faster to stabilize.

##### 4.5.2 - Build application status report export
- Estimated: 5h
- Notes: Include filters and export metadata.

##### 4.5.3 - Add export audit hooks and validation
- Estimated: 3h
- Notes: Ensure traceability for downloads.

---
## Sprint 5 - Notifications, Hardening, and Demo Readiness (Dates: Week 9 - Week 10)
**Goal:** Harden the platform with notification plumbing, admin operations views, security checks, test coverage, and a demo-ready operating experience.
**Capacity:** 28 SP

### Epic 5 - Make the Platform Operationally Credible

#### 5.1 - Implement notification service abstraction and event templates
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | BE |
| **Dependencies** | Stories 2.2, 3.2, 3.4, 4.1 |

**User Story:**
> As a platform administrator, I want notification events standardized so that users receive timely updates and the system is ready for gateway activation later.

**Acceptance Criteria:**
- [ ] AC1 - Notification events are emitted for key application and AAP lifecycle changes.
- [ ] AC2 - The system supports channel abstractions for SMS, email, WhatsApp, and in-app delivery.
- [ ] AC3 - A notification log shows delivery intent and status.

**Subtasks:**
##### 5.1.1 - Create notification event model, templates, and channel interfaces
- Estimated: 8h
- Notes: Keep providers swappable and environment-configurable.

##### 5.1.2 - Wire workflow transitions to notification events
- Estimated: 8h
- Notes: Cover submit, clarify, inspect, recommend, approve, reject, and AAP states.

##### 5.1.3 - Build notification log view or API
- Estimated: 4h
- Notes: Surface event, channel, recipient, and delivery state.

#### 5.2 - Add system health and admin operations screens
| Field | Value |
|-------|-------|
| **Priority** | Medium |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | Story 1.1 |

**User Story:**
> As an operations user, I want a system health view so that I can assess whether the platform and integrations are functioning.

**Acceptance Criteria:**
- [ ] AC1 - Health screen shows API, DB, object storage, and background job status.
- [ ] AC2 - External integrations have visible statuses such as connected, configured, or awaiting credentials.
- [ ] AC3 - Recent platform errors or failed jobs are inspectable.

**Subtasks:**
##### 5.2.1 - Expand backend health checks and dependency probes
- Estimated: 6h
- Notes: Include service readiness and configuration-state indicators.

##### 5.2.2 - Build admin health dashboard UI
- Estimated: 6h
- Notes: Keep status legible and operationally useful.

##### 5.2.3 - Add recent error/job summary endpoints
- Estimated: 4h
- Notes: Surface only safe operational detail.

#### 5.3 - Harden security, uploads, and configuration
| Field | Value |
|-------|-------|
| **Priority** | Critical |
| **Story Points** | 8 SP |
| **Owner** | BE |
| **Dependencies** | Stories 2.3, 3.5, 5.1 |

**User Story:**
> As the delivery team, I want baseline hardening complete so that the platform is credible for government review and safer to deploy.

**Acceptance Criteria:**
- [ ] AC1 - Security headers, input validation, and sensitive masking are verified on key flows.
- [ ] AC2 - Upload handling includes file restrictions and a virus-scan integration point.
- [ ] AC3 - Configuration separates local, staging, and production-safe defaults.

**Subtasks:**
##### 5.3.1 - Review and enforce security headers, validation, and masking rules
- Estimated: 8h
- Notes: Focus on auth, application, and document flows first.

##### 5.3.2 - Add upload safety hooks and storage policy cleanup
- Estimated: 6h
- Notes: Prepare ClamAV or equivalent integration point even if mocked.

##### 5.3.3 - Finalize environment-specific config management
- Estimated: 4h
- Notes: Remove unsafe defaults and document secure setup.

#### 5.4 - Raise test coverage and QA confidence on critical flows
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | QA |
| **Dependencies** | Stories 3.4, 4.4, 5.1 |

**User Story:**
> As a release owner, I want critical workflows covered by tests so that demo risk and regression risk are materially reduced.

**Acceptance Criteria:**
- [ ] AC1 - Automated tests cover login, application submission, clarification, inspection completion, approval, and dashboard aggregation paths.
- [ ] AC2 - A written regression checklist exists for manual demo rehearsal.
- [ ] AC3 - Known defects are triaged with severity and disposition.

**Subtasks:**
##### 5.4.1 - Add backend integration tests for core lifecycle flows
- Estimated: 8h
- Notes: Focus on workflow transitions and access control.

##### 5.4.2 - Add frontend happy-path tests for critical screens
- Estimated: 6h
- Notes: Cover login, application flow, officer review, and dashboard visibility.

##### 5.4.3 - Create manual regression and demo verification checklist
- Estimated: 4h
- Notes: Include venue and browser checks for demo readiness.

#### 5.5 - Prepare demo data and presentation-ready product states
| Field | Value |
|-------|-------|
| **Priority** | High |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | Stories 4.4, 5.1, 5.4 |

**User Story:**
> As a bid/demo presenter, I want realistic seeded states and polished walkthrough paths so that the committee sees a credible system rather than a raw build.

**Acceptance Criteria:**
- [ ] AC1 - Demo data covers Bihar deeply and other target states minimally.
- [ ] AC2 - The platform contains seeded applications across multiple workflow statuses.
- [ ] AC3 - A scripted demo path can be executed without live blockers.

**Subtasks:**
##### 5.5.1 - Seed realistic application, field, budget, and AAP demo data
- Estimated: 8h
- Notes: Ensure dashboards and queues show meaningful variation.

##### 5.5.2 - Create demo personas and deterministic login accounts
- Estimated: 4h
- Notes: Include beneficiary, state officer, inspector, and NMB admin.

##### 5.5.3 - Validate a full rehearsal path and patch blockers
- Estimated: 6h
- Notes: Prefer fixing flow blockers over cosmetic polishing.

## Backlog / Future Sprints

### Epic 6 - Expand Production-Grade Integration and Scale Readiness

#### 6.1 - Activate department SMS gateway
| Field | Value |
|-------|-------|
| **Priority** | Medium |
| **Story Points** | 3 SP |
| **Owner** | BE |
| **Dependencies** | Story 5.1 |

**User Story:**
> As an administrator, I want SMS delivery wired to the department gateway so that users receive official notifications outside the portal.

**Acceptance Criteria:**
- [ ] AC1 - Gateway credentials are configurable without code changes.
- [ ] AC2 - Delivery responses are logged and retryable.

**Subtasks:**
##### 6.1.1 - Implement provider adapter for the approved gateway
- Estimated: 5h
- Notes: Map current event contracts to gateway payloads.

##### 6.1.2 - Validate delivery logs and failure behavior
- Estimated: 3h
- Notes: Confirm observability and retry paths.

#### 6.2 - Integrate Aadhaar Vault and identity verification path
| Field | Value |
|-------|-------|
| **Priority** | Medium |
| **Story Points** | 8 SP |
| **Owner** | BE |
| **Dependencies** | Story 2.1 |

**User Story:**
> As a beneficiary-facing platform, I want compliant identity verification integration so that identity checks move from mocked to approved production behavior.

**Acceptance Criteria:**
- [ ] AC1 - Vault/token flow is implemented through approved credentials.
- [ ] AC2 - No plain Aadhaar data is persisted outside the approved pattern.

**Subtasks:**
##### 6.2.1 - Implement approved adapter and token exchange flow
- Estimated: 10h
- Notes: Requires external approvals and compliance review.

##### 6.2.2 - Validate masked UI and audit behavior
- Estimated: 4h
- Notes: Ensure compliance-preserving UX.

#### 6.3 - Add batch actions, advanced reports, and performance tuning
| Field | Value |
|-------|-------|
| **Priority** | Low |
| **Story Points** | 5 SP |
| **Owner** | Full-stack |
| **Dependencies** | Stories 3.4, 4.4 |

**User Story:**
> As an official, I want bulk decision actions and richer reporting so that large workloads remain manageable at scale.

**Acceptance Criteria:**
- [ ] AC1 - NMB queue supports safe batch actions with audit coverage.
- [ ] AC2 - Dashboard and report performance meets agreed thresholds on seeded scale data.

**Subtasks:**
##### 6.3.1 - Implement safe batch review actions
- Estimated: 6h
- Notes: Guard with permission checks and confirmations.

##### 6.3.2 - Tune indexes, summaries, and slow queries
- Estimated: 6h
- Notes: Measure before optimizing.

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| LGD source data is inconsistent or incomplete for some states | M | M | Prioritize Bihar-quality seed data, validate import scripts, and support manual corrections |
| Aadhaar/Agristack access remains unavailable during planned delivery | H | H | Keep adapter interfaces and mocked providers, do not couple workflow completion to live external APIs |
| Workflow complexity causes hidden status transition bugs | M | H | Centralize state machine logic, add transition tests early, and validate status/audit/history consistency |
| Dashboard queries become slow as transactional volume increases | M | M | Use summary tables/materialized views and add indexes before expanding dashboard scope |
| Government-style UX is too complex for low-tech users | M | H | Use guided forms, clear validation, and test flows with simplified labels and step-based navigation |
| File upload security gaps create deployment risk | M | H | Enforce type/size restrictions, add virus-scan hook, and isolate storage policies by entity |
| Demo environment fails during presentation | M | H | Keep deterministic seed data, health page, offline rehearsal flow, and recorded walkthrough backup |
| Team velocity is lower than assumed because of infra/setup drag | M | M | Lock foundation early, keep slices vertical, and move low-value polish to backlog |

## Dependencies Map

1. `1.1 -> 1.2 -> 1.5` establishes the secure platform baseline.
2. `1.3` unlocks every location-dependent workflow in beneficiary, AAP, and field data stories.
3. `2.1 -> 2.2 -> 3.1 -> 3.2/3.3 -> 3.4` is the critical application workflow path.
4. `3.4`, `4.2`, and `4.3` must land before `4.4` can expose credible cross-role dashboards.
5. `4.1` and `5.1` are coupled because AAP lifecycle notifications depend on evented workflow transitions.
6. `5.3` and `5.4` should run in parallel late, but only after the core flows are functionally stable.
7. `5.5` depends on dashboard, notifications, and QA coverage because demo data must validate the full story, not isolated screens.

## Open Questions

- Will the production build be expected to use `Django` as recommended here, or is `FastAPI` preferred by the team despite the extra admin/auth work?
- Is the initial delivery target a PoC for evaluation, a production MVP, or both on the same codebase?
- What is the actual team composition and velocity so sprint capacity can be recalibrated?
- Will the public portal content come from a CMS later, or should content remain code-managed in the first release?
- What are the exact scheme components and eligibility rules that must be encoded in application forms?
- Is Bihar the confirmed primary demo state, and do we already have authoritative sample data for districts, farmers, production, and budgets?
- Does the user want Superset embedded from Sprint 4 onward, or is a native dashboard implementation preferred for the first release?
- What security and hosting controls are mandatory at first deployment: NIC Cloud, on-prem, or another government-approved environment?
