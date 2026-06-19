# National Makhana Board Portal Demo Script

## Reset Before Every Demo

Run this once before starting the API:

```powershell
python scripts/reset_demo_data.py
```

Start the app:

```powershell
python -m uvicorn backend.app.main:app --reload --app-dir .
```

Open:

- Public portal: `http://127.0.0.1:8000/`
- Login: `http://127.0.0.1:8000/login`

## Demo Accounts

- `nmb.admin@example.com` / `Pass@123`
- `bihar.officer@example.com` / `Pass@123`
- `inspector@example.com` / `Pass@123`
- `farmer@example.com` / `Pass@123`

## Seeded Scenario Records

The reset creates five clean beneficiary scenarios:

1. `APP-BR-0001`
State: `Submitted`
Use: fresh application awaiting state review

2. `APP-BR-0002`
State: `Clarification Raised`
Use: show clarification workflow

3. `APP-BR-0003`
State: `Inspection Assigned`
Use: show inspector landing state and pending field visit

4. `APP-BR-0004`
State: `Recommended by State`
Use: show NMB-ready queue item

5. `APP-BR-0005`
State: `Approved`
Use: show completed success case and dashboard impact

Additional seeded records:

- `INSP-0001` assigned and pending for inspector
- `INSP-0002`, `INSP-0003` completed
- `AAP-BR-2026` submitted
- `AAP-BR-2027` approved
- `BUD-BR-01` to `BUD-BR-03` populated
- notification log seeded
- mock integration log seeded

## Role Landing States

### Farmer

Expected impression:

- profile already exists
- Aadhaar verification already shown as verified
- five applications visible with varied statuses
- citizen sees full lifecycle from submitted to approved

What to show:

1. Login as `farmer@example.com`
2. Open beneficiary workspace
3. Point out verified identity state
4. Scroll through the application cards
5. Highlight that one application is approved, one is under clarification, and one is assigned for inspection

### State Officer

Expected impression:

- queue is populated immediately
- AAP and field-data controls are usable
- budget utilization can be updated
- mock integration controls are visible but clearly non-live

What to show:

1. Login as `bihar.officer@example.com`
2. Show officer queue with mixed statuses
3. Raise a clarification on `APP-BR-0001` or review `APP-BR-0002`
4. Point out AAP submission and field data update forms
5. Show budget utilization update

### Inspector

Expected impression:

- at least one live assigned inspection exists
- role-specific work is obvious

What to show:

1. Login as `inspector@example.com`
2. Show that `INSP-0001` is assigned
3. Complete the inspection form for `INSP-0001`
4. Explain that this updates the application lifecycle and feeds the officer queue

### NMB Admin

Expected impression:

- dashboard already has meaningful cards
- NMB sees one recommended case and one approved case
- system overview, notifications, and integration-readiness panels are populated

What to show:

1. Login as `nmb.admin@example.com`
2. Show KPI cards, state rollup, trend cards, and AAP status
3. Use the decision form on `APP-BR-0004` if needed
4. Show system overview and notification log
5. Show mock integration catalog and logs
6. Run one mock notification or mock DBT event to demonstrate API-readiness

## Recommended Demo Sequence

Use this exact order:

1. Public portal
Show official framing and service entry points

2. Farmer
Show citizen registration, identity verification state, and status tracking

3. State Officer
Show review, clarification, planning, and budget control

4. Inspector
Show assigned inspection and completion flow

5. NMB Admin
Show dashboard, approvals, operations, notifications, and mock integrations

## Safe Live Actions During Demo

These are safe to perform repeatedly after reset:

- verify Aadhaar for farmer
- submit new application
- raise clarification
- assign inspection
- complete inspection
- recommend application
- review AAP
- update budget utilization
- trigger mock notification
- trigger mock Aadhaar KYC
- trigger mock DBT disbursement

## Final Talking Point

Use this line near the end:

`All workflow, audit, dashboard, notification, and integration surfaces are already productized in the PoC. Replacing mock integrations with live government APIs is an adapter activation step, not a platform redesign step.`
