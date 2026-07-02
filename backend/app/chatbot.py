from __future__ import annotations

import json
import re
from dataclasses import dataclass
from urllib import error, request

from backend.app.core.config import settings
from backend.app.data import (
    list_aap,
    list_beneficiary_applications,
    list_budgets,
    list_chat_logs,
    list_clarifications,
    list_field_data,
    list_inspections,
    list_integration_events,
    list_notifications,
    list_officer_applications,
    storage_health,
    get_beneficiary_profile,
)
from backend.app.knowledge import KnowledgeChunk, load_knowledge_chunks
from backend.app.models import User

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "of",
    "on",
    "or",
    "the",
    "this",
    "to",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
}

GENERIC_PHRASES = {
    "hello",
    "hi",
    "hey",
    "how are you",
    "who are you",
    "what can you do",
    "tell me something",
    "help me",
    "can you help me",
    "good morning",
    "good afternoon",
    "good evening",
}

PAGE_HINTS = {
    "home": {"portal", "overview", "services", "schemes"},
    "services": {"services", "registration", "application", "officer", "inspection"},
    "schemes": {"schemes", "support", "cultivation", "processing", "training"},
    "updates": {"updates", "notices", "circulars", "service"},
    "helpdesk": {"login", "helpdesk", "status", "support"},
    "login": {"login", "credentials", "access", "role"},
    "beneficiary": {"beneficiary", "application", "status", "clarification", "aadhaar"},
    "dashboard": {"dashboard", "queue", "aap", "budget", "inspection", "monitoring"},
}

PAGE_PROMPTS = {
    "home": "Use a formal public-portal tone and help the user understand what the portal does and where to go next.",
    "services": "Focus on service modules, role pathways, and the correct workspace for each task.",
    "schemes": "Explain support areas and workflow relevance without inventing detailed scheme rules.",
    "updates": "Frame notices, advisories, and operational updates in official language.",
    "helpdesk": "Focus on support triage, login help, status meaning, and routing to the correct page.",
    "login": "Explain role-based secure access, login troubleshooting, and the difference between beneficiary and officer entry.",
    "beneficiary": "Focus on the beneficiary workspace, application statuses, clarifications, and next-step guidance.",
    "dashboard": "Focus on officer, inspector, and NMB admin monitoring, queues, planning, and system-readiness guidance.",
}

SUGGESTED_ACTIONS = {
    "home": [
        {"label": "View Services", "href": "/services"},
        {"label": "Open Helpdesk", "href": "/helpdesk"},
    ],
    "services": [
        {"label": "Beneficiary Services", "href": "/beneficiary"},
        {"label": "Open Helpdesk", "href": "/helpdesk"},
    ],
    "schemes": [
        {"label": "View Services", "href": "/services"},
        {"label": "Open Secure Login", "href": "/login"},
    ],
    "updates": [
        {"label": "Open Helpdesk", "href": "/helpdesk"},
        {"label": "View Schemes", "href": "/schemes"},
    ],
    "helpdesk": [
        {"label": "Open Secure Login", "href": "/login"},
        {"label": "Beneficiary Services", "href": "/beneficiary"},
    ],
    "login": [
        {"label": "Open Helpdesk", "href": "/helpdesk"},
        {"label": "View Services", "href": "/services"},
    ],
    "beneficiary": [
        {"label": "Profile Section", "href": "#profile-form"},
        {"label": "My Applications", "href": "#status"},
    ],
    "dashboard": [
        {"label": "Dashboard Overview", "href": "#overview"},
        {"label": "Planning Workspace", "href": "#planning"},
        {"label": "Workflow Desk", "href": "#workflow"},
    ],
}


@dataclass(slots=True)
class ContextSource:
    source_id: str
    title: str
    category: str
    summary: str
    text: str


@dataclass(slots=True)
class ChatSourceItem:
    title: str
    category: str
    summary: str


@dataclass(slots=True)
class ChatResult:
    answer: str
    sources: list[ChatSourceItem]
    suggested_actions: list[dict[str, str]]
    fallback_used: bool
    mode: str


