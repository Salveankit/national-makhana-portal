# Seeded Scenarios And Demo Talk Tracks

The proof of concept includes seeded records so that demonstrations begin with meaningful workflow states instead of empty dashboards and blank queues.

Seeded beneficiary application scenarios:

- `APP-BR-0001` -> `Submitted`
  Use this case to explain fresh submission awaiting state review.

- `APP-BR-0002` -> `Clarification Raised`
  Use this case to explain how state officers request additional details and how beneficiaries respond.

- `APP-BR-0003` -> `Inspection Assigned`
  Use this case to explain pending field verification and inspector action.

- `APP-BR-0004` -> `Recommended by State`
  Use this case to explain the state-to-NMB handoff for final review.

- `APP-BR-0005` -> `Approved`
  Use this case to demonstrate a successful completed lifecycle and dashboard impact.

Additional seeded records:

- `INSP-0001` assigned and pending
- `INSP-0002` and `INSP-0003` completed
- `AAP-BR-2026` submitted
- `AAP-BR-2027` approved
- `BUD-BR-01` to `BUD-BR-03` populated
- notification log seeded
- mock integration log seeded

Recommended demo order:

1. Public portal
2. Beneficiary
3. State officer
4. Inspector
5. NMB admin

Strong demo talking point:

`All workflow, audit, dashboard, notification, and integration surfaces are already productized in the PoC. Replacing mock integrations with live government APIs is an adapter activation step, not a platform redesign step.`

Chatbot usage guidance:

- use seeded identifiers to explain what a status means
- use seeded records to show lifecycle depth
- do not claim seeded cases are live citizen records
- present them as demonstration scenarios built into the PoC
