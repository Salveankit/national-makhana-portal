# Workflow Lifecycles

The portal includes structured workflow lifecycles for beneficiary applications, Annual Action Plans, and inspections. The chatbot should explain these lifecycles in plain language while preserving operational accuracy.

Beneficiary application lifecycle:

`Draft -> Submitted -> Under State Review -> Clarification Raised -> Resubmitted -> Inspection Assigned -> Inspection Completed -> Recommended by State -> Under NMB Review -> Approved / Rejected / Returned`

Operational meaning:

- `Draft`: application exists but is not formally submitted
- `Submitted`: beneficiary has filed the application into the workflow
- `Under State Review`: state officer scrutiny is in progress
- `Clarification Raised`: officer needs additional detail, explanation, or correction
- `Resubmitted`: beneficiary has responded and returned the case to review
- `Inspection Assigned`: field verification has been created for inspector action
- `Inspection Completed`: inspection record is complete and available to officers
- `Recommended by State`: state has completed review and forwarded the case to NMB
- `Under NMB Review`: national board-level review is pending or in progress
- `Approved / Rejected / Returned`: final board outcome has been recorded

Annual Action Plan lifecycle:

`Draft -> Submitted -> Under Review -> Query Raised -> Revised Submission -> Approved / Returned`

Expected AAP content areas:

- district targets
- cultivation and farmer coverage targets
- infrastructure planning
- training plans
- budget requests
- supporting remarks and documents

Inspection lifecycle:

`Assigned -> In Progress -> Completed -> Verified -> Accepted / Reopened`

Inspection records are expected to capture:

- GPS coordinates
- timestamps
- inspector identity
- checklist-style findings
- photographs
- remarks
- verification result

Workflow expectations across the system:

- status transitions should be logged
- transitions can trigger notifications
- history should remain visible to authorized users
- chatbot answers should explain what a status means and what the likely next step is