@dataclass(slots=True)
class ScoredSource:
    score: int
    source: ContextSource


def _tokenize(value: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9]+", value.lower())
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 1]


def _static_sources() -> list[ContextSource]:
    return [
        ContextSource(
            source_id=chunk.doc_id,
            title=chunk.title,
            category=chunk.category,
            summary=chunk.summary,
            text=chunk.text,
        )
        for chunk in load_knowledge_chunks()
    ]


def _build_beneficiary_sources(user: User) -> list[ContextSource]:
    sources: list[ContextSource] = []
    profile = get_beneficiary_profile(user.id)
    if profile:
        profile_text = (
            f"Beneficiary profile for {profile.name}. State: {profile.state_code}. District: {profile.district_code}. "
            f"Identity verified: {'yes' if profile.identity_verified else 'no'}. "
            f"Makhana area acres: {profile.makhana_area_acres}. Total land acres: {profile.total_land_acres}. "
            f"Mobile: {profile.mobile}."
        )
        sources.append(ContextSource("runtime:beneficiary_profile", "Beneficiary Profile Snapshot", "runtime", "Current beneficiary profile state", profile_text))
    applications = list_beneficiary_applications(user.id)
    if applications:
        app_lines = []
        for app in applications[:6]:
            latest = app.status_history[0].remarks if app.status_history else "No remarks available."
            app_lines.append(
                f"{app.application_id}: {app.scheme_component}; current status {app.current_status}; "
                f"requested amount {app.requested_amount}; latest note {latest}"
            )
        sources.append(
            ContextSource(
                "runtime:beneficiary_applications",
                "Beneficiary Application Snapshot",
                "runtime",
                "Current beneficiary applications and stages",
                " ".join(app_lines),
            )
        )
        app_ids = {app.application_id for app in applications}
        open_clarifications = [item for item in list_clarifications(app_ids) if item.status == "Open"]
        if open_clarifications:
            clarification_lines = [
                f"{item.application_id}: clarification open; query: {item.query_text}"
                for item in open_clarifications[:4]
            ]
            sources.append(
                ContextSource(
                    "runtime:beneficiary_clarifications",
                    "Open Clarification Snapshot",
                    "runtime",
                    "Current open clarifications for the beneficiary",
                    " ".join(clarification_lines),
                )
            )
    notifications = list_notifications(limit=8, recipient=user.email)
    if notifications:
        notification_lines = [
            f"{item.subject}; status {item.status}; module {item.module}" for item in notifications[:5]
        ]
        sources.append(
            ContextSource(
                "runtime:beneficiary_notifications",
                "Beneficiary Notification Snapshot",
                "runtime",
                "Recent notifications issued for the beneficiary",
                " ".join(notification_lines),
            )
        )
    return sources


