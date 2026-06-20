# Knowledge Base

This directory contains the Phase 0 static knowledge foundation for the National Makhana Board portal chatbot.

Structure:

- `official/`: curated knowledge derived from approved project documents and public portal content
- `faq/`: structured question-answer pairs for common public and helpdesk queries
- `demo/`: seeded illustrative scenarios used to support PoC walkthroughs where live integrations are not yet available

Rules:

- Keep official and demo content separate.
- Prefer official content over demo content when both answer the same query.
- Do not place secrets, tokens, or private beneficiary data in this directory.
- Keep wording aligned to Government of India portal tone.
- Keep workflow explanations concrete enough for bid demos and committee review.
- Use seeded record identifiers where useful so the assistant can explain existing PoC states with confidence.
- Avoid “AI for AI’s sake” content; every source should improve navigation, support, workflow clarity, or bid credibility.

Content standards:

- `official` documents should read like product, operations, or policy notes rather than marketing blurbs.
- `faq` entries should answer specific user questions in language suitable for public support or committee demonstrations.
- `demo` documents should describe seeded scenarios, support talking points, and clearly distinguish illustrative examples from live production integrations.
