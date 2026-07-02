---
name: government-portal-chatbot
description: Design, restyle, implement, or review a chatbot for the National Makhana Board portal or a similar Indian government portal. Use when Codex needs to improve chatbot UI, conversation flows, accessibility, grounded-answer behavior, quick replies, helpdesk guidance, runtime data presentation, or government-compliant guardrails in this repo's chat surface.
---

# Government Portal Chatbot

Use this skill to keep the chatbot aligned with the National Makhana Board portal's product model: serious government service surface, curated knowledge grounding, role-aware runtime help, and no consumer-chat gimmicks.

## Start Here

Read these files before changing behavior:

- `README.md` for the current portal and chatbot mental model
- `frontend/assets/site.js` for launcher, panel, prompts, streaming UI, and chat actions
- `frontend/assets/styles.css` for chatbot layout and visual language
- `backend/app/main.py` for `/api/v1/chat/*` endpoints
- `backend/app/chatbot.py` for answer assembly, fallback logic, and source handling
- `knowledge/README.md`, `knowledge/manifest.json`, and `knowledge/faq/public-faq.json` for curated grounding content

Read `references/nmb-chatbot-standards.md` when the task involves visual redesign, conversational UX, accessibility, compliance, or quick-reply/launcher behavior.

## Decide The Work Surface

- Change `frontend/assets/site.js` and `frontend/assets/styles.css` when the request is about launcher behavior, panel structure, prompts, message rendering, labels, typing states, or mobile responsiveness.
- Change `backend/app/chatbot.py`, `backend/app/main.py`, or `knowledge/*` when the request is about answer quality, grounded sources, runtime data summaries, intent handling, fallback responses, or analytics.
- Change both frontend and backend when a new chat capability needs UI affordances plus response logic.

## Preserve These Rules

- Keep the chatbot formal, helpful, and government-facing. Do not introduce playful copy, popups, noisy animation, or startup-style language.
- Treat the chatbot as a portal assistant, not as the only navigation path. Always preserve direct page-based access to the same information.
- Prefer deterministic or clearly grounded behavior. Do not imply live AI capability or live integrations unless the repo is actually configured for them.
- Do not collect or echo full Aadhaar numbers in chat. Route identity-sensitive actions back into secure workflow pages.
- Allow public guidance without login, but require authenticated runtime lookups for personal or operational data.
- Keep the current stack in mind: this repo uses FastAPI plus static HTML/CSS/JS, not React components. Convert conceptual component ideas into the existing `site.js` and `styles.css` structure unless the user explicitly asks for a stack change.

## Implement Intentionally

- Make capability scope obvious in the opening state. Users should immediately see what the chatbot can help with.
- Prefer short messages, structured status blocks, and guided reply actions over long paragraphs.
- Keep source-backed answers aligned with curated `knowledge/` content and current runtime records.
- When adding quick replies or guided actions, map them to real pages, flows, or backend-supported responses.
- When changing visual design, keep the launcher and panel usable on public pages, beneficiary pages, and dashboard pages.

## Validate

- Run `python -m unittest tests.test_chatbot` after behavior changes.
- Run `python -m unittest tests.test_knowledge_base` after `knowledge/*` edits.
- Smoke test the UI by opening a public page and, if relevant, `/beneficiary` and `/dashboard`, then verify launcher, prompt chips, response rendering, and fallback behavior.
- Do not assume Gemini is active; verify the effective mode from environment/config behavior before claiming grounded-model responses are live.