def _build_operations_sources(user: User) -> list[ContextSource]:
    sources: list[ContextSource] = []
    applications = list_officer_applications(user.role, user.email)
    if applications:
        by_status: dict[str, int] = {}
        app_lines: list[str] = []
        for app in applications[:8]:
            by_status[app.current_status] = by_status.get(app.current_status, 0) + 1
            app_lines.append(f"{app.application_id}: {app.current_status}; component {app.scheme_component}; amount {app.requested_amount}")
        status_summary = ", ".join(f"{status}={count}" for status, count in sorted(by_status.items()))
        sources.append(
            ContextSource(
                "runtime:operations_queue",
                "Operational Queue Snapshot",
                "runtime",
                "Current application queue for the logged-in officer role",
                f"Queue size {len(applications)}. Status mix: {status_summary}. Sample records: {' '.join(app_lines)}",
            )
        )
    inspections = list_inspections(user.role, user.email)
    if inspections:
        inspection_lines = [f"{item.inspection_id}: {item.status}; application {item.application_id}" for item in inspections[:6]]
        sources.append(
            ContextSource(
                "runtime:inspection_queue",
                "Inspection Queue Snapshot",
                "runtime",
                "Current inspection workload and completion state",
                " ".join(inspection_lines),
            )
        )
    state_scope = user.state_code if user.role != "nmb_admin" else None
    aaps = list_aap("nmb_admin" if user.role == "nmb_admin" else "state_officer", user.email, state_scope)
    if aaps:
        aap_lines = [f"{item.aap_id}: {item.financial_year}; status {item.current_status}; budget requested {item.budget_requested}" for item in aaps[:6]]
        sources.append(
            ContextSource(
                "runtime:aap_summary",
                "Annual Action Plan Snapshot",
                "runtime",
                "Current AAP submissions and review states",
                " ".join(aap_lines),
            )
        )
    budgets = list_budgets("nmb_admin" if user.role == "nmb_admin" else "state_officer", state_scope)
    if budgets:
        budget_lines = [
            f"{item.budget_id}: {item.component_name}; allocated {item.allocated_amount}; utilized {item.utilized_amount}"
            for item in budgets[:6]
        ]
        sources.append(
            ContextSource(
                "runtime:budget_summary",
                "Budget Summary Snapshot",
                "runtime",
                "Current budget allocation and utilization figures",
                " ".join(budget_lines),
            )
        )
    field_rows = list_field_data("nmb_admin" if user.role == "nmb_admin" else "state_officer", state_scope)
    if field_rows:
        area = round(sum(item.area_hectares for item in field_rows), 2)
        production = round(sum(item.production_mt for item in field_rows), 2)
        farmer_count = sum(item.farmer_count for item in field_rows)
        sources.append(
            ContextSource(
                "runtime:field_summary",
                "Field Data Summary",
                "runtime",
                "Current field monitoring aggregates",
                f"Field coverage area hectares {area}. Production metric tonnes {production}. Farmers covered {farmer_count}.",
            )
        )
    readiness = storage_health()
    integrations = list_integration_events(limit=6)
    if integrations:
        integration_lines = [f"{item.integration_type}: {item.provider_name}; status {item.status}" for item in integrations[:4]]
        sources.append(
            ContextSource(
                "runtime:service_readiness",
                "Service Readiness Snapshot",
                "runtime",
                "Current platform health and integration-readiness indicators",
                f"API {readiness['sqlite']}; documents {readiness['documents']}. {' '.join(integration_lines)}",
            )
        )
    return sources


def _build_runtime_sources(user: User | None, page: str) -> list[ContextSource]:
    if not user:
        return []
    if user.role == "beneficiary" or page == "beneficiary":
        return _build_beneficiary_sources(user)
    return _build_operations_sources(user)


def _score_source(source: ContextSource, query_terms: set[str], page: str, user: User | None) -> int:
    haystack = " ".join([source.title, source.summary, source.text]).lower()
    score = sum(6 if term in source.title.lower() else 3 if term in source.summary.lower() else 1 for term in query_terms if term in haystack)
    score += sum(2 for term in PAGE_HINTS.get(page, set()) if term in haystack)
    if source.category == "runtime":
        score += 4
    elif source.category == "official":
        score += 3
    elif source.category == "faq":
        score += 2
    if user and user.role in haystack:
        score += 2
    return score


def rank_sources(message: str, page: str, user: User | None, limit: int = 5) -> list[ScoredSource]:
    query_terms = set(_tokenize(message))
    if not query_terms:
        query_terms = PAGE_HINTS.get(page, {"portal"})
    combined = _build_runtime_sources(user, page) + _static_sources()
    best_by_doc: dict[str, ScoredSource] = {}
    for source in combined:
        score = _score_source(source, query_terms, page, user)
        if score > 0:
            existing = best_by_doc.get(source.source_id)
            candidate = ScoredSource(score=score, source=source)
            if not existing or candidate.score > existing.score:
                best_by_doc[source.source_id] = candidate
    ranked = sorted(best_by_doc.values(), key=lambda item: item.score, reverse=True)
    return ranked[:limit]


