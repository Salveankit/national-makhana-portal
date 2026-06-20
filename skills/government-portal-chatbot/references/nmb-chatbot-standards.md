# NMB Chatbot Standards

## Contents

- Positioning
- UI rules
- Conversation rules
- Accessibility and compliance
- Repo implementation notes

## Positioning

- Present the assistant as `Makhana Mitra` or an equally formal NMB-specific helper, not a generic bot.
- Make the first state capability-led: status tracking, scheme guidance, helpdesk support, and workflow guidance.
- Keep the tone respectful, direct, and operational. Avoid jokes, filler, slang, or "AI assistant" hype.
- Treat the chatbot as an assistive layer over the portal's real workflows, not a replacement for forms and navigation.

## UI Rules

### Launcher

- Keep the launcher bottom-right, always reachable, and visually subordinate to page content until opened.
- Preserve a government-grade appearance: solid primary color, clear iconography, no bouncing or promotional motion.
- Maintain accessible touch targets of at least `44x44px`.

### Panel

- Use a compact right-side panel on desktop and a full-screen or near-full-screen treatment on mobile.
- Keep the header clear: bot identity, status/help context, and close/minimize controls.
- Make the message thread the dominant area; avoid decorative sections that steal space from conversation.

### Messages

- Differentiate bot and user messages clearly through alignment and color.
- Keep answer chunks short. Split long guidance into multiple concise messages or structured sections.
- Prefer cards or labeled rows for statuses, workflow states, contacts, or document metadata.
- Keep timestamps subtle and secondary.

### Guided Actions

- Offer a small set of high-value quick replies in the welcome state and after fallback moments.
- Remove or replace stale quick replies after the user makes a choice.
- Keep chip labels short and action-oriented.

### Input

- Keep the input visible and uncomplicated.
- Disable send when empty.
- Only expose attachment affordances if the backend flow actually supports them.

## Conversation Rules

### Welcome State

- Name the assistant and state its scope immediately.
- Show the main task paths instead of opening with a vague "How can I help you?"
- Keep the first message short enough to scan in a few seconds.

### Answer Style

- Explain statuses in plain language and include the likely next step when useful.
- For public informational answers, stay grounded in `knowledge/official`, `knowledge/faq`, and other curated docs.
- For beneficiary or dashboard answers, combine curated knowledge with runtime context when the backend supports it.
- Prefer "what this means" and "what to do next" over policy-dump paragraphs.

### Fallbacks

- Never expose raw technical errors or stack-like wording.
- When the bot is uncertain or unsupported, offer a next step: retry, main menu, relevant page, or helpdesk contact.
- After repeated misunderstanding, steer the user to a human or a clearer task menu.

### Sensitive Scope

- Refuse to treat chat as a secure Aadhaar or sensitive-document channel.
- Route identity verification, personal-record review, and final submission actions back into authenticated portal workflows.

## Accessibility And Compliance

- Keep the message container compatible with screen-reader announcement patterns such as `role="log"` and polite live updates.
- Ensure keyboard operation for open, close, quick replies, and submit.
- Preserve readable contrast in both launcher and message bubbles.
- Respect reduced-motion preferences for typing or panel transitions.
- Keep Hindi/English support visible when language switching is part of the current experience.
- Include capability transparency and automated-assistant framing; do not imply a human operator is typing unless the flow truly hands off.

## Repo Implementation Notes

- This repo's chat UI is implemented in `frontend/assets/site.js` and `frontend/assets/styles.css`; do not design as though a React component tree already exists.
- Existing chat endpoints live under `/api/v1/chat/*` in `backend/app/main.py`.
- Existing answer assembly and fallback logic live in `backend/app/chatbot.py`.
- Curated grounding content lives under `knowledge/`; update those files instead of hardcoding large answer libraries into frontend JavaScript.
- If the task asks for a visual overhaul, keep the same government portal tone already established across the rest of the project.
- If the task asks for a new flow, check whether it should become:
  - curated knowledge content,
  - backend runtime summarization logic,
  - frontend quick replies, or
  - a combination of all three.
