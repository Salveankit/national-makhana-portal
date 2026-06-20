# Portal Operating Model

The National Makhana Board Portal is designed as a government operations platform with a public information layer attached. It is not only a website for awareness. It is a single-window digital system that combines beneficiary services, state-level workflow processing, inspection management, planning, monitoring, notifications, and integration-readiness demonstrations.

The portal should be understood through three parallel responsibilities:

1. Public information and service discovery
2. Transaction workflows for beneficiary and state operations
3. Monitoring and decision support for board and central authorities

The proof of concept currently runs as one FastAPI application serving public pages, secure pages, and API workflows. Local runtime persistence uses SQLite and placeholder document files. The current deployment model is suitable for demonstration and bidding workflows, but durable production persistence still requires hosted database and object storage components.

The portal currently supports four implemented user perspectives:

- Public visitor
- Beneficiary or farmer
- State officer or inspector
- National Makhana Board administrator

The wider operating model also anticipates central authority, helpdesk/support, and super-admin roles as the product matures.

The strongest product framing is:

- a scheme management and monitoring system
- with structured application and inspection workflows
- with dashboard-led decision support
- with a public portal for transparency, scheme guidance, and support access

This framing matters for chatbot answers. The assistant should explain the portal as a serious workflow system, not as a brochure site.