def retrieve_sources(message: str, page: str, user: User | None, limit: int = 5) -> list[ContextSource]:
    return [item.source for item in rank_sources(message, page, user, limit=limit)]


def _dedupe_sources(sources: list[ContextSource]) -> list[ChatSourceItem]:
    seen: set[str] = set()
    items: list[ChatSourceItem] = []
    for source in sources:
        if source.source_id in seen:
            continue
        seen.add(source.source_id)
        items.append(ChatSourceItem(title=source.title, category=source.category, summary=source.summary))
    return items


def _source_reply_text(source: ContextSource) -> str:
    text = source.text.strip()
    if "Answer:" in text:
        text = text.split("Answer:", 1)[1].strip()
    text = re.sub(r"(?m)^#+\s*", "", text)
    text = re.sub(r"(?m)^-\s*", "", text)
    text = re.sub(r"^Question:\s*.*?\s+Answer:\s*", "", text, flags=re.IGNORECASE)
    text = text.replace(" ; ", ". ").replace("; ", ". ").replace(";", ". ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _take_sentences(text: str, limit: int = 2) -> str:
    pieces = [part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if part.strip()]
    if not pieces:
        return text
    return " ".join(pieces[:limit])


def _is_generic_prompt(message: str) -> bool:
    normalized = re.sub(r"\s+", " ", message.strip().lower())
    if not normalized:
        return True
    if normalized in GENERIC_PHRASES:
        return True
    generic_tokens = {"hello", "hi", "hey", "help", "thanks"}
    token_set = set(_tokenize(normalized))
    if token_set and token_set.issubset(generic_tokens):
        return True
    return len(token_set) <= 2 and any(phrase in normalized for phrase in GENERIC_PHRASES)


def _generic_fallback_answer(page: str, user: User | None, sources: list[ContextSource]) -> str:
    if user and user.role == "beneficiary":
        return (
            "I can help you understand your profile, application status, clarifications, and next steps in the portal. "
            "Ask about any application stage or workflow and I will explain it clearly."
        )
    if user and user.role in {"state_officer", "inspector", "nmb_admin"}:
        return (
            "I can help you navigate queues, inspections, planning, budget tracking, and workflow actions in this portal. "
            "Ask about a task, status, or module and I will explain it clearly."
        )
    if page in {"login", "helpdesk"}:
        return "I can help you with login guidance, support questions, and finding the right portal path."
    return (
        "I can help you understand the National Makhana Board portal, its services, scheme-related workflows, and where to go next. "
        "Ask about any page, service, status, or process and I will explain it in simple language."
    )


def _generic_prompt_guidance(message: str) -> str:
    if not _is_generic_prompt(message):
        return ""
    return (
        "This is a generic conversational prompt. "
        "Answer in 2 or 3 short sentences. "
        "Do not use bullets or headings. "
        "Sound natural, direct, and helpful. "
        "If you mention portal capabilities, summarize them briefly instead of listing every role or module. "
    )


def _fallback_answer(page: str, sources: list[ContextSource], user: User | None, generic_prompt: bool = False) -> str:
    if generic_prompt:
        return _generic_fallback_answer(page, user, sources)
    if not sources:
        return (
            "I could not find a trusted answer for that yet. Please use the Helpdesk or the relevant portal page for formal guidance."
        )
    excerpts: list[str] = []
    max_sources = 1 if sources[0].category == "faq" else 2
    for source in sources[:max_sources]:
        excerpt = _take_sentences(_source_reply_text(source), 2)
        if excerpt:
            excerpts.append(excerpt.rstrip(".") + ".")
    answer = " ".join(excerpts).strip()
    if not answer:
        answer = "I could not assemble a clear answer from the approved references."
    if not user:
        if page in {"login", "helpdesk"}:
            answer += " If you still need help, please use the Helpdesk or the secure login page."
        elif page in {"services", "schemes", "home"}:
            answer += " You can continue through Services, Helpdesk, or Secure Login depending on what you need."
    else:
        answer += " Please continue through the formal portal workflow for any submission, review, or approval action."
    return answer


def _gemini_ready() -> bool:
    return settings.chatbot_enabled and settings.chatbot_provider == "gemini" and bool(settings.gemini_api_key)


def _role_prompt(user: User | None) -> str:
    if not user:
        return "The current user is a public visitor. Do not answer with private application or operational data."
    if user.role == "beneficiary":
        return "The current user is a beneficiary. You may explain current profile, application, clarification, and notification state, but do not invent approvals."
    if user.role == "inspector":
        return "The current user is an inspector. Focus on inspection assignments, completion state, and queue guidance."
    if user.role == "state_officer":
        return "The current user is a state officer. Focus on review queues, clarifications, inspections, AAPs, budgets, and monitoring."
    if user.role == "nmb_admin":
        return "The current user is an NMB admin. Focus on dashboard oversight, AAP review, budgets, approvals, and system readiness."
    return "Use only the provided context and keep the response role-appropriate."


def _gemini_chat_attempt(
    message: str, page: str, language: str, user: User | None, sources: list[ContextSource]
) -> tuple[str | None, str | None]:
    if not sources:
        return None, "no_sources"
    if not settings.chatbot_enabled:
        return None, "chatbot_disabled"
    if settings.chatbot_provider != "gemini":
        return None, "unsupported_provider"
    if not settings.gemini_api_key:
        return None, "gemini_not_configured"
    endpoint = settings.gemini_api_base_url.rstrip("/")
    url = f"{endpoint}/models/{settings.gemini_model}:generateContent"
    context = "\n\n".join(f"Source: {source.title} ({source.category})\n{source.text}" for source in sources)
    generic_prompt = _is_generic_prompt(message)
    generic_guidance = _generic_prompt_guidance(message)
    body = {
        "systemInstruction": {
            "parts": [
                {
                    "text": (
                    "You are the National Makhana Board portal assistant. "
                    "Use the provided portal context as the primary factual reference whenever it is relevant. "
                    "For generic greetings or broad assistant questions, reply naturally in plain English first and then briefly connect the user to the portal help you can provide. "
                    "When relevant context exists, build the answer on top of that context instead of sounding like a pasted FAQ. "
                    "Use a clear, natural, professional tone suitable for an official public service portal. "
                    "Do not claim live integrations or private outcomes unless explicitly stated in context. "
                    "Write for chat readability: use short paragraphs, and use 3 to 5 bullets or numbered steps only when they genuinely improve clarity. "
                    "Keep the answer under 140 words unless the user explicitly asks for detail. "
                    "Prefer plain, readable formatting. Use short headings only when they improve clarity. "
                    "Use bold sparingly for short labels or important keywords only. "
                    "Do not bold full sentences or long phrases inside list items. "
                    "Keep each bullet or step to one short sentence where possible, but a short paragraph is acceptable. "
                    "Prefer flat lists. Do not create nested bullets. "
                    "Do not expose chain-of-thought, hidden reasoning, or internal analysis. "
                    "Do not repeat the user's question or add preambles like 'Based on the approved context'. "
                    f"{generic_guidance}{PAGE_PROMPTS.get(page, '')} {_role_prompt(user)}"
                ),
                }
            ]
        },
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            f"Language: {language}\n"
                            f"Question: {message}\n"
                            f"Generic prompt: {'yes' if generic_prompt else 'no'}\n\n"
                            "Portal reference context:\n"
                            f"{context}"
                        )
                    }
                ],
            }
        ],
        "generationConfig": {"temperature": 0.45, "maxOutputTokens": 420},
    }
    req = request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "x-goog-api-key": settings.gemini_api_key},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        return None, f"http_error:{exc.code}"
    except error.URLError:
        return None, "network_error"
    except TimeoutError:
        return None, "timeout"
    except json.JSONDecodeError:
        return None, "invalid_json"
    candidates = result.get("candidates") or []
    if not candidates:
        return None, "empty_candidates"
    parts = candidates[0].get("content", {}).get("parts", [])
    content = "".join(str(part.get("text", "")) for part in parts).strip() or None
    return content, None if content else "empty_message"


def _gemini_chat(message: str, page: str, language: str, user: User | None, sources: list[ContextSource]) -> str | None:
    content, _reason = _gemini_chat_attempt(message, page, language, user, sources)
    return content


def answer_chat(message: str, page: str, language: str, user: User | None = None) -> ChatResult:
    normalized_page = page if page in PAGE_HINTS else "home"
    generic_prompt = _is_generic_prompt(message)
    sources = retrieve_sources(message, normalized_page, user)
    generated = _gemini_chat(message, normalized_page, language, user, sources)
    if user and user.role == "beneficiary":
        fallback_mode = "beneficiary_runtime_fallback"
    elif user and user.role in {"state_officer", "inspector", "nmb_admin"}:
        fallback_mode = "operations_runtime_fallback"
    elif generic_prompt:
        fallback_mode = "generic_fallback"
    else:
        fallback_mode = "retrieval_fallback"
    return ChatResult(
        answer=generated or _fallback_answer(normalized_page, sources, user, generic_prompt=generic_prompt),
        sources=_dedupe_sources(sources),
        suggested_actions=SUGGESTED_ACTIONS.get(normalized_page, SUGGESTED_ACTIONS["home"]),
        fallback_used=generated is None,
        mode="gemini_grounded" if generated else fallback_mode,
    )


def chat_debug_snapshot(message: str, page: str, language: str, user: User | None = None) -> dict[str, object]:
    normalized_page = page if page in PAGE_HINTS else "home"
    generic_prompt = _is_generic_prompt(message)
    ranked = rank_sources(message, normalized_page, user, limit=8)
    sources = [item.source for item in ranked[:5]]
    generated, provider_error = _gemini_chat_attempt(message, normalized_page, language, user, sources)
    if user and user.role == "beneficiary":
        fallback_mode = "beneficiary_runtime_fallback"
    elif user and user.role in {"state_officer", "inspector", "nmb_admin"}:
        fallback_mode = "operations_runtime_fallback"
    elif generic_prompt:
        fallback_mode = "generic_fallback"
    else:
        fallback_mode = "retrieval_fallback"
    result = ChatResult(
        answer=generated or _fallback_answer(normalized_page, sources, user, generic_prompt=generic_prompt),
        sources=_dedupe_sources(sources),
        suggested_actions=SUGGESTED_ACTIONS.get(normalized_page, SUGGESTED_ACTIONS["home"]),
        fallback_used=generated is None,
        mode="gemini_grounded" if generated else fallback_mode,
    )
    return {
        "page": normalized_page,
        "language": language,
        "user_role": user.role if user else "public",
        "chatbot_enabled": settings.chatbot_enabled,
        "provider": settings.chatbot_provider,
        "gemini_model": settings.gemini_model,
        "gemini_configured": bool(settings.gemini_api_key),
        "gemini_ready": _gemini_ready(),
        "provider_error": provider_error,
        "mode": result.mode,
        "fallback_used": result.fallback_used,
        "answer_preview": result.answer,
        "top_sources": [
            {
                "rank": index,
                "score": item.score,
                "source_id": item.source.source_id,
                "title": item.source.title,
                "category": item.source.category,
                "summary": item.source.summary,
            }
            for index, item in enumerate(ranked, start=1)
        ],
    }


def chat_analytics_snapshot() -> dict[str, object]:
    logs = list_chat_logs(limit=250)
    by_role: dict[str, int] = {}
    by_page: dict[str, int] = {}
    fallback_count = 0
    for item in logs:
        by_role[item.role] = by_role.get(item.role, 0) + 1
        by_page[item.page] = by_page.get(item.page, 0) + 1
        if item.fallback_used:
            fallback_count += 1
    return {
        "total_chats": len(logs),
        "fallback_count": fallback_count,
        "by_role": by_role,
        "by_page": by_page,
    }
